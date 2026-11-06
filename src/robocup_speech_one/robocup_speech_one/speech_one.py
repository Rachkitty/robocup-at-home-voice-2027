#!/usr/bin/env python3
"""Nodo ROS 2 que extrae entidades (objeto / ubicación) usando spaCy."""

import os
import yaml
from ament_index_python.packages import get_package_share_directory

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import spacy
from spacy.matcher import PhraseMatcher

class SpeechOneNode(Node):
    def __init__(self):
        super().__init__("speech_one")

        self.ENTITIES = self.load_config()
        self.get_logger().info(f"Entidades cargadas dinámicamente: {self.ENTITIES}")

        self.get_logger().info("Loading spaCy model 'en_core_web_sm'...")
        try:
            self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        except OSError as exc:
            self.get_logger().error(
                "Model 'en_core_web_sm' not found. "
                "Install it with: python -m spacy download en_core_web_sm"
            )
            raise exc

        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LEMMA")
        for label, words in self.ENTITIES.items():
            if words:
                self.matcher.add(label, list(self.nlp.pipe(words)))

        self.publishers_by_label = {
            "target_object": self.create_publisher(String, "/target_object", 10),
            "nav_location": self.create_publisher(String, "/nav_location", 10),
        }

        # Escucha a /command (directo de voice_node tras validar)
        self.create_subscription(String, "/command", self.command_callback, 10)

        self.get_logger().info("speech_one node ready, waiting for /command...")

    def load_config(self):
        try:
            config_path = os.path.join(
                get_package_share_directory('robocup_voice'),
                'config',
                'competition_config.yaml',
            )
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return {
                    "target_object": config.get('objects', []),
                    "nav_location": config.get('locations', [])
                }
        except Exception as e:
            self.get_logger().error(f'Error cargando config en speech_one: {e}')
            return {
                "target_object": ["coke", "milk", "noodle", "yogurt"],
                "nav_location": ["bed", "table", "shelf", "counter", "kitchen", "living room", "bathroom", "bedroom"],
            }

    def command_callback(self, msg: String):
        sentence = msg.data.strip().lower()
        if not sentence:
            return
            
        doc = self.nlp(sentence)

        found = {}
        matches = sorted(self.matcher(doc), key=lambda m: m[1])
        for match_id, start, end in matches:
            label = self.nlp.vocab.strings[match_id]
            if label not in found:
                found[label] = doc[start:end].lemma_

        if not found:
            self.get_logger().info(f"No entities found in: '{sentence}'")
            return

        for label, value in found.items():
            self.publishers_by_label[label].publish(String(data=value))
            self.get_logger().info(f"Found {label}: '{value}'")


def main(args=None):
    rclpy.init(args=args)
    node = SpeechOneNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == "__main__":
    main()