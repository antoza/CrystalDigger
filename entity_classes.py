#!/usr/bin/env python3
from core import *
from transform import *
from scene import Scene

IDLE = 0
WALK = 1
ROTATE = 2
ATTACK = 3
transform_spider = rotate(axis=(1., 0., 0.), angle=45) @ scale(0.008, 0.008, 0.008)

class Player(Node):
    def __init__(self, pos, orientation = (1, 0)):
        super().__init__()
        self.pos = pos
        self.orientation = orientation
        self.alive = True
        self.state = IDLE

    def move(self, movement):
        self.rotate(movement)
        self.walk(movement)

    def mine(self, movement):
        self.rotate(movement)
        #animation minage

    def push(self, movement):
        self.rotate(movement)
        #animation lever les bras
        self.walk(movement)
        #animation baisser les bras

    def die(self):
        self.alive = False
        #animate dying

    def walk(self, movement):
        self.pos = (self.pos[0] + movement[0], self.pos[1] + movement[1])
        #self.etat = (MOVE, movement)
        while self.etat != IDLE:
            pass

    def rotate(self, movement):
        if movement[0] == self.orientation[0] or movement[1] == self.orientation[1]:
            if movement[0] == self.orientation[0] and movement[1] == self.orientation[1]:
                angle = 0
            else:
                angle = 180
                return
        else:
            if movement[1] == self.orientation[0] and movement[0] == -self.orientation[1]:
                angle = 90
                return
            else:
                angle = -90
                return
        self.orientation = movement
        #self.etat = (ROTATE, angle)
        while self.etat != IDLE:
            pass


class Spider(Node):
    def __init__(self, shader, light_dir=None, pos=(0, 0), transform=identity(), orientation=(1, 0)):
        super().__init__(transform=translate(pos[1], pos[0], 0) @ transform @ transform_spider)
        self.old_transform = translate(pos[1], pos[0], 0) @ transform
        self.pos = pos
        self.orientation = orientation
        self.states = [IDLE]
        self.listState = {IDLE: 0, WALK: 1, ROTATE: 1, ATTACK: 2}
        for way in ["Spider/Spider_Idle.fbx", "Spider/Spider_run.fbx", "Spider/Spider_attack_1.fbx"]:
            child = Node()
            child.add(*load(way, shader, light_dir=light_dir))
            child.display = False
            self.add(child)
        self.children[self.listState[IDLE]].display = True
        self.iterator = 0
        self.max_walk = 6
        self.max_rotate = 5
        self.movement = (0, 0)
        self.angle = 0


    def draw(self, model=identity(), **other_uniforms):
        if(self.states[0] == WALK):
            self.walk_iterator()
        elif(self.states[0] == ROTATE):
            self.rotate_iterator()
        
        super().draw(model=model, **other_uniforms)

    def walk_iterator(self):
        if self.iterator == 0:
            glfw.set_time(0.0)
        if self.iterator < self.max_walk:
            self.old_transform = translate(self.movement[1]/self.max_walk, -self.movement[0]/self.max_walk, 0) @ self.old_transform
            self.transform = self.old_transform @ transform_spider
            self.iterator += 1
        else:
            self.pop_state()
            self.iterator = 0

    def rotate_iterator(self):
        if self.iterator == 0:
            glfw.set_time(0.0)
        if self.iterator < self.max_rotate:
            self.old_transform = self.old_transform @ rotate(axis=(0., 0., 1.), angle=self.angle/self.max_rotate)
            self.transform = self.old_transform @ transform_spider
            self.iterator += 1
        else:
            self.pop_state()
            self.iterator = 0

    def update_state(self, new_state):
        self.children[self.listState[self.states[0]]].display = False
        self.states.insert(0, new_state)
        self.children[self.listState[self.states[0]]].display = True

    def pop_state(self):
        #self.children[self.listState[self.states[0]]].display = False
        self.states.pop(0)
        #self.children[self.listState[self.states[0]]].display = True
        glfw.set_time(0.0)

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
        if self.angle != 0:
            self.update_state(ROTATE)

    def key_handler(self, key):
        """ Dispatch keyboard events to children with key handler """
        if self.states[0] == IDLE:
            if key == glfw.KEY_UP:
                self.move((-1, 0))
                #glfw.set_time(0.0)
            if key == glfw.KEY_DOWN:
                self.move((1, 0))
                #glfw.set_time(0.0)
            if key == glfw.KEY_LEFT:
                self.move((0, -1))
                #glfw.set_time(0.0)
            if key == glfw.KEY_RIGHT:
                self.move((0, 1))
                #glfw.set_time(0.0)
        


class Ore(Node):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.etat = IDLE

    def destroy(self):
        #animation de destruction
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
        #self.etat = (MOVE, movement)
        while self.etat != IDLE:
            pass


class Minecart(Node):
    def __init__(self, pos, rail = 3):
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
        #self.etat = (MOVE, (movement[0]/2, movement[1]/2))
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

        rotation_center = ((rail-5)%2-1/2, (rail-5)//2-1/2)
        if trigo_rotation:
            angle = 45
        else:
            angle = -45

        #self.etat = (ROTATE, angle, rotation_center)
        while self.etat != IDLE:
            pass

    def init_angle(self, rail):
        if rail == 3:
            return
        elif rail == 4:
            return
            #rotate de 90°
        elif rail in (5, 6):
            self.linear_roll((-1, 0))
            self.rotative_roll((1, 0), rail)
        else:
            self.linear_roll((1, 0))
            self.rotative_roll((-1, 0), rail)


def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader = Shader("shaders/texture.vert", "shaders/scene.frag")
    spider_shader = Shader("shaders/animatedAndTextured.vert", "shaders/animatedAndTextured.frag")
    list_level = [[1, 3, 1, 1, 1],
                  [1, 0, 0, 2, 3],
                  [1, 0, 1, 0, 1],
                  [3, 0, 2, 0, 1],
                  [1, 0, 2, 0, 1],
                  [1, 1, 1, 3, 1]]
    level = np.array(list_level)
    x, y = level.shape
    scene = Scene(shader=shader, level=level, transform=translate(-x / 2, -y / 2, 0))

    spider = Spider(shader=spider_shader, transform=translate(.5, .5, 0))
    scene.add(spider)

    viewer.add(scene)
    viewer.run()


if __name__ == '__main__':
    main()
