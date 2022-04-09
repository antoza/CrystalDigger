#!/usr/bin/env python3
import sys
from itertools import cycle

import OpenGL.GL as GL  # standard Python OpenGL wrapper
import glfw  # lean window system wrapper for OpenGL
import numpy as np  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load
from texture import Textured
from perlin import Perlin2d
from transform import vec, translate, scale
from core import Node
from math import sqrt


# -------------- Notre petit jeu fait maison :) ---------------------------------

def norm(vect):
    return sqrt(vect[0] ** 2 + vect[1] ** 2 + vect[2] ** 2)


def surface_mesh(shader, amp=1, n_x=30, n_y=30, f=.2):
    # Perlin noise initialisation
    n = 16
    perlin = Perlin2d(n=n)

    vert = []
    normals = []
    indices = []

    for j in range(n_y):
        for i in range(n_x):
            # heights of the (possibly) duplicated vertices
            I = i
            J = j

            z1 = amp * perlin.noise(f * I, f * J) + amp * perlin.noise(2 * f * I, 2 * f * J)
            z2 = amp * perlin.noise(f * (I + 1), f * J) + amp * perlin.noise(2 * f * (I + 1), 2 * f * J)
            z3 = amp * perlin.noise(f * I, f * (J + 1)) + amp * perlin.noise(2 * f * I, 2 * f * (J + 1))
            z4 = amp * perlin.noise(f * (I + 1), f * (J + 1)) + amp * perlin.noise(2 * f * (I + 1), 2 * f * (J + 1))

            # vertices of the first triangle
            vert.append((i, j, z1))
            vert.append((i + 1, j, z2))
            vert.append((i, j + 1, z3))

            # vertices of the second triangle
            vert.append((i + 1, j, z2))
            vert.append((i + 1, j + 1, z4))
            vert.append((i, j + 1, z3))

            # normals of the first triangle
            zn1 = z2 + z3 - 2 * z1
            zn2 = z4 + z2 - 2 * z3
            if zn1 == 0:
                normal1 = vec((0, 0, 1))
            else:
                normal1 = vec([1, 1, zn1])
                normal1 /= norm(normal1)

            if zn2 == 0:
                normal2 = vec((0, 0, 1))
            else:
                normal2 = vec([1, 1, zn2])
                normal2 /= norm(normal2)

            normals.append(normal1)
            normals.append(normal1)
            normals.append(normal1)
            normals.append(normal2)
            normals.append(normal2)
            normals.append(normal2)

    for n in range(6 * n_x * n_y):
        indices.append(n)

    uniforms = dict({"k_a": (.4, .4, .4), "k_d": (.4, .4, .4), "k_s": (.4, .4, .4), "s": 100})
    return Mesh(shader, attributes=dict(position=np.array(vert), normal=np.array(normals)),
                index=np.array(indices), uniforms=uniforms)


class Surface:

    def __init__(self, shader, amp=1, n_x=30, n_y=30, f=.2):
        self.mesh = surface_mesh(shader, amp, n_x, n_y, f)
        self.n_x = n_x
        self.n_y = n_y

    def get_size(self):
        return self.n_x, self.n_y

    def draw(self, primitives=GL.GL_TRIANGLES, **other_uniforms):
        self.mesh.draw(primitives=primitives, **other_uniforms)


# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader = Shader("shaders/texture.vert", "shaders/scene.frag")

    surface = Node(transform=translate((-.5, -.5, 0)) @ scale(1 / 30, 1 / 30, 1 / 30))
    surface.add(Surface(shader, n_x=30, n_y=30, f=.1, amp=2))

    viewer.add(surface)

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    print("============================================================================")
    print("*            DEMONSTRATION DE LA GENERATION D'UNE SURFACE                  *")
    print("============================================================================")
    main()  # main function keeps variables locally scoped
