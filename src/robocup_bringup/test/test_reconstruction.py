"""Run the hardware-free reconstruction suite from colcon."""
from pathlib import Path
import subprocess
import sys


def test_reconstructed_stack():
    """Retain the standalone suite while exposing it to colcon test."""
    root = Path(__file__).resolve().parents[3]
    subprocess.run([sys.executable, '-m', 'pytest', str(root / 'tests'), '-q'],
                   cwd=root, check=True)
