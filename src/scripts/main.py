from visuals.visualizer import Visualizer
from environment.ecoenvironment import EcosystemEnv

if __name__ == "__main__":
    # Initialize the visualizer and environment
    visualizer = Visualizer(mode='console')
    env = EcosystemEnv(width=10, height=10, num_agents=10, visualizer=visualizer)

    # Initialize agents with the environment data
    agents = {}
    for agent_id, agent in env.my_agents.items():  # Access agents from _agents
        agents[agent_id] = agent
        print(f"Added {agent_id} at position ({agent.x}, {agent.y})")

    # Run the environment for 10 steps
    env.run(steps=10, sleep_time=0.5)

    # Final message to confirm the run is done
    print("Done")