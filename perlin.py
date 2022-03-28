#!/usr/bin/env python3
import random
from math import sqrt

import numpy as np
import matplotlib.pyplot as plt
import random


def unit_vect(dim):
    vect = []
    normal = 0
    for _ in range(dim):
        value = 2 * random.random() - 1
        vect.append(value)
        normal += value**2
    for i in range(dim):
        vect[i] /= sqrt(normal)
    return vect


def interpolate(x, y, c):
    return c * x + (1 - c) * y


def dot_prod(vect1, vect2):
    prod = 0
    for i in range(len(vect1)):
        prod += vect1[i] * vect2[i]
    return prod


class Perlin1d:

    def __init__(self, n=16, seed=0):
        # Initialize the random array with unit vectors
        self.size = n
        random.seed(seed)
        self.grad = np.array([unit_vect(1) for _ in range(n)])
        print(self.grad)

        # for o in range(min(octaves, int(np.log2(n)))):
        #     print("Octave : ", o+1)
        #     i_min = 0
        #     i_max = int(n / (2 ** o))
        #     step = i_max
        #     # Generate the whole octave
        #     while i_max <= n:
        #         print(i_min, " ", i_max)
        #         for i in range(i_min, i_max):
        #             interpolation_coeff = (i - i_min) / (i_max - i_min)
        #             amp_factor = step/n
        #             self.values[i] += amp_factor * interpolate(self.grad[i_min][0],
        #                                                        self.grad[i_max % n][0],
        #                                                        interpolation_coeff)
        #         i_min += step
        #         i_max += step

    def noise(self, x):
        # x has to be in [0, 1[
        bounded_x = x - int(x)

        # Calcul de l'indice du noeud inférieur
        index = int(bounded_x * (self.size - 1))

        # Calcul de la distance entre le point et les noeuds voisins
        previous_value = index / (self.size - 1)
        next_value = (index + 1) / (self.size - 1)
        dist_node1 = bounded_x - previous_value
        dist_node2 = next_value - bounded_x

        # Coefficient d'interpolation
        c = dist_node2 / (next_value - previous_value)

        return interpolate(self.grad[index] * dist_node1, self.grad[index + 1] * dist_node2, c)


def main():
    perlin = Perlin1d(n=4)

    n_max = 2000
    result = [0 for _ in range(n_max)]
    f = 1
    step = 1/n_max

    for p in range(4):
        freq_factor = 2**p
        amp_factor = 1 / (2**p)
        for i in range(n_max):
            result[i] += amp_factor * perlin.noise(freq_factor * f * step * i)

    for i in range(n_max):
        result[i] += 1

    plt.plot(result)
    plt.show()


if __name__ == "__main__":
    main()
