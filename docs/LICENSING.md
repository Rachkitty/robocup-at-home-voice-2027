# License adoption and scope

## Adoption

On 2026-10-12, Hiram Rafael Pérez Ibarra authorized MIT for his project-owned
code in all five ROS 2 voice packages. The root [`LICENSE`](../LICENSE) contains
the canonical MIT text and `Copyright (c) 2026 Hiram Rafael Pérez Ibarra`.
`package.xml` and `setup.py` now declare `MIT` for those package implementations.
The ASR package also declares `Apache-2.0` because its installable data includes
the separately licensed Vosk model.

Galu Robotics remains portfolio branding; no company copyright assignment or
ownership of third-party material is asserted.

## Material outside the MIT grant

| Material | License and handling |
| --- | --- |
| Hiram's original code in the five packages | MIT; see root `LICENSE` |
| Bundled Vosk English model | Apache-2.0; preserve the model's `LICENSE` and `NOTICE` |
| Vosk API dependency | Apache-2.0; installed externally, not copied here |
| OSRF test templates | Apache-2.0; original notices retained in immutable `reference/snapshot/` |
| Piper 1.4.2 runtime/native components | GPL-3.0-or-later and component terms; external dependency, not copied into the source tree |
| Lessac ONNX/JSON voice | Omitted because redistribution permission is not established |
| Other Python/ROS dependencies | External; their upstream terms apply; see requirements and dependency inventory |

Do not describe every file or a combined runtime as MIT-only. MIT is GPL-compatible
as a license for original modules, but distributing a program combined with a GPL
library can require the combined work to be conveyed under GPL-compatible terms
and to meet GPL obligations. The public distribution form (source-only listing,
installable package, or container) still needs an explicit compliance review for
Piper and its native components. That is a publication blocker for a combined
runtime/container claim, not a reason to remove the MIT grant from Hiram's code.

No voice weights with unresolved redistribution rights are included. A voice
supplied privately for local testing must remain outside this repository unless
its rights holder separately authorizes distribution.

## Sources

- [OSI MIT license text](https://opensource.org/license/mit)
- [Piper 1.4.2 package metadata](https://pypi.org/project/piper-tts/1.4.2/)
- [GNU guidance on GPL libraries](https://www.gnu.org/licenses/gpl-faq.en.html#IfLibraryIsGPL)
- [Vosk model license list](https://alphacephei.com/vosk/models)
- `LICENSES/Apache-2.0.txt` and `LICENSES/GPL-3.0.txt`
