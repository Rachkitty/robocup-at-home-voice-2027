"""Launch the historical four-node flow with portable model parameters."""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """Allow text-only DDS checks without importing audio nodes or models."""
    return LaunchDescription([
        DeclareLaunchArgument('audio', default_value='true',
                              description='Start Vosk and Piper audio nodes'),
        DeclareLaunchArgument('tts_model_path', default_value='',
                              description='User-provided authorized Piper ONNX voice'),
        Node(package='robocup_asr', executable='vosk_asr_node',
             name='vosk_asr_node', output='screen',
             condition=IfCondition(LaunchConfiguration('audio'))),
        Node(package='robocup_tts', executable='tts_node', name='tts_node',
             output='screen', condition=IfCondition(LaunchConfiguration('audio')),
             parameters=[{'model_path': LaunchConfiguration('tts_model_path')}]),
        Node(package='robocup_voice', executable='voice_node',
             name='voice_node', output='screen'),
        Node(package='robocup_speech_one', executable='speech_one',
             name='speech_one', output='screen'),
    ])
