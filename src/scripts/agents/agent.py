import random

class Agent:
    def __init__(self, agent_id, x, y, max_health=100, hunger_damage=5, food_heal=20):
        self.agent_id = agent_id
        self.x = x
        self.y = y
        self.action_space = 5  # Stay, Up, Down, Left, Right
        self.max_health = max_health
        self.current_health = max_health
        self.hunger_damage = hunger_damage
        self.food_heal = food_heal

    def move(self, action, width, height, tiles):
        new_x, new_y = self.x, self.y

        # Handle movement logic for the agent
        if action == 1 and self.y > 0 and self._can_move(self.x, self.y - 1, tiles):  # Up
            self.y -= 1
        elif action == 2 and self.y < height - 1 and self._can_move(self.x, self.y + 1, tiles):  # Down
            self.y += 1
        elif action == 3 and self.x > 0 and self._can_move(self.x - 1, self.y, tiles):  # Left
            self.x -= 1
        elif action == 4 and self.x < width - 1 and self._can_move(self.x + 1, self.y, tiles):  # Right
            self.x += 1

        # Check for food and adjust health accordingly
        if tiles[self.x][self.y].has_food:
            self.heal(self.food_heal)
            tiles[self.x][self.y].has_food = False  # Consume the food
            print(f"Agent {self.agent_id} found food! Health increased to {self.current_health}.")
        else:
            self.take_damage(self.hunger_damage)
            print(f"Agent {self.agent_id} found no food. Health decreased to {self.current_health}.")

    def take_damage(self, damage_amount):
        self.current_health = max(0, self.current_health - damage_amount)

    def heal(self, heal_amount):
        self.current_health = min(self.max_health, self.current_health + heal_amount)

    @staticmethod
    def _can_move(x, y, tiles):
        # Example: check if tile is not a mountain (impassable)
        return tiles[x][y].terrain != 2

    def get_position(self):
        return self.x, self.y

    def get_health(self):
        return self.current_health