#!/usr/bin/env python3
"""Real Vosk engine smoke check with synthetic silence; no audio device."""
import json
from pathlib import Path
from vosk import Model, KaldiRecognizer

ROOT = Path(__file__).resolve().parents[1]


def main():
    """Load the colcon-installed model and decode one second of synthetic PCM."""
    path = ROOT / 'install/robocup_asr/share/robocup_asr/vosk_models/vosk-model-small-en-us-0.15'
    recognizer = KaldiRecognizer(Model(str(path)), 16000)
    recognizer.AcceptWaveform(b'\x00\x00' * 16000)
    result = json.loads(recognizer.FinalResult())
    assert result.get('text') == ''
    print(json.dumps({'engine': 'Vosk', 'pcm': 'one second synthetic silence',
                      'text': result['text'], 'physical_audio': False, 'status': 'passed'}))


if __name__ == '__main__':
    main()
