from entity_classes import *

#solids = [ [1, 1, 1, 1, 1, 1, 1],
#           [1, 0, 4, 1, 0, 0, 1],
#           [1, 0, 4, 1, 4, 0, 1],
#           [1, 0, 4, 1, 4, 0, 1],
#           [1, 0, 7, 3, 5, 0, 1],
#           [1, 1, 1, 1, 1, 1, 1] ]

solids = [ [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
           [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
           [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
           [1, 1, 0, 0, 1, 1, 0, 0, 0, 1],
           [1, 3, 3, 0, 0, 0, 3, 3, 3, 1],
           [1, 0, 0, 0, 0, 1, 0, 1, 1, 1],
           [1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
           [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
           [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
           [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
           [1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] ]

entities = [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
             [0, 0, 3, 0, 0, 0, 0, 3, 0, 0],
             [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 1, 4, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ]
#entities = [ [0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 4, 1, 0],
#             [0, 0, 0, 0, 0, 1, 0],
#             [0, 0, 0, 0, 0, 0, 0],
#             [0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0] ]

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

character_pos = (7, 6)


def change_board(movement) :
    given_pos = position_after_move(player.pos, movement)
    if solid_on(given_pos) == 1 :
        return

    entity = entity_on(given_pos)
    if entity == 0 :
        player.move(movement)

    elif isinstance(entity, Ore) :
        change_entity(given_pos, 0)
        player.mine(movement)
        entity.destroy()

    elif isinstance(entity, Barrel) :
        target_pos = position_after_move(given_pos, movement)

        # check if the entity can be pushed
        if solid_on(target_pos) == 1 :
            return
        if entity_on(target_pos) != 0 and not isinstance(entity_on(target_pos), Spider) :
            return
        
        change_entity(target_pos, entity)
        change_entity(given_pos, 0)
        player.push(movement)
        entity.move(movement)

    elif isinstance(entity, Minecart) :
        target_pos = position_after_move(given_pos, movement)

        # check if the entity can be pushed
        if solid_on(target_pos) < 3 :
            return
        if entity_on(target_pos) != 0 and not isinstance(entity_on(target_pos), Spider) :
            return
        
        change_entity(target_pos, entity)
        change_entity(given_pos, 0)
        player.push(movement)
        entity.move(movement, solid_on(given_pos), solid_on(target_pos))

    elif isinstance(entity, Spider) :
        player.move(movement)
        entity.attack()
        player.die()
        return
    
    spiders_moving(movement)
    return


def position_after_move(pos, move) :
    return (pos[0] + move[0], pos[1] + move[1])

def solid_on(pos) :
    return solids[pos[0]][pos[1]]
    
def entity_on(pos) :
    return entities[pos[0]][pos[1]]

def change_entity(pos, value) :
    entities[pos[0]][pos[1]] = value





def spiders_moving(player_movement) :
    player_connexe = get_player_connexe()
    for spider in spiders :
        #the spider can track the player and go towards him
        if spider.pos in player_connexe :
            best_movement = find_best_movement(spider.pos, player_connexe, player_movement)
            given_pos = position_after_move(spider.pos, best_movement)
            change_entity(given_pos, spider)
            change_entity(spider.pos, 0)
            spider.move(best_movement)
            if spider.pos == player.pos :
                spider.attack()
                player.die()
        #the spider is pushed with a barrel or a minecart
        elif isinstance(entity_on(spider.pos), (Barrel, Minecart)):
            movement1 = player_movement
            movement2 = (-player_movement[1], player_movement[0])
            movement3 = (player_movement[1], -player_movement[0])
            for movement in (movement1, movement2, movement3) :
                pos = position_after_move(spider.pos, movement)
                if not (solid_on(pos) == 1 or isinstance(entity_on(pos), (Ore, Barrel, Minecart))) :
                    change_entity(pos, spider)
                    spider.move(movement)
                    return
            #the spider can't go anywhere, this poor creature is crushed :'(
            spiders.remove(spider)
            spider.die()

def get_player_connexe() :
    connexe = set()
    bboard = binary_board()
    find_connexe(bboard, connexe, player.pos)
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
            if solid_on((i,j)) == 1 or isinstance(entity_on((i,j)), (Ore, Barrel, Minecart)) :
                bline.append(1)
            else :
                bline.append(0)
        bboard.append(bline)
    return bboard

def find_best_movement(pos, connexe, player_movement) :
    #all the possible movements, in general
    movements = ((1, 0), (0, 1), (-1, 0), (0, -1))

    #all the possible movements for the spider
    possible_movements = {}
    for movement in movements :
        if position_after_move(pos, movement) in connexe :
            possible_movements[position_after_move(pos, movement)] = movement

    #if the spider is next to the player, go towards him
    if player.pos in possible_movements :
        return possible_movements[player.pos]

    #initialisation of all the visited and not-visited tiles
    visited = set()
    not_visited = set()
    for tile in connexe :
        not_visited.add(tile)
    visited.add(player.pos)
    not_visited.remove(player.pos)

    #find all the movements that allow the spider to move towards the player
    best_movements = []
    found = False
    while not found :
        temp = set()
        for tile in visited :
            for movement in movements :
                new_tile = position_after_move(tile, movement)
                if new_tile in not_visited :
                    if new_tile in possible_movements :
                        best_movements.append(possible_movements[new_tile])
                        found = True
                    not_visited.remove(new_tile)
                    temp.add(new_tile)
        visited = temp

    #if many movements are possible, prioritize the one that doesn't copy the player's movement
    for movement in best_movements :
        if movement != player_movement :
            return movement
    return player_movement


def print_board() :
    print("")
    for i in range(len(solids)) :
        line = ""
        for j in range(len(solids[0])) :
            if (i,j) == player.pos :
                line += "☺ "
            elif entity_on((i,j)) == 0 :
                if solids[i][j] == 0 :
                    line += "  "
                elif solids[i][j] == 1 :
                    line += "▓▓"
                elif solids[i][j] == 3 :
                    line += "══"
                elif solids[i][j] == 4 :
                    line += "║ "
                elif solids[i][j] == 5 :
                    line += "╝ "
                elif solids[i][j] == 6 :
                    line += "╗ "
                elif solids[i][j] == 7 :
                    line += "╚═"
                elif solids[i][j] == 8 :
                    line += "╔═"
            elif isinstance(entity_on((i,j)), Ore) :
                line += "▲ "
            elif isinstance(entity_on((i,j)), Barrel) :
                line += "o "
            elif isinstance(entity_on((i,j)), Minecart) :
                line += "◙ "
            elif isinstance(entity_on((i,j)), Spider) :
                line += "x "
        print(line)

def create_all_entities() :
    for i in range(len(entities)) :
        for j in range(len(entities[0])) :
            entity = entity_on((i,j))
            if entity != 0 :
                if entity == 1 :
                    change_entity((i,j), Ore((i,j)))
                if entity == 2 :
                    change_entity((i,j), Barrel((i,j)))
                if entity == 3 :
                    change_entity((i,j), Minecart((i,j)))
                if entity == 4 :
                    spider = Spider((i,j))
                    spiders.append(spider)
                    change_entity((i,j), spider)
                


player = Player(character_pos)
spiders = []

if __name__ == '__main__' :
    create_all_entities()
    while(player.alive) :
        print_board()
        while(True) :
            move_char = input()
            if move_char == 'z':
                movement = (-1, 0)
                break
            if move_char == 'q':
                movement = (0, -1)
                break
            if move_char == 's':
                movement = (1, 0)
                break
            if move_char == 'd':
                movement = (0, 1)
                break
        change_board(movement)
    print_board()
