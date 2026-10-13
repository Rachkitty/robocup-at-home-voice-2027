# License scope and third-party terms

The MIT License in [`LICENSE`](LICENSE) applies to the project-owned code in the
five ROS 2 voice packages, authored by Hiram Rafael Pérez Ibarra. Copyright
notice: `Copyright (c) 2026 Hiram Rafael Pérez Ibarra`.

This MIT grant does not replace licenses on third-party material. In particular,
the bundled Vosk model is Apache-2.0 and retains its `LICENSE` and `NOTICE` files;
the OSRF test templates in `reference/snapshot/` retain their original Apache-2.0
notices. External runtime dependencies retain their own terms. See
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) and [`docs/PROVENANCE.md`](docs/PROVENANCE.md).

The Piper 1.4.2 runtime is GPL-3.0-or-later. It is installed as an external
dependency and is not copied into this source tree. Before distributing an
installed combined runtime or container, review and satisfy the applicable GPL
terms and provide the required notices/source. The Lessac ONNX/JSON voice files
remain omitted because redistribution permission has not been established.
