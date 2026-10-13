# Physical validation — pending

None of these checks was performed during extraction. Record hardware, OS, ROS,
dependency versions, authorized model provenance and audio-device configuration.

1. Verify an authorized Piper ONNX/JSON pair and its expected output rate.
2. Confirm actual microphone capture and actual audible Piper playback, separately.
3. Speak `ava`, then `milk bed`, then `confirm`; observe the two bridge topics.
4. Reject with `no`; give another configured command without a wake word.
5. Measure silent timeout behavior: historical auto-publication after more than
   15 seconds is retained and must not be mistaken for explicit consent.
6. Measure TTS-to-ASR echo, false wake words, background speakers, noise, distance,
   startup calibration and successive utterances using the robot's actual devices.
7. Verify how the real navigation consumer maps `bed/table/shelf/counter` and
   receives `/nav_location`; verify acknowledgement/completion externally.
8. Keep hardware stop/supervision procedures outside this voice module.

Text doubles, model loading and device enumeration do not satisfy these checks.
