"""Launch the historical four-node flow with portable model parameters."""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """Allow text-only DDS checks without importing audio nodes or models."""
    workspace_dir = os.path.expanduser(
        '~/robocup-at-home-voice-2026/robocup-at-home-voice-2026'
    )
    venv_site_packages = os.path.join(
        workspace_dir, '.venv', 'lib', 'python3.12', 'site-packages'
    )

    # Ruta por defecto al modelo ONNX de Piper TTS
    default_tts_model = os.path.join(
        workspace_dir,
        'src',
        'robocup_tts',
        'piper-models',
        'en_US-amy-low.onnx',
    )

    current_pythonpath = os.environ.get('PYTHONPATH', '')
    new_pythonpath = (
        f'{venv_site_packages}:{current_pythonpath}'
        if current_pythonpath
        else venv_site_packages
    )

    return LaunchDescription([
        SetEnvironmentVariable(name='PYTHONPATH', value=new_pythonpath),
        DeclareLaunchArgument(
            'audio',
            default_value='true',
            description='Start Vosk and Piper audio nodes',
        ),
        DeclareLaunchArgument(
            'tts_model_path',
            default_value=default_tts_model,
            description='User-provided authorized Piper ONNX voice',
        ),
        Node(
            package='robocup_asr',
            executable='vosk_asr_node',
            name='vosk_asr_node',
            output='screen',
            condition=IfCondition(LaunchConfiguration('audio')),
        ),
        Node(
            package='robocup_tts',
            executable='tts_node',
            name='tts_node',
            output='screen',
            condition=IfCondition(LaunchConfiguration('audio')),
            parameters=[
                {'model_path': LaunchConfiguration('tts_model_path')}
            ],
        ),
        Node(
            package='robocup_voice',
            executable='voice_node',
            name='voice_node',
            output='screen',
        ),
        Node(
            package='robocup_speech_one',
            executable='speech_one',
            name='speech_one',
            output='screen',
        ),
    ])
