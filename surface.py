#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL  # standard Python OpenGL wrapper
import glfw  # lean window system wrapper for OpenGL
import numpy as np  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load
from texture import Texture, Textured
from perlin import Perlin2d
from transform import vec, translate, scale
from core import Node
from math import sqrt


# -------------- Notre petit jeu fait maison :) ---------------------------------

def norm(vect):
    return sqrt(vect[0]**2 + vect[1] ** 2 + vect[2] ** 2)


class Surface(Textured):

    def __init__(self, shader, amp=1, n_x=30, n_y=30):

        # Perlin noise initialisation
        n = 16
        perlin = Perlin2d(n=n)

        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)

        f = .2

        vert = []
        normals = []
        indices = []

        self.n_x = n_x
        self.n_y = n_y
        for j in range(n_y):
            for i in range(n_x):
                # heights of the (possibly) duplicated vertices
                I = i
                J = j

                z1 = amp * perlin.noise(f * I, f * J) + amp * perlin.noise(2 * f * I, 2 * f * J)
                z2 = amp * perlin.noise(f * (I + 1), f * J) + amp * perlin.noise(2 * f * (I+1), 2 * f * J)
                z3 = amp * perlin.noise(f * I, f * (J+1)) + amp * perlin.noise(2 * f * I, 2 * f * (J+1))
                z4 = amp * perlin.noise(f * (I+1), f * (J+1)) + amp * perlin.noise(2 * f * (I+1), 2 * f * (J+1))

                # vertices of the first triangle
                vert.append((i, j, z1))
                vert.append((i + 1, j, z2))
                vert.append((i, j + 1, z3))

                # vertices of the second triangle
                vert.append((i + 1, j, z2))
                vert.append((i + 1, j + 1, z4))
                vert.append((i, j + 1, z3))

                # normals of the first triangle
                zn1 = z2 + z3 - 2*z1
                zn2 = z4 + z2 - 2*z3
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

        self.vert = np.array(vert)
        self.normals = np.array(normals)
        self.indices = np.array(indices)

        # Defining the material and the light_direction
        uniforms = dict({"k_a": (.2, .2, .2), "k_d": (1, 1, 1), "k_s": (.5, .5, .5), "s": .1, "light_dir": (-1, -.2, -1)})

        mesh = Mesh(shader, attributes=dict(position=self.vert, normal=self.normals),
                    index=self.indices, uniforms=uniforms)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        # texture1 = Texture(tex, self.wrap, *self.filter)
        # texture2 = Texture(tex[1], self.wrap, *self.filter)
        # super().__init__(mesh, diffuse_map=texture1)  # second_texture=texture2)
        super().__init__(mesh)

    def get_size(self):
        return self.n_x, self.n_y


# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader = Shader("texture.vert", "texture.frag")

    light_dir = (0, 0, -1)
    viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader, light_dir=light_dir)])

    surface = Node(transform=translate((-1.5, -1.5, 0)) @ scale(.01, .01, .01))
    surface.add(Surface(shader))

    viewer.add(surface)

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()  # main function keeps variables locally scoped
