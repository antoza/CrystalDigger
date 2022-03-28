#!/usr/bin/env python3
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
        normal += value ** 2
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


class Perlin2d:

    def __init__(self, n=16, seed=0):
        # Initialize the random array with unit vectors
        self.size = n
        random.seed(seed)
        self.grad = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                self.grad[i][j] = unit_vect(2)

    def noise(self, x, y):
        bounded_x = x - int(x)
        bounded_y = y - int(y)
        i_max = self.size - 1

        index = [int(bounded_x * i_max), int(bounded_y * i_max)]

        # Computes the values on the 4 neighbor nodes of the given point
        nodes = [[index[0] / i_max, index[1] / i_max],
                 [index[0] / i_max, (index[1] + 1) / i_max],
                 [(index[0] + 1) / i_max, index[1] / i_max],
                 [(index[0] + 1) / i_max, (index[1] + 1) / i_max]]

        dist_nodes = [[bounded_x - nodes[0][0], bounded_y - nodes[0][1]],
                      [bounded_x - nodes[1][0], nodes[1][1] - bounded_y],
                      [nodes[2][0] - bounded_x, bounded_y - nodes[2][1]],
                      [nodes[3][0] - bounded_x, nodes[3][1] - bounded_y]]

        dot_prods = [dot_prod(dist_nodes[0], self.grad[index[0]][index[1]]),
                     dot_prod(dist_nodes[1], self.grad[index[0]][index[1] + 1]),
                     dot_prod(dist_nodes[2], self.grad[index[0] + 1][index[1]]),
                     dot_prod(dist_nodes[3], self.grad[index[0] + 1][index[1] + 1])]

        c1 = dist_nodes[2][0] / (nodes[2][0] - nodes[0][0])
        interpolated_dot_prod = [interpolate(dot_prods[0], dot_prods[2], c1),
                                 interpolate(dot_prods[1], dot_prods[3], c1)]

        c2 = dist_nodes[1][1] / (nodes[1][1] - nodes[0][1])

        return interpolate(interpolated_dot_prod[0], interpolated_dot_prod[1], c2)


class Perlin1d:

    def __init__(self, n=16, seed=0):
        # Initialize the random array with unit vectors
        self.size = n
        random.seed(seed)
        self.grad = np.array([unit_vect(1) for _ in range(n)])

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


def main(dim=2):

    if dim == 1:
        perlin = Perlin1d(n=4)

        n_max = 100
        result = [0 for _ in range(n_max)]
        f = 1
        step = 1 / (n_max - 1)

        for p in range(4):
            freq_factor = 2 ** p
            amp_factor = 1 / (2 ** p)
            for i in range(n_max):
                result[i] += amp_factor * perlin.noise(freq_factor * f * step * i)

        for i in range(n_max):
            result[i] += 1

        plt.plot(result)
        plt.show()

    else:
        perlin = Perlin2d(n=16)

        n_max = 200
        image = [[0 for _ in range(n_max)] for _ in range(n_max)]
        f = 1
        step = 1 / (n_max - 1)

        for p in range(4):
            freq_factor = 2 ** p
            amp_factor = 1 / (2 ** p)
            for i in range(n_max):
                for j in range(n_max):
                    x = freq_factor * f * step * i
                    y = freq_factor * f * step * j
                    image[i][j] += amp_factor * perlin.noise(x, y)

        for i in range(n_max):
            for j in range(n_max):
                image[i][j] += 1

        plt.imshow(np.array(image))
        plt.show()


if __name__ == "__main__":
    main()
