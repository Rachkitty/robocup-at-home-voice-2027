#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool

import queue
import sounddevice as sd
import json
import numpy as np
import threading

from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from vosk import Model, KaldiRecognizer


class VoskASRNode(Node):

    def __init__(self):
        super().__init__('vosk_asr_node')

        self.publisher = self.create_publisher(String, '/speech_text', 10)

        self.is_listening = True
        self.tts_speaking = False
        self.ignore_until = 0

        self.create_subscription(Bool, '/asr_control', self.control_callback, 10)
        self.mode = "command"
        self.create_subscription(String, '/asr_mode', self.mode_callback, 10)

        self.command_grammar = ["havva", "hava", "ava", "java", "robot", "havva robot", "hava robot", "ava robot", "java robot"]
        self.create_subscription(String, '/asr_grammar', self.grammar_callback, 10)

        self.ambient_noise_std = 100.0
        self.is_calibrated = False
        self.calibration_duration = 3.0
        self.start_time = self.get_clock().now().nanoseconds
        self.max_vol_phrase = 0.0

        self.get_logger().info("Calibrando ruido")

        self.q = queue.Queue()
        self.lock = threading.Lock()

        default_model = str(Path(get_package_share_directory('robocup_asr')).joinpath(
            'vosk_models', 'vosk-model-small-en-us-0.15'))
        self.declare_parameter('model_path', default_model)
        model_path = Path(self.get_parameter('model_path').value).expanduser()
        if not (model_path / 'am' / 'final.mdl').is_file():
            raise FileNotFoundError(f'Vosk model is incomplete or missing: {model_path}')
        self.model = Model(str(model_path))

        self.set_recognizer()
        self.get_logger().info("ASR READY")

        self.listen_thread = threading.Thread(target=self.listen, daemon=True)
        self.listen_thread.start()

    def set_recognizer(self):
        self.get_logger().info(f"Building recognizer for mode: {self.mode}")

        if self.mode == "command":
            self.recognizer = KaldiRecognizer(
                self.model,
                16000,
                json.dumps(self.command_grammar)
            )
            self.get_logger().info(f"🎞️ Gramática activa: {len(self.command_grammar)} frases")

        elif self.mode == "confirmation":
            grammar = [
                "yes", "confirm", "correct", "affirmative", "yeah", "sure",
                "no", "cancel", "negative", "nope"
            ]
            self.recognizer = KaldiRecognizer(
                self.model,
                16000,
                json.dumps(grammar)
            )

        else:
            self.recognizer = KaldiRecognizer(self.model, 16000)

    def control_callback(self, msg):
        self.tts_speaking = not msg.data
        self.update_listening_state()

    def update_listening_state(self):
        should_listen = (self.mode != "off") and not self.tts_speaking

        if should_listen and not self.is_listening:
            now = self.get_clock().now().nanoseconds
            delay = 0.1 if self.mode == "confirmation" else 0.6
            self.ignore_until = now + int(delay * 1e9)

            with self.lock:
                while not self.q.empty():
                    try:
                        self.q.get_nowait()
                    except queue.Empty:
                        break

            self.get_logger().info(f"[ASR ON] delay={delay}")

        elif not should_listen and self.is_listening:
            self.get_logger().info("[ASR OFF] (TTS speaking or mode is off)")

        self.is_listening = should_listen

    def mode_callback(self, msg):
        with self.lock:
            self.mode = msg.data
            self.get_logger().info(f"MODE CHANGED → {self.mode}")
            self.set_recognizer()
            self.recognizer.Reset()

        self.update_listening_state()
        self.get_logger().info(f"Recognizer updated for mode: {self.mode}")

    def grammar_callback(self, msg):
        try:
            new_grammar = json.loads(msg.data)
            with self.lock:
                self.command_grammar = new_grammar
                self.get_logger().info(f"Gramática actualizada: {len(new_grammar)} frases")

                if self.mode == "command":
                    self.set_recognizer()
                    self.recognizer.Reset()
        except Exception as e:
            self.get_logger().error(f"Error al parsear gramática: {e}")

    def audio_callback(self, indata, frames, time, status):
        if not self.is_listening:
            return
        now = self.get_clock().now().nanoseconds
        if now < self.ignore_until:
            return
        self.q.put(bytes(indata))

    def listen(self):
        with sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype='int16',
            channels=1,
            callback=self.audio_callback
        ):
            self.get_logger().info("Listening...")

            while rclpy.ok():
                try:
                    data = self.q.get(timeout=0.1)
                except queue.Empty:
                    continue

                if not self.is_listening:
                    continue

                audio_np = np.frombuffer(data, dtype=np.int16)
                volume = int(np.std(audio_np))
                now_ns = self.get_clock().now().nanoseconds
                elapsed_s = (now_ns - self.start_time) / 1e9

                if not self.is_calibrated:
                    self.ambient_noise_std = self.ambient_noise_std * 0.8 + volume * 0.2
                    if elapsed_s > self.calibration_duration:
                        self.is_calibrated = True
                        self.get_logger().info(" Calibración terminada.")
                    continue

                if volume < self.ambient_noise_std * 1.5:
                    self.ambient_noise_std = self.ambient_noise_std * 0.999 + volume * 0.001

                self.max_vol_phrase = max(self.max_vol_phrase, volume)

                if now_ns % 2000000000 < 100000000:
                    self.get_logger().info(f"[NOISE FLOOR] {int(self.ambient_noise_std)} | [ACTUAL] {volume}")

                with self.lock:
                    accepted = self.recognizer.AcceptWaveform(data)
                    current_mode = self.mode
                    if accepted:
                        result = json.loads(self.recognizer.Result())
                        peak_in_finished_phrase = self.max_vol_phrase
                        self.max_vol_phrase = 0.0
                    else:
                        result = None

                if not accepted or result is None:
                    continue

                text = result.get("text", "").strip().lower()
                dynamic_threshold = self.ambient_noise_std * 2.8

                if peak_in_finished_phrase < dynamic_threshold:
                    self.get_logger().info(f" Ruido ignorado (Peak: {int(peak_in_finished_phrase)} < Thr: {int(dynamic_threshold)}): '{text}'")
                    continue

                self.get_logger().info(f"[MODE ACTIVE] {current_mode} | [SNR OK: {int(peak_in_finished_phrase)}]")
                self.get_logger().info(f"[RAW TEXT] '{text}'")

                if text == "":
                    continue

                # Publicar cualquier comando escuchado si no está en modo confirmación
                if current_mode == "command":
                    self.get_logger().info(f"[COMMAND] {text}")
                    self.publisher.publish(String(data=text))
                    continue

                # Para el modo confirmación, evaluamos y publicamos a voice_node
                if current_mode == "confirmation":
                    words = text.split()
                    if any(w in words for w in ["yes", "yeah", "sure", "confirm", "correct", "affirmative"]):
                        self.get_logger().info("CONFIRM DETECTED")
                        self.publisher.publish(String(data="yes"))
                    elif any(w in words for w in ["no", "cancel", "negative", "nope"]):
                        self.get_logger().info("NO DETECTED")
                        self.publisher.publish(String(data="no"))
                    else:
                        self.get_logger().info(f" No match en confirmation: '{text}'")
                    continue

def main(args=None):
    rclpy.init(args=args)
    node = VoskASRNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()