import random


class Agent:
    def __init__(self, x, y, environment):
        self.x = x
        self.y = y
        self.environment = environment

    def act(self):
        new_x = max(0, min(self.environment.width - 1, self.x + random.choice([-1, 0, 1])))
        new_y = max(0, min(self.environment.height - 1, self.y + random.choice([-1, 0, 1])))

        self.environment.remove_agent(self)
        self.x, self.y = new_x, new_y

        self.environment.add_agent(self)
