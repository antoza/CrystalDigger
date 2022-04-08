#!/usr/bin/env python3

import numpy as np

from core import Shader, Viewer, Node
from transform import rotate, translate, scale

from surface import Surface


def generate_floor(surface, level):
    """
    Generates the floor and ceiling of the scene
    :param surface: the surface to be used for the floor
    :param level: the level, giving position of the floor
    :return: a node for the floor and ceiling
    """
    sx, sy = surface.get_size()
    x, y = level.shape

    scaling_factor = min(1/sx, 1/sy)
    s = scale(scaling_factor, scaling_factor, scaling_factor)
    floor = Node()

    for i in range(x):
        for j in range(y):
            # Generate roof of the wall
            if level[i][j] == 1:
                t = translate(i, j, 1)
            # Generate floor
            else:
                t = translate(i, j, .1)
            tile = Node(transform=t @ s)
            tile.add(surface)
            floor.add(tile)
    return floor


def generate_walls(surface, level):
    """
    Generates the walls of the scene
    :param surface: the surface to be used for the floor
    :param level: the level, giving position of the floor
    :return: a node for the walls
    """
    sx, sy = surface.get_size()
    x, y = level.shape

    scaling_factor = min(1 / sx, 1 / sy)
    s = scale(scaling_factor, scaling_factor, scaling_factor)
    walls = Node()

    for i in range(x):
        for j in range(y):
            # Generate only on walled tiles
            if level[i][j] == 1:
                i_near = [(i-1) % x, (i+1) % x]
                j_near = [(j-1) % y, (j+1) % y]

                # left wall
                if level[i_near[0]][j] != 1:
                    r = rotate((0, 1, 0), -90)
                    t = translate((i, j, 0))
                    wall = Node(transform=t @ r @ s)
                    wall.add(surface)
                    walls.add(wall)

                # right wall
                if level[i_near[1]][j] != 1:
                    r = rotate((0, 1, 0), 90)
                    t = translate((i+1, j, 1))
                    wall = Node(transform=t @ r @ s)
                    wall.add(surface)
                    walls.add(wall)

                # upper wall
                if level[i][j_near[0]] != 1:
                    r = rotate((1, 0, 0), 90)
                    t = translate((i, j, 0))
                    wall = Node(transform=t @ r @ s)
                    wall.add(surface)
                    walls.add(wall)

                # lower wall
                if level[i][j_near[1]] != 1:
                    r = rotate((1, 0, 0), -90)
                    t = translate((i, j+1, 1))
                    wall = Node(transform=t @ r @ s)
                    wall.add(surface)
                    walls.add(wall)
    return walls


def generate_torches(torch, level):
    """
    Generates the torches of the scene
    :param torch: the model to load
    :param level: the level, giving position of the torches
    :return: a node for the torches, a list of their positions in the level
    """




def generate_scene(shader, level):
    # adding the floor
    x, y = level.shape
    lights = [(1, 1, 1)]
    wall_tile = Surface(shader, n_x=50, n_y=50, amp=2, f=.1)
    floor_tile = Surface(shader, n_x=50, n_y=50, amp=.1, lights=lights)

    floor = generate_floor(floor_tile, level)
    walls = generate_walls(wall_tile, level)

    scene = Node(transform=translate(-x/2, -y/2, 0))
    scene.add(floor)
    scene.add(walls)

    return scene


def main():
    viewer = Viewer()
    shader = Shader("shaders/texture.vert", "shaders/scene.frag")

    list_level = [[1, 1, 1, 1, 1],
                  [1, 0, 0, 0, 1],
                  [1, 0, 1, 0, 1],
                  [1, 0, 1, 0, 1],
                  [1, 0, 1, 0, 1],
                  [1, 1, 1, 1, 1]]
    level = np.array(list_level)

    scene = generate_scene(shader, level)
    viewer.add(scene)
    viewer.run()


if __name__ == "__main__":
    print("============================================================================")
    print("*             DEMONSTRATION DE LA GENERATION DE LA SCENE                   *")
    print("============================================================================")
    main()
