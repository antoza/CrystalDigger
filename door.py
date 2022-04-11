#!/usr/bin/env python3

import glfw
from core import Viewer, Shader, Node, load
from texture import Texture, Textured
from transform import translate, rotate, scale, identity


class Slab(Textured):
    """ Very simple cylinder based on provided load function """

    def __init__(self, shader, tex_file):
        super().__init__(*load('slab.obj', shader), textures=Texture(tex_file))


def generate_door_frame(slab):
    frame = Node()

    left_frame = Node(transform=translate(-.1, .5, 0) @ scale(.1, .5, .1))
    left_frame.add(slab)

    right_frame = Node(transform=translate(.7, .5, 0) @ scale(.1, .5, .1))
    right_frame.add(slab)

    upper_frame = Node(transform=translate(.3, 1.1, 0) @ scale(.5, .1, .1))
    upper_frame.add(slab)

    frame.add(left_frame)
    frame.add(right_frame)
    frame.add(upper_frame)

    return frame


class Door(Node):

    def __init__(self, shader, transform=identity()):
        dark_slab = Slab(shader, "dark_wood.png")
        slab = Slab(shader, "planks.png")

        door_frame = generate_door_frame(dark_slab)
        self.door_leaf = Node(transform=translate(.3, .5, 0) @ rotate((0, 1, 0), 180) @ scale(.3, .5, .05))
        self.door_leaf.add(slab)
        self.angle = 0
        self.target_angle = 0
        self.opened = False

        super().__init__((door_frame, self.door_leaf), transform=transform@rotate((1, 0, 0), 90)@translate(.2, 0, 0))

    def key_handler(self, key):
        if key == glfw.KEY_O:
            if not self.opened:
                self.target_angle = 90
        if key == glfw.KEY_C:
            if self.opened:
                self.target_angle = -90

    def draw(self, model=identity(), **other_uniforms):
        if self.angle != self.target_angle:
            step = self.target_angle/18
            self.door_leaf.transform = rotate((0, 1, 0), step) @ self.door_leaf.transform
            self.angle += step

            if self.angle == self.target_angle:
                if self.angle == 90:
                    self.opened = True
                else:
                    self.opened = False
                self.angle = 0
                self.target_angle = 0

        super().draw(model=model, k_a=(.4, .4, .4), k_d=(.4, .4, .4), k_s=(.4, .4, .4), s=100, **other_uniforms)

    def get_size(self):
        return


def main():
    viewer = Viewer()
    shader = Shader("shaders/texture.vert", "shaders/texture.frag")

    viewer.add(Door(shader))
    viewer.run()


if __name__ == "__main__":
    main()
