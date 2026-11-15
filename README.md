# DS5020 Image Compression with the SVD

## Iteration 2

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
