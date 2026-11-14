"""Load and describe the grayscale PNG for Iteration 2."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def main():
    # imread scales 8-bit PNG samples to [0, 1].
    image = plt.imread("data/camera.png")
    if image.ndim != 2:
        raise ValueError("Save an 8-bit grayscale PNG at data/camera.png.")

    pixels = np.rint(image * 255).astype(np.uint8)
    rows, columns = pixels.shape
    print(f"Rows (vertical pixel positions): {rows}")
    print(f"Columns (horizontal pixel positions): {columns}")
    print(f"Variable: pixel brightness from 0 to 255 ({pixels.dtype})")
    print(f"Missing values: {np.count_nonzero(~np.isfinite(image))}")
    print(f"Minimum: {pixels.min()}, maximum: {pixels.max()}, mean: {pixels.mean():.2f}")

    fig, ax = plt.subplots()
    ax.imshow(pixels, cmap="gray", vmin=0, vmax=255)
    ax.set(title="Grayscale photograph", xlabel="Pixel column", ylabel="Pixel row")
    fig.savefig("figures/grayscale_image.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots()
    ax.hist(pixels.ravel(), bins=np.arange(257) - 0.5, color="0.35")
    ax.set(xlim=(-0.5, 255.5), xlabel="Pixel brightness", ylabel="Pixel count")
    fig.savefig("figures/brightness_histogram.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
