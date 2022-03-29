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
    return (1-c) * x + c * y


def interpolate_smooth(a, b, x):
    value = a + smooth_step(x) * (b - a)
    return value


def smooth_step(x):
    # return (3 - 2 * x) * (x**2)
    return 6 * (x**5) - 15 * (x**4) + 10 * (x**3)


def dot_prod(vect1, vect2):
    prod = 0
    for i in range(len(vect1)):
        prod += vect1[i] * vect2[i]
    return prod


class Perlin2d:

    def __init__(self, n=256, seed=0):
        # Initialize the random array with unit vectors
        self.size = n
        random.seed(seed)

        self.grad = [[[] for _ in range(n+1)] for _ in range(n+1)]
        for i in range(n):
            for j in range(n):
                self.grad[i][j] = unit_vect(2)

        for i in range(n):
            self.grad[i][n] = self.grad[i][0]
        for j in range(n):
            self.grad[n][j] = self.grad[0][j]
        self.grad[n][n] = self.grad[0][0]

    def noise(self, x, y):
        bounded_x = x - int(x)
        bounded_y = y - int(y)
        i_max = self.size

        # index of the upper left node close to the point
        index = [int(bounded_x * i_max),        # x
                 int(bounded_y * i_max),        # y
                 int(bounded_x * i_max) + 1,    # x+1
                 int(bounded_y * i_max) + 1]    # y+1

        # Computes the values on the 4 neighbor nodes of the given point
        nodes = [[index[0] / i_max, index[1] / i_max],
                 [index[0] / i_max, index[3] / i_max],
                 [index[2] / i_max, index[1] / i_max],
                 [index[2] / i_max, index[3] / i_max]]

        # Compute the distance vector for each node
        dist_nodes = [[bounded_x - nodes[0][0], bounded_y - nodes[0][1]],
                      [bounded_x - nodes[1][0], nodes[1][1] - bounded_y],
                      [nodes[2][0] - bounded_x, bounded_y - nodes[2][1]],
                      [nodes[3][0] - bounded_x, nodes[3][1] - bounded_y]]

        # Compute the scalar products for each node
        dot_prods = [dot_prod(dist_nodes[0], self.grad[index[0]][index[1]]),
                     dot_prod(dist_nodes[1], self.grad[index[0]][index[3]]),
                     dot_prod(dist_nodes[2], self.grad[index[2]][index[1]]),
                     dot_prod(dist_nodes[3], self.grad[index[2]][index[3]])]

        # Compute the two interpolations for axis x
        c1 = dist_nodes[0][0] / (nodes[2][0] - nodes[0][0])
        interpolated_dot_prod = [interpolate_smooth(dot_prods[0], dot_prods[2], c1),
                                 interpolate_smooth(dot_prods[1], dot_prods[3], c1)]

        # Compute the interpolation for axis y and return the result
        c2 = dist_nodes[0][1] / (nodes[1][1] - nodes[0][1])
        return interpolate_smooth(interpolated_dot_prod[0], interpolated_dot_prod[1], c2)


class Perlin1d:

    def __init__(self, n=16, seed=0):
        # Initialize the random array with unit vectors
        self.size = n
        random.seed(seed)
        grad = [unit_vect(1) for _ in range(n)]
        grad.append(grad[0])
        self.grad = np.array(grad)
        print(self.grad)

    def noise(self, x):
        # x has to be in [0, 1[
        bounded_x = x - int(x)

        # Calcul de l'indice du noeud inférieur
        i_max = self.size
        index = int(bounded_x * i_max)

        # Calcul de la distance entre le point et les noeuds voisins
        previous_value = index / i_max
        next_value = (index + 1) / i_max
        dist_node1 = bounded_x - previous_value
        dist_node2 = next_value - bounded_x

        # Coefficient d'interpolation
        c = dist_node1 / (next_value - previous_value)
        return interpolate_smooth(self.grad[index] * dist_node1, self.grad[index + 1] * dist_node2, c)


def main(dim=2, seed=0):

    if dim == 1:
        perlin = Perlin1d(n=4, seed=seed)

        n_max = 200
        result = [0 for _ in range(n_max)]
        f = 1
        step = 1 / (n_max - 1)

        for p in range(1):
            freq_factor = 2 ** p
            amp_factor = 1 / (2 ** p)
            for i in range(n_max):
                result[i] += amp_factor * perlin.noise(freq_factor * f * step * i)

        plt.plot(result)
        plt.show()

    else:
        perlin = Perlin2d(n=16, seed=seed)

        n_max = 400
        image = [[0 for _ in range(n_max)] for _ in range(n_max)]
        f = 1
        step = .001  # 1 / (n_max - 1)

        for p in range(8):
            amp_factor = 1 / (2 ** p)
            freq_factor = 2 ** p
            for i in range(n_max):
                for j in range(n_max):
                    x = freq_factor * f * step * i
                    y = freq_factor * f * step * j
                    image[i][j] += amp_factor * perlin.noise(x, y)

        for i in range(n_max):
            for j in range(n_max):
                image[i][j] += 1
                image[i][j] *= 1000

        plt.imshow(np.array(image))
        plt.show()


if __name__ == "__main__":
    main(dim=2)
