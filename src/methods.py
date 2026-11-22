"""NumPy-only truncated SVD using the Iteration 2 Gram-matrix derivation."""
import numpy as np


# G = A.T @ A
def my_gram(A):
    return A.T @ A


# v_next = G_i @ v / ||G_i @ v||_2, projected off the prior eigenvectors.
def my_power_iteration(G, basis, rng, tol, max_iter):
    v = rng.standard_normal(G.shape[0])
    v -= basis @ (basis.T @ v)
    v /= np.sqrt(v @ v)
    for steps in range(1, max_iter + 1):
        w = G @ v
        w -= basis @ (basis.T @ w)
        length = np.sqrt(w @ w)
        if length == 0:
            return v, steps, True
        w /= length
        if np.max(np.abs(w - v)) <= tol:
            return w, steps, True
        v = w
    return v, max_iter, False


# G_(i+1) = G_i - lambda_i * v_i @ v_i.T
def my_deflate(G, eigenvalue, v):
    return G - eigenvalue * np.outer(v, v)


# sigma_i = sqrt(lambda_i) for lambda_i > eps * max(m, n) * lambda_1
def my_select_components(A, eigenvalues):
    threshold = np.finfo(float).eps * max(A.shape) * eigenvalues[0]
    return np.sqrt(eigenvalues[eigenvalues > threshold])


# U_k = (A @ V_k) / sigma, dividing columnwise.
def my_encode(A, V, sigma):
    return (A @ V) / sigma


# A_k = U_k @ diag(sigma) @ V_k.T
def my_reconstruct(U, sigma, V):
    return (U * sigma) @ V.T


def my_svd_power(A, k, *, seed=0, tol=2e-14, max_iter=20000, diagnostics=None):
    """Return up to k positive singular triplets, with vectors in columns."""
    A = np.asarray(A, dtype=float)
    if A.ndim != 2 or not np.isfinite(A).all():
        raise ValueError("Expected a finite two-dimensional matrix.")
    if not 0 <= k <= min(A.shape) or tol <= 0 or max_iter < 1:
        raise ValueError("Invalid rank, tolerance, or iteration limit.")
    G = my_gram(A)
    rng = np.random.default_rng(seed)
    V = np.empty((A.shape[1], k))
    eigenvalues = np.empty(k)
    count = 0
    for i in range(k):
        v, steps, converged = my_power_iteration(G, V[:, :i], rng, tol, max_iter)
        # lambda_i = ||A @ v_i||_2^2, the Rayleigh quotient of A.T @ A.
        Av = A @ v
        eigenvalue = Av @ Av
        eigenvalues[i] = eigenvalue
        if my_select_components(A, eigenvalues[:i + 1]).size <= i:
            break
        V[:, i] = v
        count += 1
        if diagnostics is not None:
            diagnostics.append((steps, converged))
        if not converged and diagnostics is None:
            raise RuntimeError(f"Power iteration hit its limit at component {i + 1}.")
        G = my_deflate(G, eigenvalue, v)
    order = np.argsort(eigenvalues[:count])[::-1]
    V = V[:, order]
    sigma = my_select_components(A, eigenvalues[order]) if count else np.empty(0)
    return sigma, my_encode(A, V, sigma), V
