#!/usr/bin/env python3

import json
import os
import re
import time
from ament_index_python.packages import get_package_share_directory
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import yaml


class VoiceNode(Node):

    def __init__(self):
        super().__init__('voice_node')

        self.sub = self.create_subscription(String, '/speech_text', self.callback, 10)
        self.tts_pub = self.create_publisher(String, '/tts_text', 10)
        self.command_pub = self.create_publisher(String, '/command', 10)
        self.asr_mode_pub = self.create_publisher(String, '/asr_mode', 10)
        self.asr_grammar_pub = self.create_publisher(String, '/asr_grammar', 10)

        self.config = self.load_config()
        self.objects = self.config.get('objects', [])
        self.locations = self.config.get('locations', [])
        self.aliases = self.config.get('aliases', {})

        self.wake_words = self.config.get('wake_words', ['havva', 'hava', 'ava', 'java', 'robot', 'havva robot', 'hava robot', 'ava robot', 'java robot'])
        self.confirm_yes = ['yes', 'confirm', 'correct', 'affirmative', 'yeah', 'sure']
        self.confirm_no = ['no', 'cancel', 'negative', 'nope']

        self.get_logger().info(f'Objetos cargados: {self.objects}')
        self.get_logger().info(f'Locaciones cargadas: {self.locations}')
        self.get_logger().info(f'Wake words activas: {self.wake_words}')

        self.timer_grammar = self.create_timer(2.0, self.publish_grammar_once)

        # --- MEJORA 1: INICIATIVA DEL ROBOT AL INICIAR ---
        self.has_welcomed = False
        self.timer_welcome = self.create_timer(6.0, self.say_welcome_once)

        # Memoria persistente de slots para aclaraciones
        self.current_object = None
        self.current_location = None

        self.state = 'idle'
        self.last_command = None

        self.waiting_confirmation = False
        self.confirmation_start_time = 0
        self.confirmation_timeout = 15.0

        self.timer = self.create_timer(0.5, self.check_timeout)
        self.get_logger().info('Voice Node READY')

    def say_welcome_once(self):
        """El robot toma la iniciativa e instruye al usuario al posicionarse en el área."""
        if not self.has_welcomed:
            self.has_welcomed = True
            self.timer_welcome.cancel()
            presentation_msg = (
                "Hello, my name is Havva. I am here to serve you. "
                "Please say my name at the beginning of each instruction and wait for my response. "
                "What can I bring you and from where?"
            )
            self.tts_pub.publish(String(data=presentation_msg))
            self.get_logger().info('📢 Havva ha tomado la iniciativa con su presentación oficial.')
            self.state = 'waiting_command'
            self.asr_mode_pub.publish(String(data='command'))

    def load_config(self):
        try:
            config_path = os.path.join(
                get_package_share_directory('robocup_voice'),
                'config',
                'competition_config.yaml',
            )
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                self.get_logger().info(f'Config cargada desde: {config_path}')
                return config
        except Exception as e:
            self.get_logger().error(f'Error cargando config: {e}')
            return {
                'objects': ['coke', 'milk', 'noodle', 'yogurt'],
                'locations': ['bed', 'table', 'shelf', 'counter', 'kitchen'],
                'aliases': {},
            }

    def publish_grammar_once(self):
        if self.asr_grammar_pub.get_subscription_count() == 0:
            self.get_logger().info('Esperando al nodo ASR para enviarle la gramática...')
            return

        conversational_words = [
            '[unk]', 'can', 'you', 'could', 'would', 'please', 'me', 'the',
            'from', 'to', 'and', 'bring', 'get', 'take', 'go', 'find', 'fetch',
            'robot', 'a', 'an', 'some', 'is', 'it', 'on', 'in', 'at', 'for'
        ]

        vocabulary = set(conversational_words)
        vocabulary.update(self.wake_words)
        vocabulary.update(self.confirm_yes)
        vocabulary.update(self.confirm_no)
        vocabulary.update(self.objects)
        vocabulary.update(self.locations)

        grammar_words = list(vocabulary)

        self.asr_grammar_pub.publish(String(data=json.dumps(grammar_words)))
        self.get_logger().info(f'Vocabulario flexible publicado al ASR: {len(grammar_words)} palabras')
        self.timer_grammar.cancel()

    def normalize_aliases(self, text):
        for canonical, alias_list in self.aliases.items():
            for alias in alias_list:
                text = re.sub(r'\b' + re.escape(alias) + r'\b', canonical, text, flags=re.IGNORECASE)
        return text

    def callback(self, msg):
        text = msg.data.strip().lower()
        self.get_logger().info(f'[VOICE] Heard: {text}')

        # 1. ESTADO IDLE: El robot escucha cualquier oración y evalúa si dijeron su nombre.
        if self.state == 'idle':
            if any(ww in text for ww in self.wake_words):
                self.get_logger().info('🤖 Wake word detected in phrase')
                text_normalized = self.normalize_aliases(text)
                
                command = self.parse_command(text_normalized)
                if command:
                    self.process_command(command, text_normalized)
                else:
                    self.state = 'waiting_command'
                    self.asr_mode_pub.publish(String(data='off'))
                    self.tts_pub.publish(String(data='Yes, what can I bring you and from where?'))
                    time.sleep(0.15)
                    self.asr_mode_pub.publish(String(data='command'))
            return

        # 2. ESTADO WAITING_COMMAND: Escucha comandos o respuestas a preguntas de aclaración.
        elif self.state == 'waiting_command':
            text_normalized = self.normalize_aliases(text)
            command = self.parse_command(text_normalized)
            if command:
                self.process_command(command, text_normalized)
            else:
                self.tts_pub.publish(String(data='Sorry, I did not understand. Please repeat.'))
            return

        # 3. ESTADO CONFIRM: Validación final por voz.
        elif self.state == 'confirm':
            if any(word in text for word in self.confirm_yes):
                self.get_logger().info('✅ CONFIRMED (voice)')
                # Emite la frase en el formato estricto: "Bring [OBJETO] from [LUGAR]."
                repeat_msg = f"Bring {self.current_object} from {self.current_location}."
                self._execute_command(tts_msg=repeat_msg)
            elif any(word in text for word in self.confirm_no):
                self.get_logger().info('❌ REJECTED (voice)')
                self.tts_pub.publish(String(data='Okay. Please repeat the command.'))
                self.reset_slots()
                self.state = 'waiting_command'
                self.waiting_confirmation = False
                self.last_command = None
                self.asr_mode_pub.publish(String(data='command'))
            else:
                self.get_logger().info('Waiting confirmation...')
            return

    def process_command(self, command, text_normalized):
        """Maneja la acumulación de slots y preguntas de aclaración proactivas."""
        obj = command.get('object')
        loc = command.get('location')

        # Acumular entidades en los slots de memoria
        if obj:
            self.current_object = obj
        if loc:
            self.current_location = loc

        # CASO 1: Se tienen AMBOS datos -> Formato exacto y solicitud de confirmación
        if self.current_object and self.current_location:
            self.get_logger().info(f'[PARSE COMPLETE] Object: {self.current_object}, Location: {self.current_location}')
            self.command_pub.publish(String(data=text_normalized))
            
            self.last_command = {'object': self.current_object, 'location': self.current_location}
            self.state = 'confirm'
            self.asr_mode_pub.publish(String(data='off'))
            
            # Formato requerido de repetición: "Bring [OBJETO] from [LUGAR]."
            confirm_phrase = f'Bring {self.current_object} from {self.current_location}. Say confirm or no.'
            self.tts_pub.publish(String(data=confirm_phrase))
            time.sleep(0.15)
            self.get_logger().info('Switching to CONFIRMATION mode')
            self.asr_mode_pub.publish(String(data='confirmation'))

            self.waiting_confirmation = True
            self.confirmation_start_time = time.time()

        # CASO 2: Falta el LUGAR -> Iniciativa del robot preguntando por la ubicación
        elif self.current_object and not self.current_location:
            self.get_logger().info(f'[INCOMPLETE COMMAND] Object present ({self.current_object}), missing location.')
            self.asr_mode_pub.publish(String(data='off'))
            self.tts_pub.publish(String(data=f'Where should I get the {self.current_object} from?'))
            time.sleep(0.15)
            self.state = 'waiting_command'
            self.asr_mode_pub.publish(String(data='command'))

        # CASO 3: Falta el OBJETO -> Iniciativa del robot preguntando por el objeto
        elif not self.current_object and self.current_location:
            self.get_logger().info(f'[INCOMPLETE COMMAND] Location present ({self.current_location}), missing object.')
            self.asr_mode_pub.publish(String(data='off'))
            self.tts_pub.publish(String(data=f'What item should I bring from the {self.current_location}?'))
            time.sleep(0.15)
            self.state = 'waiting_command'
            self.asr_mode_pub.publish(String(data='command'))

    def check_timeout(self):
        if self.waiting_confirmation:
            elapsed = time.time() - self.confirmation_start_time
            if elapsed > self.confirmation_timeout:
                self.get_logger().info('AUTO-EJECUTANDO POR TIMEOUT')
                repeat_msg = f"Bring {self.current_object} from {self.current_location}."
                self._execute_command(tts_msg=repeat_msg)

    def _execute_command(self, tts_msg=None):
        if tts_msg is None:
            tts_msg = f"Bring {self.current_object} from {self.current_location}."
        self.get_logger().info(f'EXECUTING: {self.last_command}')
        self.tts_pub.publish(String(data=tts_msg))
        self.reset_state()

    def reset_slots(self):
        self.current_object = None
        self.current_location = None

    def reset_state(self):
        self.state = 'idle'
        self.waiting_confirmation = False
        self.last_command = None
        self.reset_slots()
        self.get_logger().info('Reset to IDLE')
        self.asr_mode_pub.publish(String(data='command'))

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

        if found_object or found_location:
            result = {}
            if found_object:
                result['object'] = found_object
            if found_location:
                result['location'] = found_location
            return result

        return None


def main(args=None):
    rclpy.init(args=args)
    node = VoiceNode()
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