# Attribution and licensing status

The supplied paper is *Highly Fault-Tolerant Discrete Lattice Information Coding Method for Screen-Shooting Scenarios*, by Daidou Guo, Ching-Chun Chang, Cheng SenMao, and Chuan Qin, in the Proceedings of the 6th ACM International Conference on Multimedia in Asia, 2024, pp. 1–5. [DOI](https://doi.org/10.1145/3696409.3700285).

This is a laboratory-maintained inherited workspace, not a verified official code distribution. The provided directory did not contain a project-wide LICENSE. No MIT, Apache, or other project-wide permission has been assigned by this preparation; confirm rights with the laboratory before a public release. Existing source comments and attribution URLs are retained.

The new `codec.py` and protocol tests are release-support additions. They import the unchanged network definitions and external dependencies rather than copying another project's trained model implementation.

PyTorch, NumPy, Pillow, OpenCV, Matplotlib, tensorboardX, protobuf, and bchlib remain external packages. bchlib's package metadata identifies the python-bchlib project and GPLv2. Their installed files and licenses are not represented as a new license for this entire repository.

The Vue source declares Vue, Vue Router, Element UI, Axios, core-js, and Vue CLI/Sass tooling. The lockfile is retained for dependency identity, but their `node_modules` implementations were not bundled. The small static code image/logo/favicon referenced by the inherited UI are retained for source completeness, not described as newly validated results.

Original model weights, datasets, logs, output image collections, dependency installations, and the full paper PDF are not redistributed in the release. The paper-title image is a crop of the supplied paper's actual first-page title/author block.
