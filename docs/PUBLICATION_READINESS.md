# Publication readiness — Galu Robotics voice portfolio

Date: 2026-10-12. Project: `robocup-at-home-voice-2026`.

**Decision: public release remains on hold pending Piper distribution review.**
No remote was created and no visibility changed.

## Author, result and scope

Hiram Rafael Pérez Ibarra explicitly confirmed authorship of all project-owned
code in the five ROS voice packages. AUTHORS.md records that statement; Galu
Robotics is portfolio branding, not an invented corporate copyright assignment.
At the author's instruction, MIT is now active for that own code. The canonical
text and 2026 copyright are in `LICENSE`; all five package manifests declare MIT,
and ASR additionally declares Apache-2.0 for its bundled Vosk model. Third-party
licenses remain separate. The previous own-code contributor uncertainty is
resolved by the author's declaration.

The README presents **10 points + 1 extra (11 total)** as an owner-reported
national 2026 result. No category, ranking, score-per-module, official score sheet
or deployment version was invented. The reported result and reconstructed source
commit are independent evidence; see COMPETITION_2026.md.

The source remains snapshot `9952f30a2775cede3d69c0dc34962ff609addead`. Exactly five
packages remain, with no 2027 HRI/LLM/Whisper functionality. Navigation integration
is publication of a location string to an external consumer, not a Nav2 controller
or navigation-completion result.

## Documentation changes

- Rewrote the English README around engineering scope, result evidence, Mermaid
  architecture, a hardware-free demo, historical/corrected behavior and actual checks.
- Separated longer native/Docker/audio instructions into SETUP.md.
- Added AUTHORS.md, the license-scope record, and qualified COMPETITION_2026.md.
- Adopted MIT for the author's original package code, updated all five `package.xml`
  and `setup.py` declarations, and retained the additional Apache-2.0 declaration
  and model notices for ASR's bundled Vosk data.
- Prepared github-metadata.json and GITHUB_PRESENTATION.md without applying them.
- Added a demo that reuses the existing four-node fixture and emits its recorded
  topic trace after its assertions pass; it does not fake a live-robot recording.
- Expanded ignores for caches, private voice configuration, settings and recordings.
- Scoped verification discovery to `src` to avoid scanning temporary Python
  environments as ROS packages. An initial validation scan encountered NumPy
  examples; the corrected scan/tests finished cleanly without adding Cython.
- Updated current validation evidence while retaining the extraction report's
  historical 42-test snapshot. The new CLI regression brings the suite to 43.
- Made `verify.sh` safe when sourcing colcon setup hooks with `nounset`; the
  current run then passed build, test, install, and Vosk checks before reporting
  the host's unavailable ROS runtime.

F01/F02 remain the only functional node corrections: bridge type validation and
Piper voice sample-rate handling. This licensing step changes the ten package
license declarations and adds license/attribution documentation; it does not
change node logic or model bytes. The immutable historical reference still
matches its extraction hashes.

## Demonstration and executed verification

`python scripts/demo_simulated.py` requires only requirements-demo.txt. Its inputs
are `ava`, `milk bed`, `confirm`; the recorded outputs include a command dictionary,
`/target_object=milk`, `/nav_location=bed`, ASR mute/resume events and an idle final
state. docs/demo-output.json contains the captured trace.

| Check | Current result and limits |
| --- | --- |
| Python/colcon build | Five packages built; no ROS underlay. Warnings only note deliberately disabled bytecode |
| Standalone pytest | 43 passed; 0 failed/errored/skipped |
| colcon test/result | One passed wrapper invokes all 43; corrected discovery is clean |
| Minimal demo environment | Passed; no ROS, Vosk, Piper or sounddevice engines installed; output equals captured trace |
| flake8 / Python syntax | Passed; 24 Python files parse on 3.12; existing style configuration disclosed |
| bash syntax / pip check | Passed |
| Compose base/audio configuration | Parses; Docker image/runtime cannot run due socket permissions |
| Installed assets | Five resource markers, four executables, YAML, launch, 14 original Vosk files and notices verified |
| Real Vosk | Installed model decodes synthetic silence; not real speech accuracy |
| Real Piper | Import/chunk API passes; no voice loading, synthesis or playback |
| ROS/DDS | Check attempted; blocked by missing rclpy/underlay and inaccessible Docker |
| Audio/robot/navigation | Not performed; requires authorized private voice and actual hardware/consumer |
| ROS dependency declarations | 30 current official source-key memberships pass; no Ubuntu rosdep installation |
| Mermaid | Parses with temporary Mermaid 12.1.0; GitHub rendering itself not executed |
| Ignore/metadata rules | 17 private/artifact paths excluded; 5 intended paths includable; topics/description valid |
| Original preservation | 1,653 entries match both extraction and preparation baselines, including .git/index/refs |

Local parser/demo tool environments were removed after testing and are not project
or runtime dependencies. Logs and JUnit remain in ignored validation/publication/.
Machine-readable results: publication-validation.json. No real TTS/audio or
navigation claim is inferred from the fixture, silence check or team score.

## Files, size and publication inventory

The candidate is approximately **67.96 MiB** of source and assets, dominated by
**70,909,410 bytes** of Vosk model files plus their notices.
The largest file is `graph/Gr.fst`: 24,013,795 bytes (**22.90 MiB**). No candidate
file exceeds 50 or 100 MiB. Final file count/bytes and per-file SHA-256 values are
recorded in FILE_MANIFEST.json and publication-inventory.json. These are candidate
file sizes, not a compressed future Git object-database estimate.

The local workspace also includes ignored build/install/validation artifacts.
They are not part of the publication candidate. The original source history was
not copied; the first local Git commit is a new snapshot of this candidate tree.

The pattern scan of the measured candidate found no credential-pattern matches;
132 text files were inspected initially. Large/binary assets were excluded, so
this is not a universal absence guarantee. Eight historical/environment path
locations were identified, mainly immutable reference/patch evidence; review them
for presentation/privacy before first publication without silently rewriting the
historical snapshot. Placeholder maintainer contact is not a real email address.

No ONNX/JSON private voice, recording, environment secret, build, installed copy,
virtual environment or temporary Node tool directory belongs in the candidate.
Vosk's original bytes are unchanged and the existing checksum tests verify them.

## Licensing and redistributable material

- Author-owned five-package code: MIT adopted with `Copyright (c) 2026 Hiram Rafael Pérez Ibarra`.
- Bundled Vosk model: Apache-2.0. All 14 model files remain included with
  `LICENSE`/`NOTICE` and checksum provenance. No uncertain model was added or
  silently substituted.
- OSRF template references: keep their Apache-2.0 headers.
- Direct external Python runtimes: NumPy (BSD-3-Clause), PyYAML (MIT),
  sounddevice (MIT), Vosk API (Apache-2.0), and Piper 1.4.2 (GPL-3.0-or-later).
  They are package requirements, not vendored libraries in the source tree.
- Piper/native components: retain each upstream term. Do not label a combined
  system MIT-only; review GPL-compatible distribution and source/notice duties
  before distributing an installed package or container.
- Lessac ONNX/JSON: omitted; an authorized private pair is needed for playback.

`requirements.lock.txt` is an observed full development-environment freeze, not
a list of vendored dependencies or a hash-verified supply-chain lock. Its
metadata inventory includes a few blank/`UNKNOWN` license fields; PyPI classifiers
identify `notify2` as BSD, and Docutils exposes BSD/GPL/public-domain choices. None
of those dependency files or packages is copied into this repository. Keep this
distinction visible and verify upstream terms before bundling any dependency.

MIT for own code does not authorize third-party weights or relicense Piper.
[OSI's MIT text](https://opensource.org/license/mit) is used for the author's
package code. [GNU's library guidance](https://www.gnu.org/licenses/gpl-faq.en.html#IfLibraryIsGPL)
explains that a program combined with a GPL library must meet GPL-compatible
licensing and distribution terms. The source tree contains no Piper wheel or
native binary, and the voice files remain omitted; the actual form of public
distribution still needs review before an installable package/container or
complete-runtime claim is published.

## Blocking items vs nonblocking improvements

| Item | Classification | Concrete next step |
| --- | --- | --- |
| Public distribution form with Piper | Blocks a public combined-runtime/package/container release until its GPL obligations are reviewed | Decide source-only listing vs installable/runtime artifacts; review Piper and native components, preserve terms and satisfy applicable source/notice requirements |
| Missing authorized TTS voice | Blocks full-voice verification, not a source portfolio with omitted weights | Supply a private authorized ONNX/JSON pair; keep uncertain weights excluded |
| ROS/DDS and robot tests | Blocks fully-tested/runtime/navigation claims | Execute verification under Jazzy, then physical checklist; retain scoped evidence labels meanwhile |
| Official score/deployment evidence | Blocks independently verified score/commit claims | Add reviewed score sheet/video and deployment record; owner-reported wording can remain |
| Maintainer contact and verified Galu homepage | Nonblocking portfolio improvement | Supply a preferred public contact/link; avoid invented URLs/private addresses |
| Docker digest and transitive dependency hashes | Nonblocking reproducibility improvement | Pin image/lock artifacts in a separately reviewed update |
| Future CI and demonstration media | Nonblocking presentation improvement | Add CI only after remote approval; use genuine permitted recordings and actual badges |
| Later model distribution strategy | Nonblocking storage improvement | Consider verified pinned downloads before adding model revisions; current files need no LFS migration |

The author's explicit statement resolves own-package authorship. Local Git history
does not itself publish the contents to a third party. Do not treat a local commit
as clearance for a public release of a combined runtime.

## Draft GitHub metadata and recommendations

Description:
> ROS 2 voice subsystem for RoboCup @Home: offline Vosk ASR, Piper TTS, historical dialogue, and navigation/object topic integration.

Topics: `ros2`, `robotics`, `robocup`, `robocup-at-home`, `human-robot-interaction`,
`speech-recognition`, `text-to-speech`, `vosk`, `piper-tts`, `python`, `offline`,
`service-robot`, `galu-robotics`.

Keep README/evidence at the landing page, author attribution visible and the score
qualified. Do not add Nav2/autonomous-navigation/2027 topics, unverified badges,
rankings or fake robot media. Use owner-approved visual assets for social preview.
Keep Wiki/Pages off initially; use versioned docs. Enable Issues after publication
approval for reproducibility discussions. Future releases should state source SHA,
F01/F02, verification scope and excluded assets.

GitHub's [topic rules](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics)
allow up to 20 short lowercase/hyphenated topics; this draft fits. Its
[large-file guidance](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)
warns above 50 MiB and blocks above 100 MiB; the present files are below both.
Git/CLI is recommended for a reviewed complete tree/file modes, not because the
current largest file violates the 25 MiB browser limit.

No remote operation is part of this preparation. License adoption does not
authorize creating a remote, publishing, pushing or modifying visibility.
