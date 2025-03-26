class Tile:
    def __init__(self, terrain=0):
        self.terrain = terrain  # 0: Normal, 1: Water, 2: Mountain
        self.agents = []

    def add_agent(self, agent):
        self.agents.append(agent)

    def remove_agent(self, agent):
        self.agents.remove(agent)
