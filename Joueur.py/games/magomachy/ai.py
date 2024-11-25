# This is where you build your AI for the Magomachy game.

from typing import List
from joueur.base_ai import BaseAI
import random

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
# <<-- /Creer-Merge: imports -->>

class AI(BaseAI):
    """ The AI you add and improve code inside to play Magomachy. """

    @property
    def game(self) -> 'games.magomachy.game.Game':
        """games.magomachy.game.Game: The reference to the Game instance this AI is playing.
        """
        return self._game # don't directly touch this "private" variable pls

    @property
    def player(self) -> 'games.magomachy.player.Player':
        """games.magomachy.player.Player: The reference to the Player this AI controls in the Game.
        """
        return self._player # don't directly touch this "private" variable pls

    def get_name(self) -> str:
        """This is the name you send to the server so your AI will control the player named this string.

        Returns:
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "Team Nithinion" # REPLACE THIS WITH YOUR TEAM NAME
        # <<-- /Creer-Merge: get-name -->>

    def start(self) -> None:
        """This is called once the game starts and your AI knows its player and game. You can initialize your AI here.
        """
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your start logic
        self.player.choose_wizard("map")
        # <<-- /Creer-Merge: start -->>

    def game_updated(self) -> None:
        """This is called every time the game's state updates, so if you are tracking anything you can update it here.
        """
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic
        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won: bool, reason: str) -> None:
        """This is called when the game ends, you can clean up your data and dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why your AI won or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your end logic
        # <<-- /Creer-Merge: end -->>
    def action(self, wizard: 'games.magomachy.wizard.Wizard') -> int:
        """This is called whenever your wizard selects an action.

        Args:
            wizard (games.magomachy.wizard.Wizard): Wizard performs action.

        Returns:
            int: Three of the choices a Wizard can make as an action.
        """
        # <<-- Creer-Merge: Action -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # Put your game logic here for Action
        return -1
        # <<-- /Creer-Merge: Action -->>
    def move(self, wizard: 'games.magomachy.wizard.Wizard') -> int:
        """This is called whenever your wizard makes a move.

        Args:
            wizard (games.magomachy.wizard.Wizard): Wizard moves.

        Returns:
            int: Eight cardinal directions.
        """
        # <<-- Creer-Merge: Move -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # Put your game logic here for Move
        return -1
        # <<-- /Creer-Merge: Move -->>
    def run_turn(self) -> bool:
        """This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
        """



        enemy_type = None
        enemy = None
        # FIRST TURNS #
        if self.game.current_turn==0 or self.game.current_turn==1:
            wizard = 'aggressive'
            self.player.choose_wizard(wizard)
            return True
        else:
            # ENEMY WIZARD DETECTION #
            enemy = self.game.players[0]
            if enemy == self.player:
                enemy = self.game.players[1]
            enemy_type = enemy.wizard.specialty
            # ENEMY WIZARD DETECTION END #
        if enemy_type is not None and enemy_type != 'aggressive' and (self.game.current_turn==2 or self.game.current_turn==3):
            spell = "Thunderous Dash"
            x = self.player.wizard.tile.x
            y = self.player.wizard.tile.y
            tile = self.game.get_tile_at(int(x), int(y))
            self.player.wizard.cast(spell,tile)
            if self.player.wizard.tile.x==8 and self.player.wizard.tile.y==1:
                tile = self.player.wizard.tile.tile_south
                self.player.wizard.move(tile)
                tile = self.player.wizard.tile.tile_south
                self.player.wizard.move(tile)
                tile = self.player.wizard.tile.tile_west
                self.player.wizard.move(tile)
                tile = self.player.wizard.tile.tile_west
                self.player.wizard.move(tile)
            else:
                tile = self.player.wizard.tile.tile_north
                self.player.wizard.move(tile)
                tile = self.player.wizard.tile.tile_north
                self.player.wizard.move(tile)
                tile = self.player.wizard.tile.tile_east
                self.player.wizard.move(tile)
                tile = self.player.wizard.tile.tile_east
                self.player.wizard.move(tile)
            return True
        # END FIRST TURNS#


        # FIND ITEMS #
        item_list = {
            'charge_rune':      [],
            'explosion_rune':   [],
            'teleport_rune':    [],
            'heal_rune':        [],
            'stone_wall':       [],
            'health_pot':       [],
            'mana_pot':         []
        }

        safe_tiles = []
        tiles = self.game.tiles
        for x in range(self.game.map_width):
            for y in range(self.game.map_height):
                current_tile = tiles[x + y*self.game.map_width]
                safe_tiles.append(current_tile)
                if current_tile.object:
                    if current_tile.object.form == 'charge rune':
                        item_list['charge_rune'].append(current_tile)
                        print(f'Charge rune found at x: {current_tile.x}, y: {current_tile.y}')
                    elif current_tile.object.form == 'heal rune':
                        item_list['heal_rune'].append(current_tile)
                    elif current_tile.object.form == 'stone':
                        item_list['stone_wall'].append(current_tile)
                    elif current_tile.object.form == 'explosion rune':
                        item_list['explosion_rune'].append(current_tile)
                    elif current_tile.object.form == 'health flask':
                        item_list['health_pot'].append(current_tile)
                    elif current_tile.object.form == 'aether flask':
                        item_list['mana_pot'].append(current_tile)
                    elif current_tile.object.form == 'teleport rune':
                        item_list['teleport_rune'].append(current_tile)

        # FIND ITEMS #

        # LASER DETECTION #
        def detect_lasers(start_tile, laser_beam_tiles):
            test_tile = start_tile
            while test_tile.tile_west.type == 'floor':
                if test_tile not in laser_beam_tiles:
                    laser_beam_tiles.append(test_tile)
                test_tile = test_tile.tile_west
            test_tile = start_tile
            while test_tile.tile_east.type == 'floor':
                if test_tile not in laser_beam_tiles:
                    laser_beam_tiles.append(test_tile)
                test_tile = test_tile.tile_east
            test_tile = start_tile
            while test_tile.tile_north.type == 'floor':
                if test_tile not in laser_beam_tiles:
                    laser_beam_tiles.append(test_tile)
                test_tile = test_tile.tile_north
            test_tile = start_tile
            while test_tile.tile_south.type == 'floor':
                if test_tile not in laser_beam_tiles:
                    laser_beam_tiles.append(test_tile)
                test_tile = test_tile.tile_south


        # DETECT END #


        # FIND PATH #
        def find_path(end_tile, hit_bombs: False):
            R, C = self.game.map_width, self.game.map_height
            m = self.game.tiles
            sr, sc = self.player.wizard.tile.x, self.player.wizard.tile.y
            rq, cq = [], []

            move_count = 0
            nodes_left_in_layer = 1
            nodes_in_next_layer = 0

            reached_end = False

            visited = [False] * ( R * C )

            parent = [-1] * (R * C)

            dr = [-1, +1, 0, 0]
            dc = [0, 0, +1, -1]

            def solve():
                nonlocal nodes_left_in_layer
                nonlocal reached_end
                nonlocal move_count
                nonlocal nodes_in_next_layer
                nonlocal hit_bombs
                rq.append(sr)
                cq.append(sc)
                visited[sr+sc*self.game.map_height]=True

                while len(rq) > 0:
                    r = rq.pop(0)
                    c = cq.pop(0)

                    if m[r + c*self.game.map_height] == end_tile:
                        reached_end = True
                        break

                    explore_neighbours(r, c)
                    nodes_left_in_layer -= 1

                    if nodes_left_in_layer == 0:
                        nodes_left_in_layer += nodes_in_next_layer
                        nodes_in_next_layer =0
                        move_count += 1

                if reached_end:
                    path = []
                    r, c = end_tile.x, end_tile.y
                    idx = end_tile.x + end_tile.y*self.game.map_height
                    while idx != sr + sc * self.game.map_height:
                        path.append(m[idx])
                        idx = parent[idx]
                    path.append(m[sr + sc * self.game.map_height])
                    path.reverse()
                    return path
                return None

            def explore_neighbours(r, c):
                nonlocal R
                nonlocal C
                nonlocal nodes_in_next_layer
                nonlocal hit_bombs
                nonlocal end_tile
                for i in range(4):
                    rr = r + dr[i]
                    cc = c + dc[i]

                    if rr < 1 or cc < 1: continue
                    if rr >= R-1 or cc >= C-1: continue

                    if visited[rr+cc*self.game.map_height]: continue
                    if m[rr+cc*self.game.map_height].type == 'wall': continue
                    if m[rr+cc*self.game.map_height].wizard is not None and m[rr+cc*self.game.map_height].wizard != self.player.wizard: continue
                    if not hit_bombs and m[rr + cc * self.game.map_height].object is not None and m[rr + cc * self.game.map_height].object.form == 'explosion rune' and m[rr + cc * self.game.map_height] != end_tile: continue
                    if m[rr + cc * self.game.map_height].object is not None and m[rr + cc * self.game.map_height].object.form == 'stone': continue

                    rq.append(rr)
                    cq.append(cc)
                    visited[rr+cc*self.game.map_height]=True

                    parent[rr + cc * self.game.map_height] = r + c * self.game.map_height

                    nodes_in_next_layer += 1
            return solve()
        # PATH FINDING END #




        # FIRST TURN? #
        first_turn = True
        if self.game.current_turn % 2 == 1:
            first_turn = False
        # FIRST TURN END #


        # ENEMY WIZARD BRANCHING #
        if enemy_type == 'strategic':
            if len(item_list['charge_rune']) > 0:
                print(f'charge runes found: {len(item_list["charge_rune"])}')

                # FILTER SAFE TILES #
                print(f'safe_tiles size before filtering {len(safe_tiles)}')
                filtered_safe_tiles = []
                for current_tile in safe_tiles:
                    dangerous = False
                    for charge_rune in item_list["charge_rune"]:
                        if abs(current_tile.x - charge_rune.x) <= 3 and abs(current_tile.y - charge_rune.y) <= 3:
                            dangerous = True
                            break
                    if not dangerous and current_tile.type == 'floor':
                        filtered_safe_tiles.append(current_tile)
                print(f'safe_tiles size after filtering {len(filtered_safe_tiles)}')
                # FILTER END #

                # RUNE CLASSIFICATION #
                most_explodey_rune = max(item_list['charge_rune'], key=lambda obj: obj.object.lifetime)
                closest_explodey_rune = item_list['charge_rune'][0]
                min_dist = 100
                for charge_rune in item_list['charge_rune']:
                    if abs(charge_rune.x - self.player.wizard.tile.x) + abs(charge_rune.y - self.player.wizard.tile.y) < min_dist:
                        min_dist = abs(charge_rune.x - self.player.wizard.tile.x) + abs(charge_rune.y - self.player.wizard.tile.y)
                        print(f'min_dist : {min_dist}')
                        closest_explodey_rune = charge_rune
                shortest_timer_rune = -1
                for charge_rune in item_list['charge_rune']:
                    if charge_rune.object.lifetime > shortest_timer_rune:
                        shortest_timer_rune = charge_rune.object.lifetime

                # CLASSIFICATION END #


                # GET AWAY FROM IT!!!
                print(f'wizard tile location: {self.player.wizard.tile.x}, {self.player.wizard.tile.y}')
                print(f'closest charge rune location: {closest_explodey_rune.x}, {closest_explodey_rune.y}')
                print(f'shortest timer: {shortest_timer_rune}')
                if not any(tile.x == self.player.wizard.tile.x and tile.y == self.player.wizard.tile.y for tile in filtered_safe_tiles):
                    print(f'Im in danger')
                    # IN DANGER

                    # FIND NEAREST SAFE TILE THAT IS NOT A BOMB #
                    path = None
                    nearest_safe_tile_no_bomb = None
                    min_path_len = 100
                    for safe_tile in filtered_safe_tiles:
                        if safe_tile.object is not None and safe_tile.object.form == 'explosion rune':
                            pass
                        temp_path = find_path(safe_tile, False)
                        if temp_path is not None and len(temp_path) < min_path_len:
                            min_path_len = len(temp_path)
                            nearest_safe_tile_no_bomb = safe_tile
                            path = temp_path

                        # if abs(safe_tile.x - self.player.wizard.tile.x) + abs(safe_tile.y - self.player.wizard.tile.y) < min_dist:
                        #     min_dist = abs(safe_tile.x - self.player.wizard.tile.x) + abs(safe_tile.y - self.player.wizard.tile.y)
                        #     nearest_safe_tile_no_bomb = safe_tile
                    # END FIND NEAREST TILE #



                    # path = find_path(nearest_safe_tile_no_bomb, False)
                    if path is None: #  CHECK PATH WITH BOMBS
                        print('no path found')
                        return True # delete this # DLETETHE THIS EDELTE THIS DELETE THIS DELETE THIS DELETE THIS
                    else:
                        print(f'Nearest safe tile: x:{nearest_safe_tile_no_bomb.x}, y:{nearest_safe_tile_no_bomb.y}')
                        print(f'path found. printing path. path length: {len(path)-1}')
                        print(f'tile 0 = start tile = wizard tile (IDEALLY)')
                        i=0
                        for tile in path:
                            print(f'Tile [{i}]: x:{tile.x}, y:{tile.y}')
                            i+=1
                        turns_to_traverse = ((len(path)-1) // 2) + ((len(path)-1) % 2)
                        turns_till_explosion = ((10 - shortest_timer_rune) // 2)
                        print(f'lifetime: {shortest_timer_rune}')
                        print(f'turns to traverse path of length {len(path)}: {turns_to_traverse}')
                        if turns_till_explosion < turns_to_traverse:
                            print('i have to dash (im a liar)')
                            # PATH TOO LONG WITHOUT DASHING #
                            if self.player.wizard.aether < 4 or turns_till_explosion < turns_to_traverse-1:
                                print(f'I HAVE TO DASH TWICE OR NO MANA')
                                # PATH TOO LONG FOR ONE DASH #
                                if self.player.wizard.aether < 7 or turns_till_explosion < turns_to_traverse-2 :
                                    print(f'I HAVE TO DASH MORE THAN TWICE OR NO MANA')
                                    # PATH TOO LONG FOR TWO DASH #
                                    # PATH WITH BOMBS (IMPLEMENT) #

                                    # ========================== PATH WITH BOMBS ========================== #

                                    path = None
                                    nearest_safe_tile_no_bomb = None
                                    min_path_len = 100
                                    for safe_tile in filtered_safe_tiles:
                                        if safe_tile.object is not None and safe_tile.object.form == 'explosion rune':
                                            pass
                                        temp_path = find_path(safe_tile, True)
                                        if temp_path is not None and len(temp_path) < min_path_len:
                                            min_path_len = len(temp_path)
                                            nearest_safe_tile_no_bomb = safe_tile
                                            path = temp_path
                                    # path = find_path(nearest_safe_tile_no_bomb, True)
                                    print(f' path with bombs allowed, to non bomb tile running')
                                    if path is None:
                                        print(f'path not found')
                                        return True # CHANGE CHANGE CHANGE CHANGE
                                    else:
                                        print(f'path found')
                                        print(f'no more comments from here, already in wrong decision tree anyways')
                                        turns_to_traverse = (len(path) - 1) // 2 + ((len(path) - 1) % 2)
                                        if turns_till_explosion < turns_to_traverse:
                                            # PATH TOO LONG WITHOUT DASHING #
                                            if self.player.wizard.aether < 4 or turns_till_explosion < turns_to_traverse-1:
                                                # ONE DASH NOT POSSIBLE TO SAVE #
                                                if self.player.wizard.aether < 7 or turns_till_explosion < turns_to_traverse-2:
                                                    # TWO DASH NOT POSSIBLE TO SAVE #

                                                    # ========================== SPACE WITH A BOMB ========================== #

                                                    # nearest_safe_tile_with_bomb = min(
                                                    #     filtered_safe_tiles,
                                                    #     key=lambda safe_tile: abs(safe_tile.x - self.player.wizard.tile.x) + abs(safe_tile.y - self.player.wizard.tile.y)
                                                    # )

                                                    path = None
                                                    nearest_safe_tile_is_bomb = None
                                                    min_path_len = 100
                                                    for safe_tile in filtered_safe_tiles:
                                                        temp_path = find_path(safe_tile, False)
                                                        if temp_path is not None and len(temp_path) < min_path_len:
                                                            min_path_len = len(temp_path)
                                                            nearest_safe_tile_is_bomb = safe_tile
                                                            path = temp_path
                                                    # path = find_path(nearest_safe_tile_with_bomb, False)
                                                    if path is None:
                                                        return True # CHANCE HCANGE CHANGE CHANGE CHANGE
                                                    else:
                                                        turns_to_traverse = (len(path) - 1) // 2 + ((len(path) - 1) % 2)
                                                        if turns_till_explosion < turns_to_traverse:
                                                            # PATH TOO LONG WITHOUT DASHING #
                                                            if self.player.wizard.aether < 4 or turns_till_explosion < turns_to_traverse-1:
                                                                # ONE DASH DOES NOT WORK #
                                                                if self.player.wizard.aether < 7 or turns_till_explosion < turns_to_traverse-2:
                                                                    # TWO DASH DOES NOT WORK #

                                                                    # ========================== SPACE WITH A BOMB HITS BOMBS ========================== #
                                                                    # path = find_path(nearest_safe_tile_is_bomb, True)

                                                                    path = None
                                                                    nearest_safe_tile_is_bomb = None
                                                                    min_path_len = 100
                                                                    for safe_tile in filtered_safe_tiles:
                                                                        temp_path = find_path(safe_tile, True)
                                                                        if temp_path is not None and len(temp_path) < min_path_len:
                                                                            min_path_len = len(temp_path)
                                                                            nearest_safe_tile_is_bomb = safe_tile
                                                                            path = temp_path
                                                                    if path is None:
                                                                        return True # CHANGE CHANGE CHANGE
                                                                    else:
                                                                        turns_to_traverse = (len(path) - 1) // 2 + ((len(path) - 1) % 2)
                                                                        if turns_till_explosion < turns_to_traverse:
                                                                            # PATH TOO LONG WITHOUT DASHING #
                                                                            if self.player.wizard.aether < 4 or turns_till_explosion < turns_to_traverse-1:
                                                                                # ONE DASH NOT POSSIBLE #
                                                                                if self.player.wizard.aether < 7 or turns_till_explosion < turns_to_traverse-2:
                                                                                    # TWO DASH NOT POSSIBLE #

                                                                                    # ========================== NEAREST USEABLE POTION ========================== #
                                                                                    # IF IN MIDDLE 4 TILES #
                                                                                    if self.player.wizard.tile.x in range (4,5) and self.player.wizard.tile.y in range (4,5) and len(item_list['mana_pot']) > 0:
                                                                                        path = find_path(item_list['mana_pot'][0],False)
                                                                                    else:
                                                                                        min_path_len = 100
                                                                                        temp_path = None
                                                                                        for health_pot in item_list['health_pot']:
                                                                                            temp_path = find_path(health_pot, False)
                                                                                            if len(temp_path) < min_path_len:
                                                                                                path = temp_path
                                                                                                min_path_len = len(temp_path)
                                                                                        if min_path_len < 100:
                                                                                            print(f'health pot found, {min_path_len} away')



                                                                                    while self.player.wizard.movement_left > 0 and path is not None and len(path) > 1:
                                                                                        path.pop(0)
                                                                                        self.player.wizard.move(path[0])
                                                                                    # ENDIF #


                                                                                    return True


                                                                                else:
                                                                                    # TWO DASH WORKS #
                                                                                    # DO DASH ONE OF TWO #
                                                                                    self.player.wizard.cast(
                                                                                        'Thunderous Dash',
                                                                                        self.player.wizard.tile)
                                                                                    # MOVE #
                                                                                    while self.player.wizard.movement_left > 0 and len(path) > 1:
                                                                                        path.pop(0)
                                                                                        self.player.wizard.move(path[0])
                                                                                    # TWO DASH SCENARIO END #
                                                                                    return True
                                                                            else:
                                                                                # ONE DASH WORKS POSSIBLE #
                                                                                # DO DASH #
                                                                                self.player.wizard.cast('Thunderous Dash', self.player.wizard.tile)
                                                                                # MOVE #
                                                                                while self.player.wizard.movement_left > 0 and len(path) > 1:
                                                                                    path.pop(0)
                                                                                    self.player.wizard.move(path[0])
                                                                                # ONE DASH SCENARIO END #
                                                                                return True
                                                                        else:
                                                                            # PATH POSSIBLE TO WALK OUT OF #
                                                                            # POSSIBLY ADD MANA POTIONS LATER #
                                                                            # MOVE #
                                                                            print('i dont have to dash!')
                                                                            while self.player.wizard.movement_left > 0 and len(path) > 1:
                                                                                if not self.player.wizard.has_cast:
                                                                                    if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                                                                                        if enemy.wizard.health == 1:
                                                                                            self.player.wizard.cast(
                                                                                                'Punch',
                                                                                                enemy.wizard.tile)
                                                                                        elif enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                                            self.player.wizard.cast(
                                                                                                'Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                                        elif self.player.wizard.aether > 2:
                                                                                            self.player.wizard.cast(
                                                                                                'Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                                        else:
                                                                                            self.player.wizard.cast(
                                                                                                'Punch',
                                                                                                enemy.wizard.tile)
                                                                                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                                                                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                                            self.player.wizard.cast(
                                                                                                'Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                                        elif self.player.wizard.aether > 2:
                                                                                            self.player.wizard.cast(
                                                                                                'Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                                                                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                                            self.player.wizard.cast(
                                                                                                'Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                                        elif self.player.wizard.aether > 2:
                                                                                            self.player.wizard.cast(
                                                                                                'Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                                                                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                                            self.player.wizard.cast(
                                                                                                'Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                                        elif self.player.wizard.aether > 2:
                                                                                            self.player.wizard.cast(
                                                                                                'Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                                                                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                                            self.player.wizard.cast(
                                                                                                'Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                                        elif self.player.wizard.aether > 2:
                                                                                            self.player.wizard.cast(
                                                                                                'Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                                path.pop(0)
                                                                                self.player.wizard.move(path[0])

                                                                            if not self.player.wizard.has_cast:
                                                                                if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                                                                                    if enemy.wizard.health == 1:
                                                                                        self.player.wizard.cast('Punch',
                                                                                                                enemy.wizard.tile)
                                                                                    elif enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                                        self.player.wizard.cast(
                                                                                            'Fire Slash',
                                                                                            enemy.wizard.tile)
                                                                                    elif self.player.wizard.aether > 2:
                                                                                        self.player.wizard.cast(
                                                                                            'Fire Slash',
                                                                                            enemy.wizard.tile)
                                                                                    else:
                                                                                        self.player.wizard.cast('Punch',
                                                                                                                enemy.wizard.tile)
                                                                                elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                                                                                    if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                                        self.player.wizard.cast(
                                                                                            'Fire Slash',
                                                                                            enemy.wizard.tile)
                                                                                    elif self.player.wizard.aether > 2:
                                                                                        self.player.wizard.cast(
                                                                                            'Fire Slash',
                                                                                            enemy.wizard.tile)
                                                                                elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                                                                                    if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                                        self.player.wizard.cast(
                                                                                            'Fire Slash',
                                                                                            enemy.wizard.tile)
                                                                                    elif self.player.wizard.aether > 2:
                                                                                        self.player.wizard.cast(
                                                                                            'Fire Slash',
                                                                                            enemy.wizard.tile)
                                                                                elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                                                                                    if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                                        self.player.wizard.cast(
                                                                                            'Fire Slash',
                                                                                            enemy.wizard.tile)
                                                                                    elif self.player.wizard.aether > 2:
                                                                                        self.player.wizard.cast(
                                                                                            'Fire Slash',
                                                                                            enemy.wizard.tile)
                                                                                elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                                                                                    if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                                        self.player.wizard.cast(
                                                                                            'Fire Slash',
                                                                                            enemy.wizard.tile)
                                                                                    elif self.player.wizard.aether > 2:
                                                                                        self.player.wizard.cast(
                                                                                            'Fire Slash',
                                                                                            enemy.wizard.tile)
                                                                            return True



                                                                else:
                                                                    # TWO DASH POSSIBLE WORKS #
                                                                    # DO DASH ONE OF TWO #
                                                                    self.player.wizard.cast('Thunderous Dash', self.player.wizard.tile)
                                                                    # MOVE #
                                                                    while self.player.wizard.movement_left > 0 and len(path) > 1:
                                                                        path.pop(0)
                                                                        self.player.wizard.move(path[0])
                                                                    # TWO DASH SCENARIO END #
                                                                    return True
                                                            else:
                                                                # ONE DASH POSSIBLE, WORKS #
                                                                # DO DASH #
                                                                self.player.wizard.cast('Thunderous Dash',self.player.wizard.tile)
                                                                # MOVE #
                                                                while self.player.wizard.movement_left > 0 and len(path) > 1:
                                                                    path.pop(0)
                                                                    self.player.wizard.move(path[0])
                                                                # ONE DASH SCENARIO END #
                                                                return True
                                                        else:
                                                            # PATH POSSIBLE WITHOUT DASHING #
                                                            # POSSIBLY ADD MANA POTIONS LATER #
                                                            # MOVE #
                                                            print('i dont have to dash!')
                                                            while self.player.wizard.movement_left > 0 and len(path) > 1:
                                                                if not self.player.wizard.has_cast:
                                                                    if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                                                                        if enemy.wizard.health == 1:
                                                                            self.player.wizard.cast('Punch',
                                                                                                    enemy.wizard.tile)
                                                                        elif enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                            self.player.wizard.cast('Fire Slash',
                                                                                                    enemy.wizard.tile)
                                                                        elif self.player.wizard.aether > 2:
                                                                            self.player.wizard.cast('Fire Slash',
                                                                                                    enemy.wizard.tile)
                                                                        else:
                                                                            self.player.wizard.cast('Punch',
                                                                                                    enemy.wizard.tile)
                                                                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                                                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                            self.player.wizard.cast('Fire Slash',
                                                                                                    enemy.wizard.tile)
                                                                        elif self.player.wizard.aether > 2:
                                                                            self.player.wizard.cast('Fire Slash',
                                                                                                    enemy.wizard.tile)
                                                                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                                                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                            self.player.wizard.cast('Fire Slash',
                                                                                                    enemy.wizard.tile)
                                                                        elif self.player.wizard.aether > 2:
                                                                            self.player.wizard.cast('Fire Slash',
                                                                                                    enemy.wizard.tile)
                                                                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                                                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                            self.player.wizard.cast('Fire Slash',
                                                                                                    enemy.wizard.tile)
                                                                        elif self.player.wizard.aether > 2:
                                                                            self.player.wizard.cast('Fire Slash',
                                                                                                    enemy.wizard.tile)
                                                                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                                                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                            self.player.wizard.cast('Fire Slash',
                                                                                                    enemy.wizard.tile)
                                                                        elif self.player.wizard.aether > 2:
                                                                            self.player.wizard.cast('Fire Slash',
                                                                                                    enemy.wizard.tile)
                                                                path.pop(0)
                                                                self.player.wizard.move(path[0])

                                                            if not self.player.wizard.has_cast:
                                                                if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                                                                    if enemy.wizard.health == 1:
                                                                        self.player.wizard.cast('Punch',
                                                                                                enemy.wizard.tile)
                                                                    elif enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                        self.player.wizard.cast('Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                    elif self.player.wizard.aether > 2:
                                                                        self.player.wizard.cast('Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                    else:
                                                                        self.player.wizard.cast('Punch',
                                                                                                enemy.wizard.tile)
                                                                elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                                                                    if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                        self.player.wizard.cast('Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                    elif self.player.wizard.aether > 2:
                                                                        self.player.wizard.cast('Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                                                                    if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                        self.player.wizard.cast('Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                    elif self.player.wizard.aether > 2:
                                                                        self.player.wizard.cast('Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                                                                    if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                        self.player.wizard.cast('Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                    elif self.player.wizard.aether > 2:
                                                                        self.player.wizard.cast('Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                                                                    if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                                        self.player.wizard.cast('Fire Slash',
                                                                                                enemy.wizard.tile)
                                                                    elif self.player.wizard.aether > 2:
                                                                        self.player.wizard.cast('Fire Slash',
                                                                                                enemy.wizard.tile)
                                                            return True


                                                else:
                                                    # TWO DASH SAVES AND CAN DASH TWICE #
                                                    # DO DASH ONE OF TWO #
                                                    self.player.wizard.cast('Thunderous Dash', self.player.wizard.tile)
                                                    # MOVE #
                                                    while self.player.wizard.movement_left > 0 and len(path) > 1:
                                                        path.pop(0)
                                                        self.player.wizard.move(path[0])
                                                    # TWO DASH SCENARIO END #
                                                    return True
                                            else:
                                                # ONE DASH SAVES AND CAN DASH #
                                                # DO DASH #
                                                self.player.wizard.cast('Thunderous Dash', self.player.wizard.tile)
                                                # MOVE #
                                                while self.player.wizard.movement_left > 0 and len(path) > 1:
                                                    path.pop(0)
                                                    self.player.wizard.move(path[0])
                                                # ONE DASH SCENARIO END #
                                                return True
                                        else:
                                            # PATH NOT TOO LONG WITHOUT DASHING #
                                            # POSSIBLY ADD MANA POTIONS LATER #
                                            # MOVE #
                                            print('i dont have to dash!')
                                            while self.player.wizard.movement_left > 0 and len(path) > 1:
                                                if not self.player.wizard.has_cast:
                                                    if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                                                        if enemy.wizard.health == 1:
                                                            self.player.wizard.cast('Punch', enemy.wizard.tile)
                                                        elif enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                        elif self.player.wizard.aether > 2:
                                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                        else:
                                                            self.player.wizard.cast('Punch', enemy.wizard.tile)
                                                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                        elif self.player.wizard.aether > 2:
                                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                        elif self.player.wizard.aether > 2:
                                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                        elif self.player.wizard.aether > 2:
                                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                        elif self.player.wizard.aether > 2:
                                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                path.pop(0)
                                                self.player.wizard.move(path[0])

                                            if not self.player.wizard.has_cast:
                                                if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                                                    if enemy.wizard.health == 1:
                                                        self.player.wizard.cast('Punch', enemy.wizard.tile)
                                                    elif enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                    elif self.player.wizard.aether > 2:
                                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                    else:
                                                        self.player.wizard.cast('Punch', enemy.wizard.tile)
                                                elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                                                    if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                    elif self.player.wizard.aether > 2:
                                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                                                    if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                    elif self.player.wizard.aether > 2:
                                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                                                    if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                    elif self.player.wizard.aether > 2:
                                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                                                    if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                                    elif self.player.wizard.aether > 2:
                                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)

                                            return True

                                else:
                                    # TWO DASH SAVES #
                                    # DO DASH ONE OF TWO #
                                    self.player.wizard.cast('Thunderous Dash',self.player.wizard.tile)
                                    # MOVE #
                                    while self.player.wizard.movement_left > 0 and len(path) > 1:
                                        path.pop(0)
                                        self.player.wizard.move(path[0])
                                    # TWO DASH SCENARIO END #
                                    return True
                            else:
                                # ONE DASH SAVES #
                                if self.player.wizard.aether >= 4 and not self.player.wizard.has_cast:
                                    # DO DASH #
                                    self.player.wizard.cast('Thunderous Dash',self.player.wizard.tile)
                                    # MOVE #
                                    while self.player.wizard.movement_left > 0 and len(path) > 1:
                                        path.pop(0)
                                        self.player.wizard.move(path[0])
                                    # ONE DASH SCENARIO END #
                                    return True
                        else:
                            # PATH NOT TOO LONG #
                            # POSSIBLY ADD MANA POTIONS LATER #
                            # MOVE #
                            print('i dont have to dash!')
                            while self.player.wizard.movement_left > 0 and len(path) > 1:
                                if not self.player.wizard.has_cast:
                                    if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                                        if enemy.wizard.health == 1:
                                            self.player.wizard.cast('Punch', enemy.wizard.tile)
                                        elif enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                        elif self.player.wizard.aether > 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                        else:
                                            self.player.wizard.cast('Punch', enemy.wizard.tile)
                                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                        elif self.player.wizard.aether > 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                        elif self.player.wizard.aether > 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                        elif self.player.wizard.aether > 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                        elif self.player.wizard.aether > 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                path.pop(0)
                                self.player.wizard.move(path[0])

                            if not self.player.wizard.has_cast:
                                if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                                    if enemy.wizard.health == 1:
                                        self.player.wizard.cast('Punch',enemy.wizard.tile)
                                    elif enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                        self.player.wizard.cast('Fire Slash',enemy.wizard.tile)
                                    elif self.player.wizard.aether > 2:
                                        self.player.wizard.cast('Fire Slash',enemy.wizard.tile)
                                    else:
                                        self.player.wizard.cast('Punch',enemy.wizard.tile)
                                elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                                    if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                        self.player.wizard.cast('Fire Slash',enemy.wizard.tile)
                                    elif self.player.wizard.aether > 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                                    if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                        self.player.wizard.cast('Fire Slash',enemy.wizard.tile)
                                    elif self.player.wizard.aether > 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                                    if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                        self.player.wizard.cast('Fire Slash',enemy.wizard.tile)
                                    elif self.player.wizard.aether > 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                                    if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                        self.player.wizard.cast('Fire Slash',enemy.wizard.tile)
                                    elif self.player.wizard.aether > 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            return True
                else:
                    print(f'Not in a charge rune!')
                    if self.player.wizard.aether < 4 and len(item_list['mana_pot'])>0:
                        path = find_path(item_list['mana_pot'][0], False)
                    else:
                        path = find_path(enemy.wizard.tile, False)
                    if path is not None:
                        path.pop(0)
                        while self.player.wizard.movement_left > 0:
                            next_tile = path[0]
                            dangerous = True
                            for safe_tile in safe_tiles:
                                if next_tile.x == safe_tile.x and next_tile.y == safe_tile.y:
                                    dangerous = False
                            if not dangerous:
                                if not self.player.wizard.has_cast:
                                    if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                                        if enemy.wizard.health == 1:
                                            self.player.wizard.cast('Punch', enemy.wizard.tile)
                                        elif enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                        elif self.player.wizard.aether > 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                        else:
                                            self.player.wizard.cast('Punch', enemy.wizard.tile)
                                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                        elif self.player.wizard.aether > 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                        elif self.player.wizard.aether > 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                        elif self.player.wizard.aether > 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                        elif self.player.wizard.aether > 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                self.player.wizard.move(next_tile)
                        if not self.player.wizard.has_cast:
                            if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                                if enemy.wizard.health == 1:
                                    self.player.wizard.cast('Punch', enemy.wizard.tile)
                                elif enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                else:
                                    self.player.wizard.cast('Punch', enemy.wizard.tile)
                            elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                                if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                                if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                                if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                                if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        return True
                    else:
                        # NO PATH TO THEM #
                        return True





                # for charge_rune in item_list['charge_rune']:
            else:
                print('no charge runes found')
                if self.player.wizard.aether < 4 and len(item_list['mana_pot'])>0:
                    path = find_path(item_list['mana_pot'][0], False)
                else:
                    path = find_path(enemy.wizard.tile, False)
                if path is not None:
                    path.pop(0)
                    while self.player.wizard.movement_left > 0:
                        next_tile = path[0]
                        if not self.player.wizard.has_cast:
                            if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                                if enemy.wizard.health == 1:
                                    self.player.wizard.cast('Punch', enemy.wizard.tile)
                                elif enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                else:
                                    self.player.wizard.cast('Punch', enemy.wizard.tile)
                            elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                                if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                                if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                                if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                                if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        self.player.wizard.move(next_tile)
                    if not self.player.wizard.has_cast:
                        if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                            if enemy.wizard.health == 1:
                                self.player.wizard.cast('Punch', enemy.wizard.tile)
                            elif enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            else:
                                self.player.wizard.cast('Punch', enemy.wizard.tile)
                        elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                            if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                            if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                            if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                            if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                    return True
                else:
                    # NO PATH TO THEM #
                    return True


            # if you see charge rune we can reach before it runs out, rush it and push
        elif enemy_type == 'defensive':
            filtered_safe_tiles = []
            for current_tile in safe_tiles:
                dangerous = False
                if (abs(self.player.wizard.tile.x - enemy.wizard.tile.x) < 4) and (abs(self.player.wizard.tile.y - enemy.wizard.tile.y) < 4) or (current_tile.object is not None and current_tile.object.form == 'stone'):
                    dangerous = True
                if not dangerous and current_tile.type == 'floor' :
                    filtered_safe_tiles.append(current_tile)
            if not any(tile.x == self.player.wizard.tile.x and tile.y == self.player.wizard.tile.y for tile in
                       filtered_safe_tiles):
                if not self.player.wizard.has_cast:  # changed kill threshold from 5 to 8
                    if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                        if enemy.wizard.health == 1:
                            self.player.wizard.cast('Punch', enemy.wizard.tile)
                        elif enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        else:
                            self.player.wizard.cast('Punch', enemy.wizard.tile)
                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                        if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                        if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                        if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                        if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                path = find_path(enemy.wizard.tile, False)
                if path is not None:
                    while self.player.wizard.movement_left > 0 and len(path) > 1:
                        if not self.player.wizard.has_cast:  # changed kill threshold from 5 to 3
                            if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                                if enemy.wizard.health == 1:
                                    self.player.wizard.cast('Punch', enemy.wizard.tile)
                                elif enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                else:
                                    self.player.wizard.cast('Punch', enemy.wizard.tile)
                            elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                                if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                                if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                                if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                                if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        path.pop(0)
                        self.player.wizard.move(path[0])
                    if not self.player.wizard.has_cast:  # changed kill threshold from 5 to 3
                        if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                            if enemy.wizard.health == 1:
                                self.player.wizard.cast('Punch', enemy.wizard.tile)
                            elif enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            else:
                                self.player.wizard.cast('Punch', enemy.wizard.tile)
                        elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                            if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                            if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                            if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                            if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                    else:
                        return True
                else:
                    # NO PATH TO THEM , WE IN DANGER BOY #
                    if len(item_list['mana_pot']) > 0:
                        path = find_path(item_list['mana_pot'][0], False)
                    elif len(item_list['health pot']) > 0:
                        path = find_path(item_list['health_pot'][0], False)
                    if path is not None:
                        path.pop(0)
                        while self.player.wizard.movement_left > 0:
                            next_tile = path[0]
                            dangerous = True
                            for safe_tile in safe_tiles:
                                if next_tile.x == safe_tile.x and next_tile.y == safe_tile.y:
                                    dangerous = False
                            if not dangerous:
                                if not self.player.wizard.has_cast:
                                    if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                                        if enemy.wizard.health == 1:
                                            self.player.wizard.cast('Punch', enemy.wizard.tile)
                                        elif enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                        elif self.player.wizard.aether > 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                        else:
                                            self.player.wizard.cast('Punch', enemy.wizard.tile)
                                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                                        if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                        elif self.player.wizard.aether > 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                                        if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                        elif self.player.wizard.aether > 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                                        if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                        elif self.player.wizard.aether > 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                                        if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                        elif self.player.wizard.aether > 2:
                                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                self.player.wizard.move(next_tile)
                        if not self.player.wizard.has_cast:
                            if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                                if enemy.wizard.health == 1:
                                    self.player.wizard.cast('Punch', enemy.wizard.tile)
                                elif enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                else:
                                    self.player.wizard.cast('Punch', enemy.wizard.tile)
                            elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                                if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                                if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                                if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                                if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        return True
                    else:
                        # NO PATH TO THEM #
                        return True

            else:
                if self.player.wizard.aether < 4 and len(item_list['mana_pot']) > 0:
                    path = find_path(item_list['mana_pot'][0], False)
                else:
                    path = find_path(enemy.wizard.tile, False)
                if path is not None:
                    path.pop(0)
                    while self.player.wizard.movement_left > 0:
                        next_tile = path[0]
                        dangerous = True
                        for safe_tile in safe_tiles:
                            if next_tile.x == safe_tile.x and next_tile.y == safe_tile.y:
                                dangerous = False
                        if not dangerous:
                            if not self.player.wizard.has_cast:
                                if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                                    if enemy.wizard.health == 1:
                                        self.player.wizard.cast('Punch', enemy.wizard.tile)
                                    elif enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif self.player.wizard.aether > 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    else:
                                        self.player.wizard.cast('Punch', enemy.wizard.tile)
                                elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                                    if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif self.player.wizard.aether > 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                                    if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif self.player.wizard.aether > 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                                    if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif self.player.wizard.aether > 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                                    if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif self.player.wizard.aether > 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            self.player.wizard.move(next_tile)
                    if not self.player.wizard.has_cast:
                        if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                            if enemy.wizard.health == 1:
                                self.player.wizard.cast('Punch', enemy.wizard.tile)
                            elif enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            else:
                                self.player.wizard.cast('Punch', enemy.wizard.tile)
                        elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                            if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                            if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                            if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                            if enemy.wizard.health <= 3 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                    return True
                else:
                    # NO PATH TO THEM #
                    return True
            return True
        elif enemy_type == 'sustaining':
            filtered_safe_tiles = []
            laser_beam_tiles = []

            detect_lasers(enemy.wizard.tile, laser_beam_tiles)
            if enemy.wizard.tile.tile_north.type == 'floor':
                detect_lasers(enemy.wizard.tile.tile_north,laser_beam_tiles)
                if enemy.wizard.tile.tile_north.tile_north.type == 'floor':
                    detect_lasers(enemy.wizard.tile.tile_north.tile_north, laser_beam_tiles)
            if enemy.wizard.tile.tile_south.type == 'floor':
                detect_lasers(enemy.wizard.tile.tile_south,laser_beam_tiles)
                if enemy.wizard.tile.tile_south.tile_south.type == 'floor':
                    detect_lasers(enemy.wizard.tile.tile_south.tile_south, laser_beam_tiles)
            if enemy.wizard.tile.tile_east.type == 'floor':
                detect_lasers(enemy.wizard.tile.tile_east,laser_beam_tiles)
                if enemy.wizard.tile.tile_east.tile_east.type == 'floor':
                    detect_lasers(enemy.wizard.tile.tile_east.tile_east, laser_beam_tiles)
            if enemy.wizard.tile.tile_west.type == 'floor':
                detect_lasers(enemy.wizard.tile.tile_west,laser_beam_tiles)
                if enemy.wizard.tile.tile_west.tile_west.type == 'floor':
                    detect_lasers(enemy.wizard.tile.tile_west.tile_west, laser_beam_tiles)



            # if current_tile.type == 'floor':
                #     laser_beam_tiles.append(current_tile)
            for current_tile in safe_tiles:
                dangerous = False
                for laser_tile in laser_beam_tiles:
                    if current_tile.x == laser_tile.x and current_tile.y == laser_tile.y:
                        dangerous = True
                if not dangerous and current_tile.type == 'floor':
                    filtered_safe_tiles.append(current_tile)
            if self.player.wizard.health <= 6 and len(item_list['health_pot']) > 0:
                path = find_path(item_list['health_pot'][0], False)
            elif self.player.wizard.aether < 4 and len(item_list['mana_pot']) > 0:
                path = find_path(item_list['mana_pot'][0], False)
            else:
                path = find_path(enemy.wizard.tile, False)
            if path is not None:
                path.pop(0)
                while self.player.wizard.movement_left > 0:
                    next_tile = path[0]
                    dangerous = True
                    for safe_tile in safe_tiles:
                        if next_tile.x == safe_tile.x and next_tile.y == safe_tile.y:
                            dangerous = False
                    if not dangerous:
                        if not self.player.wizard.has_cast:
                            if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(
                                    enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                                if enemy.wizard.health == 1:
                                    self.player.wizard.cast('Punch', enemy.wizard.tile)
                                elif enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                else:
                                    self.player.wizard.cast('Punch', enemy.wizard.tile)
                            elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                                if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                                if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                                if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                                if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        self.player.wizard.move(next_tile)
                    else:
                        if len(item_list['health_pot']) > 0:
                            path = find_path(item_list['health_pot'][0], False)
                        elif len(item_list['mana_pot']) > 0:
                            path = find_path(item_list['mana_pot'][0], False)
                        if not self.player.wizard.has_cast:
                            if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(
                                    enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                                if enemy.wizard.health == 1:
                                    self.player.wizard.cast('Punch', enemy.wizard.tile)
                                elif enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                else:
                                    self.player.wizard.cast('Punch', enemy.wizard.tile)
                            elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                                if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                                if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                                if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                                if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif self.player.wizard.aether > 2:
                                    self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        path.pop(0)

                        next_tile = path[0]
                        self.player.wizard.move(next_tile)

                if not self.player.wizard.has_cast:
                    if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                        if enemy.wizard.health == 1:
                            self.player.wizard.cast('Punch', enemy.wizard.tile)
                        elif enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        else:
                            self.player.wizard.cast('Punch', enemy.wizard.tile)
                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                        if enemy.wizard.health <= 6 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                return True
            else:
                # NO PATH TO THEM #
                return True
        elif enemy_type == 'aggressive':
            filtered_safe_tiles = []
            for current_tile in safe_tiles:
                dangerous = False
                if (abs(self.player.wizard.tile.x-enemy.wizard.tile.x)<5) and (abs(self.player.wizard.tile.y-enemy.wizard.tile.y)<5):
                    dangerous=True
                if not dangerous and current_tile.type == 'floor':
                    filtered_safe_tiles.append(current_tile)
            if not any(tile.x == self.player.wizard.tile.x and tile.y == self.player.wizard.tile.y for tile in filtered_safe_tiles):
                if not self.player.wizard.has_cast: #changed kill threshold from 5 to 8
                    if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                        if enemy.wizard.health == 1:
                            self.player.wizard.cast('Punch', enemy.wizard.tile)
                        elif enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        else:
                            self.player.wizard.cast('Punch', enemy.wizard.tile)
                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                        if enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                        if enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                        if enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                        if enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                path = find_path(enemy.wizard.tile, False)
                while self.player.wizard.movement_left > 0 and len(path) > 1:
                    path.pop(0)
                    self.player.wizard.move(path[0])
                if not self.player.wizard.has_cast: #changed kill threshold from 5 to 8
                    if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                        if enemy.wizard.health == 1:
                            self.player.wizard.cast('Punch', enemy.wizard.tile)
                        elif enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        else:
                            self.player.wizard.cast('Punch', enemy.wizard.tile)
                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                        if enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                    elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                        if enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                        if enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                    elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                        if enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif self.player.wizard.aether > 2:
                            self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                    else:
                        return True
            else:
                if self.player.wizard.aether < 4 and len(item_list['mana_pot']) > 0:
                    path = find_path(item_list['mana_pot'][0], False)
                else:
                    path = find_path(enemy.wizard.tile, False)
                if path is not None:
                    path.pop(0)
                    while self.player.wizard.movement_left > 0:
                        next_tile = path[0]
                        dangerous = True
                        for safe_tile in safe_tiles:
                            if next_tile.x == safe_tile.x and next_tile.y == safe_tile.y:
                                dangerous = False
                        if not dangerous:
                            if not self.player.wizard.has_cast:
                                if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                                    if enemy.wizard.health == 1:
                                        self.player.wizard.cast('Punch', enemy.wizard.tile)
                                    elif enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif self.player.wizard.aether > 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    else:
                                        self.player.wizard.cast('Punch', enemy.wizard.tile)
                                elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                                    if enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif self.player.wizard.aether > 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                                    if enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif self.player.wizard.aether > 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                                    if enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif self.player.wizard.aether > 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                                    if enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                                    elif self.player.wizard.aether > 2:
                                        self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            self.player.wizard.move(next_tile)
                    if not self.player.wizard.has_cast:
                        if (abs(enemy.wizard.tile.x - self.player.wizard.tile.x) == 1 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0) or (abs(enemy.wizard.tile.y - self.player.wizard.tile.y) == 1 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0):
                            if enemy.wizard.health == 1:
                                self.player.wizard.cast('Punch', enemy.wizard.tile)
                            elif enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            else:
                                self.player.wizard.cast('Punch', enemy.wizard.tile)
                        elif enemy.wizard.tile.x - self.player.wizard.tile.x == 2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_east.type == 'floor':
                            if enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif enemy.wizard.tile.x - self.player.wizard.tile.x == -2 and self.player.wizard.tile.y - enemy.wizard.tile.y == 0 and self.player.wizard.tile.tile_west.type == 'floor':
                            if enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif enemy.wizard.tile.y - self.player.wizard.tile.y == 2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_south.type == 'floor':
                            if enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                        elif enemy.wizard.tile.y - self.player.wizard.tile.y == -2 and self.player.wizard.tile.x - enemy.wizard.tile.x == 0 and self.player.wizard.tile.tile_north.type == 'floor':
                            if enemy.wizard.health <= 8 and self.player.wizard.aether >= 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                            elif self.player.wizard.aether > 2:
                                self.player.wizard.cast('Fire Slash', enemy.wizard.tile)
                    return True
                else:
                    # NO PATH TO THEM #
                    return True

        return True
        # ENEMY WIZARD BRANCHING END #


        return True
        # <<-- /Creer-Merge: runTurn -->>

    def find_path(self, start: 'games.magomachy.tile.Tile', goal: 'games.magomachy.tile.Tile') -> List['games.magomachy.tile.Tile']:
        """A very basic path finding algorithm (Breadth First Search) that when given a starting Tile, will return a valid path to the goal Tile.

        Args:
            start (games.magomachy.tile.Tile): The starting Tile to find a path from.
            goal (games.magomachy.tile.Tile): The goal (destination) Tile to find a path to.

        Returns:
            list[games.magomachy.tile.Tile]: A list of Tiles representing the path, the the first element being a valid adjacent Tile to the start, and the last element being the goal.
        """

        if start == goal:
            # no need to make a path to here...
            return []

        # queue of the tiles that will have their neighbors searched for 'goal'
        fringe = []

        # How we got to each tile that went into the fringe.
        came_from = {}

        # Enqueue start as the first tile to have its neighbors searched.
        fringe.append(start)

        # keep exploring neighbors of neighbors... until there are no more.
        while len(fringe) > 0:
            # the tile we are currently exploring.
            inspect = fringe.pop(0)

            # cycle through the tile's neighbors.
            for neighbor in inspect.get_neighbors():
                # if we found the goal, we have the path!
                if neighbor == goal:
                    # Follow the path backward to the start from the goal and
                    # # return it.
                    path = [goal]

                    # Starting at the tile we are currently at, insert them
                    # retracing our steps till we get to the starting tile
                    while inspect != start:
                        path.insert(0, inspect)
                        inspect = came_from[inspect.id]
                    return path
                # else we did not find the goal, so enqueue this tile's
                # neighbors to be inspected

                # if the tile exists, has not been explored or added to the
                # fringe yet, and it is pathable
                if neighbor and neighbor.id not in came_from and (
                    neighbor.is_pathable()
                ):
                    # add it to the tiles to be explored and add where it came
                    # from for path reconstruction.
                    fringe.append(neighbor)
                    came_from[neighbor.id] = inspect

        # if you're here, that means that there was not a path to get to where
        # you want to go; in that case, we'll just return an empty path.
        return []

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you need additional functions for your AI you can add them here
    # <<-- /Creer-Merge: functions -->>