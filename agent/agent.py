from game.player import Player, Direction
import random
from config import TILE_SIZE

class Agent(Player):
    def __init__(self, image, x, y, game_map, team_id=0):
        super().__init__(image, x, y, a=None, game_map=game_map)
        self.team_id = team_id
        self.action = None
        self.move_dir = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])

    def decide_action(self):
        # Tu na razie losowa decyzja, później RL
        import random
        self.action = random.choice(["UP", "DOWN", "LEFT", "RIGHT", "IDLE"])

    def apply_action(self):
        acc = self.ACC
        if self.action == "UP":
            self.VEL_Y -= acc
            self.DIR = Direction.UP
        elif self.action == "DOWN":
            self.VEL_Y += acc
            self.DIR = Direction.DOWN
        elif self.action == "LEFT":
            self.VEL_X -= acc
            self.DIR = Direction.LEFT
        elif self.action == "RIGHT":
            self.VEL_X += acc
            self.DIR = Direction.RIGHT

    def get_movement(self):
        self.decide_action()
        self.apply_action()
        self.clamp_velocity()
        self.moving = (self.VEL_X != 0 or self.VEL_Y != 0)
        return self.VEL_X, self.VEL_Y

    def get_bounds(self):
        left = self.x // TILE_SIZE
        top = self.y // TILE_SIZE
        right = (self.x + TILE_SIZE) // TILE_SIZE
        bottom = (self.y + TILE_SIZE) // TILE_SIZE
        return int(left), int(top), int(right), int(bottom)