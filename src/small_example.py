"""Exact 2 x 2 worked example plus a check of the shared numerical solver."""
from fractions import Fraction
from math import isqrt

import numpy as np

from check_simulation import report
from methods import my_encode, my_gram, my_reconstruct, my_svd_power


def main():
    A = np.array([[3, 0], [4, 5]])
    G = my_gram(A)
    trace = int(G[0, 0] + G[1, 1])
    det = int(G[0, 0] * G[1, 1] - G[0, 1] * G[1, 0])
    gap = isqrt(trace**2 - 4 * det)
    eigenvalues = [Fraction(trace + gap, 2), Fraction(trace - gap, 2)]
    directions = np.array([[1, 1], [1, -1]])
    V = directions / np.sqrt(np.sum(directions**2, axis=0))
    sigma = np.sqrt(np.array(eigenvalues, dtype=float))
    U = my_encode(A, V, sigma)
    A1 = my_reconstruct(U[:, :1], sigma[:1], V[:, :1])
    full = my_reconstruct(U, sigma, V)
    # A1 = A v1 v1.T; each entry of the exact projector v1 v1.T is 1/2.
    exact_A1 = [[Fraction(int(sum(row)), 2)] * 2 for row in A]
    exact_residual = [[int(A[i, j]) - exact_A1[i][j] for j in range(2)] for i in range(2)]
    print(f"A =\n{A}\nG = A.T @ A =\n{G}")
    print(f"det(lambda I - G) = lambda^2 - {trace} lambda + {det}")
    print("Eigenvalues:", *eigenvalues)
    print(f"Unnormalized eigenvectors (columns):\n{directions}\nV =\n{V}")
    print("Singular values: 3 sqrt(5), sqrt(5)", sigma)
    print(f"A @ V =\n{A @ V}\nU =\n{U}\nSigma =\n{np.diag(sigma)}")
    print(f"A1 =\n{A1}\nExact A1 entries: {[[str(x) for x in row] for row in exact_A1]}")
    print("Exact residual entries:", [[str(x) for x in row] for row in exact_residual])
    print("Exact squared residual:", sum(x**2 for row in exact_residual for x in row))
    report("Rank-one approximation", A1, exact_A1)
    report("Squared rank-one error", np.sum((A - A1)**2), eigenvalues[-1])
    report("Eigenpair substitution", G @ V, V * sigma**2)
    report("Full reconstruction", full, A)
    estimate, U_est, V_est = my_svd_power(A, 2)
    report("Power SVD vs exact spectrum", estimate, sigma)
    report("Power SVD reconstruction", my_reconstruct(U_est, estimate, V_est), A)


if __name__ == "__main__":
    main()
