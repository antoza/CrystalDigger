#!/usr/bin/env python3

import glfw
import numpy as np

from core import Node, Shader, Viewer, load
from transform import translate, rotate, scale, identity
from scene import Scene
from minecart import MinecartObj

IDLE = 0
WALK = 1
ROTATE = 2
ATTACK = 3


class Creature(Node):
    def __init__(self, shader, ways=[], pos=(0, 0), transform=identity(),
                 base_transform=identity(), orientation=(1, 0), listState={}):
        super().__init__(transform=translate(pos[1] + .5, -pos[0] - .5, .1)
                         @ transform @ base_transform)
        self.old_transform = translate(pos[1] + .5, -pos[0] - .5, 0) @ transform
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

    def mine(self, movement):
        self.attack()
        self.rotate(movement)

    def push(self, movement):
        self.move(movement)

    def die(self):
        ...


class Spider(Creature):
    def __init__(self, pos=(0, 0), transform=identity()):
        shader = Shader("shaders/animatedAndTextured.vert", "shaders/animatedAndTextured.frag")
        ways = ["src/Spider/Spider_Idle.fbx", "src/Spider/Spider_run.fbx", "src/Spider/Spider_attack_1.fbx"]
        transform_spider = rotate(axis=(1., 0., 0.), angle=90) @ scale(0.008, 0.008, 0.008)
        listState = {IDLE: 0, WALK: 1, ROTATE: 1, ATTACK: 2}
        super().__init__(shader=shader, ways=ways, pos=pos, transform=transform, base_transform=transform_spider,
                         listState=listState)



class Ore(Node):
    def __init__(self, pos=(0, 0), transform=identity()):
        shader = Shader("shaders/textured.vert", "shaders/textured.frag")
        self.base_transform = translate(0, 0, .5) @ rotate((1,0,0),90) @ scale(.1, .1, .1)
        self.pos = pos
        super().__init__(transform=translate(pos[1]+.5, -pos[0]-.5, 0) @ transform @ self.base_transform)
        self.states = [IDLE]
        self.add(*load(file="src/crystal/Crystals.obj", tex_file="src/crystal/Tex1.png", shader=shader, light_dir=(0,0,1)))
        self.destroyed = False
        self.max_wait = 10
        self.iterator = 0

    def destroy(self):
        self.destroyed = True

    def draw(self, model, **other_uniforms):
        if self.destroyed:
            self.iterator += 1
        if self.iterator == self.max_wait:
            self.display(False)
        super().draw(model=model, **other_uniforms)

class Barrel(Node):
    def __init__(self, pos):
        super().__init__(transform=translate(pos[1] + .5, -pos[0] - .5, .2) @ rotate((0, 0, 1), 90))
        self.pos = pos
        self.old_pos = pos
        self.states = [IDLE]

        self.iterator = 0
        self.movement = (0, 0)

        self.max_walk = 10
        self.max_wait = 10

        shader = Shader("shaders/barrel.vert", "shaders/barrel.frag")
        self.add(*load(file="src/cube/cube.obj", tex_file="src/cube/cube.png", shader=shader))

    def move(self, movement):
        self.old_pos = self.pos
        self.pos = (self.pos[0] + movement[0], self.pos[1] + movement[1])
        self.movement = movement
        self.update_state(WALK)

    def draw(self, model=identity(), **other_uniforms):
        if self.iterator == 0:
            glfw.set_time(0.0)
        if self.states[-1] == WALK:
            self.walk_iterator()

        super().draw(model=model, **other_uniforms)

    def walk_iterator(self):
        if self.iterator < self.max_wait:
            self.iterator += 1
            return
        if self.iterator < self.max_wait + self.max_walk:
            self.transform = translate(self.movement[1] / self.max_walk, -self.movement[0] / self.max_walk,
                                           0) @ self.transform
            self.iterator += 1
            return

        self.update_state()
        self.iterator = 0

    def update_state(self, new_state=None):
        if new_state is None:
            self.states.pop()
        else:
            self.states.append(new_state)


class Minecart(Node):
    def __init__(self, pos, rail=4):
        super().__init__(transform=translate(pos[1], -pos[0]+rail-5, .2) @ rotate((0, 0, 1), 90*(4-rail)))
        self.pos = pos
        self.old_pos = pos
        self.states = [IDLE]

        self.iterator = 0
        self.movement = (0, 0)
        self.angle = []
        self.rotation_center = []

        self.max_wait = 10
        self.max_walk = 5
        self.max_rotate = 5

        shader = Shader("shaders/texture.vert", "shaders/texture.frag")
        self.add(MinecartObj(shader))

    def move(self, movement, src_rail, dst_rail):
        self.old_pos = self.pos
        self.pos = (self.pos[0] + movement[0], self.pos[1] + movement[1])
        for rail in (dst_rail, src_rail):
            if rail in (4, 5):
                self.linear_roll(movement)
            else:
                self.rotative_roll(movement, rail, rail == dst_rail)

    def linear_roll(self, movement):
        self.movement = movement
        self.update_state(WALK)


    def rotative_roll(self, movement, rail, is_dst):
        if movement[0] == -1:
            trigo_rotation = rail in (6, 7)
        if movement[0] == 1:
            trigo_rotation = rail in (8, 9)
        if movement[1] == -1:
            trigo_rotation = rail in (7, 9)
        if movement[1] == 1:
            trigo_rotation = rail in (6, 8)

        if trigo_rotation:
            self.angle.append(45)
        else:
            self.angle.append(-45)

        if is_dst:
            rotation_center = (self.pos[0] + (rail - 6) % 2, self.pos[1] + (rail - 6) // 2)
        else:
            rotation_center = (self.old_pos[0] + (rail - 6) % 2, self.old_pos[1] + (rail - 6) // 2)
        self.rotation_center.append(rotation_center)

        self.update_state(ROTATE)

    def draw(self, model=identity(), **other_uniforms):
        if self.iterator == 0:
            glfw.set_time(0.0)
        if self.states[-1] == WALK:
            self.walk_iterator()
        elif self.states[-1] == ROTATE:
            self.rotate_iterator()

        super().draw(model=model, **other_uniforms)

    def walk_iterator(self):
        if self.iterator < self.max_wait * (len(self.states)-2):
            self.iterator += 1
            return
        if self.iterator < self.max_wait * (len(self.states)-2) + self.max_walk:
            self.transform = translate(self.movement[1] / self.max_walk / 2, -self.movement[0] / self.max_walk / 2,
                                           0) @ self.transform
            self.iterator += 1
            return

        self.update_state()
        self.iterator = 0

    def rotate_iterator(self):
        if self.iterator < self.max_wait * (len(self.states)-2):
            self.iterator += 1
            return
        if self.iterator < self.max_wait * (len(self.states)-2) + self.max_rotate:
            angle = self.angle[-1]
            rotation_center = self.rotation_center[-1]
            self.transform = translate(rotation_center[1], -rotation_center[0], 0) @ rotate(axis=(0., 0., 1.), angle=angle / self.max_rotate) @ translate(-rotation_center[1], rotation_center[0], 0) @ self.transform
            self.iterator += 1
            return

        self.angle.pop()
        self.rotation_center.pop()
        self.update_state()
        self.iterator = 0

    def update_state(self, new_state=None):
        if new_state is None:
            self.states.pop()
        else:
            self.states.append(new_state)


def test():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    viewer.trackball.zoom(-50, glfw.get_window_size(viewer.win)[1])
    list_level = [[0, 3, 1, 1, 1],
                  [0, 2, 0, 2, 3],
                  [0, 0, 1, 0, 1],
                  [3, 2, 0, 2, 1],
                  [1, 2, 2, 2, 1],
                  [1, 1, 1, 3, 1]]
    level = np.array(list_level)
    x, y = level.shape
    scene = Scene(level=level, transform=translate(-y / 2, x / 2, 0))

    player = Player(pos=(4, 0), transform=translate(x / 2, y / 2, 0))
    spider = Spider(pos=(5, 0), transform=translate(x / 2, y / 2, 0))
    ore = Ore(pos=(6, 0), transform=translate(x / 2, y / 2, 0))

    scene.add(spider)
    scene.add(player)
    scene.add(ore)
    viewer.add(scene)
    viewer.run()


if __name__ == '__main__':
    test()
