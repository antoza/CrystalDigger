from core import *

IDLE = 0
MOVE = 1
ROTATE = 2

class Player(Node) :
    def __init__(self, pos, orientation = (1, 0)) :
        super().__init__()
        self.pos = pos
        self.orientation = orientation
        self.alive = True
        self.etat = IDLE
    
    def move(self, movement) :
        self.rotate(movement)
        self.walk(movement)

    def mine(self, movement) :
        self.rotate(movement)
        #animation minage
    
    def push(self, movement) :
        self.rotate(movement)
        #animation lever les bras
        self.walk(movement)
        #animation baisser les bras

    def die(self) :
        self.alive = False
        #animate dying

    def walk(self, movement) :
        self.pos = (self.pos[0] + movement[0], self.pos[1] + movement[1])
        #self.etat = (MOVE, movement)
        while self.etat != IDLE :
            pass
    
    def rotate(self, movement) :
        if movement[0] == self.orientation[0] or movement[1] == self.orientation[1] :
            if movement[0] == self.orientation[0] and movement[1] == self.orientation[1] :
                angle = 0
            else :
                angle = 180
                return
        else :
            if movement[1] == self.orientation[0] and movement[0] == -self.orientation[1] :
                angle = 90
                return
            else :
                angle = -90
                return
        self.orientation = movement
        #self.etat = (ROTATE, angle)
        while self.etat != IDLE :
            pass


class Spider(Node) :
    def __init__(self, pos, orientation = (1, 0)) :
        super().__init__()
        self.pos = pos
        self.orientation = orientation
        self.etat = IDLE
    
    def move(self, movement) :
        self.rotate(movement)
        self.walk(movement)

    def attack(self) :
        #animate attacking
        return
    
    def die(self) :
        #animer une flaque de sang ?
        self.__del__()

    def walk(self, movement) :
        self.pos = (self.pos[0] + movement[0], self.pos[1] + movement[1])
        #self.etat = (MOVE, movement)
        while self.etat != IDLE :
            pass
    
    def rotate(self, movement) :
        if movement[0] == self.orientation[0] or movement[1] == self.orientation[1] :
            if movement[0] == self.orientation[0] and movement[1] == self.orientation[1] :
                angle = 0
            else :
                angle = 180
                return
        else :
            if movement[1] == self.orientation[0] and movement[0] == -self.orientation[1] :
                angle = 90
                return
            else :
                angle = -90
                return
        self.orientation = movement
        #self.etat = (ROTATE, angle)
        while self.etat != IDLE :
            pass


class Ore(Node) :
    def __init__(self, pos) :
        super().__init__()
        self.pos = pos
        self.etat = IDLE
    
    def destroy(self) :
        #animation de destruction
        self.__del__()

    def __del__(self):
        return


class Barrel(Node) :
    def __init__(self, pos) :
        super().__init__()
        self.pos = pos
        self.etat = IDLE
    
    def move(self, movement) :
        self.pos = (self.pos[0] + movement[0], self.pos[1] + movement[1])
        #self.etat = (MOVE, movement)
        while self.etat != IDLE :
            pass


class Minecart(Node) :
    def __init__(self, pos, rail = 3) :
        super().__init__()
        self.pos = pos
        self.init_angle(rail)
        self.etat = IDLE
    
    def move(self, movement, src_rail, dst_rail) :
        self.pos = (self.pos[0] + movement[0], self.pos[1] + movement[1])
        for rail in (src_rail, dst_rail) :
            if rail in (3, 4) :
                self.linear_roll(movement)
            else :
                self.rotative_roll(movement, rail)
                
    def linear_roll(self, movement) :
        #self.etat = (MOVE, (movement[0]/2, movement[1]/2))
        while self.etat != IDLE :
            pass
    
    def rotative_roll(self, movement, rail) :
        if movement[0] == -1 :
            trigo_rotation = rail in (5, 6)
        if movement[0] == 1 :
            trigo_rotation = rail in (7, 8)
        if movement[1] == -1 :
            trigo_rotation = rail in (6, 8)
        if movement[1] == 1 :
            trigo_rotation = rail in (5, 7)
        
        rotation_center = ((rail-5)%2-1/2, (rail-5)//2-1/2)
        if trigo_rotation :
            angle = 45
        else :
            angle = -45 

        #self.etat = (ROTATE, angle, rotation_center)
        while self.etat != IDLE :
            pass
    
    def init_angle(self, rail) :
        if rail == 3 :
            return
        elif rail == 4 :
            #rotate de 90°
        elif rail in (5, 6) :
            linear_roll((-1, 0))
            rotative_roll((1, 0), rail)
        else :
            linear_roll((1, 0))
            rotative_roll((-1, 0), rail)
