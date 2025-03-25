from src.scripts.environment.tile import Tile

import random
import time


class Environment:
    def __init__(self, width, height, visualizer=None):
        self.width = width
        self.height = height
        self.tiles = [[Tile() for _ in range(height)] for _ in range(width)]
        self.agents = []
        self.visualizer = visualizer

    def get_tile(self, x, y):
        return self.tiles[x][y]

    def add_agent(self, agent):
        tile = self.get_tile(agent.x, agent.y)
        tile.add_agent(agent)
        self.agents.append(agent)

    def remove_agent(self, agent):
        tile = self.get_tile(agent.x, agent.y)
        tile.remove_agent(agent)
        self.agents.remove(agent)

    def step(self):
        for agent in self.agents:
            agent.act()
        if self.visualizer:
            self.visualizer.update()

    def run(self, steps, sleep_time=0.1):
        for _ in range(steps):
            self.step()
            self.sleep(sleep_time)

    @staticmethod
    def sleep(duration):
        time.sleep(duration)

    def get_random_position(self):
        return random.randint(0, self.width - 1), random.randint(0, self.height - 1)
