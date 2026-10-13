import os

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Nodo ASR (Vosk)
        Node(
            package='robocup_asr',
            executable='vosk_asr_node',
            name='vosk_asr_node',
            output='screen'
        ),
        # Nodo TTS (Piper)
        Node(
            package='robocup_tts',
            executable='tts_node',
            name='tts_node',
            output='screen'
        ),
        # Nodo principal de Voice 
        Node(
            package='robocup_voice',
            executable='voice_node',
            name='voice_node',
            output='screen'
        ),
        # Nodo speech One
        Node(
            package='robocup_speech_one',
            executable='speech_one',
            name='speech_one',
            output='screen'
        )
    ])
