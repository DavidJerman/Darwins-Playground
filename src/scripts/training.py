from ray.rllib.algorithms import PPOConfig, DQNConfig, SACConfig, APPOConfig, IMPALAConfig
from ray.rllib.connectors.env_to_module import (
    FlattenObservations,
    PrevActionsPrevRewards,
)
from ray.rllib.core.rl_module.default_model_config import DefaultModelConfig
from ray.rllib.utils.test_utils import (
    run_rllib_example_script_experiment,
)

algo_map = {
    "PPO": PPOConfig,
    "DQN": DQNConfig,
    "SAC": SACConfig,
    "APPO": APPOConfig,
    "IMPALA": IMPALAConfig,
}

# TODO: DQN requires NO shared policy!
# TODO: SAC only supports soft action spaces (no discrete)!
# TODO: APPO and IMPALA need the same issue fixed!


def _setup_connectors(env):
    is_multi_agent = True
    return [
        PrevActionsPrevRewards(multi_agent=is_multi_agent),
        FlattenObservations(multi_agent=is_multi_agent),
    ]


def setup_and_run_training(args, env_name, env_config):
    """Configures and runs the RLlib training experiment."""
    print(f"\n--- Starting Training (Env={env_name}) ---")

    try:
        algo_name = args.algo.upper()
        config_class = algo_map.get(algo_name)

        if algo_name == "DQN":
            raise ValueError("DQN does not support shared policy!")

        if algo_name == "SAC":
            raise ValueError("SAC only supports soft action spaces (no discrete)!")

        if algo_name == "APPO":
            raise ValueError("APPO not supported!")

        if algo_name == "IMPALA":
            raise ValueError("IMPALA not supported!")

        if config_class is None:
            raise ValueError(f"Unsupported algo '{args.algo}'. Available: {list(algo_map.keys())}")

        config_builder = config_class()

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
            .framework(args.framework)
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
        print("Results:", results)  # Optionally print results path

    except Exception as e:
        print(f"\nError during training setup or execution: {e}")
        import traceback
        traceback.print_exc()
