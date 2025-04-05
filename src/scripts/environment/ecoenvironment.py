import random
import time

from gymnasium.spaces import Discrete, Dict
from ray.rllib.env.multi_agent_env import MultiAgentEnv

from src.scripts.agents.agent import Agent
from src.scripts.environment.tile import Tile


class EcosystemEnv(MultiAgentEnv):
    def __init__(self, width=10, height=10, num_agents=5, visualizer=None):
        super().__init__()
        self.width = width
        self.height = height
        self.visualizer = visualizer
        if self.visualizer:
            self.visualizer.set_environment(self)

        # Initialize the grid
        self.tiles = [[Tile() for _ in range(height)] for _ in range(width)]
        self.tiles = [[Tile(terrain=random.randint(0, 0), has_food=random.choice([True, False, False]))
                       for _ in range(height)] for _ in range(width)]

        # Initialize agents with random positions
        self.my_agents = {f"agent_{i}": Agent(f"agent_{i}", random.randint(0, width - 1), random.randint(0, height - 1))
                          for i in range(num_agents)}

        self.agents = self.possible_agents = list(self.my_agents.keys())

        # Define action and observation spaces
        self.observation_spaces = {agent_id: Dict({
            "x": Discrete(width),
            "y": Discrete(height),
            "terrain": Discrete(3)  # Terrain types: 0 - Normal, 1 - Water, 2 - Mountain
        }) for agent_id in self.agents}

        self.action_spaces = {agent_id: Discrete(5)  # Actions: Stay, Up, Down, Left, Right
                              for agent_id in self.agents}

    def get_tile(self, x, y):
        return self.tiles[x][y]

    def reset(self, **kwargs):
        for agent in self.my_agents.values():
            agent.x = random.randint(0, self.width - 1)
            agent.y = random.randint(0, self.height - 1)
        return {agent_id: {"x": agent.x, "y": agent.y, "terrain": random.randint(0, 2)}
                for agent_id, agent in self.my_agents.items()}, {}

    def step(self, action_dict):
        rewards, dones, infos = {}, {}, {}

        for agent_id, action in action_dict.items():
            if agent_id in self.agents:
                agent = self.my_agents[agent_id] # Get the agent from the dictionary
                agent.move(action, self.width, self.height, self.tiles)  # Move agent based on action
                # rewards[agent_id] = 0  # Temporary reward system
                # dones[agent_id] = False
                tile = self.get_tile(agent.x, agent.y)  # Get new tile after movement

                if tile.has_food:
                    agent.heal(20)  # Gain health when finding food
                    tile.has_food = False  # Consume food
                    rewards[agent_id] = 10  # Reward for finding food
                else:
                    agent.take_damage(5)  # Lose health when no food is found
                    rewards[agent_id] = -2  # Small penalty for not finding food

                # Check if agent has died
                if agent.get_health() <= 0:
                    dones[agent_id] = True
                    self.agents.remove(agent_id)  # Remove dead agent from simulation
                else:
                    dones[agent_id] = False
                infos[agent_id] = {}

        # Return updated observations
        observations = {agent_id: self._get_obs(agent_id) for agent_id in self.agents}
        dones["__all__"] = False  # Set the global termination flag (adjust as needed)
        return observations, rewards, dones, infos

    def _get_obs(self, agent_id):
        # Get the agent's observation (position and terrain type)
        agent = self.my_agents[agent_id]
        x, y = agent.get_position()
        return {"x": x, "y": y, "terrain": self.tiles[x][y].terrain}

    def run(self, steps, sleep_time=0.1):
        for _ in range(steps):
            time.sleep(sleep_time)

            # Randomly move each agent
            action_dict = {}
            for agent_id in self.agents:
                action_dict[agent_id] = random.randint(1, 4)  # Random action between 1 and 4 (up, down, left, right)

            # Apply actions
            self.step(action_dict)

            # Visualize the step
            if self.visualizer:
                self.visualizer.update()
