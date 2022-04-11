#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from math import sin

from perlin import Perlin2d


def genere_ppm(file_name, points_array, size):
    """
    Generates a ppm image of size 'size * size' corresponding
    to the list of points 'points_array'.
    """

    file = open(file_name, 'wb+')

    # Header
    file.write(b"P6\n")
    file.write(f"{size} {size}\n".encode('UTF-8'))
    file.write(b"255\n")

    # Content
    for j in range(size):
        for i in range(size):
            current_color = bytearray(points_array[i][j])
            file.write(current_color)

    file.close()


def apply_noise(image, noise, size, step, f_sin=8):
    for i in range(size):
        x = f_sin * step * i
        for j in range(size):
            perturbation = sin(x + f_sin * noise[i][j]) / 3
            image[i][j][0] *= 1 + perturbation
            image[i][j][1] *= 1 + perturbation
            image[i][j][2] *= 1 + perturbation
            image[i][j][0] = int(image[i][j][0])
            image[i][j][1] = int(image[i][j][1])
            image[i][j][2] = int(image[i][j][2])


def main(seed=0):
    # Image of lines
    n = 8
    perlin = Perlin2d(n=n, seed=seed)

    n_max = 200
    noise = [[0 for _ in range(n_max)] for _ in range(n_max)]
    # Uniform image of brown
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

    dark_wood = [[[66, 40, 14] for _ in range(n_max)] for _ in range(n_max)]
    apply_noise(dark_wood, noise, n_max, step, f_sin=4)

    # defining planks image
    planks = [[[175, 128, 87] for _ in range(n_max)] for _ in range(n_max)]
    for i in range(n_max):
        for j in range(n_max):
            if j % (n_max // 10) in range(-2, 3):
                planks[j][i] = [66, 40, 14]

    # For the planks, we work on the noise a little more to apply an offset to distinguish the different planks
    for p in range(5):
        amp_factor = 1 / (2 ** p)
        freq_factor = 2 ** p
        for i in range(n_max):
            for j in range(n_max):
                x = freq_factor * f_noise * step * i
                y = freq_factor * f_noise * step * j
                offset = j % (n_max // 10)
                # don't override the separation of the planks
                if j % (n_max // 10) in range(-2, 3):
                    noise[j][i] = 0
                else:
                    noise[j][i] += amp_factor * perlin.noise(x, y + offset)

    apply_noise(planks, noise, n_max, step, f_sin=4)

    genere_ppm("dark_wood.ppm", dark_wood, n_max)
    genere_ppm("planks.ppm", planks, n_max)


if __name__ == "__main__":
    main()