# === Simplest RLlib + PettingZoo Example ===

# --- Prerequisites ---
# 1. Install required libraries:
#    pip install "ray[rllib]" pettingzoo gymnasium torch numpy (or tensorflow)

import ray
from ray import tune
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.env.wrappers.pettingzoo_env import PettingZooEnv
from ray.rllib.policy.policy import PolicySpec
from pettingzoo.classic import rps_v2 # A very simple PettingZoo env
import gymnasium as gym


# --- 1. Environment Creator ---
def env_creator(env_config):
    env = rps_v2.env(**env_config)
    return env

# --- 2. Register Environment with RLlib ---
env_name = "rps_v2"
tune.register_env(env_name, lambda config: PettingZooEnv(env_creator(config)))


# --- 3. Basic RLlib Configuration ---

# Need observation and action spaces - get from a dummy instance
# Important: Must wrap with PettingZooEnv to get RLlib-compatible spaces
temp_env = PettingZooEnv(env_creator({}))
obs_space = temp_env.observation_space
act_space = temp_env.action_space
agent_ids = temp_env.possible_agents # Should be ['player_0', 'player_1']
temp_env.close()

# Define policies for the two players
policies = {
    "policy_0": PolicySpec(observation_space=obs_space, action_space=act_space),
    "policy_1": PolicySpec(observation_space=obs_space, action_space=act_space),
}

# Map agents to policies (simple mapping)
def policy_mapping_fn(agent_id, episode, worker, **kwargs):
    # agent_id is 'player_0' or 'player_1'
    player_num = agent_id.split("_")[-1] # Extracts '0' or '1'
    return f"policy_{player_num}"

# Configure PPO with minimal settings
config = (
    PPOConfig()
    .environment(
        env=env_name,
        # Disable env checking for potentially simpler startup
        disable_env_checking=True
    )
    .framework("torch") # Or "tf2"
    .multi_agent(
        policies=policies,
        policy_mapping_fn=policy_mapping_fn,
        policies_to_train=["policy_0", "policy_1"] # Train both
    )
    # Use minimal resources for basic test
    .env_runners(
         num_env_runners=0 # Run env in the main driver process for simplicity
    )
    .resources(
         num_gpus=0 # Ensure CPU only
    )
    # --- Let's NOT explicitly enable the new API stack for max stability ---
    # .api_stack(...) # Commented out for simplicity
    .debugging(log_level="WARN") # Reduce log noise
)

# --- 4. Training Execution ---
if __name__ == "__main__":
    print("Starting basic RLlib + PettingZoo (RPS) example...")

    # Initialize Ray (minimal setup)
    ray.init(num_cpus=2, ignore_reinit_error=True, include_dashboard=False)

    # Run for just one iteration to check if setup works
    print("Running tune.run for 1 iteration...")
    results = tune.run(
        "PPO",
        name="PPO_RPS_basic_test",
        stop={
            "training_iteration": 1, # Stop after one iteration
        },
        config=config.to_dict(),
        verbose=1, # Show basic progress
    )

    print("Tune run finished.")

    # Check if run completed without error
    if results.get_best_trial(metric="training_iteration", mode="max"):
         print("Experiment completed one iteration successfully!")
    else:
         print("Experiment failed to complete one iteration.")

    # Cleanup
    print("Shutting down Ray...")
    ray.shutdown()
    print("Script finished.")