# Executed verification and limits

## Current portfolio preparation

The latest preparation passed **43 standalone tests** and one colcon wrapper
that invokes them. The README diagram parsed with Mermaid 12.1.0, and the
simulated demo was repeated in a fresh Python environment with only its three
direct demo requirements and their dependencies. No ROS/Vosk/Piper/sounddevice
engine was installed there. Active package code and model assets did not change.
Read [publication-validation.json](publication-validation.json) and
[PUBLICATION_READINESS.md](PUBLICATION_READINESS.md) for the current evidence.

Real ROS/DDS remains blocked, physical audio/navigation are unverified, and the
owner-reported score is separate from these checks. MIT applies to the author's
five package code; third-party licenses and combined-runtime obligations remain
separate.

## Original extraction verification (historical snapshot)

Date: 2026-10-12 (America/Monterrey). Python 3.12.14 in an isolated local virtual
environment. No ROS underlay is installed on the host; Docker socket permission
is denied. Ubuntu/Jazzy is the intended reconstruction target, not a runtime
validated in this session.

| Check | Result | Scope |
| --- | --- | --- |
| `colcon build --executor sequential` | 5 packages passed | Real ament_python build/install; no ROS runtime imports |
| `colcon test` / `test-result --verbose` | 1 wrapper passed; 0 errors/failures/skips | Wrapper invokes the 42-test hardware-free suite |
| Standalone pytest JUnit | 42 passed; 0 skipped | ROS, recognition and synthesis doubles; differential historical traces |
| flake8 | Passed | src/tests/scripts; max line length 160 and E303 exception documented in config |
| Python 3.12 syntax | 22 files passed | Active Python source, tests and verification tools |
| Shell / Compose configuration | Passed | verify.sh syntax; base and optional audio Compose parsing |
| `pip check` | Passed | Isolated dependency environment |
| Dependency keys | 30 declarations resolved statically | Official Jazzy/rosdep source membership; no Ubuntu rosdep installation |
| Installed assets | Passed | 5 ament markers, 4 executables, YAML, launch, 14 original model files, LICENSE/NOTICE |
| Real Vosk engine | Passed | Loads installed model and decodes one second of synthetic silence; not speech accuracy |
| Real Piper import/chunk API | Passed | 1.4.2 import and audio_int16_array contract; no model/synthesis/playback |
| Real ROS/DDS text flow | Blocked | verify_ros_flow.py reports missing rclpy; Docker inaccessible |
| Docker image build | Not executed | Socket denied; no host permissions modified |
| Physical audio / navigation | Not performed | No authorized TTS voice and no robot hardware validation |
| Source bundle relocation | 42 tests passed | Extracted into a separate work directory; no .git copied |
| Original preservation | Passed | All 1,653 file/directory/symlink entries including .git remained identical |

Logs and JUnit XML are under ignored validation/ in the working project. The
machine-readable summary is validation-results.json. Do not interpret simulated
flow, silence decoding, or model enumeration as physical voice or robot tests.
No claims are made about the actual national deployment, real spoken accuracy,
Piper synthesis, echo, ROS middleware transport or navigation completion.

The new Git repository has no copied history or remote. This validation record
predates adoption of MIT for the author's package code; third-party terms remain
separate. See PROVENANCE.md and PUBLICATION_READINESS.md for current status.
