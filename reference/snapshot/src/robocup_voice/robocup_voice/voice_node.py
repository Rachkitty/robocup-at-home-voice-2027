#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time
import re
import os
import yaml
from ament_index_python.packages import get_package_share_directory


class VoiceNode(Node):

    def __init__(self):
        super().__init__('voice_node')

        # Subscriber
        self.sub = self.create_subscription(
            String,
            '/speech_text',
            self.callback,
            10
        )

        # Publishers
        self.tts_pub = self.create_publisher(String, '/tts_text', 10)
        self.command_pub = self.create_publisher(String, '/command', 10)
        self.asr_mode_pub = self.create_publisher(String, '/asr_mode', 10)
        self.asr_grammar_pub = self.create_publisher(String, '/asr_grammar', 10)

        # Cargar configuración
        self.config = self.load_config()
        self.objects = self.config.get('objects', [])
        self.locations = self.config.get('locations', [])
        self.aliases = self.config.get('aliases', {})
        self.wake_words = self.config.get('wake_words', ['havva'])

        self.get_logger().info(f"Objetos cargados: {self.objects}")
        self.get_logger().info(f"Locaciones cargadas: {self.locations}")

        # Publicar gramática al ASR
        self.timer_grammar = self.create_timer(2.0, self.publish_grammar_once)

        self.state = "idle"
        self.last_command = None

        self.waiting_confirmation = False
        self.confirmation_start_time = 0
        self.confirmation_timeout = 15.0  # dar tiempo al operador

        self.timer = self.create_timer(0.5, self.check_timeout)

        self.get_logger().info("Voice Node READY")

    # CARGAR YAML
    def load_config(self):

        try:
            config_path = os.path.join(
                get_package_share_directory('robocup_voice'),
                'config',
                'competition_config.yaml'
            )
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                self.get_logger().info(f"Config cargada desde: {config_path}")
                return config

        except Exception as e:
            self.get_logger().error(f"Error cargando config: {e}")
            return {
                'objects': ['coke'],
                'locations': ['kitchen'],
                'aliases': {}
            }

    # PUBLICAR GRAMÁTICA AL ASR
    def publish_grammar_once(self):
        """Publica la lista de frases al ASR node para construir su gramática."""

        if self.asr_grammar_pub.get_subscription_count() == 0:
            self.get_logger().info("Esperando al nodo ASR para enviarle la gramática...")
            return

        grammar_sentences = ["[unk]"]
        grammar_sentences.extend(self.wake_words)

        for obj in self.objects:
            grammar_sentences.append(obj)
        for loc in self.locations:
            grammar_sentences.append(loc)

        import json
        self.asr_grammar_pub.publish(String(data=json.dumps(grammar_sentences)))
        self.get_logger().info(f"Gramática publicada: {len(grammar_sentences)} frases")

        self.timer_grammar.cancel()

    # NORMALIZAR ALIASES
    def normalize_aliases(self, text):
        """Reemplaza variantes fonéticas por el término canónico."""

        for canonical, alias_list in self.aliases.items():
            for alias in alias_list:
                text = re.sub(r'\b' + re.escape(alias) + r'\b', canonical, text, flags=re.IGNORECASE)

        return text

    # MAIN CALLBACK
    def callback(self, msg):

        text = msg.data.strip().lower()
        self.get_logger().info(f"[VOICE] Heard: {text}")

        # IDLE (WAKE WORD)
        if self.state == "idle":

            if text in self.wake_words:

                self.get_logger().info("🤖 Wake word detected")

                self.state = "waiting_command"

                # apagar ASR (evitar eco)
                self.asr_mode_pub.publish(String(data="off"))

                # TTS
                self.tts_pub.publish(String(data="yes, what can I bring you?"))

                # activar modo comando
                time.sleep(0.15)
                self.asr_mode_pub.publish(String(data="command"))

                return

        # WAITING COMMAND
        elif self.state == "waiting_command":

            # Normalizar aliases antes de parsear
            text_normalized = self.normalize_aliases(text)
            self.get_logger().info(f"[NORMALIZED] {text_normalized}")

            command = self.parse_command(text_normalized)

            self.get_logger().info(f"[PARSE RESULT] {command}")

            if command:

                self.last_command = command
                self.state = "confirm"

                # apagar ASR
                self.asr_mode_pub.publish(String(data="off"))

                obj = command['object']
                loc = command['location']
                self.tts_pub.publish(
                    String(data=f"I heard: bring {obj} from {loc}. Say confirm or no.")
                )

                # ACTIVAR CONFIRMATION
                time.sleep(0.15)
                self.get_logger().info("Switching to CONFIRMATION mode")
                self.asr_mode_pub.publish(String(data="confirmation"))

                self.waiting_confirmation = True
                self.confirmation_start_time = time.time()

            else:
                self.tts_pub.publish(
                    String(data="Sorry, I did not understand. Please repeat the command.")
                )

            return

        # CONFIRMATION
        elif self.state == "confirm":

            if text == "yes":

                self.get_logger().info("✅ CONFIRMED (voice)")
                self._execute_command()

            elif text == "no":

                self.get_logger().info("❌ REJECTED (voice)")

                self.tts_pub.publish(
                    String(data="Okay. Please repeat the command.")
                )

                # Regresar a esperar comando directamente sin pasar por IDLE (sin wake word)
                self.state = "waiting_command"
                self.waiting_confirmation = False
                self.last_command = None
                self.asr_mode_pub.publish(String(data="command"))

            else:
                self.get_logger().info("Waiting confirmation...")

            return

    # AUTO-EJECUTA el comando si no dice "no"
    def check_timeout(self):

        if self.waiting_confirmation:

            elapsed = time.time() - self.confirmation_start_time

            if elapsed > self.confirmation_timeout:

                self.get_logger().info("AUTO-EJECUTANDO")
                # Un solo mensaje: evita el doble TTS
                self._execute_command(tts_msg="Executing command automatically.")

    # EXECUTE COMMAND
    def _execute_command(self, tts_msg="Okay. Executing command."):

        self.get_logger().info(f"EXECUTING: {self.last_command}")

        self.tts_pub.publish(String(data=tts_msg))

        self.command_pub.publish(
            String(data=str(self.last_command))
        )

        self.reset_state()

    # RESET
    def reset_state(self):

        self.state = "idle"
        self.waiting_confirmation = False
        self.last_command = None

        self.get_logger().info("Reset to IDLE")

        self.asr_mode_pub.publish(String(data="command"))

    # usa objetos y locaciones del YAML
    def parse_command(self, text):

        self.get_logger().info(f"[PARSING] '{text}'")

        found_object = None
        found_location = None

        sorted_objects = sorted(self.objects, key=len, reverse=True)
        sorted_locations = sorted(self.locations, key=len, reverse=True)

        for obj in sorted_objects:
            if re.search(r'\b' + re.escape(obj) + r'\b', text, re.IGNORECASE):
                found_object = obj
                break
                
        for loc in sorted_locations:
            if re.search(r'\b' + re.escape(loc) + r'\b', text, re.IGNORECASE):
                found_location = loc
                break

        if found_object and found_location:
            return {
                'object': found_object,
                'location': found_location
            }

        return None


# MAIN
def main(args=None):

    rclpy.init(args=args)

    node = VoiceNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
