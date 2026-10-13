# Provenance and authorship review

## Extraction

Source commit: `9952f30a2775cede3d69c0dc34962ff609addead` (2026-04-16).
The source is the Interaccion-Humano-Robot project. The national deployment
association remains a candidate attribution; no competition release tag or
runtime manifest establishes which checkout was deployed. The owner now reports
10 points + 1 extra for the national 2026 result; see COMPETITION_2026.md for the
evidence level and the distinction between a team score and this source snapshot.

Extraction used `git archive --format=tar <commit> --` with exactly these pathspecs:

```text
.gitignore
src/robocup_asr
src/robocup_tts
src/robocup_voice
src/robocup_bringup
src/robocup_speech_one
```

The stream was filtered before writing to omit the ONNX weights; its JSON
configuration was subsequently omitted too. `extraction-manifest.json` retains
source hashes, sizes, modes and the explicit omission status for both files.
Text source was also copied verbatim to the reference tree, including historical
absolute paths and template tests. It is intentionally excluded from colcon.

The destination was initialized with `git init -b main`. There are no commits,
no source object database, no remotes, and no publication. No source branch,
index, reference, tag, working-tree file or ignored build artifact was changed.
An independent preservation comparison records all original entries, including
`.git`, symlinks, regular-file hashes, modes and modification times.

## Authorship declaration and historical evidence

Hiram Rafael Pérez Ibarra explicitly declared authorship of all project-owned
code in the five voice packages on 2026-10-12. This owner declaration resolves
previous uncertainty about the authors of that code; see [AUTHORS.md](../AUTHORS.md).
The ten April commits record the Git author name Raphinha1. Historical metadata
names raffiki/gauseineri as maintainers; those records remain intact in the
reference snapshot and are not used to invent additional contributors.

On 2026-10-12 the author authorized MIT for his project-owned code in all five
packages. The root `LICENSE` contains that grant; the package manifests declare
MIT, and `robocup_asr` additionally declares Apache-2.0 for the bundled Vosk
model. See [license scope](../LICENSE.md) and
[adoption record](LICENSING.md). Third-party code and assets retain
their own notices and licenses. A real future maintainer contact
is still not supplied, so current contact metadata remains an explicit placeholder.

## Vosk

API dependency: `vosk==0.3.45`; upstream `alphacep/vosk-api`, Apache-2.0.
Bundled model: `vosk-model-small-en-us-0.15`, Copyright 2020 Alpha Cephei Inc.
The official model list declares Apache-2.0. All fourteen model files match the
freshly fetched official ZIP byte-for-byte. ZIP and per-file hashes are recorded
in `model-provenance.json`. No original model file was modified; LICENSE and
NOTICE were added for redistribution and are installed with the model.

Sources:
- https://alphacephei.com/vosk/models
- https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
- https://github.com/alphacep/vosk-api/blob/master/COPYING

## Piper runtime and Lessac voice

The reconstruction uses `piper-tts==1.4.2`, released April 2, 2026, declared
GPL-3.0-or-later by its PyPI metadata. This is a reconstruction choice; the
competition dependency version is unknown. The older `rhasspy/piper` MIT line
must not be used to infer the license of this package. Piper wheels include
native components such as eSpeak NG. The dependency is external and not bundled
in this tree; review component notices and applicable GPL obligations before
distributing an installed combined runtime or container.

Historical voice: `en_US-lessac-medium` (22,050 Hz). The upstream MODEL_CARD links
to the Lessac/Blizzard dataset research license. That license alone does not
establish this project's permission to redistribute the trained ONNX weights.
Both ONNX and JSON are therefore omitted; there is no automatic voice download,
no substitute voice, and no private voice copied into the new workspace.
A model card is retained as licensing evidence, not a grant of rights.

Sources:
- https://pypi.org/project/piper-tts/1.4.2/
- https://github.com/OHF-Voice/piper1-gpl/tree/v1.4.2
- https://github.com/rhasspy/piper/blob/master/LICENSE.md
- https://huggingface.co/rhasspy/piper-voices/raw/main/en/en_US/lessac/medium/MODEL_CARD
- https://www.cstr.ed.ac.uk/projects/blizzard/2013/lessac_blizzard2013/license.html

## Other third-party material

The immutable reference includes OSRF-generated Apache-2.0 test templates;
retain their copyright/license headers. Historical Git itself does not record a
complete provenance statement for the custom nodes; Hiram has since explicitly
confirmed that he authored all project-owned code in the five packages. Later
`.agents`/`.claude` tooling and HRI 2.0 contracts were not extracted. Installed
Python dependencies and their declared
licenses are inventoried separately in `dependency-inventory.json`. The observed
full environment freeze contains development tooling and is not a source bundle
or canonical runtime dependency list. Some package metadata fields are blank or
`UNKNOWN`; those packages are not copied into this repository. Verify the license
of any future dependency artifact before bundling it.
