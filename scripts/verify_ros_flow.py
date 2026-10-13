#!/usr/bin/env python3
"""Real ROS/DDS text flow with Voice and SpeechOne; ASR/TTS/audio are excluded."""
import ast
import json
import time
from collections import defaultdict


def main():
    """Use real rclpy nodes and subscriptions, with bounded discovery and waits."""
    try:
        import rclpy
        from rclpy.node import Node
        from rclpy.executors import SingleThreadedExecutor
        from std_msgs.msg import String
        from robocup_voice.voice_node import VoiceNode
        from robocup_speech_one.speech_one import SpeechOneNode
    except ImportError as error:
        raise SystemExit('ROS runtime unavailable. Source Jazzy and install/setup.bash: ' + str(error))

    rclpy.init()
    executor = SingleThreadedExecutor()
    nodes = []
    received = defaultdict(list)
    try:
        voice = VoiceNode()
        nodes.append(voice)
        bridge = SpeechOneNode()
        nodes.append(bridge)
        probe = Node('voice_reconstruction_probe')
        nodes.append(probe)
        speech = probe.create_publisher(String, '/speech_text', 10)
        for topic in ['/command', '/target_object', '/nav_location', '/tts_text']:
            probe.create_subscription(String, topic,
                                      lambda msg, name=topic: received[name].append(msg.data), 10)
        for node in nodes:
            executor.add_node(node)

        def wait_for(condition, timeout=10.0):
            deadline = time.monotonic() + timeout
            while not condition() and time.monotonic() < deadline:
                executor.spin_once(timeout_sec=0.05)
            if not condition():
                raise AssertionError('Timed out waiting for ROS discovery or expected topic data')

        wait_for(lambda: all([speech.get_subscription_count() > 0,
                             voice.command_pub.get_subscription_count() >= 2,
                             bridge.location_pub.get_subscription_count() > 0,
                             bridge.object_pub.get_subscription_count() > 0,
                             voice.tts_pub.get_subscription_count() > 0]))
        speech.publish(String(data='ava'))
        wait_for(lambda: voice.state == 'waiting_command')
        speech.publish(String(data='milk bed'))
        wait_for(lambda: voice.state == 'confirm')
        # Direct text injection: this bypasses the historical ASR literal-yes gap.
        speech.publish(String(data='yes'))
        wait_for(lambda: all([received['/nav_location'], received['/target_object'],
                             received['/command'], len(received['/tts_text']) >= 3]))
        assert ast.literal_eval(received['/command'][-1]) == {'object': 'milk', 'location': 'bed'}
        assert received['/target_object'][-1] == 'milk'
        assert received['/nav_location'][-1] == 'bed'
        print(json.dumps({'status': 'passed', 'transport': 'real ROS/DDS',
                          'nodes': ['voice_node', 'speech_one'], 'physical_audio': False,
                          'ASR_and_TTS_engines_in_flow': False, 'messages': dict(received)}))
    finally:
        executor.shutdown()
        for node in reversed(nodes):
            node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
