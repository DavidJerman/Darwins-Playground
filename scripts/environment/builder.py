from environment import *


class EnvironmentBuilder:
    def __init__(self, width, height):
        self.environment = Environment(width, height)

    def add_resources(self, density=0.1):
        for _ in range(int(self.environment.width * self.environment.height * density)):
            x, y = self.environment.get_random_position()
            self.environment.grid[y, x] = 1  # Representing resources
        return self

    def add_agents(self, agent_class, count):
        for _ in range(count):
            x, y = self.environment.get_random_position()
            agent = agent_class(x, y)
            self.environment.add_agent(agent)
        return self

    def build(self):
        return self.environment
