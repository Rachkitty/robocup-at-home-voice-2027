# Future GitHub presentation — draft only

No GitHub repository is created or modified by this preparation.

## About panel

Name: `robocup-at-home-voice-2026`.

Description:
> ROS 2 voice subsystem for RoboCup @Home: offline Vosk ASR, Piper TTS, historical dialogue, and navigation/object topic integration.

Topics are specified in [github-metadata.json](github-metadata.json). They are
lowercase/hyphenated, below 50 characters each, and fewer than 20, following
[GitHub's topic guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics).
Do not add `nav2`, `autonomous-navigation`, `whisper`, `llm` or a 2027 topic:
those implementations/capabilities are not present in this repository.
No organization URL/homepage is invented; the owner can supply a verified link.

## Repository page

1. Keep the README as the primary landing page: project value, qualified score,
   Mermaid architecture, one-command simulated demo, evidence table and limitations.
2. Keep license/provenance status visible. MIT is now active for the author's
   package code. Before publishing an installable combined runtime/container,
   resolve Piper/native-component GPL compliance and document the distribution form.
3. Present it as Galu Robotics portfolio engineering with historical provenance;
   credit Hiram Rafael Pérez Ibarra for the own package code and preserve third-party
   notices. Do not replace personal attribution with a new company copyright assertion.
4. Use the JSON demo trace as immediate reviewable evidence. Add a short recording
   later only if it is a genuine capture and all imagery/audio are publishable.
5. Use an owner-approved social preview image showing architecture/project name;
   no stock robot, result podium, organizer logo or invented hardware depiction.
6. Enable Issues for reproducibility questions after publication; keep Wiki and
   Pages off initially because source-controlled documentation is sufficient.
7. Add CI/status badges only after those checks actually run in the future remote.
   Current local checks are snapshots, not a continuously passing GitHub CI badge.
8. First future release notes should list reconstruction SHA, F01/F02, omitted
   Lessac assets, dependency pins and exact executed vs pending verification.

## Storage recommendation

Retain the currently verified Apache-2.0 Vosk model for the first reproducible
source snapshot; no model was moved/deleted or added during this task. The largest
individual model file is below GitHub's ordinary-file limit. No LFS migration is
required for the present inventory. Before later model upgrades, prefer a pinned,
checksum-verified external download with explicit licensing over repeatedly
committing large binary revisions; implement that only as a separate reviewed change.

GitHub warns above 50 MiB and blocks ordinary files above 100 MiB; browser uploads
are limited to 25 MiB. No current file exceeds even the browser cap. Prefer Git/CLI for the complete
directory tree and file modes once publication is authorized. See
[GitHub large-file guidance](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).
The local workspace includes build/install artifacts that are excluded from the
candidate publication; use the measured inventory in PUBLICATION_READINESS.md.

## Go/no-go

Do not publish yet: the distribution form and Piper/combined-runtime GPL
obligations need review before a public release. Authorship and the own-code MIT
grant are now author-confirmed. Missing ROS/DDS, physical audio or official score
proof block stronger claims, but need not block an honestly scoped historical
portfolio once rights are resolved. Follow the report rather than implying that
simulation establishes robot hardware or competition performance.
