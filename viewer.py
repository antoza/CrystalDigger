#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args

from core import *
from transform import *
from animation import *


# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader = Shader("shaders/animatedAndTextured.vert", "shaders/texture.frag")

    light_dir = (0, 0, -1)
    viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader,
        light_dir=light_dir)])

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
