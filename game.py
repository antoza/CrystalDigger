#!/usr/bin/env python3
import sys

from load_game import load_from_txt
from entity_classes import *
from core import *


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


class Game(Viewer):
    def __init__(self, solids, entities, door_location, first_move, fps):
        width = 100*len(solids[0])
        height = 100*len(solids)
        size = max(width, height)
        super().__init__(width=size, height=size)
        self.temporary_shader = Shader("shaders/animatedAndTextured.vert", "shaders/animatedAndTextured.frag")
        self.solids = solids
        self.shader = Shader("shaders/texture.vert", "shaders/scene.frag")
        level = np.array(solids)
        x,y = level.shape
        self.scene = Scene(level=level, transform=translate(-y / 2, x / 2, 0))
        self.add(self.scene)

        self.entities = entities
        self.player = Player(door_location, fps=fps)
        self.player.move(first_move)
        self.scene.open_door()
        self.scene.add(self.player)
        self.ores = 0
        self.spiders = []
        self.create_all_entities(fps)
        self.waiting = True
        self.fps = fps
        self.iterator = 0
        self.game_over = False

        self.trackball.zoom(-max(height, width)**2/15000, size)
        self.trackball.drag((size//2, size//2), (size//2,  size//2  + 50), size)

    def run(self):
        """ Main render loop for this OpenGL window """
        while not glfw.window_should_close(self.win):
            if self.ores != 0:
                self.scene.close_door()
            else:
                self.scene.open_door()
            if not self.waiting:
                if self.iterator < 5*self.fps:
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
                self.spiders.remove(spider)
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

    def create_all_entities(self, fps):
        for i in range(len(self.entities)):
            for j in range(len(self.entities[0])):
                entity = self.entity_on((i,j))
                if entity != 0:
                    if entity == 1:
                        self.change_entity((i,j), Ore((i,j), fps=fps))
                        self.ores += 1
                    if entity == 2:
                        self.change_entity((i,j), Barrel((i,j), fps=fps))
                    if entity == 3:
                        self.change_entity((i,j), Minecart((i,j), rail=self.solid_on((i,j)), fps=fps))
                    if entity == 4:
                        spider = Spider((i,j), fps=fps)
                        self.spiders.append(spider)
                        self.change_entity((i,j), spider)
                    self.scene.add(self.entity_on((i,j)))


def main(path, fps):
    solids, entities, door_location = load_from_txt("GameLevels/"+path)
    if door_location[0] == 0:
        first_move = (1, 0)
    elif door_location[1] == 0:
        first_move = (0, 1)
    elif door_location[0] == len(solids) - 1:
        first_move = (-1, 0)
    else:
        first_move = (0, -1)

    game = Game(solids, entities, door_location, first_move, fps)
    game.run()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please enter a .txt game level")
        sys.exit()
    fps = 5
    if len(sys.argv) == 3:
        fps = int(sys.argv[2])
    main(sys.argv[1], fps)
