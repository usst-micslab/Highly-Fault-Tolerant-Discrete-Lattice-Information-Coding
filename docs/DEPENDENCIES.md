# Dependency notes

The main codec was tested using Python 3.8.18 on Windows with CPU inference. The existing PyTorch build was 1.11.0+cu113; CUDA was not used. A fresh CPU-only wheel or another PyTorch version needs its own check.

| Package | Observed version |
| --- | --- |
| PyTorch | 1.11.0+cu113 |
| NumPy | 1.24.3 |
| Pillow | 10.2.0 |
| OpenCV | 4.9.0.80 |
| Matplotlib | 3.7.5 |
| tensorboardX | 2.6 |
| protobuf | 3.20.3 |
| bchlib | 2.1.3 |

The [root requirements](../requirements.txt) cover the main-path packages except PyTorch. `tensorboardX` is needed because the inherited `model.py` imports it even during inference. `utils.py` also imports Matplotlib/OpenCV. `bchlib` 2.x is used by the new wrapper; it does not make the original helper calls compatible automatically.

The private validation environment uses `--system-site-packages` to read the existing framework installation. Only bchlib/tensorboardX were installed into its own virtual-environment directory, without modifying the base environment. It therefore depends on that original framework remaining available; it is not an independent copy of PyTorch. Machine-specific interpreter/resource paths are documented only under gitignored `.local/`.

Optional inherited paths need other packages: torchvision for the old inference helpers, Flask/Flask-CORS/requests for the old server, and torchgeometry/kornia for `model1.py`. Their complete compatibility and workflows were not validated and are not implied by the main requirements file.

The Vue source has its own `package.json` and `package-lock.json`. `node_modules` was deliberately not copied. A frontend build or `npm ci` was not performed; no npm packages were installed globally or into the original project. Treat `npm ci` and `npm run build` as an optional separate restoration task, not a tested part of this release.
