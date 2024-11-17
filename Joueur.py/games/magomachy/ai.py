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

        # FIND VALID CHOICES #
        def valid_choices(self):
            """This finds valid choices for the server to accept

            Returns:
                dictionary: Key: actions Value: boolean for valid
            """
            result = {
                'move':   False,
                'attack': False,
                'dash':   False,
                'push':   False,
                'punch':  False
            }
            result['move'] = self.player.wizard.movement_left > 0
            result['attack'] = self.player.wizard.aether >= 2 and not self.player.wizard.has_cast
            result['dash'] = self.player.wizard.aether >= 3 and not self.player.wizard.has_cast
            result['push'] = self.player.wizard.aether >= 4 and not self.player.wizard.has_cast
            enemy = None
            if self.game.players[0] != self.player:
                enemy = self.game.player[0]
            else:
                enemy = self.game.player[1]
            if not self.player.wizard.has_cast and (enemy.wizard.tile == self.player.wizard.tile.tile_east or enemy.wizard.tile == self.player.wizard.tile.tile_west or enemy.wizard.tile == self.player.wizard.tile.tile_north or enemy.wizard.tile == self.player.wizard.tile.tile_south):
                result['punch'] = True
            return result
        # END FUNC #


        # FIRST TURNS #
        if self.game.current_turn==0 or self.game.current_turn==1:
            wizard = 'aggressive'
            self.player.choose_wizard(wizard)
            return True
        elif self.game.current_turn==2 or self.game.current_turn==3:
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
                    if not hit_bombs and m[rr + cc * self.game.map_height].object is not None and m[rr + cc * self.game.map_height].object.form == 'explosion rune' and m[rr + cc * self.game.map_height] != end_tile: continue

                    rq.append(rr)
                    cq.append(cc)
                    visited[rr+cc*self.game.map_height]=True

                    parent[rr + cc * self.game.map_height] = r + c * self.game.map_height

                    nodes_in_next_layer += 1
            return solve()
        # PATH FINDING END #


        # ENEMY WIZARD DETECTION #
        enemy_type = self.game.players[0]
        if enemy_type == self.player:
            enemy_type = self.game.players[1]
        enemy_type = enemy_type.wizard.specialty
        # ENEMY WIZARD DETECTION END #


        # FIRST TURN? #
        first_turn = True
        if self.game.current_turn % 2 == 1:
            first_turn = False
        # FIRST TURN END #


        # ENEMY WIZARD BRANCHING #
        if enemy_type == 'strategic':
            if len(item_list['charge_rune']) > 0:
                print(f'charge runes found: {len(item_list["charge_rune"])}')
                print(f'safe_tiles size before filtering {len(safe_tiles)}')
                filtered_safe_tiles = safe_tiles
                for current_tile in safe_tiles:
                    for charge_rune in item_list["charge_rune"]:
                        if abs(current_tile.x - charge_rune.x) <= 3 or abs(current_tile.y - charge_rune.y) <= 3:
                            filtered_safe_tiles.remove(current_tile)
                            break
                    if current_tile.type == 'wall':
                        filtered_safe_tiles.remove(current_tile)

                print(f'safe_tiles size after filtering {len(filtered_safe_tiles)}')
                # temp = [
                #     tile for tile in safe_tiles
                #     if not any(  # Keep it only if there are NO matches with objects
                #         abs(tile.x - charge_rune.x) <= 3 or abs(tile.y - charge_rune.y) <= 3  # Match condition
                #         for charge_rune in item_list['charge_rune']  # Iterate through each object
                #     )
                # ]
                # safe_tiles = temp

                most_explodey_rune = max(item_list['charge_rune'], key=lambda obj: obj.object.lifetime)
                closest_explodey_rune = item_list['charge_rune'][0]
                min_dist = 100
                for charge_rune in item_list['charge_rune']:
                    if abs(charge_rune.x - self.player.wizard.tile.x) + abs(charge_rune.y - self.player.wizard.tile.y) < min_dist:
                        min_dist = abs(charge_rune.x - self.player.wizard.tile.x) + abs(charge_rune.y - self.player.wizard.tile.y)
                        print(f'min_dist : {min_dist}')
                        closest_explodey_rune = charge_rune

                # GET AWAY FROM IT!!!
                print(f'wizard tile location: {self.player.wizard.tile.x}, {self.player.wizard.tile.y}')
                print(f'closest charge rune location: {closest_explodey_rune.x}, {closest_explodey_rune.y}')
                # if self.player.wizard.tile not in safe_tiles:
                if not any(tile.x == self.player.wizard.tile.x and tile.y == self.player.wizard.tile.y for tile in filtered_safe_tiles):
                    print(f'Im in danger')
                    # IN DANGER
                    nearest_safe_tile_no_bomb = None
                    min_dist = 100
                    for safe_tile in filtered_safe_tiles:
                        if safe_tile.object is not None and safe_tile.object.form != 'charge rune':
                            if abs(safe_tile.x - self.player.wizard.tile.x) + abs(safe_tile.y - self.player.wizard.tile.y) < min_dist:
                                nearest_safe_tile_no_bomb = safe_tile

                    # nearest_safe_tile_no_bomb = min(
                    #     (safe_tile for safe_tile in safe_tiles if safe_tile.object is not None and safe_tile.object.form != 'charge rune'),
                    #     key=lambda safe_tile: abs(safe_tile.x - self.player.wizard.tile.x) + abs(safe_tile.y - self.player.wizard.tile.y)  # Manhattan distance
                    # )
                    path = find_path(nearest_safe_tile_no_bomb, False)
                    if path is None: #  CHECK PATH WITH BOMBS
                        print('no path found')
                        return True # delete this # DLETETHE THIS EDELTE THIS DELETE THIS DELETE THIS DELETE THIS
                    else:
                        print('path found')
                        turns_to_traverse = len(path)-1 // 2 + len(path)-1 % 2
                        turns_till_explosion = (10 - closest_explodey_rune.object.lifetime) // 2 + 1
                        if turns_till_explosion < turns_to_traverse:
                            print('i have to dash (im a liar)')
                            # PATH TOO LONG WITHOUT DASHING #
                            if self.player.wizard.aether < 4 or turns_till_explosion < turns_to_traverse-1:
                                # PATH TOO LONG FOR ONE DASH #
                                if self.player.wizard.aether < 7 or turns_till_explosion < turns_to_traverse-2 :
                                    # PATH TOO LONG FOR TWO DASH #
                                    # PATH WITH BOMBS (IMPLEMENT) #

                                    # ========================== PATH WITH BOMBS ========================== #

                                    path = find_path(nearest_safe_tile_no_bomb, True)
                                    if path is None:
                                        return True # CHANGE CHANGE CHANGE CHANGE
                                    else:
                                        turns_to_traverse = len(path) - 1 // 2 + len(path) - 1 % 2
                                        if turns_till_explosion < turns_to_traverse:
                                            # PATH TOO LONG WITHOUT DASHING #
                                            if self.player.wizard.aether < 4 or turns_till_explosion < turns_to_traverse-1:
                                                # ONE DASH NOT POSSIBLE TO SAVE #
                                                if self.player.wizard.aether < 7 or turns_till_explosion < turns_to_traverse-2:
                                                    # TWO DASH NOT POSSIBLE TO SAVE #

                                                    # ========================== SPACE WITH A BOMB ========================== #

                                                    nearest_safe_tile_with_bomb = min(
                                                        filtered_safe_tiles,
                                                        key=lambda safe_tile: abs(safe_tile.x - self.player.wizard.tile.x) + abs(safe_tile.y - self.player.wizard.tile.y)
                                                    )
                                                    path = find_path(nearest_safe_tile_with_bomb, False)
                                                    if path is None:
                                                        return True # CHANCE HCANGE CHANGE CHANGE CHANGE
                                                    else:
                                                        turns_to_traverse = len(path) - 1 // 2 + len(path) - 1 % 2
                                                        if turns_till_explosion < turns_to_traverse:
                                                            # PATH TOO LONG WITHOUT DASHING #
                                                            if self.player.wizard.aether < 4 or turns_till_explosion < turns_to_traverse-1:
                                                                # ONE DASH DOES NOT WORK #
                                                                if self.player.wizard.aether < 7 or turns_till_explosion < turns_to_traverse-2:
                                                                    # TWO DASH DOES NOT WORK #

                                                                    # ========================== SPACE WITH A BOMB HITS BOMBS ========================== #
                                                                    path = find_path(nearest_safe_tile_with_bomb, True)
                                                                    if path is None:
                                                                        return True # CHANGE CHANGE CHANGE
                                                                    else:
                                                                        turns_to_traverse = len(path) - 1 // 2 + len(path) - 1 % 2
                                                                        if turns_till_explosion < turns_to_traverse:
                                                                            # PATH TOO LONG WITHOUT DASHING #
                                                                            if self.player.wizard.aether < 4 or turns_till_explosion < turns_to_traverse-1:
                                                                                # ONE DASH NOT POSSIBLE #
                                                                                if self.player.wizard.aether < 7 or turns_till_explosion < turns_to_traverse-2:
                                                                                    # TWO DASH NOT POSSIBLE #

                                                                                    # ========================== NEAREST USEABLE POTION ========================== #
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
                                path.pop(0)
                                self.player.wizard.move(path[0])
                            return True
                else:
                    print(f'No danger! (im probably a liar)')






                # for charge_rune in item_list['charge_rune']:
            else:
                print('no charge runes found')

            # if you see charge rune we can reach before it runs out, rush it and push

        elif enemy_type == 'defensive':
            return True
        elif enemy_type == 'sustaining':
            return True
        elif enemy_type == 'aggressive':
            return True
        # ENEMY WIZARD BRANCHING END #


        # VALID_CHOICES EXAMPLE
        # choices = valid_choices(self)
        # if choices['attack'] and it would kill them:
        #     self.player.wizard.spell('Scorching Slash',enemycoords)



        # def valid_actions(self):
        #     if self.

        # notChosen = True
        # print("Your turn! Here's the map:")
        # while(True):
        #     self.player.choose_wizard("map")
        #     if not self.player.wizard and notChosen:
        #         print("WARNING: You have not chosen a wizard. Do that ASAP!")
        #     elif self.player.wizard:
        #         print("HEALTH:",self.player.wizard.health)
        #         print("AETHER",self.player.wizard.aether)
        #
        #     choice = input('What next? Type help for a list of commands.')
        #     components = choice.split()
        #     if len(components) == 0:
        #         pass
        #     elif components[0] == 'help':
        #         print("Valid commands:")
        #         print("choose [wizardClass]: pick a class at the start of the game")
        #         print("move [up, down, right, left]: move in specified direction.")
        #         print("cast [spell] [x] [y]: cast spell at specified coordinate")
        #         print("spells [wizardClass]: see spell list for given wizard")
        #     elif components[0] == 'spells':
        #         print("Punch: 0 aether, 1 damage, 1 range")
        #         if components[1] == 'aggressive':
        #             print("Fire Slash: 2 aether, 3 damage, 2 range")
        #             print("Thunderous Dash: 3 aether, boosts speed by 2 for 1 turn, lets you swap places with enemy if you pass them")
        #             print("Furious Telekinesis: 4 aether, 1 range, pushes item away, forces other wizard to use it if it hits them")
        #         elif components[1] == 'defensive':
        #             print("Rock Lob: 2 aether, 2 damage, exactly 2 or 3 tile range")
        #             print("Force Push: 3 aether, pushes adjacent opponent up to 4 spaces, using items along the way. 3 damage if they hit a wall")
        #             print("Stone Summon: 4 aether, 1 range, summon impassable stone for 10 total turns")
        #         elif components[1] == 'sustaining':
        #             print("Calming Blast: 3 aether, fires projectile, on hit steal 1 HP and decrease speed for 1 turn")
        #             print("Teleport: 3 aether, 2 range, move to target tile. Also costs 1 movement.")
        #             print("Dispel Magic: 3 aether, 1 range, deletes target item/rune")
        #         elif components[1] == 'strategic':
        #             print("Explosion Rune: 2 aether, 4 damage, 1 range, blows up for 4 damage when stepped on")
        #             print("Heal Rune: 5 aether, 1 range, heals for 5 HP when stepped on (up to max)")
        #             print("Teleport Rune: 3 aether (0 if rune already placed), 1 range, places teleport rune if none exists, or teleports you to it otherwise")
        #             print("Charge Rune: 4 aether, infinite range, blows up for 5 damage in 3 tile radius after 5 turns")
        #             print("Force Pull: 3 aether, 4 range, fires projectile that does no damage, but drags opponent toward you if it hits them, using runes along the way")
        #         else:
        #             print("That's not a wizard! Choose aggressive, defensive, sustaining, or strategic.")
        #     elif components[0] == 'end':
        #         print("Ending turn...")
        #         break;
        #     elif components[0] == 'choose':
        #         wizard = None
        #
        #         if self.player.wizard:
        #             print("You've already chosen a wizard!")
        #         elif len(components) != 2:
        #             print("Wrong number of arguments!")
        #         elif (components[1] == 'aggressive'
        #         or components[1] == 'defensive'
        #         or components[1] == 'sustaining'
        #         or components[1] == 'strategic'):
        #             wizard = components[1]
        #         else:
        #             print("Choose aggressive, defensive, sustaining, or strategic.")
        #
        #         if wizard:
        #             self.player.choose_wizard(wizard)
        #             notChosen = False
        #     elif components[0] == 'move':
        #         tile = None
        #         if len(components) != 2:
        #             tile = None
        #         elif components[1] == 'left':
        #             tile = self.player.wizard.tile.tile_west
        #         elif components[1] == 'right':
        #             tile = self.player.wizard.tile.tile_east
        #         elif components[1] == 'down':
        #             tile = self.player.wizard.tile.tile_south
        #         elif components[1] == 'up':
        #             tile = self.player.wizard.tile.tile_north
        #         if tile:
        #             self.player.wizard.move(tile)
        #         else:
        #             print("Command not executed. Choose a direction.")
        #     elif components[0] == 'cast':
        #         #if self.player.wizard.has_cast:
        #             #print("You've already cast a spell this turn...")
        #         if len(components) < 4 or len(components) > 5:
        #             print("Wrong number of arguments")
        #         else:
        #             spell = components[1]
        #             x = components[2]
        #             y = components[3]
        #             if len(components) == 5:
        #                 spell = components[1] + " " + components[2]
        #                 x = components[3]
        #                 y = components[4]
        #             if not x.isdigit() or not y.isdigit():
        #                 print("Choose actual coordinates...")
        #             else:
        #                 tile = self.game.get_tile_at(int(x),int(y))
        #                 self.player.wizard.cast(spell,tile)
        #     else:
        #         print("Command not recognized, try again")
        # # <<-- Creer-Merge: runTurn -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # # Put your game logic here for runTurn
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