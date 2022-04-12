#!/usr/bin/env python3

import numpy as np


def catmull_derivatives(p, c):
    coeff = 1 - c
    derivatives = np.zeros(p.shape)

    # First derivative
    derivatives[0] = coeff * (3 * (p[1] - p[0]) + (p[2] - p[0])) / 4

    # Last derivative
    derivatives[-1] = coeff * (3 * (p[-1] - p[-2]) + (p[-1] - p[-3])) / 4

    # In-between derivatives
    for k in range(1, p.shape[0] - 1):
        derivatives[k] = coeff * (p[k + 1] - p[k - 1]) / 2

    return derivatives


fire = np.array(((1, 1, .28), (.99, .87, .17), (.965, .565, .067), (.729, .012, .012), (.502, 0, 0),
                (0, 0, 0)))


def main():
    print(catmull_derivatives(fire, .5))


if __name__ == "__main__":
    main()