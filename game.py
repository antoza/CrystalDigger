from entity_classes import *
from core import *

#solids = [ [1, 1, 1, 1, 1, 1, 1],
#           [1, 0, 4, 1, 0, 0, 1],
#           [1, 0, 4, 1, 4, 0, 1],
#           [1, 0, 4, 1, 4, 0, 1],
#           [1, 0, 7, 3, 5, 0, 1],
#           [1, 1, 1, 1, 1, 1, 1] ]
"""
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
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ]"""
#entities = [ [0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 4, 1, 0],
#             [0, 0, 0, 0, 0, 1, 0],
#             [0, 0, 0, 0, 0, 0, 0],
#             [0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0] ]

solids = [[1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 2, 0, 1],
            [1, 0, 9, 4, 4, 5, 1],
            [1, 0, 8, 7, 8, 5, 1],
            [1, 0, 0, 8, 4, 6, 1],
            [1, 0, 0, 1, 2, 0, 3],
            [1, 1, 1, 1, 1, 1, 1]]

entities = [[0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]]

"""
111111
100201
194401
151001
101001
101203
111111

000000
000000
000300
000100
...
"""

character_pos = (2, 5)
# Values meaning:

# value: solid
# 0: void
# 1: wall
# 2: torch
# 3: door
# 4: rails ═
# 5: rails ║
# 6: rails ╝
# 7: rails ╗
# 8: rails ╚
# 9: rails ╔

# value: entity
# 0: nothing
# 1: gold ore
# 2: barrel
# 3: minecart
# 4: spider

#character_pos = (7, 6)

class Game(Viewer):
    def __init__(self, solids, entities, character_pos):
        super().__init__()
        self.temporary_shader = Shader("shaders/animatedAndTextured.vert", "shaders/animatedAndTextured.frag")
        self.solids = solids
        self.shader = Shader("shaders/texture.vert", "shaders/scene.frag")
        level = np.array(solids)
        x,y = level.shape
        self.scene = Scene(level=level, transform=translate(-y / 2, x / 2, 0))
        self.add(self.scene)

        self.entities = entities
        self.player = Player(character_pos)
        self.scene.add(self.player)
        self.ores = 0
        self.spiders = []
        self.create_all_entities()
        self.waiting = True
        self.iterator = 0
        self.game_over = False
        self.trackball.zoom(-50, glfw.get_window_size(self.win)[1])

    def run(self):
        """ Main render loop for this OpenGL window """
        while not glfw.window_should_close(self.win):
            if not self.waiting:
                if self.iterator < 3:#0:
                    self.iterator += 1
                else:
                    self.iterator = 0
                    self.waiting = True
            # clear draw buffer and depth buffer (<-TP2)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            win_size = glfw.get_window_size(self.win)

            # draw our scene objects
            cam_pos = np.linalg.inv(self.trackball.view_matrix())[:, 3]
            self.draw(view=self.trackball.view_matrix(),
                      projection=self.trackball.projection_matrix(win_size),
                      model=identity(),
                      w_camera_position=cam_pos)

            # flush render commands, and swap draw buffers
            glfw.swap_buffers(self.win)

            # Poll for and process events
            glfw.poll_events()


    def change_board(self, movement):
        given_pos = self.position_after_move(self.player.pos, movement)
        if self.solid_on(given_pos) == 1:
            return
        if self.solid_on(given_pos) == 3 and self.ores > 0:
            return

        entity = self.entity_on(given_pos)
        if entity == 0:
            self.player.move(movement)
            if self.solid_on(given_pos) == 3 and self.ores == 0:
                self.game_over = True

        elif isinstance(entity, Ore):
            self.change_entity(given_pos, 0)
            self.player.mine(movement)
            entity.destroy()
            self.ores -= 1

        elif isinstance(entity, Barrel):
            target_pos = self.position_after_move(given_pos, movement)

            # check if the entity can be pushed
            if self.solid_on(target_pos) == 1 or self.solid_on(target_pos) == 3:
                return
            if self.entity_on(target_pos) != 0 and not isinstance(self.entity_on(target_pos), Spider):
                return

            self.change_entity(target_pos, entity)
            self.change_entity(given_pos, 0)
            self.player.push(movement)
            entity.move(movement)

        elif isinstance(entity, Minecart):
            target_pos = self.position_after_move(given_pos, movement)

            # check if the entity can be pushed
            if self.solid_on(target_pos) < 4:
                return
            if self.entity_on(target_pos) != 0 and not isinstance(self.entity_on(target_pos), Spider):
                return
            if movement == (1, 0):
                if not self.solid_on(given_pos) in (5, 7, 9) or not self.solid_on(target_pos) in (5, 6, 8):
                    return
            elif movement == (-1, 0):
                if not self.solid_on(given_pos) in (5, 6, 8) or not self.solid_on(target_pos) in (5, 7, 9):
                    return
            elif movement == (0, 1):
                if not self.solid_on(given_pos) in (4, 8, 9) or not self.solid_on(target_pos) in (4, 6, 7):
                    return
            else:
                if not self.solid_on(given_pos) in (4, 6, 7) or not self.solid_on(target_pos) in (4, 8, 9):
                    return 

            self.change_entity(target_pos, entity)
            self.change_entity(given_pos, 0)
            self.player.push(movement)
            entity.move(movement, self.solid_on(given_pos), self.solid_on(target_pos))

        elif isinstance(entity, Spider):
            self.player.move(movement)
            entity.attack()
            self.player.die()
            self.game_over = True
            return

        self.waiting = False
        self.spiders_moving(movement)
        return


    def position_after_move(self, pos, move):
        return (pos[0] + move[0], pos[1] + move[1])

    def solid_on(self, pos):
        return self.solids[pos[0]][pos[1]]

    def entity_on(self, pos):
        return self.entities[pos[0]][pos[1]]

    def change_entity(self, pos, value):
        self.entities[pos[0]][pos[1]] = value





    def spiders_moving(self, player_movement):
        player_connexe = self.get_player_connexe()
        for spider in self.spiders:
            #the spider can track the player and go towards him
            if spider.pos in player_connexe:
                best_movement = self.find_best_movement(spider.pos, player_connexe, player_movement)
                given_pos = self.position_after_move(spider.pos, best_movement)
                self.change_entity(given_pos, spider)
                self.change_entity(spider.pos, 0)
                spider.move(best_movement)
                if spider.pos == self.player.pos:
                    spider.attack()
                    self.player.die()
                    self.game_over = True
            #the spider is pushed with a barrel or a minecart
            elif isinstance(self.entity_on(spider.pos), (Barrel, Minecart)):
                movement1 = player_movement
                movement2 = (-player_movement[1], player_movement[0])
                movement3 = (player_movement[1], -player_movement[0])
                for movement in (movement1, movement2, movement3):
                    pos = self.position_after_move(spider.pos, movement)
                    if not (self.solid_on(pos) == 1 or self.solid_on(pos) == 3 or isinstance(self.entity_on(pos), (Ore, Barrel, Minecart))):
                        self.change_entity(pos, spider)
                        spider.move(movement)
                        return
                #the spider can't go anywhere, this poor creature is crushed:'(
                spiders.remove(spider)
                spider.die()

    def get_player_connexe(self):
        connexe = set()
        bboard = self.binary_board()
        self.find_connexe(bboard, connexe, self.player.pos)
        return connexe

    def find_connexe(self, bboard, connexe, pos):
        i, j = pos
        if bboard[i][j] == 0:
            connexe.add(pos)
            bboard[i][j] = 1
            for neighbors in ((i-1, j), (i+1, j), (i, j-1), (i, j+1)):
                self.find_connexe(bboard, connexe, neighbors)

    def binary_board(self):
        bboard = []
        for i in range(len(self.solids)):
            bline = []
            for j in range(len(self.solids[0])):
                if self.solid_on((i,j)) == 1 or self.solid_on((i,j)) == 3 or isinstance(self.entity_on((i,j)), (Ore, Barrel, Minecart)):
                    bline.append(1)
                else:
                    bline.append(0)
            bboard.append(bline)
        return bboard

    def find_best_movement(self, pos, connexe, player_movement):
        #all the possible movements, in general
        movements = ((1, 0), (0, 1), (-1, 0), (0, -1))

        #all the possible movements for the spider
        possible_movements = {}
        for movement in movements:
            if self.position_after_move(pos, movement) in connexe:
                possible_movements[self.position_after_move(pos, movement)] = movement

        #if the spider is next to the player, go towards him
        if self.player.pos in possible_movements:
            return possible_movements[self.player.pos]

        #initialisation of all the visited and not-visited tiles
        visited = set()
        not_visited = set()
        for tile in connexe:
            not_visited.add(tile)
        visited.add(self.player.pos)
        not_visited.remove(self.player.pos)

        #find all the movements that allow the spider to move towards the player
        best_movements = []
        found = False
        while not found:
            temp = set()
            for tile in visited:
                for movement in movements:
                    new_tile = self.position_after_move(tile, movement)
                    if new_tile in not_visited:
                        if new_tile in possible_movements:
                            best_movements.append(possible_movements[new_tile])
                            found = True
                        not_visited.remove(new_tile)
                        temp.add(new_tile)
            visited = temp

        #if many movements are possible, prioritize the one that doesn't copy the player's movement
        for movement in best_movements:
            if movement != player_movement:
                return movement
        return player_movement

    def key_handler(self, key):
        """ Dispatch keyboard events to children with key handler """
        if self.waiting and not self.game_over:
            if key == glfw.KEY_UP:
                self.change_board((-1, 0))
                #glfw.set_time(0.0)
            if key == glfw.KEY_DOWN:
                self.change_board((1, 0))
                #glfw.set_time(0.0)
            if key == glfw.KEY_LEFT:
                self.change_board((0, -1))
                #glfw.set_time(0.0)
            if key == glfw.KEY_RIGHT:
                self.change_board((0, 1))
                #glfw.set_time(0.0)


    """ def print_board():
        print("")
        for i in range(len(self.solids)):
            line = ""
            for j in range(len(self.solids[0])):
                if (i,j) == player.pos:
                    line += "☺ "
                elif entity_on((i,j)) == 0:
                    if self.solids[i][j] == 0:
                        line += "  "
                    elif solids[i][j] == 1:
                        line += "▓▓"
                    elif solids[i][j] == 3:
                        line += "══"
                    elif solids[i][j] == 4:
                        line += "║ "
                    elif solids[i][j] == 5:
                        line += "╝ "
                    elif solids[i][j] == 6:
                        line += "╗ "
                    elif solids[i][j] == 7:
                        line += "╚═"
                    elif solids[i][j] == 8:
                        line += "╔═"
                elif isinstance(entity_on((i,j)), Ore):
                    line += "▲ "
                elif isinstance(entity_on((i,j)), Barrel):
                    line += "o "
                elif isinstance(entity_on((i,j)), Minecart):
                    line += "◙ "
                elif isinstance(entity_on((i,j)), Spider):
                    line += "x "
            print(line) """

    def create_all_entities(self):
        for i in range(len(self.entities)):
            for j in range(len(self.entities[0])):
                entity = self.entity_on((i,j))
                if entity != 0:
                    if entity == 1:
                        self.change_entity((i,j), Ore((i,j)))
                        self.ores += 1
                    #if entity == 2:
                    #    self.change_entity((i,j), Barrel((i,j)))
                    if entity == 3:
                        self.change_entity((i,j), Minecart((i,j), rail=self.solid_on((i,j))))
                    if entity == 4:
                        spider = Spider((i,j))
                        self.spiders.append(spider)
                        self.change_entity((i,j), spider)
                    self.scene.add(self.entity_on((i,j)))


def main():
    game = Game(solids, entities, character_pos)
    game.run()


if __name__ == '__main__':
    main()

    # create_all_entities()
    # while(player.alive):
    #     print_board()
    #     while(True):
    #         move_char = input()
    #         if move_char == 'z':
    #             movement = (-1, 0)
    #             break
    #         if move_char == 'q':
    #             movement = (0, -1)
    #             break
    #         if move_char == 's':
    #             movement = (1, 0)
    #             break
    #         if move_char == 'd':
    #             movement = (0, 1)
    #             break
    #     change_board(movement)
    #print_board()
