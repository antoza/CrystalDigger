solids = [ [1, 1, 1, 1, 1, 1, 1],
           [1, 0, 4, 1, 0, 0, 1],
           [1, 0, 4, 1, 4, 0, 1],
           [1, 0, 4, 1, 4, 0, 1],
           [1, 0, 7, 3, 5, 0, 1],
           [1, 1, 1, 1, 1, 1, 1] ]

entities = [ [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 1, 0],
             [0, 0, 0, 0, 0, 1, 0],
             [0, 0, 0, 0, 3, 4, 0],
             [0, 1, 2, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0] ]

# Values meaning :

# value : solid
# 0 : void
# 1 : wall
# 3 : rails ═
# 4 : rails ║
# 5 : rails ╝
# 6 : rails ╗
# 7 : rails ╚
# 8 : rails ╔

# value : entity
# 0 : nothing
# 1 : gold ore
# 2 : barrel
# 3 : minecart
# 4 : spider

character_pos = (1, 1)

alive = True

def change_board(move) :
    global character_pos
    given_pos = position_after_move(character_pos, move)
    if solid_on(given_pos) == 1 :
        return
    entity = entity_on(given_pos)
    if entity == 0 :
        character_pos = given_pos
        #animate character moving
    elif entity == 1 :
        mine(given_pos)
        #animate mining
    elif entity == 2 or entity == 3 :
        if not push(given_pos, move, entity) :
            return
        character_pos = given_pos
        #animate pushing
    elif entity == 4 :
        character_pos = given_pos
        die()
    spiders_moving()
    return

def position_after_move(pos, move) :
    return (pos[0] + move[0], pos[1] + move[1])

def solid_on(pos) :
    return solids[pos[0]][pos[1]]
    
def entity_on(pos) :
    return entities[pos[0]][pos[1]]

def change_entity(pos, value) :
    entities[pos[0]][pos[1]] = value

def mine(pos) :
    change_entity(pos, 0)

def push(pos, move, entity) :
    given_object_pos = position_after_move(pos, move)

    # check if the entity can be pushed
    if entity == 3 and solid_on(given_object_pos) < 3 :
        return False
    elif entity == 2 and solid_on(given_object_pos) == 1 :
        return False
    if entity_on(given_object_pos) not in (0, 4) :
        return False
    
    change_entity(given_object_pos, entity)
    change_entity(pos, 0)
    return True

def die() :
    global alive
    alive = False
    #animate dying
    return





def spiders_moving() :
    spiders = get_spiders()
    player_connexe = get_player_connexe()
    for spider in spiders :
        if spider in player_connexe :
            new_spider = best_movement(spider)


def get_spiders() :
    spiders = []
    for i in range(len(entities)) :
        for j in range(len(entities[0])) :
            if entity_on((i,j)) == 4 :
                spiders.append((i,j))
    return spiders

def get_player_connexe() :
    connexe = set()
    bboard = binary_board()
    find_connexe(bboard, connexe, character_pos)
    return connexe

def find_connexe(bboard, connexe, pos) :
    i, j = pos
    if bboard[i][j] == 0 :
        connexe.add(pos)
        bboard[i][j] = 1
        for neighbors in ((i-1, j), (i+1, j), (i, j-1), (i, j+1)) :
            find_connexe(bboard, connexe, neighbors)

def binary_board() :
    bboard = []
    for i in range(len(solids)) :
        bline = []
        for j in range(len(solids[0])) :
            if solids[i][j] == 1 or entities[i][j] in (1, 2, 3) :
                bline.append(1)
            else :
                bline.append(0)
        bboard.append(bline)
    return bboard

def find_best_movement(pos) :


class Player :
    def __init__(self, pos, orientation = (1, 0)) :
        self.pos = pos
        self.orientation = orientation
    
    def move(movement) :
        self.rotate(movement)
        self.walk(movement)

    def mine(movement) :
        self.rotate(movement)
        #animation minage
    
    def push(movement) :
        self.rotate(movement)
        #animation lever les bras
        self.walk(movement)
        #animation baisser les bras

    def die() :
        #animate dying

    def walk(movement) :
        self.pos[0] += movement[0]
        self.pos[1] += movement[1]
        #animation avec translation de movement
    
    def rotate(movement) :
        if movement[0] == orientation[0] or movement[1] == orientation[1] :
            if movement[0] == orientation[0] and movement[1] == orientation[1] :
                #animation sans rotation
            else :
                #animation avec rotation de 180° dans le sens trigo
        else :
            if movement[1] == orientation[0] and movement[0] == -orientation[1] :
                #animation avec rotation de 90° dans le sens trigo
            else :
                #animation avec rotation de -90° dans le sens trigo
        self.orientation = movement


class Spider :
    def __init__(self, pos, orientation = (1, 0)) :
        self.pos = pos
        self.orientation = orientation
    
    def move(movement) :
        self.rotate(movement)
        self.walk(movement)

    def attack() :
        #animate attacking

    def walk(movement) :
        self.pos[0] += movement[0]
        self.pos[1] += movement[1]
        #animation avec translation de movement
    
    def rotate(movement) :
        if movement[0] == orientation[0] or movement[1] == orientation[1] :
            if movement[0] == orientation[0] and movement[1] == orientation[1] :
                #animation sans rotation
            else :
                #animation avec rotation de 180° dans le sens trigo
        else :
            if movement[1] == orientation[0] and movement[0] == -orientation[1] :
                #animation avec rotation de 90° dans le sens trigo
            else :
                #animation avec rotation de -90° dans le sens trigo
        self.orientation = movement


class Barrel :
    def __init__(self, pos) :
        self.pos = pos
    
    def move(movement, src_rail, dst_rail) :
        self.pos[0] += movement[0]
        self.pos[1] += movement[1]
        #animation avec translation de movement


class Minecart :
    def __init__(self, pos, rail = 3) :
        self.pos = pos
        # TODO : modifier l'initialisation de l'orientation
        self.rail = 3
    
    def move(movement, src_rail, dst_rail) :
        self.pos[0] += movement[0]
        self.pos[1] += movement[1]
        for rail in (src_rail, dst_rail) :
            if rail in (3, 4) :
                self.linear_roll(movement)
            else :
                self.rotative_roll(movement, rail)
                
    def linear_roll(movement) :
        #animation avec translation de movement/2
    
    def rotative_roll(movement, rail) :
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

def print_board() :
    print("")
    for i in range(len(solids)) :
        line = ""
        for j in range(len(solids[0])) :
            if (i,j) == character_pos :
                line += "☺"
            elif entities[i][j] == 0 :
                if solids[i][j] == 0 :
                    line += " "
                elif solids[i][j] == 1 :
                    line += "▓"
                elif solids[i][j] == 3 :
                    line += "═"
                elif solids[i][j] == 4 :
                    line += "║"
                elif solids[i][j] == 5 :
                    line += "╝"
                elif solids[i][j] == 6 :
                    line += "╗"
                elif solids[i][j] == 7 :
                    line += "╚"
                elif solids[i][j] == 8 :
                    line += "╔"
            elif entities[i][j] == 1 :
                line += "▲"
            elif entities[i][j] == 2 :
                line += "o"
            elif entities[i][j] == 3 :
                line += "◙"
            elif entities[i][j] == 4 :
                line += "x"
        print(line)

if __name__ == '__main__' :
    while(alive) :
        print_board()
        while(True) :
            move_char = input()
            if move_char == 'z':
                move = (-1, 0)
                break
            if move_char == 'q':
                move = (0, -1)
                break
            if move_char == 's':
                move = (1, 0)
                break
            if move_char == 'd':
                move = (0, 1)
                break
        change_board(move)
    print_board()