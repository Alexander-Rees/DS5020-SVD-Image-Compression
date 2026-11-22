# DS5020 Image Compression with the SVD

## Iteration 3

Run from the repository root after installing `requirements.txt` in a virtual
environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The included `data/camera.png` is the project image.

```sh
export OPENBLAS_NUM_THREADS=1 MPLBACKEND=Agg
set -o pipefail
mkdir -p outputs
python src/small_example.py | tee outputs/small_example.txt
python src/check_simulation.py | tee outputs/simulation.txt
python src/run_real.py | tee outputs/real_image.txt
```

Each command prints results for the report's verification table and exits with an
error if a required check fails. `pipefail` preserves failures when piping to `tee`.
Tied singular values are checked using their paired singular subspaces, including
when a requested rank cuts through a tied block.
The PNGs in `outputs/` show simulation error against width, retained image energy,
and the original alongside the rank-5, 20, 50, and 95%-energy reconstructions.
An optional path argument to `run_real.py` selects a different 8-bit grayscale PNG.

- `src/methods.py` builds the Gram matrix, extracts eigenvectors with power
  iteration and deflation, then encodes and reconstructs the low-rank matrix.
  Projection off the prior eigenvectors limits accumulated roundoff. In the
  Gram power iteration, the convergence rate is governed by
  `lambda[i+1] / lambda[i] = (sigma[i+1] / sigma[i])**2`.
- `src/simulate.py` returns the noisy observation and its clean rank-5 truth.
  The baseline preserves the Iteration 2 generator's draw order, parameters,
  dimensions, and seed 0. The size sweep uses a fixed aspect ratio and the same
  noise and rank, with seeds 0–9 at each size to measure RMS relative spectral error.
  The baseline truth comparison uses three times the first-order noise
  standard deviation: for unit singular vectors, the perturbation
  `u.T @ (0.01 * Z) @ v` has standard deviation 0.01.
- The image script computes total energy directly as the sum of squared entries.
  Its power-iteration curve covers the computed ranks. Direct NumPy SVD
  supplies the full reference curve and tail sums. Raw byte counts use the
  original uint8 pixel dtype and the float64 factor dtype. Compressed NPZ sizes
  are measured by serializing the factors in memory.
- `data/camera.png` is the Iteration 2 grayscale camera image from
  scikit-image's sample data, credited to Lav Varshney (CC0) in the Iteration 2 report.

Run the verification regression checks with
`python -m unittest discover -s tests -v`.

### Results for the report

- [`outputs/small_example.txt`](outputs/small_example.txt): exact worked example
  and numerical checks.
- [`outputs/simulation.txt`](outputs/simulation.txt): clean-truth and library
  comparisons, sample-size sweep, assumption checks, and the k=8 stress test.
- [`outputs/real_image.txt`](outputs/real_image.txt): image checks, library
  comparisons, retained energy, reconstruction errors, and storage costs.
- [`outputs/simulation_error.png`](outputs/simulation_error.png): RMS relative
  spectral error against matrix width.
- [`outputs/image_energy.png`](outputs/image_energy.png): retained energy and
  the first rank reaching 95%.
- [`outputs/image_reconstructions.png`](outputs/image_reconstructions.png):
  original image and the requested reconstructions.

The simulation data is regenerated from the recorded parameters and seeds; no
separate simulated dataset is needed. The Iteration 3 report and updated project
plan are still to be completed. The files under `docs/` currently document
Iteration 2.

## Iteration 2

**Project lead:** Alexander Rees

**Team members:** Alexander Rees and Jiaxiao Chen

[Read the report](docs/iteration-2-report.pdf) · [Download the Excel project plan](docs/project-plan.xlsx) · [Edit the LaTeX source](docs/main.tex)

The report answers all five SVD questions and compares the measured residual against the discarded singular-value energy. In the seeded simulation, rank five stores 1,005 of 9,600 scalars and gives squared error 0.87302222. The factor count assumes equal scalar widths. The report also gives a byte comparison for the 8-bit photograph.

The LaTeX source uses the two generated PNGs in `figures/`. To reproduce the PDF locally, run `tectonic main.tex` from `docs/`. For Overleaf, upload `main.tex` at the project root and put both PNGs in a `figures/` folder. The review record on page 6 has space for both members' sign-offs. The clean singular values in the results table can be reproduced inside the simulation from `np.sqrt(clean_eigenvalues[-rank:][::-1])`; subsequent values are zero by construction.

Run these commands from the repository root.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/simulate_svd.py
```

The simulation uses seed 0, a 120 × 80 rank-5 signal and Gaussian noise with standard deviation 0.01.
It checks the Gram eigenvalues, left singular vector orthogonality, reconstruction, Frobenius energy,
and rank-`k` error for `k = 1, 3, 5, 10`. Its terminal table gives the measured squared errors,
predicted squared errors, and storage costs in scalars for the report.

For the real-data portion, download the 512 × 512 [Camera image](https://scikit-image.org/docs/0.25.x/api/skimage.data.html#skimage.data.camera) and run the loader.

```sh
curl -fL https://raw.githubusercontent.com/scikit-image/scikit-image/v0.25.2/skimage/data/camera.png -o data/camera.png
python src/load_image.py
```

The loader prints the dimensions, pixel type, intensity summary, and missing-value count. It saves
`figures/grayscale_image.png` and `figures/brightness_histogram.png`.
To use another photo, save it as an 8-bit grayscale PNG at `data/camera.png`.
