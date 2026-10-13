"""Check archive fidelity and omitted weights without requiring ROS."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_immutable_text_reference_matches_source_manifest():
    manifest = json.loads((ROOT / 'docs/extraction-manifest.json').read_text())
    for entry in manifest['files']:
        reference = ROOT / 'reference/snapshot' / entry['path']
        if reference.exists():
            assert hashlib.sha256(reference.read_bytes()).hexdigest() == entry['sha256']


def test_Vosk_matches_verified_upstream_manifest():
    manifest = json.loads((ROOT / 'docs/model-provenance.json').read_text())
    for entry in manifest['vosk']['files']:
        model = ROOT / 'src/robocup_asr/vosk_models' / entry['path']
        assert hashlib.sha256(model.read_bytes()).hexdigest() == entry['sha256']
        assert entry['upstream_match']


def test_no_Piper_weights_are_bundled():
    assert not list(ROOT.rglob('*.onnx'))


def test_package_and_reference_boundaries():
    assert (ROOT / 'reference/COLCON_IGNORE').exists()
    assert sorted(path.name for path in (ROOT / 'src').iterdir()) == [
        'robocup_asr', 'robocup_bringup', 'robocup_speech_one', 'robocup_tts', 'robocup_voice']
