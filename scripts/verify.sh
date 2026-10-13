#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p validation
colcon build --base-paths src --executor sequential
# ROS/colcon setup hooks reference optional environment variables; source them
# without nounset, then restore the verification script's strict mode.
set +u
source install/setup.bash
set -u
colcon test --base-paths src --executor sequential
colcon test-result --verbose
python3 -m pytest tests -q --junitxml=validation/simulated-tests.xml
python3 -m flake8 src tests scripts
python3 scripts/verify_install.py
python3 scripts/verify_vosk.py
# A real ROS underlay is required here. Failure is not hidden as a skip.
python3 scripts/verify_ros_flow.py
