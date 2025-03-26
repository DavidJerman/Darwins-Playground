from visuals.visualizer import Visualizer
from environment.ecoenvironment import EcosystemEnv
from agents.agent import Agent

if __name__ == "__main__":
    visualizer = Visualizer()
    env = EcosystemEnv(width=10, height=10, num_agents=10, visualizer=visualizer)

    for agent_id, agent_data in env.agents.items():
        agent = Agent(agent_data['x'], agent_data['y'])
        print(f"Added {agent_id} at position ({agent_data['x']}, {agent_data['y']})")

    env.run(steps=10, sleep_time=0.5)

    print("Done")
