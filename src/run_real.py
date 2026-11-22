"""Compress the Iteration 2 camera image and verify with direct NumPy SVD."""
import argparse
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from check_simulation import check_assumptions, compare_svd, report
from methods import my_reconstruct, my_svd_power


# A_ij = brightness_ij / 255 for the original 8-bit grayscale PNG.
def my_load_image(path):
    with Image.open(path) as image:
        pixels = np.array(image)
        if image.mode != "L" or pixels.ndim != 2 or pixels.dtype != np.uint8:
            raise ValueError("Expected an 8-bit grayscale image.")
    print(f"Input: {path.name}, shape={pixels.shape}, channels=1, dtype={pixels.dtype}, "
          f"missing={pixels.size - np.isfinite(pixels).sum()}, range=[{pixels.min()}, {pixels.max()}], "
          f"mean={pixels.mean():.4f}, PNG size={path.stat().st_size} bytes")
    return pixels / 255.0, pixels.dtype


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", nargs="?", type=Path, default=Path("data/camera.png"))
    args = parser.parse_args()
    output = Path("outputs")
    output.mkdir(exist_ok=True)
    A, original_dtype = my_load_image(args.image)
    m, n = A.shape
    k = min(50, m, n)
    total_energy = np.sum(A**2)
    if total_energy == 0:
        raise ValueError("Energy fractions require a nonzero image.")
    while True:
        sigma, U, V = my_svd_power(A, k)
        energy = np.cumsum(sigma**2) / total_energy
        if len(energy) and energy[-1] >= 0.95:
            break
        if len(sigma) < k or k == min(m, n):
            raise RuntimeError("The retained components did not reach 95% energy.")
        k = min(2 * k, m, n)
    k95 = int(np.searchsorted(energy, 0.95)) + 1
    ranks = [min(rank, len(sigma)) for rank in (5, 20, 50)] + [k95]
    print(f"First rank retaining 95%: {k95}; energy={energy[k95 - 1]:.8%}; "
          f"prior rank energy={energy[k95 - 2] if k95 > 1 else 0:.8%}")
    U_ref, s_ref, Vt_ref = np.linalg.svd(A, full_matrices=False)
    ref_energy = np.cumsum(s_ref**2) / total_energy
    k95_ref = int(np.searchsorted(ref_energy, 0.95)) + 1
    report("95% rank vs NumPy", k95, k95_ref, atol=0)
    compare_svd(sigma, U, V, U_ref, s_ref, Vt_ref)
    check_assumptions(A, sigma, U, V, s_ref, original_dtype=original_dtype)

    fig, ax = plt.subplots()
    ax.plot(np.arange(1, len(s_ref) + 1), ref_energy, "--", label="NumPy reference")
    ax.plot(np.arange(1, len(sigma) + 1), energy, label="Power iteration")
    ax.axhline(0.95, color="gray", linestyle=":")
    ax.scatter(k95, energy[k95 - 1], zorder=3, label=f"First rank at 95%: {k95}")
    ax.set(xlabel="Components retained (k)", ylabel="Cumulative fraction of energy",
           xscale="log", ylim=(0, 1.02))
    ax.legend()
    fig.tight_layout()
    fig.savefig(output / "image_energy.png", dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(1, 5, figsize=(15, 3.3), layout="constrained")
    axes[0].imshow(A, cmap="gray", vmin=0, vmax=1)
    axes[0].set_title("Original")
    axes[0].axis("off")
    for ax, rank in zip(axes[1:], ranks):
        Uk, sk, Vk = U[:, :rank], sigma[:rank], V[:, :rank]
        reconstructed = my_reconstruct(Uk, sk, Vk)
        print(f"Rank {rank}: energy={energy[rank - 1]:.8%}; "
              f"storage={rank * (m + n + 1)}/{m*n} scalars")
        factors = BytesIO()
        np.savez_compressed(factors, U=Uk, sigma=sk, V=Vk)
        print(f"  Raw factor bytes={Uk.nbytes + sk.nbytes + Vk.nbytes}; "
              f"compressed NPZ bytes={factors.tell()}")
        residual = np.sum((A - reconstructed)**2)
        tail = np.sum(s_ref[rank:]**2)
        print(f"  Squared residual={residual:.12g}, library tail={tail:.12g}")
        report(f"Rank {rank} squared error vs tail", residual, tail)
        compare_svd(sk, Uk, Vk, U_ref, s_ref, Vt_ref)
        ax.imshow(reconstructed, cmap="gray", vmin=0, vmax=1)
        ax.set_title(f"k = {rank} ({energy[rank - 1]:.1%})")
        ax.axis("off")
    fig.savefig(output / "image_reconstructions.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
