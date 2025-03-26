import random

class Agent:
    def __init__(self, agent_id, x, y):
        self.agent_id = agent_id
        self.x = x
        self.y = y
        self.action_space = 5  # Stay, Up, Down, Left, Right

    def move(self, action, width, height, tiles):
        # Handle movement logic for the agent
        if action == 1 and self.y > 0 and self._can_move(self.x, self.y - 1, tiles):  # Up
            self.y -= 1
        elif action == 2 and self.y < height - 1 and self._can_move(self.x, self.y + 1, tiles):  # Down
            self.y += 1
        elif action == 3 and self.x > 0 and self._can_move(self.x - 1, self.y, tiles):  # Left
            self.x -= 1
        elif action == 4 and self.x < width - 1 and self._can_move(self.x + 1, self.y, tiles):  # Right
            self.x += 1

    @staticmethod
    def _can_move(x, y, tiles):
        # Example: check if tile is not a mountain (impassable)
        return tiles[x][y].terrain != 2

    def get_position(self):
        return self.x, self.y