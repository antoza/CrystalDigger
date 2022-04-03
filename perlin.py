#!/usr/bin/env python3
from math import sqrt

import numpy as np
import matplotlib.pyplot as plt
import random
from math import sin

from transform import vec


def unit_vect(dim):
    vect = []
    normal = 0
    for _ in range(dim):
        value = 2 * random.random() - 1
        vect.append(value)
        normal += value ** 2
    for i in range(dim):
        vect[i] /= sqrt(normal)
    return vec(vect)


def interpolate(x, y, c):
    return (1-c) * x + c * y


def interpolate_smooth(a, b, x):
    value = a + smooth_step(x) * (b - a)
    return value


def smooth_step(x):
    return (3 - 2 * x) * (x**2)
    # return 6 * (x**5) - 15 * (x**4) + 10 * (x**3)


class Perlin2d:

    def __init__(self, n=16, seed=0):
        # Initialize the random array with unit vectors
        self.size = n
        random.seed(seed)

        self.grad = [[[] for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                self.grad[i][j] = unit_vect(2)

    def noise(self, x, y):
        i_max = self.size

        # indexes necessary to the evaluation of the gradient
        i = int(x) % i_max
        j = int(y) % i_max
        i_sup = (i+1) % i_max
        j_sup = (j+1) % i_max

        # Computes the distance to the upper left node
        u = x - int(x)
        v = y - int(y)

        # Compute the scalar products for each node
        dot_prods = [np.dot(self.grad[i][j], np.array([u, v])),
                     np.dot(self.grad[i_sup][j], np.array([u-1, v])),
                     np.dot(self.grad[i][j_sup], np.array([u, v-1])),
                     np.dot(self.grad[i_sup][j_sup], np.array([u-1, v-1]))]

        # Compute the two interpolations for axis x
        interpolated_dot_prod = [interpolate_smooth(dot_prods[0], dot_prods[1], u),
                                 interpolate_smooth(dot_prods[2], dot_prods[3], u)]

        # Compute the interpolation for axis y and return the result
        return interpolate_smooth(interpolated_dot_prod[0], interpolated_dot_prod[1], v)


class Perlin1d:

    def __init__(self, n=16, seed=0):
        # Initialize the random array with unit vectors
        self.size = n
        random.seed(seed)
        grad = [unit_vect(1) for _ in range(n)]
        self.grad = np.array(grad)

    def noise(self, x):
        # Compute the indexes of the framing nodes
        i_max = self.size
        index = int(x) % i_max
        index_sup = (index + 1) % i_max

        # Compute the distance to the lower node
        u = x - int(x)

        prods = np.array([self.grad[index] * u, self.grad[index_sup] * (u-1)])

        return interpolate_smooth(prods[0], prods[1], u)


def main(dim=2, seed=0):

    if dim == 1:
        n = 4
        perlin = Perlin1d(n=n, seed=seed)

        n_max = 200
        result = [0 for _ in range(n_max)]
        f = 1
        step = n / (n_max - 1)

        for p in range(5):
            freq_factor = 2 ** p
            amp_factor = 1 / (2 ** p)
            for i in range(n_max):
                result[i] += amp_factor * perlin.noise(freq_factor * f * step * i)

        plt.plot(result)
        plt.show()

    else:
        n = 8
        perlin = Perlin2d(n=n, seed=seed)

        n_max = 200
        noise = [[0 for _ in range(n_max)] for _ in range(n_max)]
        image = [[0 for _ in range(n_max)] for _ in range(n_max)]
        f = 1
        step = n / (n_max - 1)

        for p in range(5):
            amp_factor = 1 / (2 ** p)
            freq_factor = 2 ** p
            for i in range(n_max):
                for j in range(n_max):
                    x = freq_factor * f * step * i
                    y = freq_factor * f * step * j
                    noise[i][j] += amp_factor * perlin.noise(x, y)

        for i in range(n_max):
            for j in range(n_max):
                x = f * step * i
                y = f * step * j
                image[i][j] += sin(x + y + 8 * noise[i][j])

        plt.imshow(np.array(image), cmap='gray')
        plt.show()


if __name__ == "__main__":
    main(dim=2)
