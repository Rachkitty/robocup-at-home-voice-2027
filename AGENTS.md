# Project instructions

This is an independent reconstruction from commit
9952f30a2775cede3d69c0dc34962ff609addead, not the 2027 HRI workspace.
Read README.md, docs/CHANGES.md, docs/PROVENANCE.md and docs/VALIDATION.md.
Never edit the source workspace as part of this project. Do not commit, push,
publish, add remotes or choose a project license without explicit authorization.

Keep reference/snapshot text immutable; verify it against extraction-manifest.json.
Keep exactly five packages under src/. Do not import the later robocup_hri package.
Do not bundle unauthorized voices. Private ONNX/JSON pairs stay outside this tree.
Separate portability changes from functional corrections and document the latter.
Preserve historical parser/topic/timeout contracts unless explicitly changed.

MIT is adopted only for Hiram Rafael Pérez Ibarra's original code in the five
packages. Preserve Vosk/OSRF notices and each external dependency/model license;
do not describe a combined Piper runtime as MIT-only or distribute it before its
GPL obligations have been reviewed.

Use Python 3.12 / Ubuntu 24.04 / ROS 2 Jazzy as the reconstruction target.
Run scripts/verify.sh in ROS; when ROS/audio are unavailable, report each blocked
check separately from simulated tests and real Vosk synthetic-PCM smoke tests.
Avoid privileged containers and host permission changes. Keep build/install/log,
virtual environments and private models outside version control and source bundles.
