# Known issues in inherited entries

The original 15 Python files were not rewritten. These observations explain why the new `codec.py` is the checked entry point.

1. **Unbounded startup behavior.** `black_white/train.py` constructs CUDA models and calls `train(14000)` at module scope. Importing it or attempting `--help` can start training. Do not use it for a quick dependency check.
2. **Hard threshold blocks encoder learning.** `Encoder.forward` returns constant zero/one branches using `torch.where`. The diagnostic found no encoder gradients. The active training function also comments out its `transform_net` call, so the paper's joint-noise-training behavior is not established by this script.
3. **Fixed GPU/batch assumptions.** The original training path calls `.cuda()` directly, uses a global batch size of 4, and constructs a white reference image with a hard-coded batch of 4. CPU compatibility and safe step limits are not built into that entry.
4. **Legacy text API.** Original inference helpers use the old bchlib constructor order and `decode_inplace`. Their `--cuda` uses `type=bool`, so a string `False` does not reliably disable it. Some help text mentions 56 bits/100 bits even though the active networks use 32-bit packets.
5. **Encoder is not a usable standalone CLI.** `encoded(secret)` parses process arguments internally, its direct-entry call is commented out, its final output ignores `--save_dir`, writes to `D:/html/vue02/src/assets`, and returns the placeholder string `abc`.
6. **Decoder direct entry is incomplete.** `decoded(url)` requires an argument, but the file's main block calls it without one. Input images are not explicitly converted to grayscale there. The new codec does both path/device handling and grayscale conversion.
7. **Training/inference filenames differ.** Training saves `encoder.pth` and `decoder.pth`, whereas the supplied demo loads `encoder1.pth` and `decoder1.pth`. They should not be confused or overwritten automatically.
8. **Web interface is development source.** The Vue encoder view displays a statically imported image rather than the new response image. Flask has fixed upload/output paths, unrestricted development CORS, a debug server on all interfaces, and a placeholder encoder return. It was not started or exposed during this task.
9. **Fixed helper inputs and GUI calls.** Geometry/noise scripts reference specific image filenames and some call `imshow`, `waitKey`, or `plt.show` at module scope. They are not safe general-purpose CLI tools or an integrated camera-rectification pipeline.
10. **Separate alternative network.** `model1.py` imports optional torchgeometry/kornia and defines a different StegaStamp-style experiment. It is not the architecture used by the supplied `encoder1.pth` and `decoder1.pth` codec.

The new wrapper uses the exact inherited network definitions, supports explicit paths and CPU inference, validates the two-byte text protocol, adapts BCH 2.x APIs, and saves results only to its requested output directory. It does not claim to repair the old web application, noise training, or physical capture alignment.
