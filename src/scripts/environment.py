import copy
import random
import pygame
import numpy as np

from ray.rllib.env.multi_agent_env import MultiAgentEnv
import gymnasium as gym

from agent import Agent
from terrain_generator import generate_terrain, print_terrain


class GridFoodSearchEnv(MultiAgentEnv):
    VERBOSE = False

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, config=None):
        super().__init__()

        config = config or {}

        # --- Grid config ---
        self.width = config.get("width", 10)
        self.height = config.get("height", 10)
        self._max_episode_steps = config.get("max_steps", 50)

        self.original_tiles = generate_terrain(self.width, self.height)
        self.tiles = copy.deepcopy(self.original_tiles)
        print_terrain(self.tiles, self.width, self.height)
        # ---

        # --- Get render_mode from config ---
        self.render_mode = config.get("render_mode", None)
        self.window = None
        self.clock = None
        self.cell_size = 50  # Size of each grid cell in pixels
        self._renderer_initialized = False
        # ---

        # Define the agents in the game.
        self.agents = self.possible_agents = [f"agent_{i}" for i in range(config.get("num_agents", 2))]
        self.my_agents = {agent: Agent(agent, random.randint(0, self.width - 1), random.randint(0, self.height - 1))
                          for agent in self.agents}

        obs_space_dict = {
            "agent_position": gym.spaces.Box(low=0.0, high=1.0, shape=(2,), dtype=np.float32),
            "food_position": gym.spaces.Box(low=0.0, high=1.0, shape=(2,), dtype=np.float32),
            "terrain": gym.spaces.Discrete(3),
        }
        self.observation_spaces = {
            agent_id: gym.spaces.Dict(obs_space_dict)
            for agent_id in self.agents
        }

        self.action_spaces = {
            agent_id: gym.spaces.Discrete(4)
            for agent_id in self.agents
        }

        self.agent_positions = {}
        self.food_position = None
        self._steps_taken = 0

        print(f"Env Initialized: ... render_mode={self.render_mode}")

    def get_tile(self, x, y):
        return self.tiles[x][y]

    def get_tiles(self):
        return self.tiles

    def _get_random_position(self, existing_positions=None):
        """Helper to get a random unoccupied position."""
        existing_positions = existing_positions or set()
        while True:
            pos = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if pos not in existing_positions:
                return pos

    def find_food(self, agent):
        min_dist = float('inf')
        closest_food_pos = None
        ax, ay = agent.x, agent.y

        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[x][y]
                if tile.has_food:
                    dist = abs(ax - x) + abs(ay - y)
                    if dist < min_dist:
                        min_dist = dist
                        closest_food_pos = (x, y)

        return closest_food_pos

    def return_food_positions(self):
        positions = []
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x][y].has_food:
                    positions.append((x, y))
        return positions

    def _get_observations(self):
        """Returns the observation dictionary for all agents."""
        obs = {}

        for agent_id in self.agents:
            agent = self.my_agents[agent_id]

            ax, ay = agent.x, agent.y

            norm_ax = ax / (self.width - 1) if self.width > 1 else 0.0
            norm_ay = ay / (self.height - 1) if self.height > 1 else 0.0
            closest = self.find_food(agent)
            fx, fy = closest if closest else (agent.x, agent.y)
            norm_fx = fx / (self.width - 1) if self.width > 1 else 0.0
            norm_fy = fy / (self.height - 1) if self.height > 1 else 0.0

            norm_agent_pos = np.array([norm_ax, norm_ay], dtype=np.float32)
            norm_food_pos = np.array([norm_fx, norm_fy], dtype=np.float32)

            obs_this_agent = {
                "agent_position": norm_agent_pos,
                "food_position": norm_food_pos,
                "terrain": self.tiles[ax][ay].terrain,
            }
            obs[agent_id] = obs_this_agent
        return obs

    def reset(self, *, seed=None, options=None):
        self.tiles = copy.deepcopy(self.original_tiles)

        used = set()
        for agent in self.my_agents.values():
            pos = self._get_random_position(used)
            used.add(pos)
            agent.reset()
            agent.x, agent.y = pos

        self._steps_taken = 0

        observations = self._get_observations()
        infos = {agent_id: {} for agent_id in self.agents}

        return observations, infos

    def step(self, action_dict):
        rewards = {agent_id: 0.0 for agent_id in self.agents}
        terminateds = {"__all__": False}
        truncateds = {"__all__": False}
        infos = {agent_id: {} for agent_id in self.agents}

        self._steps_taken += 1

        for agent_id, action in action_dict.items():
            agent = self.my_agents[agent_id]
            tile = self.get_tile(agent.x, agent.y)

            food_pos = self.find_food(agent)
            if food_pos is None:
                prev_dist = None
            else:
                prev_dist = abs(agent.x - food_pos[0]) + abs(agent.y - food_pos[1])

            agent.move(action, self.width, self.height, self.tiles)

            if food_pos is None:
                dist_reward = 0
            else:
                new_dist = abs(agent.x - food_pos[0]) + abs(agent.y - food_pos[1])
                dist_reward = 1.0 if new_dist < prev_dist else -1.0

            if tile.has_food:
                agent.heal(20)
                tile.has_food = False
                rewards[agent_id] += 100.0
                terminateds["__all__"] = True
                infos[agent_id]["found_food"] = True
            else:
                agent.take_damage(5)
                rewards[agent_id] -= 0.1
                rewards[agent_id] += dist_reward

            agent.move(action, self.width, self.height, self.tiles)

        # Check for truncation (max steps)
        if self._steps_taken >= self._max_episode_steps:
            truncateds["__all__"] = True

        observations = self._get_observations()

        final_terminateds = {agent_id: terminateds["__all__"] for agent_id in self.agents}
        final_truncateds = {agent_id: truncateds["__all__"] for agent_id in self.agents}
        final_terminateds["__all__"] = terminateds["__all__"]
        final_truncateds["__all__"] = truncateds["__all__"]

        return observations, rewards, final_terminateds, final_truncateds, infos

    def _init_render(self):
        if self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(
                (self.width * self.cell_size, self.height * self.cell_size)
            )
            pygame.display.set_caption("Grid Food Search")
            if self.clock is None:
                self.clock = pygame.time.Clock()
        self._renderer_initialized = True
        print("Pygame renderer initialized.")

    def _render_frame(self):
        if self.render_mode is None:
            gym.logger.warn(
                "You are calling render method without specifying any render mode. "
                "You can specify the render_mode at initialization, "
                f'e.g. env = {type(self).__name__}(render_mode="human")'
            )
            return

        if self.render_mode == "human" and self.window is None:
            print("Warning: Render called after window closed or failed init.")
            return None

        # --- Create the surface to draw on ---
        canvas = pygame.Surface((self.width * self.cell_size, self.height * self.cell_size))
        canvas.fill((255, 255, 255))  # White background

        # Draw Grid Lines (optional)
        for x in range(0, self.width * self.cell_size, self.cell_size):
            pygame.draw.line(canvas, (200, 200, 200), (x, 0), (x, self.height * self.cell_size))
        for y in range(0, self.height * self.cell_size, self.cell_size):
            pygame.draw.line(canvas, (200, 200, 200), (0, y), (self.width * self.cell_size, y))

        # Draw Food
        if self.food_position:
            fx, fy = self.food_position
            food_rect = pygame.Rect(fx * self.cell_size, fy * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(canvas, (0, 255, 0), food_rect)  # Green food

        # Draw Agents
        agent_colors = [(255, 0, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]
        for i, agent_id in enumerate(self.agents):
            if agent_id in self.agent_positions:
                ax, ay = self.agent_positions[agent_id]
                agent_rect = pygame.Rect(ax * self.cell_size, ay * self.cell_size, self.cell_size, self.cell_size)
                color = agent_colors[i % len(agent_colors)]
                pygame.draw.rect(canvas, color, agent_rect.inflate(-4, -4))  # Smaller rect

        # --- Update the display if in human mode ---
        if self.render_mode == "human":
            self.window.blit(canvas, canvas.get_rect())
            pygame.display.update()  # <-- Show the frame

            # --- Process events AFTER updating display ---
            for event in pygame.event.get():
                # Add this print for debugging events:
                # print(f"DEBUG: Processing event: {event}")
                if event.type == pygame.QUIT:
                    print("DEBUG: pygame.QUIT event detected!")  # Add specific print
                    self.close()
                    return None  # Signal window closed

            # --- Tick clock LAST ---
            self.clock.tick(self.metadata["render_fps"])

        return []

    def render(self):
        if self.render_mode in ["human", "rgb_array"]:
            if not self._renderer_initialized:
                self._init_render()  # <--- Initialization happens here
            return self._render_frame()
        return []

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
            self.window = None
            self._renderer_initialized = False
            print("Pygame renderer closed.")

    def set_render_mode(self, render_mode):
        self.render_mode = render_mode
