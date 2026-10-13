"""Explicit ROS/audio test doubles; these tests do not exercise DDS or hardware."""
import importlib.util
import sys
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def environment(monkeypatch):
    records = []
    streams = []
    threads = []
    parameters = {}
    errors = []
    clock = types.SimpleNamespace(nanoseconds=10_000_000_000)

    class Message:
        def __init__(self, data=''):
            self.data = data

    class Publisher:
        def __init__(self, topic):
            self.topic = topic

        def publish(self, msg):
            records.append((self.topic, msg.data))

        def get_subscription_count(self):
            return 1

    class Timer:
        def cancel(self):
            pass

    class Node:
        def __init__(self, name):
            self.name = name
            self.parameters = {}

        def create_subscription(self, *args):
            return args

        def create_publisher(self, _, topic, depth):
            return Publisher(topic)

        def create_timer(self, *args):
            return Timer()

        def get_logger(self):
            return types.SimpleNamespace(info=lambda *_: None, warn=lambda *_: None,
                                         error=lambda message: errors.append(message))

        def get_clock(self):
            return types.SimpleNamespace(now=lambda: clock)

        def declare_parameter(self, name, default):
            self.parameters[name] = parameters.get(name, default)

        def get_parameter(self, name):
            return types.SimpleNamespace(value=self.parameters[name])

    class Recognizer:
        def __init__(self, *args):
            self.text = ''

        def Reset(self):
            pass

        def AcceptWaveform(self, data):
            return True

        def Result(self):
            import json
            return json.dumps({'text': self.text})

    class Thread:
        def __init__(self, *args, **kwargs):
            threads.append(self)

        def start(self):
            pass

    class Stream:
        def __init__(self, **kwargs):
            self.options = kwargs
            self.writes = []
            streams.append(self)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def write(self, array):
            self.writes.append(array.copy())

    ros = types.ModuleType('rclpy')
    ros.ok = lambda: False
    ros.Node = Node
    node = types.ModuleType('rclpy.node')
    node.Node = Node
    msgs = types.ModuleType('std_msgs.msg')
    msgs.String = msgs.Bool = Message
    share = types.ModuleType('ament_index_python.packages')
    share.get_package_share_directory = lambda name: str(ROOT / 'src' / name)
    vosk = types.ModuleType('vosk')
    vosk.Model = lambda path: path
    vosk.KaldiRecognizer = Recognizer
    sound = types.ModuleType('sounddevice')
    sound.RawInputStream = sound.OutputStream = Stream
    piper = types.ModuleType('piper')
    piper.PiperVoice = types.SimpleNamespace(load=lambda path: types.SimpleNamespace(
        config=types.SimpleNamespace(sample_rate=22050),
        synthesize=lambda text: [types.SimpleNamespace(audio_int16_array=b'\x01\x00' * 32)]))
    modules = {'rclpy': ros, 'rclpy.node': node, 'std_msgs': types.ModuleType('std_msgs'),
               'std_msgs.msg': msgs, 'ament_index_python': types.ModuleType('ament_index_python'),
               'ament_index_python.packages': share, 'vosk': vosk, 'piper': piper,
               'sounddevice': sound}
    for name, module in modules.items():
        monkeypatch.setitem(sys.modules, name, module)

    def load(package, filename, historical=False):
        base = ROOT / 'reference' / 'snapshot' if historical else ROOT
        path = base / 'src' / package / package / filename
        spec = importlib.util.spec_from_file_location('fixture_' + package + str(historical), path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, 'time'):
            module.time = types.SimpleNamespace(sleep=lambda *_: None, time=lambda: 100.0)
        if hasattr(module, 'threading'):
            module.threading = types.SimpleNamespace(Lock=__import__('threading').Lock, Thread=Thread)
        return module

    return types.SimpleNamespace(load=load, records=records, streams=streams, threads=threads,
                                 parameters=parameters, errors=errors, clock=clock,
                                 Message=Message, ros=ros, root=ROOT)
