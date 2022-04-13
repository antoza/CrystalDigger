#!/usr/bin/env python3

import glfw
from core import Viewer, Shader, Node, load
from texture import Texture, Textured
from transform import translate, rotate, scale, identity


class Slab(Textured):
    """ Very simple cylinder based on provided load function """

    def __init__(self, shader, tex_file):
        super().__init__(*load('src/slab.obj', shader), textures=Texture(tex_file))

class Cylinder(Textured):
    """ Very simple cylinder based on provided load function """

    def __init__(self, shader, tex_file):
        super().__init__(*load('src/cylinder.obj', shader), textures=Texture(tex_file))

def generate_wagon(slab):
    frame = Node()

    bottom = Node(transform=translate(.5, .5, .2) @ scale(.4, .3, .05))
    bottom.add(slab)

    left = Node(transform=translate(.09, .5, .5) @ rotate((0, 1, 0), 80) @ scale(.3, .3, .05))
    left.add(slab)

    right = Node(transform=translate(.91, .5, .5) @ rotate((0, 1, 0), -80) @ scale(.3, .3, .05))
    right.add(slab)

    down = Node(transform=translate(.5, .19, .5) @ rotate((1, 0, 0), -90) @ scale(.4, .3, .05))
    down.add(slab)

    up = Node(transform=translate(.5, .81, .5) @ rotate((1, 0, 0), 90) @ scale(.4, .3, .05))
    up.add(slab)

    frame.add(bottom)
    frame.add(left)
    frame.add(right)
    frame.add(down)
    frame.add(up)

    return frame


class Minecart(Node):

    def __init__(self, shader, transform=identity()):
        iron = Slab(shader, "src/iron.png")
        wood = Cylinder(shader, "src/dark_wood.png")

        iron_wagon = generate_wagon(iron)
        self.wheels = []
        for x in (.15, .85):
            for y in (.20, .80):
                self.wheels.append(Node(transform=translate(x, y, .1) @ scale(.15, .1, .15)))
                self.wheels[-1].add(wood)
        #self.door_leaf = Node(transform=translate(.3, .5, 0) @ rotate((0, 1, 0), 180) @ scale(.3, .5, .05))
        #self.door_leaf.add(slab)
        #self.angle = 0
        #self.target_angle = 0
        #self.opened = False

        super().__init__([iron_wagon] + self.wheels, transform=transform)

   # def key_handler(self, key):
   #     if key == glfw.KEY_O:
   #         if not self.opened:
   #             self.target_angle = 90
   #     if key == glfw.KEY_C:
   #         if self.opened:
   #             self.target_angle = -90

    def draw(self, model=identity(), **other_uniforms):
        #if self.angle != self.target_angle:
        #    step = self.target_angle/18
        #    self.door_leaf.transform = rotate((0, 1, 0), step) @ self.door_leaf.transform
        #    self.angle += step

        #    if self.angle == self.target_angle:
        #        if self.angle == 90:
        #            self.opened = True
        #        else:
        #            self.opened = False
        #        self.angle = 0
        #        self.target_angle = 0

        super().draw(model=model, k_a=(.4, .4, .4), k_d=(.4, .4, .4), k_s=(.4, .4, .4), s=100, **other_uniforms)

    def get_size(self):
        return


def main():
    viewer = Viewer()
    shader = Shader("shaders/texture.vert", "shaders/materialTexture.frag")

    viewer.add(Minecart(shader))
    viewer.run()


if __name__ == "__main__":
    main()
