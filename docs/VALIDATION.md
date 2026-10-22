# Validation record

Validation date: **2026-10-22**. All 15 inherited Python files were preserved. The new `codec.py` is a compatibility interface, not a replacement neural network. The original external project and existing base environment were not modified.

## Environment

- Windows, Python 3.8.18, CPU only; two PyTorch compute threads.
- PyTorch 1.11.0+cu113, NumPy 1.24.3, Pillow 10.2.0.
- New private dependency overlay: bchlib 2.1.3 and tensorboardX 2.6.
- The supplied encoder and decoder weights loaded with `strict=True`.

## Checked results

| Check | Result |
| --- | --- |
| Inherited Python syntax | All 15 files compiled without executing them. |
| Main network/module loading | Passed using the unchanged `model.py` and local weights. |
| PNG encode/reload/decode | Passed for four messages, shown below. |
| Public round-trip CLI | Exit code 0; `cv` was recovered with one BCH-corrected error. |
| Separate public decode CLI | Exit code 0; recovered `cv` from the generated PNG. |
| Public encode-only CLI | Exit code 0; saved a 400 × 400 code image for `ab`. |
| Protocol unit tests | Four passed: shape/round trip, 1–3 bit correction, ASCII limits, invalid predictions. |
| Isolated BCE/Adam update | Finite loss and nonzero decoder parameter update; no encoder gradients. |
| Original 14,000-step training entry | Not run. |
| Real screen-camera capture / robustness benchmark | Not run. |
| Flask/Vue integration, frontend build, and server deployment | Not tested. |

## Four digital round trips

Each message was packed with the existing 32-bit protocol, passed through the supplied encoder, saved as an actual 400 × 400 PNG, reopened, decoded, and BCH-corrected. All generated pixels were 0 or 255.

| Input | Raw bit errors | BCH-corrected errors | Recovered text |
| --- | --- | --- | --- |
| `cv` | 1 | 1 | `cv` |
| `ab` | 0 | 0 | `ab` |
| `hi` | 1 | 1 | `hi` |
| `A` | 0 | 0 | `A` |

This tiny unmodified-image check does **not** establish a general accuracy rate, robustness, visual sparsity, camera tolerance, or the paper's reported results. The test messages are legitimate inputs to this message-to-code model; no cover-image dataset is required by that path.

## Optimizer diagnostic

A separate one-batch check used the unchanged model classes, a valid `cv` packet, BCE loss, and Adam with learning rate 0.001, matching the original training choices. The loss was finite (approximately 0.054888). Eighteen decoder parameter tensors had gradients, and a tracked decoder tensor changed by approximately 0.00100005.

**Zero encoder parameter tensors had gradients.** The hard threshold in the inherited encoder disconnects that gradient path. This was recorded rather than silently replaced with a surrogate/straight-through estimator. This check is not a claim that the original long training entry ran or that both networks learned.

## External resources used

The weights remain outside the public release:

| File | Bytes | SHA256 |
| --- | --- | --- |
| `encoder1.pth` | 87,386,294 | `d66b97e6c361939154d0f5cc98af1773a14fb6c6c467094e415f3f9b72b66fbc` |
| `decoder1.pth` | 45,669,536 | `759cef55c437df07e44d656ed8716a1f2c87c4e13cc51b7b60d306487195b71a` |

The state dictionaries had 32 and 18 entries, respectively. They were read from the original local resource directory, not copied into Git, downloaded, or overwritten. No official/pretrained-public provenance is inferred solely from their filenames.

Generated images, reports, the private virtual environment, and installation wheels live under gitignored `.local/`. Source-preservation checksums are listed in [inherited_source_sha256.txt](inherited_source_sha256.txt); current release Python checksums are in [source_sha256.txt](source_sha256.txt).

## Release-package checks

- All 34 selected inherited source/config/UI files matched their original SHA256 values. Both external weight checksums also remained unchanged.
- All 17 release Python files (15 inherited files plus the new wrapper and test file) passed syntax compilation without execution.
- Local Markdown file/image links resolved; a basic common-token/private-key pattern scan found no matches. This is not an exhaustive security audit.
- A disposable copy was staged in a separate temporary Git repository. All 47 public files were included, including the small Vue assets and network source.
- Ten dummy private/runtime paths were tested against the ignore rules, including checkpoints, datasets, environment files, node_modules, and experiment images. None entered the staged file list.
- The skill's file/index audit returned exit code 0 and no review candidates. The real D-drive release was not initialized, committed, or pushed.
- The public file set is approximately 0.6 MB; private `.local/` assets are not part of that figure.
