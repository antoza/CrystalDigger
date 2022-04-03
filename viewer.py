#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL  # standard Python OpenGL wrapper
import glfw  # lean window system wrapper for OpenGL
import numpy as np  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load
from texture import Texture, Textured
from perlin import Perlin2d


# -------------- Example textured plane class ---------------------------------
class TexturedPlane(Textured):
    """ Simple first textured object """

    def __init__(self, shader, tex_files):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.files = tex_files

        # setup plane mesh to be textured
        base_coords = ((-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0))
        scaled = 100 * np.array(base_coords, np.float32)
        indices = np.array((0, 1, 2, 0, 2, 3), np.uint32)
        mesh = Mesh(shader, attributes=dict(position=scaled), index=indices)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(tex_files, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture)

    def key_handler(self, key):
        # cycle through texture modes on keypress of F6 (wrap) or F7 (filtering)
        self.wrap = next(self.wraps) if key == glfw.KEY_F6 else self.wrap
        self.filter = next(self.filters) if key == glfw.KEY_F7 else self.filter
        if key in (glfw.KEY_F6, glfw.KEY_F7):
            texture = Texture(self.files, self.wrap, *self.filter)
            self.textures.update(diffuse_map=texture)


class Floor(Textured):

    def __init__(self, shader, tex):
        perlin = Perlin2d()

        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.tex = tex

        f = 2.5

        vert = []
        indices = []
        amp = 1
        n_x = 30  # number of squares x-axis
        n_y = 30  # number of squares y-axis
        off_x = n_x / 2
        off_y = n_y / 2
        for j in range(n_y+1):
            for i in range(n_x+1):
                # vertices
                vert.append((i - off_x, j - off_y, amp * perlin.noise(f * i, f * j)))

        for j in range(n_y):
            for i in range(n_x):
                # first triangle
                indices.append(i + (n_x + 1) * j)
                indices.append(i + 1 + (n_x + 1) * j)
                indices.append(i + (n_x + 1) * (j + 1))

                # second triangle
                indices.append(i + (n_x + 1) * (j + 1))
                indices.append(i + 1 + (n_x + 1) * j)
                indices.append(i + 1 + (n_x + 1) * (j+1))

        self.vert = np.array(vert)
        self.indices = np.array(indices)

        mesh = Mesh(shader, attributes=dict(position=self.vert), index=self.indices)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture1 = Texture(tex, self.wrap, *self.filter)
        # texture2 = Texture(tex[1], self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture1)  # second_texture=texture2)

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

    light_dir = (2, 1, 3)
    viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader, light_dir=light_dir)])
    viewer.add(Floor(shader, "grass.png"))

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()  # main function keeps variables locally scoped
