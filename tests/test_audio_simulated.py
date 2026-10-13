"""Synthetic PCM and fake recognition/synthesis: no microphone, speaker, or DDS."""
import numpy as np
import pytest


def asr(environment):
    return environment.load('robocup_asr', 'vosk_asr_node.py').VoskASRNode()


def deliver(environment, node, text):
    node.recognizer.text = text
    node.is_calibrated = True
    node.ambient_noise_std = 10.0
    node.q.put(np.array([5000, -5000] * 4000, dtype=np.int16).tobytes())
    iterations = iter([True, False])
    environment.ros.ok = lambda: next(iterations)
    node.listen()


@pytest.mark.parametrize('text,expected', [
    ('confirm', 'yes'), ('correct', 'yes'), ('affirmative', 'yes'),
    ('no', 'no'), ('negative', 'no'), ('yes', None),
])
def test_ASR_confirmation_mapping_preserves_historical_yes_gap(environment, text, expected):
    node = asr(environment)
    node.mode_callback(environment.Message('confirmation'))
    deliver(environment, node, text)
    values = [data for topic, data in environment.records if topic == '/speech_text']
    assert values == ([] if expected is None else [expected])


def test_audio_callback_drops_muted_and_guard_window_pcm(environment):
    node = asr(environment)
    node.control_callback(environment.Message(False))
    node.audio_callback(b'\x01\x00', 1, None, None)
    assert node.q.empty()
    node.mode_callback(environment.Message('confirmation'))
    assert not node.is_listening  # Mode switching must not override TTS mute.
    node.control_callback(environment.Message(True))
    node.audio_callback(b'\x01\x00', 1, None, None)
    assert node.q.empty()
    environment.clock.nanoseconds += 200_000_000
    node.audio_callback(b'\x01\x00', 1, None, None)
    assert node.q.get_nowait() == b'\x01\x00'


def tts(environment, tmp_path):
    model = tmp_path / 'authorized-fixture.onnx'
    model.touch()
    (tmp_path / 'authorized-fixture.onnx.json').write_text('{}')
    environment.parameters['model_path'] = str(model)
    module = environment.load('robocup_tts', 'tts_node.py')
    return module, module.TTSNode()


def test_TTS_missing_weights_has_actionable_error(environment):
    module = environment.load('robocup_tts', 'tts_node.py')
    with pytest.raises(FileNotFoundError, match='intentionally not bundled'):
        module.TTSNode()


def test_TTS_requires_matching_config(environment, tmp_path):
    model = tmp_path / 'fixture.onnx'
    model.touch()
    environment.parameters['model_path'] = str(model)
    with pytest.raises(FileNotFoundError, match='onnx.json'):
        environment.load('robocup_tts', 'tts_node.py').TTSNode()


@pytest.mark.parametrize('failure', [False, True])
def test_TTS_mutes_before_output_and_resumes_after_failure(environment, tmp_path, failure):
    _, node = tts(environment, tmp_path)
    observed = []

    def synthesize(text):
        observed.append(environment.records[-1])
        if failure:
            raise RuntimeError('synthetic synthesis failure')
        from types import SimpleNamespace
        return [SimpleNamespace(audio_int16_array=b'\x01\x00' * 32)]

    node.voice.synthesize = synthesize
    node.speak_callback(environment.Message('Hello operator'))
    assert observed == [('/asr_control', False)]
    assert environment.records == [('/asr_control', False), ('/asr_control', True)]
    if failure:
        assert environment.errors
    else:
        assert environment.streams[-1].writes[0].shape == (32, 1)


def test_four_node_flow_synthetic_recognition_to_navigation(environment, tmp_path):
    voice = environment.load('robocup_voice', 'voice_node.py').VoiceNode()
    bridge = environment.load('robocup_speech_one', 'speech_one.py').SpeechOneNode()
    asr_node = asr(environment)
    _, tts_node = tts(environment, tmp_path)
    processed = 0
    voice.publish_grammar_once()
    for text in ['ava', 'milk bed', 'confirm']:
        deliver(environment, asr_node, text)
        while processed < len(environment.records):
            topic, data = environment.records[processed]
            processed += 1
            message = environment.Message(data)
            if topic == '/speech_text':
                voice.callback(message)
            elif topic == '/tts_text':
                tts_node.speak_callback(message)
            elif topic == '/command':
                bridge.command_callback(message)
            elif topic == '/asr_grammar':
                asr_node.grammar_callback(message)
            elif topic == '/asr_mode':
                asr_node.mode_callback(message)
            elif topic == '/asr_control':
                asr_node.control_callback(message)
        environment.clock.nanoseconds += 2_000_000_000
    assert ('/target_object', 'milk') in environment.records
    assert ('/nav_location', 'bed') in environment.records
    assert voice.state == 'idle'
    assert asr_node.is_listening
    assert len([stream for stream in environment.streams if stream.writes]) == 3

    import json
    import os
    if os.environ.get('VOICE_DEMO_TRACE') == '1':
        observed = {}
        for topic, data in environment.records:
            observed.setdefault(topic, []).append(data)
        print('VOICE_DEMO_JSON=' + json.dumps({
            'mode': 'simulated', 'ROS_DDS': False, 'physical_audio': False,
            'recognition_and_synthesis': 'test doubles',
            'input_fixtures': ['ava', 'milk bed', 'confirm'],
            'observed_topics': observed,
            'final_dialogue_state': voice.state,
            'status': 'passed',
        }))


@pytest.mark.parametrize('sample_rate', [16000, 22050, 24000])
def test_F02_TTS_output_uses_authorized_voice_sample_rate(environment, tmp_path, sample_rate):
    _, node = tts(environment, tmp_path)
    node.voice.config.sample_rate = sample_rate
    node.speak_callback(environment.Message('Hello operator'))
    assert environment.streams[-1].options['samplerate'] == sample_rate


def test_ASR_model_override_is_portable(environment, tmp_path):
    model = tmp_path / 'external-vosk' / 'am'
    model.mkdir(parents=True)
    (model / 'final.mdl').touch()
    environment.parameters['model_path'] = str(model.parent)
    assert asr(environment).model == str(model.parent)


def test_ASR_missing_model_has_explicit_error(environment, tmp_path):
    environment.parameters['model_path'] = str(tmp_path / 'missing')
    with pytest.raises(FileNotFoundError, match='incomplete or missing'):
        asr(environment)
