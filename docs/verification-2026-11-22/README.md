# Independent verification, 22 November 2026

These logs are fresh executions of the unchanged implementation at repository
commit `3a7dc93aecb41656a4ed86f93029cdb301a18199`. The original evidence
in `outputs/` is preserved. Differences in the final floating-point digits and
compressed NPZ sizes reflect the numerical/serialization environment; they do
not change the stated pass criteria or selected image rank.

## Environment and execution

- Python 3.12.14, macOS 26.2, ARM64.
- NumPy 2.5.5, Matplotlib 3.11.2, Pillow 13.0.0.
- `OPENBLAS_NUM_THREADS=1`, `VECLIB_MAXIMUM_THREADS=1`, `MPLBACKEND=Agg`.
- The three scripts ran in a separate working directory against the repository
  source and the original `data/camera.png`, so teammate source and saved output
  files were not overwritten.

Equivalent commands from the repository root:

```sh
python src/small_example.py
python src/check_simulation.py
python src/run_real.py
python -m unittest discover -s tests -v
```

All four commands exited successfully. All seven existing regression tests
passed, including rejection of incorrect singular values, nonorthogonal vectors,
inconsistent left/right rotations, and injected comparison failures. The logs
retain harmless font-cache warnings from the plotting environment. No timings
are used as performance evidence.

## Findings

The exact fractional small-example squared error is 5. In the fresh baseline
simulation, top-five singular values differ from the direct NumPy SVD by at most
`4.263e-14`; the clean-truth maximum difference is `1.862e-02`, below the
script's first-order `0.03` threshold. The three RMS relative errors and all
eight stress-test iteration counts reproduce the original saved results to
their printed precision. The image again first reaches 95% energy at rank 3.
Every numerical assertion in all three scripts passed.

This is an AI-assisted mathematical, numerical and documentation review. It
does not certify either student's personal contribution, substitute for the
assignment's second-member review, resolve the leader-rotation rule, publish an
Overleaf project, or submit anything to Canvas. Those facts are tracked in
`../iteration-3-status.md`.
