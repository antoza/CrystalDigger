#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args

from core import *
from transform import *

class MultiAnimatedSpider(Node):
    def __init__(self, shader, light_dir=(0, 0, -1), transform=identity()):
        super().__init__(transform=transform)
        self.etat = "idle"
        self.listEtat = {"idle": 0, "walk": 1}
        for way in ["Spider/Spider_Idle.fbx", "Spider/Spider_run.fbx"]:
            child = Node()
            child.add(*load(way, shader, light_dir=light_dir))
            child.display = False
            self.add(child)
        self.children[0].display = True
        self.iteration = 0

    def key_handler(self, key):
        """ Dispatch keyboard events to children with key handler """
        if key == glfw.KEY_O:
            self.etat = "walk"
            glfw.set_time(0.0)
            self.children[1].display = True
            self.children[0].display = False

    def draw(self, model=identity(), **other_uniforms):
        limit = 30
        if self.iteration < limit and self.etat == "walk":
            self.transform = self.transform @ translate(0, -.25, 0)
            self.iteration += 1
        if self.iteration >= limit and self.etat == "walk":
            self.etat = "idle"
            self.iteration = 0
            self.children[0].display = True
            self.children[1].display = False
            #glfw.set_time(0.0)
        super().draw(model=model, **other_uniforms)

class AnimatedSpider(Node):
    """ Very simple spider based on provided load function """
    def __init__(self, shader, light_dir=(0, 0, -1), transform=identity()):
        super().__init__(transform=transform)
        way = 'Spider/Spider_Idle.fbx'
        self.add(*load(way, shader, light_dir=light_dir))


    def draw(self, model=identity(), **other_uniforms):
        super().draw(model=model, **other_uniforms)



# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader = Shader("shaders/animatedAndTextured.vert", "shaders/animatedAndTextured.frag")
    #viewer.trackball.zoom(0, glfw.get_window_size(viewer.win)[1])

    scalevalue = 0.05
    matrix = rotate((1, 0, 0), 45) @ scale(scalevalue, scalevalue, scalevalue)
    spider = MultiAnimatedSpider(shader=shader, transform=matrix)
    spider2 = AnimatedSpider(shader=shader, transform=matrix)

    viewer.add(spider)

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
