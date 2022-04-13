#!/usr/bin/env python3

import glfw
from core import Viewer, Shader, Node, load
from texture import Texture, Textured
from transform import translate, rotate, scale, identity


class Slab(Textured):
    """ Very simple cylinder based on provided load function """

    def __init__(self, shader, tex_file):
        super().__init__(*load('src/slab.obj', shader), textures=Texture(tex_file))


def straight_rail(bar_slab, plank_slab):
    frame = Node()

    left_bar = Node(transform=translate(.2, .5, 0) @ scale(.05, .5, .1))
    left_bar.add(bar_slab)

    right_bar = Node(transform=translate(.8, .5, 0) @ scale(.05, .5, .1))
    right_bar.add(bar_slab)

    upper_plank = Node(transform=translate(.5, .75, 0) @ scale(.5, .15, .05))
    upper_plank.add(plank_slab)

    lower_plank = Node(transform=translate(.5, .25, 0) @ scale(.5, .15, .05))
    lower_plank.add(plank_slab)

    frame.add(left_bar)
    frame.add(right_bar)
    frame.add(upper_plank)
    frame.add(lower_plank)

    return frame


def curved_rail(bar_slab, plank_slab):
    frame = Node()

    outter_bar1 = Node(transform=translate(.765, .22, 0) @ rotate((0, 0, 1), 8) @ scale(.05, .23, .1))
    outter_bar1.add(bar_slab)
    outter_bar2 = Node(transform=translate(.582, .582, 0) @ rotate((0, 0, 1), 45) @ scale(.05, .24, .1))
    outter_bar2.add(bar_slab)
    outter_bar3 = Node(transform=translate(.22, .765, 0) @ rotate((0, 0, 1), 82) @ scale(.05, .24, .1))
    outter_bar3.add(bar_slab)

    inner_bar1 = Node(transform=translate(.168, .078, 0) @ rotate((0, 0, 1), 20) @ scale(.05, .1, .1))
    inner_bar1.add(bar_slab)
    inner_bar2 = Node(transform=translate(.078, .168, 0) @ rotate((0, 0, 1), 70) @ scale(.05, .1, .1))
    inner_bar2.add(bar_slab)

    upper_plank = Node(transform=translate(.47, .22, 0) @ rotate((0, 0, 1), 14) @ scale(.5, .15, .05))
    upper_plank.add(plank_slab)

    lower_plank = Node(transform=translate(.22, .47, 0) @ rotate((0, 0, 1), 76) @ scale(.5, .15, .05))
    lower_plank.add(plank_slab)

    frame.add(outter_bar1)
    frame.add(outter_bar2)
    frame.add(outter_bar3)
    frame.add(inner_bar1)
    frame.add(inner_bar2)
    frame.add(upper_plank)
    frame.add(lower_plank)

    return frame


class Rails(Node):

    def __init__(self, shader, rail_type, transform=identity()):
        bar_slab = Slab(shader, "src/iron.png")
        wood_slab = Slab(shader, "src/wood.png")

        if rail_type == 3:
            rail = straight_rail(bar_slab, wood_slab)
            node = Node(transform=translate(1, 0, 0) @ rotate((0, 0, 1), 90))
            node.add(rail)
        if rail_type == 4:
            node = straight_rail(bar_slab, wood_slab)
        if rail_type == 5:
            rail = curved_rail(bar_slab, wood_slab)
            node = Node(transform=translate(0, 1, 0) @ rotate((0, 0, 1), -90))
            node.add(rail)
        if rail_type == 6:
            node = curved_rail(bar_slab, wood_slab)
        if rail_type == 7:
            rail = curved_rail(bar_slab, wood_slab)
            node = Node(transform=translate(1, 1, 0) @ rotate((0, 0, 1), 180))
            node.add(rail)
        if rail_type == 8:
            rail = curved_rail(bar_slab, wood_slab)
            node = Node(transform=translate(1, 0, 0) @ rotate((0, 0, 1), 90))
            node.add(rail)

        super().__init__([node], transform=transform)




def main():
    viewer = Viewer()
    shader = Shader("shaders/texture.vert", "shaders/texture.frag")

    viewer.add(Rails(shader, rail_type=3))
    viewer.run()


if __name__ == "__main__":
    main()
