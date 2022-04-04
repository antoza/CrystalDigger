#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL  # standard Python OpenGL wrapper
import glfw  # lean window system wrapper for OpenGL
import numpy as np  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load
from texture import Texture, Textured
from perlin import Perlin2d


# -------------- Notre petit jeu fait maison :) ---------------------------------

class Floor(Textured):

    def __init__(self, shader, tex=None):
        perlin = Perlin2d()

        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        #self.tex = tex

        f = .1

        vert = []
        normals = []
        indices = []
        amp = 1
        n_x = 30  # number of squares x-axis
        n_y = 30  # number of squares y-axis
        off_x = n_x / 2
        off_y = n_y / 2
        for j in range(n_y):
            for i in range(n_x):
                # heights of the (possibly) duplicated vertices
                z1 = amp * perlin.noise(f * i, f * j) + amp * perlin.noise(2 * f * i, 2 * f * j)
                z2 = amp * perlin.noise(f * (i + 1), f * j) + amp * perlin.noise(2 * f * (i+1), 2 * f * j)
                z3 = amp * perlin.noise(f * i, f * (j+1)) + amp * perlin.noise(2 * f * i, 2 * f * (j+1))
                z4 = amp * perlin.noise(f * (i+1), f * (j+1)) + amp * perlin.noise(2 * f * (i+1), 2 * f * (j+1))

                # vertices of the first triangle
                vert.append((i - off_x, j - off_y, z1))
                vert.append((i + 1 - off_x, j - off_y, z2))
                vert.append((i - off_x, j + 1 - off_y, z3))

                # vertices of the second triangle
                vert.append((i + 1 - off_x, j - off_y, z2))
                vert.append((i + 1 - off_x, j + 1 - off_y, z4))
                vert.append((i - off_x, j + 1 - off_y, z3))

                # normals of the first triangle
                normal1 = [1, 1, z2 + z3 - 2*z1]
                normal2 = [1, 1, z4 + z2 - 2*z3]
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
        uniforms = dict({"k_a": (.25, .21, .21), "k_d": (1, .83, .83), "k_s": (.3, .3, .3), "s": .088, "light_dir": (0, 0, -1)})

        mesh = Mesh(shader, attributes=dict(position=self.vert, normal=self.normals),
                    index=self.indices, uniforms=uniforms)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        # texture1 = Texture(tex, self.wrap, *self.filter)
        # texture2 = Texture(tex[1], self.wrap, *self.filter)
        # super().__init__(mesh, diffuse_map=texture1)  # second_texture=texture2)
        super().__init__(mesh)

    def key_handler(self, key):
        # cycle through texture modes on keypress of F6 (wrap) or F7 (filtering)
        self.wrap = next(self.wraps) if key == glfw.KEY_F6 else self.wrap
        self.filter = next(self.filters) if key == glfw.KEY_F7 else self.filter
        if key in (glfw.KEY_F6, glfw.KEY_F7):
            texture = Texture(self.tex, self.wrap, *self.filter)
            self.textures.update(diffuse_map=texture)


# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader = Shader("texture.vert", "texture.frag")

    light_dir = (0, 0, -1)
    viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader, light_dir=light_dir)])
    viewer.add(Floor(shader))

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()  # main function keeps variables locally scoped
