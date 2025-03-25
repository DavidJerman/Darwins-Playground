class Tile:
    def __init__(self, terrain_type='grass', temperature=20, resources=0):
        self.terrain_type = terrain_type
        self.temperature = temperature
        self.resources = resources
        self.agents = []

    def add_agent(self, agent):
        self.agents.append(agent)

    def remove_agent(self, agent):
        self.agents.remove(agent)

    def __repr__(self):
        return f"Tile({self.terrain_type}, Temp: {self.temperature}, Resources: {self.resources})"
