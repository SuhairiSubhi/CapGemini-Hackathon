"""Stratégie d'exemple : un joueur qui cherche des items."""
from game import Action, Game, Player, Tile, entities
from random import choice

class Nautilus(Player):
    """Le célèbre sous-marins"""

    NAME = "5 - Nautilus"

    def play(self, game: Game) -> Action:
        """Cherche les objets les plus proches et se mettre en sécurité."""
        # Renvoie `True` si la destination est acceptable
        accept_target = (
            lambda x, y: game.background[y][x] == Tile.FLOOR
            and game.tile_grid[y][x].is_bonus()
        )

        # Renvoie `True` si le chemin est sûr
        is_safe = (
            lambda x, y: game.background[y][x] == Tile.FLOOR
            and not game.tile_grid[y][x].is_dangerous()
        )

        # Si on est en danger, on cherche un endroit sûr
        if game.background[self.y][self.x] == Tile.DAMAGED_FLOOR:
            accept_target = is_safe

            # N'importe quel endroit où on peut marcher est sûr
            is_safe = lambda x, y: game.background[y][x].is_floor()

        # Matrice des cases explorées par la recherche de chemin
        explored = [[False for x in range(game.size)] for y in range(game.size)]
        explored[self.y][self.x] = True

        # Tous les chemins possibles sans demi-tour depuis la case actuelle
        paths = []

        # On regarde quelles sont les cases atteignables depuis la case actuelle
        for direction in (
            Action.MOVE_UP,
            Action.MOVE_DOWN,
            Action.MOVE_LEFT,
            Action.MOVE_RIGHT,
        ):

            # Coordonnées de la case voisine
            x, y = direction.apply((self.x, self.y))

            # Si on peut aller dans cette direction, on explore les possibilités offertes
            if self.is_action_valid(direction):
            # On retient quelle est la direction de départ
                paths.append((x, y, direction))
                explored[y][x] = True

        # Cherche joueur à attaquer

        for direction in (
            Action.MOVE_UP,
            Action.MOVE_DOWN,
            Action.MOVE_LEFT,
            Action.MOVE_RIGHT,
            ):
            # Coordonnées de l'ennemi
            x,y = self.x, self.y
            for chercheur in range(1,4):
                if direction == Action.MOVE_UP and game.background[y][x] != Tile.WALL :
                        x, y = direction.apply((x,y))
                elif direction == Action.MOVE_DOWN and game.background[y][x] != Tile.WALL :
                        x, y = direction.apply((x,y))
                elif direction == Action.MOVE_LEFT and game.background[y][x] != Tile.WALL :
                        x, y = direction.apply((x,y))
                elif direction == Action.MOVE_RIGHT and game.background[y][x] != Tile.WALL :
                        x, y = direction.apply((x,y))
                else :
                        None;

            if game.tile_grid[y][x].is_player():
                if self.is_action_valid(Action.MOVE_UP) and direction == Action.MOVE_UP and self.action != Action.MOVE_UP:
                    return Action.MOVE_UP
                elif self.is_action_valid(Action.MOVE_DOWN) and direction == Action.MOVE_DOWN and self.action != Action.MOVE_DOWN:
                    return Action.MOVE_DOWN
                elif self.is_action_valid(Action.MOVE_RIGHT) and direction == Action.MOVE_RIGHT and self.action != Action.MOVE_RIGHT:
                    return Action.MOVE_RIGHT
                elif self.is_action_valid(Action.MOVE_LEFT) and direction == Action.MOVE_LEFT and self.action != Action.MOVE_LEFT:
                    return Action.MOVE_LEFT
                else:
                    return direction.to_attack()
            else:
                None

        # Cherche boule a feu
        for direction in (
            Action.MOVE_UP,
            Action.MOVE_DOWN,
            Action.MOVE_LEFT,
            Action.MOVE_RIGHT,
        ):


            # Coordonnées de boule de feu
            x,y = self.x, self.y
            for chercheur in range(1,5):
                    if direction == Action.MOVE_UP and game.background[y][x] != Tile.WALL:
                        x, y = direction.apply((x,y))
                    elif direction == Action.MOVE_DOWN and game.background[y][x] != Tile.WALL :
                        x, y = direction.apply((x,y))
                    elif direction == Action.MOVE_LEFT and game.background[y][x] != Tile.WALL :
                        x, y = direction.apply((x,y))
                    elif direction == Action.MOVE_RIGHT and game.background[y][x] != Tile.WALL :
                        x, y = direction.apply((x,y))
                    else :
                        None;

                    if game.background[y][x] == Tile.SUPER_FIREBALL or game.background[y][x] == Tile.FIREBALL:
                        break

            if isinstance(game.tile_grid[y][x], entities.Fireball) and direction == Action.MOVE_UP:
                if self.is_action_valid(Action.MOVE_RIGHT) and is_safe(x, y):
                    return Action.MOVE_RIGHT
                elif self.is_action_valid(Action.MOVE_LEFT) and is_safe(x, y):
                    return Action.MOVE_LEFT
                elif self.is_action_valid(Action.MOVE_DOWN):
                    return Action.MOVE_DOWN
                else:
                    None
            elif isinstance(game.tile_grid[y][x], entities.Fireball) and direction == Action.MOVE_DOWN:
                if self.is_action_valid(Action.MOVE_RIGHT) and is_safe(x, y):
                    return Action.MOVE_RIGHT
                elif self.is_action_valid(Action.MOVE_LEFT) and is_safe(x, y):
                    return Action.MOVE_LEFT
                elif self.is_action_valid(Action.MOVE_UP):
                    return Action.MOVE_UP
                else:
                    None
            elif isinstance(game.tile_grid[y][x], entities.Fireball) and direction == Action.MOVE_RIGHT:
                if self.is_action_valid(Action.MOVE_UP) and is_safe(x, y):
                    return Action.MOVE_UP
                elif self.is_action_valid(Action.MOVE_DOWN) and is_safe(x, y):
                    return Action.MOVE_DOWN
                elif self.is_action_valid(Action.MOVE_LEFT):
                    return Action.MOVE_LEFT
                else:
                    None
            elif isinstance(game.tile_grid[y][x], entities.Fireball) and direction == Action.MOVE_LEFT:
                if self.is_action_valid(Action.MOVE_UP) and is_safe(x, y):
                    return Action.MOVE_UP
                elif self.is_action_valid(Action.MOVE_DOWN) and is_safe(x, y):
                    return Action.MOVE_DOWN
                elif self.is_action_valid(Action.MOVE_RIGHT):
                    return Action.MOVE_RIGHT
                else:
                    None
            else:
                None




        # Tant qu'il existe des chemins possibles
        while len(paths) > 0:

            # On regarde un chemin envisageable
            x, y, direction = paths.pop(0)

            # Si sa destination est acceptable, on va dans la direction de départ
            # pour s'y rendre
            if accept_target(x, y):
                return direction

            # On regarde les 4 cases potentiellement atteignable depuis le bout du
            # chemin considéré
            for d in (
                Action.MOVE_UP,
                Action.MOVE_DOWN,
                Action.MOVE_LEFT,
                Action.MOVE_RIGHT,
            ):
                # On regarde la case voisine
                new_x, new_y = d.apply((x, y))

                # Si le chemin est sécurisé, on envisage d'y aller
                if is_safe(new_x, new_y) and not explored[new_y][new_x]:
                    paths.append((new_x, new_y, direction))  # Direction d'origine
                    explored[new_y][new_x] = True
        return Action.WAIT
