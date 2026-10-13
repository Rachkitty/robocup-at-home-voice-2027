#!/usr/bin/env python3
"""Check colcon-installed assets and entry points without importing ROS."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ['robocup_asr', 'robocup_tts', 'robocup_voice', 'robocup_bringup', 'robocup_speech_one']
ENTRIES = {'robocup_asr': 'vosk_asr_node', 'robocup_tts': 'tts_node',
           'robocup_voice': 'voice_node', 'robocup_speech_one': 'speech_one'}


def main():
    """Validate isolated install prefixes against the extraction manifests."""
    for name in PACKAGES:
        prefix = ROOT / 'install' / name
        assert (prefix / 'share/ament_index/resource_index/packages' / name).is_file(), name
        assert (prefix / 'share' / name / 'package.xml').is_file(), name
        if name in ENTRIES:
            assert (prefix / 'lib' / name / ENTRIES[name]).is_file(), name
    config = 'src/robocup_voice/config/competition_config.yaml'
    assert (ROOT / config).read_bytes() == (ROOT / 'install/robocup_voice/share/robocup_voice/config/competition_config.yaml').read_bytes()
    assert (ROOT / 'install/robocup_bringup/share/robocup_bringup/launch/robot_launch.py').is_file()
    manifest = json.loads((ROOT / 'docs/model-provenance.json').read_text())
    base = ROOT / 'install/robocup_asr/share/robocup_asr/vosk_models'
    for entry in manifest['vosk']['files']:
        assert hashlib.sha256((base / entry['path']).read_bytes()).hexdigest() == entry['sha256']
    assert (base / 'vosk-model-small-en-us-0.15/LICENSE').is_file()
    assert (base / 'vosk-model-small-en-us-0.15/NOTICE').is_file()
    assert not list((ROOT / 'install').rglob('*.onnx'))
    print(json.dumps({'packages': len(PACKAGES), 'entry_points': len(ENTRIES),
                      'model_files_verified': len(manifest['vosk']['files']), 'status': 'passed'}))


if __name__ == '__main__':
    main()
