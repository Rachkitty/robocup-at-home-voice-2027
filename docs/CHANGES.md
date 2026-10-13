# Changes relative to the imported snapshot

Source: `9952f30a2775cede3d69c0dc34962ff609addead`.
Exact text source is retained under `reference/snapshot/`; the SHA-256 inventory
is `extraction-manifest.json`. Model assets are handled separately.

## Packaging and portability (no intended dialogue change)

- Complete runtime/package declarations, Python dependency pins, resource markers,
  model installation preserving the Vosk directory tree, and four-node launch.
- Package version 0.1.0 identifies the reconstruction, not a competition release.
- Use ament package-share lookup for Vosk; expose `model_path` on ASR and TTS.
- Omit Lessac ONNX and JSON, requiring a user-provided authorized Piper voice.
  Missing/incomplete models fail with actionable startup errors.
- Add optional `audio:=false` launch mode for text-only operation. The default
  still starts the historical four nodes, once a private TTS model is supplied.
- Supply isolated Docker/dependency setup; no host ROS/permission modifications.
- Replace generated linter templates in the active tree with behavioral tests,
  standalone flake8 checks, and a colcon wrapper. The original templates and
  OSRF Apache headers remain intact in the reference tree.
- Strip trailing whitespace; adjust blank lines, indentation, unnecessary f-string
  markers and unused packaging imports. No keyword/parser/grammar/topic changes.

## Functional corrections

### F01 — Reject nonstring bridge fields

Historical `speech_one.py` calls `.strip()` on both dictionary values; values
such as `None`, numbers, lists and dictionaries raise `AttributeError`.
The reconstruction rejects either nonstring value and publishes nothing.
Valid string inputs and the historical partial-field publishing behavior remain
unchanged. Differential tests prove valid/rejected-string parity and demonstrate
that the original crashes on the same nonstring fixtures.

### F02 — Honor the supplied voice sample rate

Historical TTS always opens a 22,050 Hz output stream. The reconstruction uses
`PiperVoice.config.sample_rate`, so an authorized replacement voice is not played
at the wrong rate. The original Lessac rate is 22,050 Hz; its nominal playback
rate remains unchanged. Tests cover 16,000, 22,050 and 24,000 Hz with fake voices.
Real synthesis/playback is pending because no authorized voice was supplied.

## Known historical behaviors intentionally retained

- Timeout greater than 15 seconds autoexecutes; silence is not explicit consent.
- Confirmation ASR transforms `confirm/correct/affirmative` into `yes`, but drops
  literal recognized `yes`, despite including it in its grammar.
- Voice accepts exact wake words; parser searches object/location keywords,
  without requiring a specific imperative verb.
- A rejection accepts a new command without repeating the wake word.
- `/command` is a Python-dictionary string, not JSON; bridge outputs are separate
  string topics with no task ID, navigation acknowledgement or atomic delivery.
- Fixed energy thresholds, noise calibration, queue handling, anti-echo delays
  and blocking dialogue/TTS callbacks remain. No AEC, barge-in or stop redesign.

## Portfolio preparation (documentation and demo only)

- README now presents Galu Robotics branding, a Mermaid architecture and the
  owner-reported national result, separated from source/deployment evidence.
- Added a simulated demonstration reusing the existing four-node fixture and its
  actual recorded topic trace. Added one CLI regression test. No active node,
  parser, dictionary, timeout, ROS schema or model changed.
- Expanded ignores for caches, private voice configuration, settings and recordings.
- Added draft GitHub metadata and a publication-readiness report; no remote actions.

- Verification now uses `colcon --base-paths src` so temporary local environments
  and validation tools are not mistaken for ROS packages. This is a discovery/
  tooling correction, with no change to node behavior; it was verified after an
  initial scan encountered NumPy example setup files in a temporary demo venv.
- The author confirmed authorship of all project-owned package code and authorized
  MIT on 2026-10-12. Added the canonical root license and updated all five ROS
  manifests and setuptools metadata; ASR declares Apache-2.0 additionally for its
  bundled Vosk model. Third-party notices and model licenses remain separate.
- `scripts/verify.sh` sources colcon's generated setup with `nounset` temporarily
  disabled, because ROS setup hooks reference optional unset environment variables.
  This repairs only verification-shell handling and changes no node behavior.
