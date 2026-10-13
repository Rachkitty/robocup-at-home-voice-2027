# ROS 2 setup and hardware verification

Reconstruction target: Ubuntu 24.04 / Python 3.12 / ROS 2 Jazzy. The April
competition distro/dependency versions remain unknown. Current local Python
builds do not establish ROS runtime compatibility. See VALIDATION.md.

For the hardware-free portfolio demo, follow the README instead; it needs only
requirements-demo.txt and does not start ROS or speech engines.

## Native ROS installation and build

From an existing ROS 2 Jazzy installation:

```bash
source /opt/ros/jazzy/setup.bash
sudo apt update
sudo apt install python3-venv python3-pip python3-colcon-common-extensions \
  python3-rosdep portaudio19-dev libasound2-plugins
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
# Run sudo rosdep init only if rosdep has not already been initialized.
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro jazzy -r -y
colcon build --base-paths src --executor sequential
source install/setup.bash
```

ROS dependencies are declared in `package.xml`; pip-only speech dependencies
are pinned in requirements and package installation metadata. Build from the
workspace root, never from `src/`.

## Docker on a Linux host

```bash
export HOST_UID="$(id -u)"
export HOST_GID="$(id -g)"
docker compose build
docker compose run --rm ros
```

Inside the container:

```bash
source /opt/ros/jazzy/setup.bash
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro jazzy -r -y
colcon build --base-paths src --executor sequential
source install/setup.bash
bash scripts/verify.sh
```

Compose does not mount the original repository and does not use privileged mode.
The default service exposes no microphone, speaker, or private voice model.
The Docker image and real ROS/DDS flow were not validated in the extraction
session: Docker socket access was denied and no host ROS underlay was installed.

## Text-only operation

```bash
source /opt/ros/jazzy/setup.bash
source .venv/bin/activate  # Native installation only
source install/setup.bash
export ROS_DOMAIN_ID=86
export ROS_LOCALHOST_ONLY=1
ros2 launch robocup_bringup robot_launch.py audio:=false
```

From another terminal with the same environment, publish `ava`, then `milk bed`,
then `yes` to `/speech_text` using `std_msgs/msg/String`. Observe `/command`,
`/nav_location` and `/target_object`. This tests text transport, not recognition.
Alternatively, `python3 scripts/verify_ros_flow.py` starts its own real Voice and
SpeechOne nodes and verifies the text flow; **do not run the launch concurrently**.

## Full voice operation with an authorized private model

Supply an ONNX voice and its neighboring `voice.onnx.json` configuration from a
source whose use you are authorized to exercise. Do not add these files to Git.
The original Lessac weights were omitted and are not downloaded automatically.

```bash
source /opt/ros/jazzy/setup.bash
source .venv/bin/activate
source install/setup.bash
ros2 launch robocup_bringup robot_launch.py \
  tts_model_path:=/absolute/path/to/authorized/voice.onnx
```

The Vosk default path resolves from the installed package share directory. An
alternative can be provided with:

```bash
ros2 run robocup_asr vosk_asr_node --ros-args -p model_path:=/absolute/path/to/vosk-model
```

For Docker physical audio, export `VOICE_MODEL_DIR` to a private directory and
check `test -S "$XDG_RUNTIME_DIR/pulse/native"`. Start:

```bash
docker compose -f compose.yaml -f compose.audio.yaml run --rm ros
# Inside: source ROS/overlay, then use tts_model_path:=/models/private/voice.onnx.
```

The optional override mounts that private directory read-only and forwards only
the PulseAudio/PipeWire socket. Device enumeration alone is not a physical test.


## Full verification in a ROS environment

With Jazzy and the dependency environment sourced, run `bash scripts/verify.sh`.
It rebuilds, sources the overlay, invokes colcon/pytest/lint/install/Vosk checks
and finally the real ROS/DDS text-flow check. A missing underlay is an explicit
failure rather than a simulated success. See PHYSICAL_CHECKLIST.md for checks
requiring an authorized voice, microphone/speaker and actual robot consumers.
