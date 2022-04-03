map = [ [1, 1, 1, 1, 1, 1, 1],
        [1, 2, 0, 1, 3, 3, 1],
        [1, 0, 0, 1, 0, 3, 1],
        [1, 0, 0, 3, 0, 0, 1],
        [1, 3, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1] ]

character_pos = (1, 1)

def change_map(move) :
    global character_pos
    given_pos = (character_pos[0] + move[0], character_pos[1] + move[1])
    element = element_on(given_pos)
    if element == 0 :
        swap(character_pos, given_pos)
        character_pos = given_pos
        #animate character moving
    elif element == 1 :
        return
    elif element == 3 :
        mine(given_pos)
    return

def element_on(pos) :
    return map[pos[0]][pos[1]]

def change_element(pos, value) :
    map[pos[0]][pos[1]] = value

def swap(pos1, pos2) :
    temp = element_on(pos2)
    change_element(pos2, element_on(pos1))
    change_element(pos1, temp)

def mine(pos) :
    change_element(pos, 0)
    #animate mining

def print_map() :
    print("")
    for line in map :
        print(line)

if __name__ == '__main__' :
    while(True) :
        print_map()
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
        change_map(move)