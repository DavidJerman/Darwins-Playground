from ray.rllib.algorithms import PPOConfig
from ray.rllib.connectors.env_to_module import (
    FlattenObservations,
    PrevActionsPrevRewards,
)
from ray.rllib.core.rl_module.default_model_config import DefaultModelConfig
from ray.rllib.utils.test_utils import (
    run_rllib_example_script_experiment,
)


def _setup_connectors(env):
    is_multi_agent = True # Hardcoded for GridFoodSearchEnv > 1 agent
    return [
        PrevActionsPrevRewards(multi_agent=is_multi_agent),
        FlattenObservations(multi_agent=is_multi_agent),
    ]

def setup_and_run_training(args, env_name, env_config):
    """Configures and runs the RLlib training experiment."""
    print(f"\n--- Starting Training (Env={env_name}) ---")

    try:
        if args.algo.upper() == "PPO":
            config_builder = PPOConfig()
        else:
            print(f"Warning: Algo '{args.algo}' not explicitly supported, using PPOConfig.")
            config_builder = PPOConfig() # Fallback

        # Build the main config using the builder pattern
        base_config = (
            config_builder
            .environment(
                env_name,
                env_config=env_config
            )
            .multi_agent(
                policies={"shared_policy"},
                policy_mapping_fn=lambda agent_id, episode, **kw: "shared_policy",
            )
            .framework("torch")
            .api_stack(
                enable_rl_module_and_learner=True,
                enable_env_runner_and_connector_v2=True,
            )
            .env_runners(env_to_module_connector=_setup_connectors)
            .rl_module(
                model_config=DefaultModelConfig(
                    use_lstm=False,
                    fcnet_hiddens=[256, 256],
                    fcnet_activation="relu",
                )
            )
        )

        print("--- Training Configuration ---")
        print(f"Algorithm: {args.algo}")
        print(f"Framework: {args.framework}")
        print(f"API Stack Enabled: {base_config.enable_rl_module_and_learner}")
        print("----------------------------")

        # Run the experiment using RLlib utility function
        results = run_rllib_example_script_experiment(base_config, args)
        print("\n--- Training finished ---")
        print("Results:", results) # Optionally print results path

    except Exception as e:
         print(f"\nError during training setup or execution: {e}")
         import traceback
         traceback.print_exc()