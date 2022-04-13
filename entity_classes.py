#!/usr/bin/env python3


import glfw
import numpy as np

from core import Node, Shader, Viewer, load
from transform import translate, rotate, scale, identity
from scene import Scene

IDLE = 0
WALK = 1
ROTATE = 2
ATTACK = 3


class Creature(Node):
    def __init__(self, shader, ways=[], pos=(0, 0), transform=identity(), base_transform=identity(), orientation=(1, 0),
                 listState={}):
        super().__init__(transform=translate(pos[1], -pos[0], 0) @ transform @ base_transform)
        self.old_transform = translate(pos[1], -pos[0], 0) @ transform
        self.base_transform = base_transform
        self.pos = pos
        self.orientation = orientation
        self.states = [IDLE]
        self.listState = listState
        # Load all animation and display idle
        for way in ways:
            child = Node()
            child.add(*load(way, shader))
            child.display(False)
            self.add(child)
        self.children[self.listState[IDLE]].display(True)

        # parameter for rotation and movement
        self.iterator = 0
        self.movement = (0, 0)
        self.angle = 0
        self.max_walk = 10
        self.max_rotate = 10
        self.max_attack = 15

    def draw(self, model=identity(), **other_uniforms):
        if self.iterator == 0:
            glfw.set_time(0.0)
        if self.states[-1] == WALK:
            self.walk_iterator()
        elif self.states[-1] == ROTATE:
            self.rotate_iterator()
        elif self.states[-1] == ATTACK:
            self.attack_iterator()

        super().draw(model=model, **other_uniforms)

    def walk_iterator(self):
        if self.iterator < self.max_walk:
            self.old_transform = translate(self.movement[1] / self.max_walk, -self.movement[0] / self.max_walk,
                                           0) @ self.old_transform
            self.transform = self.old_transform @ self.base_transform
            self.iterator += 1
            return

        self.update_state()
        self.iterator = 0

    def rotate_iterator(self):
        max_rotate = self.max_rotate
        if self.angle == 180:
            max_rotate = 2 * max_rotate

        if self.iterator < max_rotate:
            self.old_transform = self.old_transform @ rotate(axis=(0., 0., 1.), angle=self.angle / max_rotate)
            self.transform = self.old_transform @ self.base_transform
            self.iterator += 1
            return

        self.update_state()
        self.iterator = 0

    def attack_iterator(self):
        if self.iterator < self.max_attack:
            self.iterator += 1
            return

        self.update_state()
        self.iterator = 0

    def update_state(self, new_state=None):
        self.children[self.listState[self.states[-1]]].display(False)
        if new_state is None:
            self.states.pop()
        else:
            self.states.append(new_state)
        self.children[self.listState[self.states[-1]]].display(True)

    def move(self, movement):
        self.walk(movement)
        self.rotate(movement)

    def attack(self):
        self.update_state(ATTACK)

    def walk(self, movement):
        self.pos = (self.pos[0] + movement[0], self.pos[1] + movement[1])
        self.movement = movement
        self.update_state(WALK)

    def rotate(self, movement):
        if movement[0] == self.orientation[0] or movement[1] == self.orientation[1]:
            if movement[0] == self.orientation[0] and movement[1] == self.orientation[1]:
                self.angle = 0
            else:
                self.angle = 180
        else:
            if movement[1] == self.orientation[0] and movement[0] == -self.orientation[1]:
                self.angle = 90
            else:
                self.angle = -90
        self.orientation = movement
        self.update_state(ROTATE)


class Player(Creature):
    def __init__(self, pos=(0, 0), transform=identity()):
        shader = Shader("shaders/animatedAndTextured.vert", "shaders/animatedAndTextured.frag")
        ways = ["src/Knight/Knight_Idle.fbx", "src/Knight/Knight_run.fbx", "src/Knight/Knight_attack_2.fbx"]
        transform_knight = rotate(axis=(1., 0., 0.), angle=90) @ scale(0.003, 0.002, 0.003)
        listState = {IDLE: 0, WALK: 1, ROTATE: 1, ATTACK: 2}
        super().__init__(shader=shader, ways=ways, pos=pos, transform=transform, base_transform=transform_knight,
                         listState=listState)

    def key_handler(self, key):
        """ Dispatch keyboard events to children with key handler """
        if key == glfw.KEY_UP:
            self.move((-1, 0))
        if key == glfw.KEY_DOWN:
            self.move((1, 0))
        if key == glfw.KEY_LEFT:
            self.attack()
        if key == glfw.KEY_RIGHT:
            self.move((0, 1))


class Spider(Creature):
    def __init__(self, pos=(0, 0), transform=identity()):
        shader = Shader("shaders/animatedAndTextured.vert", "shaders/animatedAndTextured.frag")
        ways = ["src/Spider/Spider_Idle.fbx", "src/Spider/Spider_run.fbx", "src/Spider/Spider_attack_1.fbx"]
        transform_spider = rotate(axis=(1., 0., 0.), angle=90) @ scale(0.008, 0.008, 0.008)
        listState = {IDLE: 0, WALK: 1, ROTATE: 1, ATTACK: 2}
        super().__init__(shader=shader, ways=ways, pos=pos, transform=transform, base_transform=transform_spider,
                         listState=listState)

    def key_handler(self, key):
        """ Dispatch keyboard events to children with key handler """
        if key == glfw.KEY_UP:
            self.move((-1, 0))
        if key == glfw.KEY_DOWN:
            self.move((1, 0))
        if key == glfw.KEY_LEFT:
            self.move((0, -1))
        if key == glfw.KEY_RIGHT:
            self.move((0, 1))


class Ore(Node):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.etat = IDLE

    def destroy(self):
        # animation de destruction
        self.__del__()

    def __del__(self):
        return


class Barrel(Node):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.etat = IDLE

    def move(self, movement):
        self.pos = (self.pos[0] + movement[0], self.pos[1] + movement[1])
        # self.etat = (MOVE, movement)
        while self.etat != IDLE:
            pass


class Minecart(Node):
    def __init__(self, pos, rail=3):
        super().__init__()
        self.pos = pos
        self.init_angle(rail)
        self.etat = IDLE

    def move(self, movement, src_rail, dst_rail):
        self.pos = (self.pos[0] + movement[0], self.pos[1] + movement[1])
        for rail in (src_rail, dst_rail):
            if rail in (3, 4):
                self.linear_roll(movement)
            else:
                self.rotative_roll(movement, rail)

    def linear_roll(self, movement):
        # self.etat = (MOVE, (movement[0]/2, movement[1]/2))
        while self.etat != IDLE:
            pass

    def rotative_roll(self, movement, rail):
        if movement[0] == -1:
            trigo_rotation = rail in (5, 6)
        if movement[0] == 1:
            trigo_rotation = rail in (7, 8)
        if movement[1] == -1:
            trigo_rotation = rail in (6, 8)
        if movement[1] == 1:
            trigo_rotation = rail in (5, 7)

        rotation_center = ((rail - 5) % 2 - 1 / 2, (rail - 5) // 2 - 1 / 2)
        if trigo_rotation:
            angle = 45
        else:
            angle = -45

        # self.etat = (ROTATE, angle, rotation_center)
        while self.etat != IDLE:
            pass

    def init_angle(self, rail):
        if rail == 3:
            return
        elif rail == 4:
            return
            # rotate de 90°
        elif rail in (5, 6):
            self.linear_roll((-1, 0))
            self.rotative_roll((1, 0), rail)
        else:
            self.linear_roll((1, 0))
            self.rotative_roll((-1, 0), rail)


def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    viewer.trackball.zoom(-20, glfw.get_window_size(viewer.win)[1])
    shader = Shader("shaders/texture.vert", "shaders/scene.frag")
    list_level = [[0, 3, 1, 1, 1],
                  [0, 2, 0, 2, 3],
                  [0, 0, 1, 0, 1],
                  [3, 2, 0, 2, 1],
                  [1, 2, 2, 2, 1],
                  [1, 1, 1, 3, 1]]
    level = np.array(list_level)
    x, y = level.shape
    scene = Scene(level=level, transform=translate(y / 2, -x / 2, 0))

    player = Player(pos=(1, 0), transform=translate(0.5 - x / 2, 0.5 - y / 2, 0.1))
    spider = Spider(pos=(0, 0), transform=translate(0.5 - x / 2, 0.5 - y / 2, 0.1))

    scene.add(spider)
    scene.add(player)
    viewer.add(scene)
    viewer.run()


if __name__ == '__main__':
    main()
