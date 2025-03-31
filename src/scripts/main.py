import torch
from visuals.visualizer import Visualizer
from environment.ecoenvironment import EcosystemEnv

if __name__ == "__main__":
    # Use GPU if available
    device = torch.device("cuda" if torch.__version__ >= "2.8" and torch.cuda.is_available() else "cpu")

    # Initialize the visualizer and environment
    visualizer = Visualizer(mode='console')#(mode='matplotlib')
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
