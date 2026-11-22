"""Run the truth sweep, library verification and near-tied noise stress test."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from methods import my_gram, my_reconstruct, my_svd_power
from simulate import simulate_low_rank


def report(name, mine, ref, *, atol=1e-8, rtol=0.0):
    """Print a verification result and stop the script on failure."""
    mine, ref = np.asarray(mine, float), np.asarray(ref, float)
    diff = mine - ref
    abs_err = np.max(np.abs(diff))
    reference_norm = np.sqrt(np.sum(ref**2))
    diff_norm = np.sqrt(np.sum(diff**2))
    rel_err = diff_norm / reference_norm if reference_norm else (0.0 if diff_norm == 0 else np.inf)
    passed = abs_err <= atol + rtol * np.max(np.abs(ref))
    print(f"{name:32s} max|diff| = {abs_err:.3e}   rel = {rel_err:.3e}   {'PASS' if passed else 'FAIL'}")
    if not passed:
        raise SystemExit(f"Verification failed: {name}")
    return passed


def compare_svd(sigma, U, V, U_ref, s_ref, Vt_ref):
    k = len(sigma)
    report("Singular values", sigma, s_ref[:k])
    report("SVD U orthogonality", U.T @ U, np.eye(k))
    report("SVD V orthogonality", V.T @ V, np.eye(k))
    # A tied singular space may have any orthonormal basis, including when k
    # cuts through that space. Use the full reference block and the SAME
    # coefficients for U and V to verify the pairing of the singular vectors.
    tie_tol = 64 * np.finfo(float).eps * max(U_ref.shape[0], Vt_ref.shape[1])
    tie_tol *= s_ref[0] if len(s_ref) else 0
    start = 0
    while start < k:
        end = start + 1
        while end < len(s_ref) and abs(s_ref[end] - s_ref[start]) <= tie_tol:
            end += 1
        retained_end = min(end, k)
        reference_V = Vt_ref[start:end].T
        coefficients = reference_V.T @ V[:, start:retained_end]
        report(f"V subspace {start + 1}:{retained_end}",
               V[:, start:retained_end], reference_V @ coefficients)
        report(f"U paired subspace {start + 1}:{retained_end}",
               U[:, start:retained_end], U_ref[:, start:end] @ coefficients)
        start = end
    return True


def check_assumptions(A, sigma, U, V, s_ref, *, original_dtype=None):
    k = len(sigma)
    m, n = A.shape
    G = my_gram(A)
    print(f"Shape={A.shape}, ndim={A.ndim}, finite={np.isfinite(A).sum()}/{A.size}, "
          f"dtype={A.dtype}, range=[{A.min():.6g}, {A.max():.6g}]")
    report("Gram symmetry", G, G.T)
    report("U.T @ U", U.T @ U, np.eye(k))
    report("V.T @ V", V.T @ V, np.eye(k))
    eigenvalue_cutoff = np.finfo(float).eps * max(A.shape) * sigma[0]**2
    eigenvalues = np.linalg.eigvalsh(G)  # PSD verification only
    print(f"Min Gram eigenvalue={eigenvalues[0]:.8g}, PSD={eigenvalues[0] >= -eigenvalue_cutoff}, "
          f"cutoff={eigenvalue_cutoff:.8g}, min retained eigenvalue={sigma[-1]**2:.8g}, "
          f"positive above cutoff={bool(np.all(sigma**2 > eigenvalue_cutoff))}, "
          f"descending={bool(np.all(np.diff(sigma) <= 0))}")
    report("Gram positive semidefinite", eigenvalues[0] >= -eigenvalue_cutoff, True, atol=0)
    report("Retained values above cutoff", np.all(sigma**2 > eigenvalue_cutoff), True, atol=0)
    report("Descending singular values", np.all(np.diff(sigma) <= 0), True, atol=0)
    residual = np.sum((A - my_reconstruct(U, sigma, V))**2)
    tail = np.sum(s_ref[k:]**2)
    print(f"Measured squared residual={residual:.12g}, library tail={tail:.12g}")
    report("Squared residual vs tail", residual, tail, rtol=1e-12)
    count = k * (m + n + 1)
    original_dtype = A.dtype if original_dtype is None else np.dtype(original_dtype)
    print(f"Storage: {count}/{m*n} scalars, factors={sigma.dtype}, pixels={original_dtype}, "
          f"{U.nbytes + sigma.nbytes + V.nbytes}/{m*n*original_dtype.itemsize} raw bytes")


def main():
    output = Path("outputs")
    output.mkdir(exist_ok=True)
    A, B = simulate_low_rank()
    sigma, U, V = my_svd_power(A, 5)
    U_ref, s_ref, Vt_ref = np.linalg.svd(A, full_matrices=False)
    print("BASELINE: 120 x 80, seed 0, rank 5, noise 0.01")
    clean_values = np.linalg.svd(B, compute_uv=False)[:5]
    print("Clean singular values:", clean_values)
    report("Spectrum vs clean truth", sigma, clean_values,
           atol=3 * 0.01, rtol=0)  # First-order singular-value noise SD is 0.01.
    print("Observed estimate:", sigma)
    compare_svd(sigma, U, V, U_ref, s_ref, Vt_ref)
    check_assumptions(A, sigma, U, V, s_ref)

    # Fixed aspect ratio and rank. RMS aggregates relative errors over independent draws.
    sizes = [(30, 20), (120, 80), (480, 320)]
    rms_errors = []
    print("\nTRUTH SWEEP: relative singular-value error, RMS over seeds 0–9")
    for m, n in sizes:
        squared_errors = []
        for seed in range(10):
            observed, clean = simulate_low_rank(m=m, n=n, seed=seed)
            estimate, _, _ = my_svd_power(observed, 5)
            truth = np.linalg.svd(clean, compute_uv=False)[:5]
            relative = np.sqrt(np.sum((estimate - truth)**2) / np.sum(truth**2))
            squared_errors.append(relative**2)
        rms_errors.append(np.sqrt(np.mean(squared_errors)))
        print(f"{m} x {n}: n={n}, RMS relative error={rms_errors[-1]:.8g}")

    fig, ax = plt.subplots()
    ax.loglog([n for _, n in sizes], rms_errors, "o-")
    ax.set(xlabel="Matrix width n (height = 1.5n)", ylabel="RMS relative error vs clean spectrum")
    ax.grid(True, which="both", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output / "simulation_error.png", dpi=180)
    plt.close(fig)

    print("\nSTRESS TEST: k=8")
    diagnostics = []
    my_svd_power(A, 8, diagnostics=diagnostics)
    for i, (steps, converged) in enumerate(diagnostics):
        ratio = s_ref[i + 1] / s_ref[i]
        print(f"i={i + 1}: sigma_next/sigma={ratio:.6f}, "
              f"Gram power rate={ratio**2:.6f}, steps={steps}, converged={converged}")


if __name__ == "__main__":
    main()
