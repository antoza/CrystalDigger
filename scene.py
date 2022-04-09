#!/usr/bin/env python3

import numpy as np

from core import Shader, Viewer, Node
from transform import rotate, translate, scale, vec, identity

from surface import Surface
from color import fire, catmull_derivatives


def generate_floor(surface, level):
    """
    Generates the floor and ceiling of the scene
    :param surface: the surface to be used for the floor
    :param level: the level, giving position of the floor
    :return: a node for the floor and ceiling
    """
    sx, sy = surface.get_size()
    x, y = level.shape

    scaling_factor = min(1 / sx, 1 / sy)
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
                i_near = [(i - 1) % x, (i + 1) % x]
                j_near = [(j - 1) % y, (j + 1) % y]

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
                    t = translate((i + 1, j, 1))
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
                    t = translate((i, j + 1, 1))
                    wall = Node(transform=t @ r @ s)
                    wall.add(surface)
                    walls.add(wall)
    return walls


def generate_torches(level):
    """
    Generates the torches of the scene
    :param torch: the model to load
    :param level: the level, giving position of the torches
    :return: a node for the torches, a list of their positions in the level
    """
    x, y = level.shape
    lights = []

    for i in range(x):
        for j in range(y):
            if level[i][j] == 2:
                lights.append(vec(i + .25, j + .25, .5, 1))

    return Node(), np.array(lights)


class Scene(Node):

    def __init__(self, shader, level, transform=identity()):
        torches, self.lights_pos = generate_torches(level)
        for i in range(len(self.lights_pos)):
            self.lights_pos[i] = transform @ self.lights_pos[i]

        self.light_colors = fire
        self.catmull = catmull_derivatives(fire, .5)

        wall_tile = Surface(shader, n_x=50, n_y=50, amp=2, f=.1)
        floor_tile = Surface(shader, n_x=50, n_y=50, amp=.1)

        floor = generate_floor(floor_tile, level)
        walls = generate_walls(wall_tile, level)

        super().__init__((floor, walls), transform=transform)

    def draw(self, model=identity(), **other_uniforms):
        super().draw(model=model, lights=self.lights_pos, nb_lights=self.lights_pos.shape,
                     light_colors=self.light_colors, nb_colors=self.light_colors.shape[0],
                     catmull=self.catmull, d_segt=.5, **other_uniforms)


def main():
    viewer = Viewer()
    shader = Shader("shaders/texture.vert", "shaders/scene.frag")

    list_level = [[1, 1, 1, 1, 1],
                  [1, 2, 0, 0, 1],
                  [1, 0, 1, 0, 1],
                  [1, 0, 0, 2, 1],
                  [1, 0, 1, 0, 1],
                  [1, 1, 1, 1, 1]]
    level = np.array(list_level)
    x, y = level.shape

    scene = Scene(shader, level, transform=translate(-x / 2, -y / 2, 0))
    viewer.add(scene)
    viewer.run()


if __name__ == "__main__":
    print("============================================================================")
    print("*             DEMONSTRATION DE LA GENERATION DE LA SCENE                   *")
    print("============================================================================")
    main()
