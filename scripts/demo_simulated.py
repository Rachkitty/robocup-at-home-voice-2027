#!/usr/bin/env python3
"""Run the existing four-node fixture and print its actual recorded topic trace."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    """Return a simulation trace only after the existing end-to-end assertions pass."""
    (ROOT / 'validation').mkdir(exist_ok=True)
    env = dict(os.environ, VOICE_DEMO_TRACE='1', PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='demo-', dir=ROOT / 'validation') as temporary:
        target = str(ROOT / 'tests/test_audio_simulated.py') + '::test_four_node_flow_synthetic_recognition_to_navigation'
        command = [sys.executable, '-m', 'pytest', '-q', '-s', '--basetemp', temporary, target]
        result = subprocess.run(command, cwd=ROOT, env=env, text=True,
                                capture_output=True, timeout=60)
    if result.returncode:
        print(result.stdout + result.stderr, file=sys.stderr)
        return result.returncode
    prefix = 'VOICE_DEMO_JSON='
    lines = [line.split(prefix, 1)[1] for line in result.stdout.splitlines() if prefix in line]
    if len(lines) != 1:
        print('Simulation passed but its trace is missing or ambiguous.', file=sys.stderr)
        return 1
    print(json.dumps(json.loads(lines[0]), indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
