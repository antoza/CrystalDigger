#!/usr/bin/env python3

import numpy as np
from math import sin, cos

from core import Shader, Viewer, Node
from transform import rotate, translate, scale, vec, identity

from surface import Surface
from door import Door, Slab
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
                if level[i_near[0]][j] != 1 or 3:
                    r = rotate((0, 1, 0), -90)
                    t = translate((i, j, 0))
                    wall = Node(transform=t @ r @ s)
                    wall.add(surface)
                    walls.add(wall)

                # right wall
                if level[i_near[1]][j] != 1 or 3:
                    r = rotate((0, 1, 0), 90)
                    t = translate((i + 1, j, 1))
                    wall = Node(transform=t @ r @ s)
                    wall.add(surface)
                    walls.add(wall)

                # upper wall
                if level[i][j_near[0]] != 1 or 3:
                    r = rotate((1, 0, 0), 90)
                    t = translate((i, j, 0))
                    wall = Node(transform=t @ r @ s)
                    wall.add(surface)
                    walls.add(wall)

                # lower wall
                if level[i][j_near[1]] != 1 or 3:
                    r = rotate((1, 0, 0), -90)
                    t = translate((i, j + 1, 1))
                    wall = Node(transform=t @ r @ s)
                    wall.add(surface)
                    walls.add(wall)
    return walls


def generate_doors(shader, level):
    x, y = level.shape

    doors = Node()

    for i in range(x):
        for j in range(y):
            if level[i][j] == 3:
                door = Node()

                i_near = [(i - 1) % x, (i + 1) % x]
                j_near = [(j - 1) % y, (j + 1) % y]

                # right door
                if level[i_near[0]][j] != 1:
                    r = rotate((0, 0, 1), -90)
                    t = translate((i + 1, j + 1, 0))
                    door.transform = t @ r @ door.transform
                    door.add(Door(shader))

                # left door
                elif level[i_near[1]][j] != 1:
                    r = rotate((0, 0, 1), 90)
                    t = translate((i, j, 0))
                    door.transform = t @ r @ door.transform
                    door.add(Door(shader))

                # lower door
                elif level[i][j_near[0]] != 1:
                    t = translate((i, j + 1, 0))
                    door.transform = t @ door.transform
                    door.add(Door(shader))

                # upper door
                elif level[i][j_near[1]] != 1:
                    r = rotate((0, 0, 1), 180)
                    t = translate((i + 1, j, 0))
                    door.transform = t @ r @ door.transform
                    door.add(Door(shader))

                doors.add(door)

    return doors


def generate_torches(shader, level):
    """
    Generates the torches of the scene
    :param shader: the shader to use on the torches
    :param level: the level, giving position of the torches
    :return: a node for the torches, a list of their positions in the level
    """
    x, y = level.shape
    lights = []
    scene_torches = Node()

    slab = Slab(shader, "dark_wood.png")
    single_torch = Node(transform=rotate((1, 0, 0), 90) @ translate(0, .5, 0) @ scale(.1, .5, .1))
    single_torch.add(slab)

    scaling = scale(.2, .2, .2)

    for i in range(x):
        for j in range(y):
            if level[i][j] == 2:
                # add a torch on all the adjacent walls
                torches = Node()

                i_near = [(i - 1) % x, (i + 1) % x]
                j_near = [(j - 1) % y, (j + 1) % y]

                # left wall
                if level[i_near[0]][j] == 1:
                    r = rotate((0, 1, 0), 30)
                    t = translate((i, j + .5, .5))
                    torch = Node(transform=t@r@scaling)
                    torch.add(single_torch)
                    torches.add(torch)
                    # add the new light source to the list
                    lights.append(t @ r @ scaling @ vec(0, 0, 1, 1))

                # right wall
                if level[i_near[1]][j] == 1:
                    r = rotate((0, 1, 0), -30)
                    t = translate((i + 1, j + .5, .5))
                    torch = Node(transform=t @ r @ scaling)
                    torch.add(single_torch)
                    torches.add(torch)
                    # add the new light source to the list
                    lights.append(t @ r @ scaling @ vec(0, 0, 1, 1))

                # lower wall
                if level[i][j_near[0]] == 1:
                    r = rotate((1, 0, 0), -30)
                    t = translate((i + .5, j, .5))
                    torch = Node(transform=t @ r @ scaling)
                    torch.add(single_torch)
                    torches.add(torch)
                    # add the new light source to the list
                    lights.append(t @ r @ scaling @ vec(0, 0, 1, 1))

                # upper wall
                if level[i][j_near[1]] == 1:
                    r = rotate((1, 0, 0), 30)
                    t = translate((i + .5, j + 1, .5))
                    torch = Node(transform=t @ r @ scaling)
                    torch.add(single_torch)
                    torches.add(torch)
                    # add the new light source to the list
                    lights.append(t @ r @ scaling @ vec(0, 0, 1, 1))
                scene_torches.add(torches)

    return scene_torches, np.array(lights)


class Scene(Node):

    def __init__(self, shader, level, transform=identity()):
        shader_wood = Shader("shaders/texture.vert", "shaders/texture.frag")
        torches, self.lights_pos = generate_torches(shader_wood, level)
        for i in range(len(self.lights_pos)):
            self.lights_pos[i] = transform @ self.lights_pos[i]

        self.light_colors = fire
        self.catmull = catmull_derivatives(fire, .5)

        wall_tile = Surface(shader, n_x=50, n_y=50, amp=2, f=.1)
        floor_tile = Surface(shader, n_x=50, n_y=50, amp=.1)

        floor = generate_floor(floor_tile, level)
        walls = generate_walls(wall_tile, level)

        shader_wood = Shader("shaders/texture.vert", "shaders/texture.frag")
        doors = generate_doors(shader_wood, level)

        super().__init__((floor, walls, doors, torches), transform=transform)

    def draw(self, model=identity(), **other_uniforms):
        super().draw(model=model, lights=self.lights_pos, nb_lights=self.lights_pos.shape,
                     light_colors=self.light_colors, nb_colors=self.light_colors.shape[0],
                     catmull=self.catmull, d_segt=1, **other_uniforms)


def main():
    viewer = Viewer()
    shader = Shader("shaders/texture.vert", "shaders/scene.frag")

    list_level = [[1, 3, 1, 1, 1],
                  [1, 0, 2, 0, 3],
                  [1, 0, 0, 0, 1],
                  [3, 0, 0, 0, 1],
                  [1, 2, 1, 0, 1],
                  [1, 1, 1, 3, 1]]
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
