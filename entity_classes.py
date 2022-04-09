from core import *

class Player(Node) :
    def __init__(self, pos, orientation = (1, 0)) :
        super().__init__()
        self.pos = pos
        self.orientation = orientation
        self.alive = True
    
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
        #animation avec translation de movement
    
    def rotate(self, movement) :
        if movement[0] == self.orientation[0] or movement[1] == self.orientation[1] :
            if movement[0] == self.orientation[0] and movement[1] == self.orientation[1] :
                #pas d'animation
                return
            else :
                #animation avec rotation de 180° dans le sens trigo
                return
        else :
            if movement[1] == self.orientation[0] and movement[0] == -self.orientation[1] :
                #animation avec rotation de 90° dans le sens trigo
                return
            else :
                #animation avec rotation de -90° dans le sens trigo
                return
        self.orientation = movement


class Spider(Node) :
    def __init__(self, pos, orientation = (1, 0)) :
        super().__init__()
        self.pos = pos
        self.orientation = orientation
    
    def move(self, movement) :
        self.rotate(movement)
        self.walk(movement)

    def attack(self) :
        #animate attacking
        return

    def walk(self, movement) :
        self.pos = (self.pos[0] + movement[0], self.pos[1] + movement[1])
        #animation avec translation de movement
    
    def rotate(self, movement) :
        if movement[0] == orientation[0] or movement[1] == orientation[1] :
            if movement[0] == orientation[0] and movement[1] == orientation[1] :
                #animation sans rotation
                return
            else :
                #animation avec rotation de 180° dans le sens trigo
                return
        else :
            if movement[1] == orientation[0] and movement[0] == -orientation[1] :
                #animation avec rotation de 90° dans le sens trigo
                return
            else :
                #animation avec rotation de -90° dans le sens trigo
                return
        self.orientation = movement


class Ore(Node) :
    super().__init__()
    def __init__(self, pos) :
        self.pos = pos
    
    def destroy(self) :
        #animation de destruction
        self.__del__()

    def __del__(self):
        return


class Barrel(Node) :
    super().__init__()
    def __init__(self, pos) :
        self.pos = pos
    
    def move(self, movement) :
        self.pos = (self.pos[0] + movement[0], self.pos[1] + movement[1])
        #animation avec translation de movement


class Minecart(Node) :
    super().__init__()
    def __init__(self, pos, rail = 3) :
        self.pos = pos
        # TODO : modifier l'initialisation de l'orientation
        self.rail = 3
    
    def move(self, movement, src_rail, dst_rail) :
        self.pos = (self.pos[0] + movement[0], self.pos[1] + movement[1])
        for rail in (src_rail, dst_rail) :
            if rail in (3, 4) :
                self.linear_roll(movement)
            else :
                self.rotative_roll(movement, rail)
                
    def linear_roll(self, movement) :
        #animation avec translation de movement/2
        return
    
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
        #animation avec rotation d'angle 45° dans le sens trigo si trigo_rotation est à True
        #autour de rotation_center
