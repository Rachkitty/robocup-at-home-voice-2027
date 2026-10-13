# Third-party notices

- **Alpha Cephei Vosk API**: dependency `vosk==0.3.45`, Apache-2.0.
- **Alpha Cephei Vosk English model**: `vosk-model-small-en-us-0.15`, Copyright
  2020 Alpha Cephei Inc., Apache-2.0 per the official model list. Original bytes
  verified; LICENSE and NOTICE added and installed beside the assets.
- **Open Source Robotics Foundation templates**: original test source in
  `reference/snapshot/`, including Copyright 2015/2017 OSRF and Apache-2.0 headers.
- **Piper runtime**: dependency `piper-tts==1.4.2`, GPL-3.0-or-later. Runtime wheels
  are installed externally and are not bundled in the source deliverable. Review
  their native components and corresponding-source obligations before distribution.
- **Lessac/Blizzard voice**: ONNX and JSON omitted; model card retained only as
  provenance evidence. No redistribution permission is asserted.
- **Other dependencies**: see `docs/dependency-inventory.json` for installed
  versions and declared metadata. Dependency metadata is not a legal clearance.

Apache and GPL texts are in `LICENSES/`. The root `LICENSE` applies MIT to Hiram
Rafael Pérez Ibarra's project-owned code only. The `robocup_asr` package also
contains separately licensed Apache-2.0 Vosk model assets; its original
`LICENSE`/`NOTICE` remain installed with those assets. OSRF source retains its
own Apache-2.0 notices. No third-party work is relicensed under MIT.
