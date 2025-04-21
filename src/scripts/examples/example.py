import random
import time

import gymnasium as gym
import numpy as np
import pygame
import ray
import torch
from ray.rllib.algorithms import PPOConfig
from ray.rllib.algorithms.ppo import PPO
from ray.rllib.connectors.env_to_module import (
    FlattenObservations,
    PrevActionsPrevRewards,
)
from ray.rllib.core.rl_module.default_model_config import DefaultModelConfig
from ray.rllib.env.multi_agent_env import MultiAgentEnv
from ray.rllib.utils.test_utils import (
    add_rllib_example_script_args,
    run_rllib_example_script_experiment,
)
from ray.tune.registry import register_env


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

        obs_space_dict = {
            "agent_position": gym.spaces.Box(low=0.0, high=1.0, shape=(2,), dtype=np.float32),
            "food_position": gym.spaces.Box(low=0.0, high=1.0, shape=(2,), dtype=np.float32)
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

            norm_agent_pos = np.array([norm_ax, norm_ay], dtype=np.float32)
            norm_food_pos = np.array([norm_fx, norm_fy], dtype=np.float32)

            obs_this_agent = {
                "agent_position": norm_agent_pos,
                "food_position": norm_food_pos
            }
            obs[agent_id] = obs_this_agent
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
        if GridFoodSearchEnv.VERBOSE:
            print("\n--- Environment Reset ---")

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


parser = add_rllib_example_script_args(
    default_reward=10000,
    default_iters=5,
    default_timesteps=100000
)
parser.set_defaults(
    enable_new_api_stack=True,
    # num_agents=2,
)


def visualize_policy(checkpoint_path, env_config, num_episodes=5):
    print(f"\n--- Starting Visualization ---")
    print(f"Loading checkpoint from: {checkpoint_path}")

    try:
        # Restore the Algorithm using the generic base class
        algo = PPO.from_checkpoint(checkpoint_path)
        print("--- DEBUG INFO ---")
        print(f"Checkpoint loaded.")
        print(f"Type of 'algo' object: {type(algo)}")  # Check the type
        print("--------------------")
        print("Algorithm loaded successfully.")
    except Exception as e:
        print(f"Error loading checkpoint: {e}")
        return

    # Create the environment instance with render_mode='human'
    vis_env_config = env_config.copy()  # Important: Copy env_config
    vis_env_config["render_mode"] = "human"
    try:
        env = GridFoodSearchEnv(config=vis_env_config)
        print("Environment created for visualization.")
    except Exception as e:
        print(f"Error creating environment: {e}")
        return

    for episode in range(num_episodes):
        print(f"\n--- Starting Visualization Episode {episode + 1}/{num_episodes} ---")
        obs, info = env.reset()
        terminated = {"__all__": False}
        truncated = {"__all__": False}
        step_count = 0
        total_reward_dict = {agent_id: 0.0 for agent_id in env.agents}
        render_active = True

        while not terminated["__all__"] and not truncated["__all__"] and render_active:
            # Render the environment state
            render_result = env.render()

            if render_result is None:  # Check if render signaled exit (window closed)
                print("Render window closed by user.")
                render_active = False
                continue  # Skip rest of the loop for this episode

            time.sleep(0.8)

            try:
                # 1. Get the RL Module (can potentially be moved outside the loop if static)
                module = algo.get_module("shared_policy")
                try:
                    device = next(module.parameters()).device
                except Exception:
                    device = "cpu"
                module.to(device)
                module.eval()

                # 2. Prepare batch from the observations dictionary
                agent_ids = list(obs.keys())
                if not agent_ids:  # Handle case where obs might be empty temporarily
                    print("Warning: No agents found in observation dict. Skipping step.")
                    time.sleep(0.1)  # Avoid busy-waiting
                    continue

                obs_list = [obs[agent_id] for agent_id in agent_ids]
                obs_batch = np.stack(obs_list, axis=0)

                # Create the input dictionary expected by the RLModule
                input_dict = {
                    "obs": torch.tensor(obs_batch, dtype=torch.float32).to(device)
                }

                with torch.no_grad():  # Inference
                    forward_out = module.forward_inference(input_dict)

                # 4. Extract actions
                # Output structure depends on the specific RLModule.
                # Usually a dict containing 'actions', possibly already deterministic.
                action_logits = forward_out.get("action_dist_inputs")

                if action_logits is None:
                    print("Error: Could not find 'action_dist_inputs' in RLModule output.")
                    print("Full module output:", forward_out)
                    break  # Stop episode

                actions_batch_tensor = torch.argmax(action_logits, dim=-1)
                actions_batch = actions_batch_tensor.cpu().numpy()

                # 5. Map batch actions back to agent dictionary
                actions = {agent_ids[i]: int(actions_batch[i]) for i in range(len(agent_ids))}

            except Exception as e:
                print(f"\nError during action computation: {e}")
                import traceback
                traceback.print_exc()
                render_active = False  # Stop visualization on error
                continue  # Skip to next loop iteration or break
            # +++ End: INSERT THE NEW RLModule ACTION COMPUTATION CODE HERE +++

            # Step the environment
            obs, reward, terminated, truncated, info = env.step(actions)
            step_count += 1

            for agent_id, r in reward.items():
                total_reward_dict[agent_id] += r

            # Optional small delay if render FPS isn't enough
            # time.sleep(0.1)

        if render_active:  # Don't print end status if window was closed mid-episode
            print(f"Episode finished after {step_count} steps.")
            print(f"Total rewards: {total_reward_dict}")
            if terminated["__all__"]:
                print("Reason: Food Found (Terminated)")
            elif truncated["__all__"]:
                print("Reason: Max Steps Reached (Truncated)")

            try:
                # Keep showing the last frame and wait for user input
                print("Press Enter to continue to the next episode (or close the window)...")
                # Keep processing events so window doesn't freeze and close button works
                while True:
                    event_processed = False
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            render_active = False
                            event_processed = True
                            break
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:  # Check for Enter key
                                event_processed = True
                                break
                    if event_processed:
                        break  # Exit inner event loop
                    time.sleep(0.05)  # Prevent busy-waiting

                if not render_active:  # If user closed window during pause
                    print("Window closed during pause.")
                    env.close()  # Close immediately if user quit
                    break  # Exit the outer episode loop

            except KeyboardInterrupt:  # Allow Ctrl+C to exit
                render_active = False
                print("\nInterrupted by user.")
                break  # Exit the outer episode loop

        if not render_active:  # Exit outer loop if window was closed
            break

    env.close()  # Clean up the rendering window
    print("\nVisualization finished.")


if __name__ == "__main__":
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Run visualization using a checkpoint."
    )
    parser.add_argument(
        "--checkpoint-path",
        type=str,
        default=None,
        help="Path to the specific checkpoint directory (e.g., .../checkpoint_000050) for visualization."
    )

    args = parser.parse_args()

    print(f"Running with arguments: {args}")

    env_config = {
        "width": 10,
        "height": 10,
        "num_agents": args.num_agents,
        "max_steps": 50,
    }

    env_name = "grid_food_search"
    register_env(env_name, lambda cfg: GridFoodSearchEnv(cfg))

    if args.visualize:
        if args.checkpoint_path:
            visualize_policy(args.checkpoint_path, env_config, num_episodes=5)
        else:
            print("\nError: --checkpoint-path must be provided for visualization.")
            print("Example: --checkpoint-path /path/to/my/results/PPO.../checkpoint_000050")
    else:
        print("\n--- Starting Training ---")

        if args.algo.upper() == "PPO":
            config_builder = PPOConfig()
        else:
            config_builder = PPOConfig()


        def _env_to_module(env):
            is_multi_agent = True
            return [
                PrevActionsPrevRewards(multi_agent=is_multi_agent),
                FlattenObservations(multi_agent=is_multi_agent),
            ]


        base_config = (
            config_builder
            .environment(env_name, env_config=env_config)
            .multi_agent(
                policies={"shared_policy"},
                policy_mapping_fn=lambda agent_id, episode, **kw: "shared_policy",
            )
            .framework("torch")
            .api_stack(
                enable_rl_module_and_learner=True,
                enable_env_runner_and_connector_v2=True,
            )
            .env_runners(env_to_module_connector=_env_to_module)
            .rl_module(
                model_config=DefaultModelConfig(
                    use_lstm=False,
                    fcnet_hiddens=[256, 256],
                    fcnet_activation="relu",
                )
            )
        )

        run_rllib_example_script_experiment(base_config, args)

        print("\n--- Training finished ---")

    if ray.is_initialized():
        ray.shutdown()
    print("Script finished.")
