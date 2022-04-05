solids = [ [1, 1, 1, 1, 1, 1, 1],
           [1, 0, 4, 1, 0, 0, 1],
           [1, 0, 4, 1, 4, 0, 1],
           [1, 0, 4, 1, 4, 0, 1],
           [1, 0, 7, 3, 5, 0, 1],
           [1, 1, 1, 1, 1, 1, 1] ]

entities = [ [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 1, 0],
             [0, 0, 0, 0, 0, 1, 0],
             [0, 0, 0, 0, 3, 0, 0],
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
        die()
        #animate dying
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
    return

def spiders_moving() :
    return

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
    while(True) :
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