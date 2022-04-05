#!/usr/bin/env python3

from core import Shader, Viewer, Mesh, load, Node
from transform import rotate, translate, scale

from viewer import Surface


def generate_walls(surface, rotation=rotate((0, 0, 1), 0), n_x=10, n_y=10):
    offset_x = n_x / 2
    offset_x -= offset_x / n_x
    offset_y = n_y / 2
    offset_y -= offset_y / n_y

    scale_x = 30
    scale_y = 30

    r = rotate((1, 0, 0), 45)
    s = scale(1 / scale_x, 1 / scale_y, min(1 / scale_x, 1 / scale_y))
    walls = Node(transform = rotation)
    for i in range(-1, n_x + 1):
        t = translate(-offset_x + i, offset_y, offset_x / n_x)
        wall = Node(transform=t @ r @ s)
        wall.add(surface)
        walls.add(wall)
    return walls


def generate_scene(shader):
    scene = Node(transform=rotate((1, 0, 0), -30) @ translate(0, 5, -10))

    surface = Surface(shader, n_x=30, n_y=30)

    # adding the floor
    n_x = 10
    n_y = 10
    scene.add(Surface(shader, amp=.1, n_x=n_x, n_y=n_y))

    upper_walls = generate_walls(surface, n_x=n_x, n_y=n_y)
    right_walls = generate_walls(surface, n_x=n_x, n_y=n_y, rotation=rotate((0, 0, 1), -90))
    left_walls = generate_walls(surface, n_x=n_x, n_y=n_y, rotation=rotate((0, 0, 1), 90))
    lower_walls = generate_walls(surface, n_x=n_x, n_y=n_y, rotation=rotate((0, 0, 1), 180))
    scene.add(upper_walls)
    scene.add(right_walls)
    scene.add(left_walls)
    scene.add(lower_walls)

    return scene


def main():
    viewer = Viewer()
    shader = Shader("texture.vert", "texture.frag")

    scene = generate_scene(shader)

    viewer.add(scene)

    viewer.run()


if __name__ == "__main__":
    main()