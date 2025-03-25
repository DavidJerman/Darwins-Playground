# from environment.environment import Environment
# from agents.agent import Agent
# from visuals.visualizer import Visualizer
#
# import random
#
# if __name__ == "__main__":
#     width, height = 10, 10
#     environment = Environment(width, height)
#     visualizer = Visualizer(environment, live=True)
#     environment.visualizer = visualizer
#
#     # Create and add agents
#     for _ in range(5):
#         agent = Agent(random.randint(0, width - 1), random.randint(0, height - 1), environment)
#         environment.add_agent(agent)
#
#     # Run the simulation
#     environment.run(steps=50, sleep_time=0.1)

from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.connectors.env_to_module import FlattenObservations

# Configure the algorithm.
config = (
    PPOConfig()
    .environment("Taxi-v3")
    .env_runners(
        num_env_runners=2,
        # Observations are discrete (ints) -> We need to flatten (one-hot) them.
        env_to_module_connector=lambda env: FlattenObservations(),
    )
    .evaluation(evaluation_num_env_runners=1)
)

from pprint import pprint

# Build the algorithm.
algo = config.build_algo()

# Train it for 5 iterations ...
for _ in range(5):
    pprint(algo.train())

# ... and evaluate it.
pprint(algo.evaluate())

# Release the algo's resources (remote actors, like EnvRunners and Learners).
algo.stop()
