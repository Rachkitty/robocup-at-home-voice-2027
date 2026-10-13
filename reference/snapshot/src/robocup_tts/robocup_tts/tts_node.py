#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool

import time
import numpy as np
import sounddevice as sd

from piper import PiperVoice


class TTSNode(Node):

    def __init__(self):
        super().__init__('tts_node')

        # Subscriber (texto a voz)
        self.subscription = self.create_subscription(
            String,
            '/tts_text',
            self.speak_callback,
            10
        )

        # Control ASR (pausar/reanudar)
        self.asr_control_pub = self.create_publisher(
            Bool,
            '/asr_control',
            10
        )

        # Configuración audio (opcional)
        # sd.default.device = 0

        # Cargar modelo Piper
        self.model_path = "/home/raffiki/ros2_ws/src/robocup_tts/piper-models/en_US-lessac-medium.onnx"

        self.get_logger().info("Loading Piper model...")
        self.voice = PiperVoice.load(self.model_path)
        self.get_logger().info("Piper TTS Ready")

        # Saludo inicial
        self.greeted = False
        self.greeting_timer = self.create_timer(2.0, self.greeting_callback)

    def greeting_callback(self):
        if not self.greeted:
            msg = String()
            msg.data = "Hello, my name is Havva, say my name if you need my help, and wait for my response before you ask me a petition"
            self.speak_callback(msg)
            self.greeted = True
            self.greeting_timer.cancel()

    # CALLBACK PRINCIPAL
    def speak_callback(self, msg):

        text = msg.data.strip()

        if text == "":
            return

        # limpiar texto
        text = text.replace('"', '')

        self.get_logger().info(f"Speaking: {text}")

        # PAUSAR ASR
        self.asr_control_pub.publish(Bool(data=False))
        
        # Darle tiempo al nodo ASR de recibir el mensaje y pausarse antes de hacer ruido
        time.sleep(0.1)

        try:
            # Reproducir cada chunk al generarse.
            with sd.OutputStream(
                samplerate=22050,
                channels=1,
                dtype='int16',
                latency='high'
            ) as stream:
                for chunk in self.voice.synthesize(text):

                    arr = chunk.audio_int16_array

                    if arr is None or len(arr) == 0:
                        continue

                    if isinstance(arr, (bytes, bytearray)):
                        arr_np = np.frombuffer(arr, dtype=np.int16)
                    else:
                        arr_np = np.array(arr, dtype=np.int16).flatten()

                    stream.write(arr_np.reshape(-1, 1))

        except Exception as e:
            self.get_logger().error(f"TTS error: {e}")

        # DELAY ANTI-ECO
        # latency='high' hace que al terminar el loop aún quede audio en el hardware buffer.
        # Además, el "reverb" físico del robot suma milisegundos.
        word_count = len(text.split())
        delay = 0.8 if word_count <= 3 else 1.2
        time.sleep(delay)

        # REACTIVAR ASR
        self.asr_control_pub.publish(Bool(data=True))


# MAIN
def main(args=None):

    rclpy.init(args=args)

    node = TTSNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
