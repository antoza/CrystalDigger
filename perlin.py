#!/usr/bin/env python3
import random

import numpy as np
import matplotlib.pyplot as plt
import random


# class UnitVect:
#
#     def __init__(self, dim=1):
#         self.vect = vect = [random.random() for _ in range(dim)]
#         self.normalize()
#
#     def normalize(self):
#         normal = sum(self.vect)
#         for elt in self.vect:
#             elt /= normal
#
#     def unit_vect(self):
#         return self.vect


def unit_vect(dim):
    vect = [random.random() for _ in range(dim)]
    normal = sum(vect)
    for elt in vect:
        elt /= normal
    return vect


def interpolate(x, y, c):
    return c * x + (1 - c) * y


class Perlin1d:

    def __init__(self, octaves=4, n=16, seed=0):
        # Initialize the random array with unit vectors
        self.size = n
        random.seed(seed)
        self.grad = np.array([unit_vect(1) for _ in range(n)])
        self.values = np.zeros(n)

        for o in range(min(octaves, int(np.log2(n)))):
            i_min = 0
            i_max = int(n / (2 ** o))
            step = i_max
            # Generate the whole octave
            while i_max <= n:
                for i in range(i_min, i_max):
                    interpolation_coeff = (i - i_min) / (i_max - i_min)
                    amp_factor = step/n
                    self.values[i] += amp_factor * interpolate(self.grad[i_min][0],
                                                               self.grad[i_max % n][0],
                                                               interpolation_coeff)
                i_min += step
                i_max += step

    def noise(self, x):
        # For each octave, add the corresponding value to the noise vector
        index = int(int(x * self.size) % self.size)
        c = x * self.size - int(x * self.size)
        return interpolate(self.values[index], self.values[int((index + 1) % self.size)], c)


def main():
    perlin = Perlin1d(octaves=2, n=2048)
    result = []
    image = []
    for t in np.arange(0, 1.01, .01):
        result.append(perlin.noise(t))
    for t in np.arange(0, 1.01, .01):
        image.append(result)
    #plt.plot(np.array(image))
    plt.imshow(np.array(image))
    plt.show()


if __name__ == "__main__":
    main()
