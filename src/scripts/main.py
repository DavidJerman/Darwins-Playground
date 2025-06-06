import os

from setup import setup

used_device_initial = setup()

import ray
from ray.rllib.utils.test_utils import add_rllib_example_script_args
from ray.tune.registry import register_env

from environment import GridFoodSearchEnv
from training import setup_and_run_training
from visualizer import visualize_policy

parser = add_rllib_example_script_args(
    default_reward=10000,
    default_iters=100,
    default_timesteps=100000
)

parser.add_argument(
    "--width",
    type=int,
    default=10
)
parser.add_argument(
    "--height",
    type=int,
    default=10
)
parser.add_argument(
    "--max-steps",
    type=int,
    default=50
)
parser.add_argument(
    "--visualize",
    action="store_true",
    help="Run visualization using a checkpoint."
)
parser.add_argument(
    "--checkpoint-path",
    type=str,
    default=None,
    help="Path to checkpoint dir for visualization (e.g., .../checkpoint_000XXX)"
)
parser.add_argument(
    "--vis-episodes",
    type=int,
    default=5,
    help="Number of episodes to visualize."
)
parser.add_argument(
    "--vis-delay",
    type=float,
    default=0.3,
    help="Delay between steps during visualization."
)
parser.add_argument(
    "--device",
    type=str,
    default=used_device_initial,
    help="Device to run on (e.g., 'cpu', 'cuda')."
         "If not provided, will use the device used by Ray."
         "If provided, will override the device used by Ray."
         "This is useful for running on a remote cluster."
         "Note that this is not supported for all algorithms."
)

args = parser.parse_args()

default_gpus_per_learner = 1.0 if args.device == 'cuda' else 0.0

parser.set_defaults(
    enable_new_api_stack=True,
    num_gpus_per_learner=default_gpus_per_learner,
    num_cpus_per_learner=int((os.cpu_count() - 1) * 0.75) if os.cpu_count() is not None else 2,
    num_agents=2,
    verbose=1,
    algo="PPO",
)

if __name__ == "__main__":
    args = parser.parse_args()

    if not hasattr(args, 'algo') or args.algo is None:
        args.algo = "PPO"

    if not hasattr(args, 'framework') or args.framework is None:
        args.framework = "torch"

    print(f"----- Running RLlib Example -----")
    print(f"Algorithm: {args.algo}")
    print(f"Framework: {args.framework}")
    print("Running with the following arguments:")
    for key, value in vars(args).items():
        print(f"- {key}: {value}")

    env_config = {
        "width": 10,
        "height": 10,
        "num_agents": args.num_agents,
        "max_steps": 50,
    }

    env_name = "grid_food_search"
    register_env(env_name, lambda cfg: GridFoodSearchEnv(cfg))
    print(f"Environment '{env_name}' registered.")

    if args.visualize:
        if args.checkpoint_path:
            visualize_policy(args.checkpoint_path, env_config, num_episodes=5)
        else:
            print("\nError: --checkpoint-path must be provided for visualization.")
            print("Example: --checkpoint-path /path/to/my/results/PPO.../checkpoint_000050")
    else:
        # Run training
        setup_and_run_training(args, env_name, env_config)

    # --- Ray Shutdown ---
    if ray.is_initialized():
        ray.shutdown()
        print("Ray shut down.")

    print("Script finished.")
