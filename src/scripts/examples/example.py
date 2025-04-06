import gymnasium as gym
import numpy as np
import random

from ray.rllib.env.multi_agent_env import MultiAgentEnv
from ray.rllib.utils.test_utils import (
    add_rllib_example_script_args,
    run_rllib_example_script_experiment,
)
from ray.tune.registry import get_trainable_cls, register_env


class GridFoodSearchEnv(MultiAgentEnv):
    def __init__(self, config=None):
        super().__init__()

        config = config or {}

        self.width = config.get("width", 10)
        self.height = config.get("height", 10)
        self._max_episode_steps = config.get("max_steps", 50)

        # Define the agents in the game.
        self.agents = self.possible_agents = [f"agent_{i}" for i in range(config.get("num_agents", 2))]

        self.observation_spaces = {
            agent_id: gym.spaces.Box(0.0, 1.0, (4,), np.float32)
            for agent_id in self.agents
        }

        self.action_spaces = {
            agent_id: gym.spaces.Discrete(4)
            for agent_id in self.agents
        }

        self.agent_positions = {}
        self.food_position = None
        self._steps_taken = 0
        self.render_mode = None
        self._agent_ids = set(self.agents)

    def _get_random_position(self, existing_positions=None):
        """Helper to get a random unoccupied position."""
        existing_positions = existing_positions or set()
        while True:
            pos = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if pos not in existing_positions:
                return pos

    def _get_observations(self):
        """Returns the observation dictionary for all agents."""
        obs = {}
        fx, fy = self.food_position
        for agent_id in self.agents:
            ax, ay = self.agent_positions[agent_id]
            # Normalize positions
            norm_ax = ax / (self.width - 1) if self.width > 1 else 0.0
            norm_ay = ay / (self.height - 1) if self.height > 1 else 0.0
            norm_fx = fx / (self.width - 1) if self.width > 1 else 0.0
            norm_fy = fy / (self.height - 1) if self.height > 1 else 0.0
            obs[agent_id] = np.array([norm_ax, norm_ay, norm_fx, norm_fy], dtype=np.float32)
            # Alternative: Non-normalized observation
            # obs[agent_id] = np.array([ax, ay, fx, fy], dtype=np.float32)
        return obs

    def reset(self, *, seed=None, options=None):
        occupied_positions = set()

        self.food_position = self._get_random_position()
        occupied_positions.add(self.food_position)

        self.agent_positions = {}
        for agent_id in self.agents:
            pos = self._get_random_position(occupied_positions)
            self.agent_positions[agent_id] = pos
            occupied_positions.add(pos)

        self._steps_taken = 0

        observations = self._get_observations()
        infos = {agent_id: {} for agent_id in self.agents}

        return observations, infos

    def step(self, action_dict):
        rewards = {agent_id: 0.0 for agent_id in self.agents}
        terminateds = {"__all__": False}
        truncateds = {"__all__": False}
        infos = {agent_id: {} for agent_id in self.agents}

        food_found = False
        self._steps_taken += 1

        for agent_id, action in action_dict.items():
            current_x, current_y = self.agent_positions[agent_id]
            new_x, new_y = current_x, current_y

            # --- Move Agent ---
            if action == 0:  # Up
                new_y = min(self.height - 1, current_y + 1)
            elif action == 1:  # Down
                new_y = max(0, current_y - 1)
            elif action == 2:  # Left
                new_x = max(0, current_x - 1)
            elif action == 3:  # Right
                new_x = min(self.width - 1, current_x + 1)

            self.agent_positions[agent_id] = (new_x, new_y)

            # --- Check for Food ---
            if self.agent_positions[agent_id] == self.food_position:
                rewards[agent_id] += 10.0  # Reward for finding food
                food_found = True
                terminateds["__all__"] = True
                infos[agent_id]["found_food"] = True  # Example info
            else:
                rewards[agent_id] -= 0.1

        # Check for truncation (max steps)
        if self._steps_taken >= self._max_episode_steps:
            truncateds["__all__"] = True

        observations = self._get_observations()

        final_terminateds = {agent_id: terminateds["__all__"] for agent_id in self.agents}
        final_truncateds = {agent_id: truncateds["__all__"] for agent_id in self.agents}
        final_terminateds["__all__"] = terminateds["__all__"]
        final_truncateds["__all__"] = truncateds["__all__"]

        return observations, rewards, final_terminateds, final_truncateds, infos


parser = add_rllib_example_script_args(
    default_reward=10000,
    default_iters=5,
    default_timesteps=100000
)
parser.set_defaults(
    enable_new_api_stack=True,
    # num_agents=2,
)

if __name__ == "__main__":
    args = parser.parse_args()

    env_config = {
        "width": 10,
        "height": 10,
        "num_agents": args.num_agents,
        "max_steps": 50,
    }

    register_env("grid_food_search", lambda cfg: GridFoodSearchEnv(cfg))

    algo_cls = get_trainable_cls(args.algo)

    base_config = (
        algo_cls.get_default_config()
        .environment("grid_food_search", env_config=env_config)
        .multi_agent(
            policies={"shared_policy"},
            policy_mapping_fn=lambda agent_id, episode, **kw: "shared_policy",
        )
        .framework("torch")
    )

    run_rllib_example_script_experiment(base_config, args)
