#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args

from core import *
from transform import *


class Spider(Node):
    """ Very simple spider based on provided load function """
    def __init__(self, shader, light_dir=(0, 0 ,-1), transform=identity()):
        super().__init__(transform=transform)
        way = 'Spider/Spider_run.fbx'
        self.add(*load(way, shader, light_dir=light_dir))


# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader = Shader("shaders/animatedAndTextured.vert", "shaders/animatedAndTextured.frag")

    spider = Spider(shader)
    #spider2 = Spider(shader, transform=translate(100, 0, 0))
    #spider3 = Spider(shader, transform=translate(-100, 0, 0))


    viewer.add(spider)
    #viewer.add(spider2)
    #viewer.add(spider3)

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
