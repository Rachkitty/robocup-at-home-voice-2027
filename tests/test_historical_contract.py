"""Compare the reconstructed dialogue with the immutable April source."""
import ast

import pytest


@pytest.mark.parametrize('text,expected', [
    ('milk bed', {'object': 'milk', 'location': 'bed'}),
    ('please get cake from the table', {'object': 'coke', 'location': 'table'}),
    ('noodle on shelf', {'object': 'noodle', 'location': 'shelf'}),
    ('bring water from kitchen', None),
    ('milk', None),
])
def test_keyword_parser_matches_reference(environment, text, expected):
    for historical in [False, True]:
        module = environment.load('robocup_voice', 'voice_node.py', historical)
        node = module.VoiceNode()
        assert node.parse_command(node.normalize_aliases(text)) == expected


@pytest.mark.parametrize('confirmation,state,has_command', [
    ('yes', 'idle', True), ('no', 'waiting_command', False), ('confirm', 'confirm', False),
])
def test_dialogue_sequence_matches_reference(environment, confirmation, state, has_command):
    traces = []
    for historical in [False, True]:
        environment.records.clear()
        module = environment.load('robocup_voice', 'voice_node.py', historical)
        node = module.VoiceNode()
        for text in ['ava', 'milk bed', confirmation]:
            node.callback(environment.Message(text))
        assert node.state == state
        commands = [data for topic, data in environment.records if topic == '/command']
        assert bool(commands) == has_command
        if commands:
            assert ast.literal_eval(commands[-1]) == {'object': 'milk', 'location': 'bed'}
        traces.append(environment.records.copy())
    assert traces[0] == traces[1]


def test_timeout_boundary_and_autoexecution_match_reference(environment):
    for historical in [False, True]:
        environment.records.clear()
        module = environment.load('robocup_voice', 'voice_node.py', historical)
        node = module.VoiceNode()
        for text in ['ava', 'milk bed']:
            node.callback(environment.Message(text))
        module.time.time = lambda: 115.0
        node.check_timeout()
        assert not any(topic == '/command' for topic, _ in environment.records)
        module.time.time = lambda: 115.01
        node.check_timeout()
        assert ('/command', "{'object': 'milk', 'location': 'bed'}") in environment.records
        assert node.state == 'idle'


def test_rejection_accepts_next_command_without_wake(environment):
    module = environment.load('robocup_voice', 'voice_node.py')
    node = module.VoiceNode()
    for text in ['ava', 'milk bed', 'no', 'yogurt shelf', 'yes']:
        node.callback(environment.Message(text))
    assert ('/command', "{'object': 'yogurt', 'location': 'shelf'}") in environment.records


@pytest.mark.parametrize('text,outputs', [
    ("{'object': 'milk', 'location': 'bed'}", [('/target_object', 'milk'), ('/nav_location', 'bed')]),
    ("{'object': 'milk'}", [('/target_object', 'milk')]),
    ("{'location': 'bed'}", [('/nav_location', 'bed')]),
    ("{'object': '', 'location': ''}", []), ('not a dict', []), ('[]', []),
    ("__import__('os').system('false')", []),
])
def test_bridge_valid_and_rejected_payloads_match_reference(environment, text, outputs):
    for historical in [False, True]:
        environment.records.clear()
        module = environment.load('robocup_speech_one', 'speech_one.py', historical)
        module.SpeechOneNode().command_callback(environment.Message(text))
        assert environment.records == outputs


@pytest.mark.parametrize('bad', [None, 3, [], {}])
def test_F01_rejects_nonstring_fields_without_publishing(environment, bad):
    module = environment.load('robocup_speech_one', 'speech_one.py')
    module.SpeechOneNode().command_callback(environment.Message(str({'object': bad, 'location': 'bed'})))
    assert environment.records == []
    assert environment.errors
    original = environment.load('robocup_speech_one', 'speech_one.py', True)
    with pytest.raises(AttributeError):
        original.SpeechOneNode().command_callback(environment.Message(str({'object': bad, 'location': 'bed'})))
