from environment.environment import Environment
from agents.agent import Agent
from visuals.visualizer import Visualizer

import random

if __name__ == "__main__":
    width, height = 10, 10
    environment = Environment(width, height)
    visualizer = Visualizer(environment, live=True)
    environment.visualizer = visualizer

    # Create and add agents
    for _ in range(5):
        agent = Agent(random.randint(0, width - 1), random.randint(0, height - 1), environment)
        environment.add_agent(agent)

    # Run the simulation
    environment.run(steps=50, sleep_time=0.1)
