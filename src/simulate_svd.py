"""Numerically check the five Project 3 SVD results."""

import numpy as np


def main():
    rng = np.random.default_rng(0)
    m, n, rank = 120, 80, 5
    noise_sd = 0.01
    clean = rng.normal(size=(m, rank)) @ rng.normal(size=(rank, n))
    image = clean + noise_sd * rng.normal(size=(m, n))

    # Q1: diagonalize the Gram matrix and order the components by energy.
    gram = image.T @ image
    eigenvalues, v = np.linalg.eigh(gram)
    eigenvalues, v = eigenvalues[::-1], v[:, ::-1]
    tolerance = np.finfo(float).eps * max(m, n) * eigenvalues[0]
    np.testing.assert_allclose(gram, gram.T)
    assert eigenvalues[-1] >= -tolerance
    sigma = np.sqrt(np.clip(eigenvalues, 0, None))

    clean_eigenvalues = np.linalg.eigvalsh(clean.T @ clean)
    clean_rank = np.count_nonzero(clean_eigenvalues > tolerance)
    assert clean_rank == rank
    print(f"Seed 0, matrix {m} x {n}, clean rank {clean_rank}, noise SD {noise_sd}")
    print(f"Q1 minimum noisy Gram eigenvalue: {eigenvalues[-1]:.6g}")
    print(f"Singular values 1 through 10: {sigma[:10].round(6)}")
    print(f"Drop after component 5: {sigma[rank - 1] / sigma[rank]:.2f}x")
    assert sigma[rank - 1] / sigma[rank] > 10

    # Q2 and Q3: recover left singular vectors and sum the rank-one terms.
    positive = eigenvalues > tolerance
    v_positive = v[:, positive]
    u = (image @ v_positive) / sigma[positive]
    orthogonality_error = np.max(np.abs(u.T @ u - np.eye(u.shape[1])))
    reconstructed = (u * sigma[positive]) @ v_positive.T
    np.testing.assert_allclose(u.T @ u, np.eye(u.shape[1]), atol=1e-8)
    np.testing.assert_allclose(reconstructed, image, atol=1e-10)
    print(f"Q2 max orthogonality error: {orthogonality_error:.3e}")
    print(f"Q3 max reconstruction error: {np.max(np.abs(image - reconstructed)):.3e}")

    # Q4: compare all three expressions for squared Frobenius energy.
    energy = np.sum(image**2)
    np.testing.assert_allclose([np.trace(gram), np.sum(sigma**2)], energy, rtol=1e-12)
    print(f"Q4 squared Frobenius energy: {energy:.8f}")
    print(f"   trace: {np.trace(gram):.8f}, sum of squared singular values: {np.sum(sigma**2):.8f}")

    # Q5: truncate the rank-one sum and compare the measured error to the tail.
    print(f"\nQ5 original storage: {m * n} scalars")
    print(f"{'k':>3} {'Measured error squared':>24} {'Predicted tail sum':>20} {'Stored scalars':>16}")
    for k in (1, 3, 5, 10):
        approximation = (u[:, :k] * sigma[:k]) @ v[:, :k].T
        error = np.sum((image - approximation)**2)
        tail_sum = np.sum(sigma[k:]**2)
        np.testing.assert_allclose(error, tail_sum, rtol=1e-9)
        print(f"{k:3d} {error:24.8f} {tail_sum:20.8f} {k * (m + n + 1):16d}")

    reference = np.linalg.svd(image, compute_uv=False)
    np.testing.assert_allclose(sigma, reference, rtol=1e-8)
    print(f"\nMax singular-value difference vs NumPy SVD: {np.max(np.abs(sigma - reference)):.3e}")


if __name__ == "__main__":
    main()
