#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from math import sin

from perlin import Perlin2d


def main(seed=0):
    # Image of lines
    n = 8
    perlin = Perlin2d(n=n, seed=seed)

    n_max = 200
    noise = [[0 for _ in range(n_max)] for _ in range(n_max)]
    image = [[0 for _ in range(n_max)] for _ in range(n_max)]
    f_sin = 8
    f_noise = .5
    step = n / (n_max - 1)

    for p in range(5):
        amp_factor = 1 / (2 ** p)
        freq_factor = 2 ** p
        for i in range(n_max):
            for j in range(n_max):
                x = freq_factor * f_noise * step * i
                y = freq_factor * f_noise * step * j
                noise[i][j] += amp_factor * perlin.noise(x, y)

    for i in range(n_max):
        for j in range(n_max):
            y = f_sin * step * j
            image[i][j] += sin(y + 8 * noise[i][j])

    plt.imshow(np.array(image), cmap='gray')
    plt.show()


if __name__ == "__main__":
    main()