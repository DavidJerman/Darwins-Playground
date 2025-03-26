import random
import time
from gymnasium.spaces import Discrete, Dict
from ray.rllib.env.multi_agent_env import MultiAgentEnv
from src.scripts.environment.tile import Tile


class EcosystemEnv(MultiAgentEnv):
    def __init__(self, width=10, height=10, num_agents=5, visualizer=None):
        super().__init__()
        self.width = width
        self.height = height
        self.num_agents = num_agents
        self.visualizer = visualizer
        self.visualizer.set_environment(self)

        # Initialize the grid
        self.tiles = [[Tile() for _ in range(height)] for _ in range(width)]

        # Initialize agents with random positions
        self.agents = {f"agent_{i}": {'x': random.randint(0, width - 1), 'y': random.randint(0, height - 1)} for i in
                       range(num_agents)}

        # Define action and observation spaces
        self.action_space = Discrete(5)  # Actions: Stay, Up, Down, Left, Right
        self.observation_space = Dict({
            "x": Discrete(width),
            "y": Discrete(height),
            "terrain": Discrete(3)  # Terrain types: 0 - Normal, 1 - Water, 2 - Mountain
        })

    @property
    def num_agents(self):
        return self._num_agents

    @num_agents.setter
    def num_agents(self, value):
        if value < 1:
            raise ValueError("Number of agents must be at least 1")
        self._num_agents = value

    def get_tile(self, x, y):
        return self.tiles[x][y]

    def reset(self, **kwargs):
        # Reset agents' positions randomly
        self.agents = {f"agent_{i}": {'x': random.randint(0, self.width - 1), 'y': random.randint(0, self.height - 1)}
                       for i in range(self.num_agents)}
        return {agent_id: self._get_obs(agent_id) for agent_id in self.agents}

    def step(self, action_dict):
        rewards, dones, infos = {}, {}, {}

        for agent_id, action in action_dict.items():
            if agent_id in self.agents:
                self._apply_action(agent_id, action)
                rewards[agent_id] = 0  # Temporary reward system
                dones[agent_id] = False
                infos[agent_id] = {}

        # Return updated observations
        return {agent_id: self._get_obs(agent_id) for agent_id in self.agents}, rewards, dones, infos

    def _apply_action(self, agent_id, action):
        # Move the agent according to the action taken
        x, y = self.agents[agent_id]['x'], self.agents[agent_id]['y']

        if action == 1 and y > 0 and self._can_move(x, y - 1):  # Up
            self.agents[agent_id]['y'] -= 1
        elif action == 2 and y < self.height - 1 and self._can_move(x, y + 1):  # Down
            self.agents[agent_id]['y'] += 1
        elif action == 3 and x > 0 and self._can_move(x - 1, y):  # Left
            self.agents[agent_id]['x'] -= 1
        elif action == 4 and x < self.width - 1 and self._can_move(x + 1, y):  # Right
            self.agents[agent_id]['x'] += 1

    def _can_move(self, x, y):
        # Example: check if tile is not a mountain (impassable)
        return self.tiles[x][y].terrain != 2

    def _get_obs(self, agent_id):
        # Get the agent's observation (position and terrain type)
        x, y = self.agents[agent_id]['x'], self.agents[agent_id]['y']
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
