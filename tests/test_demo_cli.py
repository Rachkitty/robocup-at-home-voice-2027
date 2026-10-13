"""Verify that the portfolio demo runs from another working directory."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_demo_cli_reports_actual_simulation_trace_from_another_directory(tmp_path):
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/demo_simulated.py')],
                            cwd=tmp_path, capture_output=True, text=True, timeout=60, check=True)
    trace = json.loads(result.stdout)
    assert trace['mode'] == 'simulated'
    assert trace['ROS_DDS'] is False and trace['physical_audio'] is False
    assert trace['recognition_and_synthesis'] == 'test doubles'
    assert trace['observed_topics']['/speech_text'] == ['ava', 'milk bed', 'yes']
    assert trace['observed_topics']['/target_object'] == ['milk']
    assert trace['observed_topics']['/nav_location'] == ['bed']
    assert trace['final_dialogue_state'] == 'idle'
