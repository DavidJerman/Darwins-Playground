from statistics import mean
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from environment import GridFoodSearchEnv
from terrain_generator import print_terrain
from ctde_q_agent import CTDEQLearningAgent

env = GridFoodSearchEnv({"num_agents": 2, "width": 10, "height": 10})
env.set_render_mode("human")

agents = {agent_id: CTDEQLearningAgent(agent_id, env.action_spaces[agent_id])
          for agent_id in env.agents}

n_episodes = 5000

reward_history = {agent_id: [] for agent_id in env.agents}
apples_eaten_history = {agent_id: [] for agent_id in env.agents}
steps_intervals = {agent_id: [] for agent_id in env.agents}

for episode in range(n_episodes):
    obs, _ = env.reset()
    total_reward = {agent_id: 0 for agent_id in env.agents}
    apples_eaten = {agent_id: 0 for agent_id in env.agents}
    steps_since_last_apple = {agent_id: 0 for agent_id in env.agents}

    food_positions_before = set(env.return_food_positions())

    for _ in range(env._max_episode_steps):
        actions = {agent_id: agents[agent_id].select_action(obs[agent_id])
                   for agent_id in env.agents}
        next_obs, rewards, dones, truncs, _ = env.step(actions)

        for agent_id in env.agents:
            if not dones[agent_id] and not truncs[agent_id]:
                steps_since_last_apple[agent_id] += 1

        food_positions_after = set(env.return_food_positions())
        eaten_positions = food_positions_before - food_positions_after

        for pos in eaten_positions:
            for agent_id in env.agents:
                agent_pos = (env.my_agents[agent_id].x, env.my_agents[agent_id].y)
                if agent_pos == pos:
                    apples_eaten[agent_id] += 1
                    steps_intervals[agent_id].append(steps_since_last_apple[agent_id])
                    steps_since_last_apple[agent_id] = 0

        food_positions_before = food_positions_after

        for agent_id in env.agents:
            done = dones[agent_id] or truncs[agent_id]
            agents[agent_id].update(obs, actions[agent_id], rewards[agent_id], next_obs, done)
            total_reward[agent_id] += rewards[agent_id]

        obs = next_obs

        if all(dones.values()) or all(truncs.values()):
            break

    for agent_id in env.agents:
        reward_history[agent_id].append(total_reward[agent_id])
        apples_eaten_history[agent_id].append(apples_eaten[agent_id])
        agents[agent_id].decay_epsilon()

    if episode % 50 == 0:
        avg_rewards = {aid: mean(reward_history[aid]) for aid in env.agents}
        if all(len(apples_eaten_history[aid]) > 0 for aid in env.agents):
            avg_apples = {aid: mean(apples_eaten_history[aid]) for aid in env.agents}
        else:
            avg_apples = {aid: 0 for aid in env.agents}

        avg_steps = {}
        for aid in env.agents:
            if len(steps_intervals[aid]) > 0:
                avg_steps[aid] = mean(steps_intervals[aid][-100:])
            else:
                avg_steps[aid] = None

        print(f"Episode {episode}")
        print(f"Rewards: {total_reward}")
        print(f"Average (last 100): {avg_rewards}")
        print(f"Average Apples Eaten (last 100): {avg_apples}")
        print(f"Avg Steps Before Apple (last 100): {avg_steps}")
        agent_positions = [(env.my_agents[aid].x, env.my_agents[aid].y) for aid in env.agents]
        print_terrain(env.tiles, env.width, env.height, agent_positions)

avg_rewards = [
    sum(reward_history[aid][i] for aid in env.agents) / len(env.agents)
    for i in range(len(reward_history[env.agents[0]]))
]

window = 100
avg_rewards_smooth = np.convolve(avg_rewards, np.ones(window) / window, mode='valid')

plt.figure()
plt.plot(range(len(avg_rewards_smooth)), avg_rewards_smooth, label=f"Moving Avg (window={window})", color="black")
plt.xlabel("Episode")
plt.ylabel("Average Reward")
plt.title("Smoothed Average Reward Over Episodes")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("avg_reward_smooth.png")
print("Saved plot to avg_reward_smooth.png")

avg_apples = [
    sum(apples_eaten_history[aid][i] for aid in env.agents) / len(env.agents)
    for i in range(len(apples_eaten_history[env.agents[0]]))
]

window = 100
avg_apples_smooth = np.convolve(avg_apples, np.ones(window) / window, mode='valid')

plt.figure()
plt.plot(range(len(avg_apples_smooth)), avg_apples_smooth, label=f"Moving Avg (window={window})", color="green")
plt.xlabel("Episode")
plt.ylabel("Average Apples Eaten")
plt.title("Smoothed Average Apples Eaten Over Episodes")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("avg_apples_eaten_smooth.png")
print("Saved plot to avg_apples_eaten_smooth.png")

avg_steps_intervals = [
    np.mean([steps_intervals[aid][i] for aid in env.agents if i < len(steps_intervals[aid])])
    for i in range(min(len(steps_intervals[aid]) for aid in env.agents))
]

window = 100
avg_steps_smooth = np.convolve(avg_steps_intervals, np.ones(window) / window, mode='valid')

plt.figure()
plt.plot(range(len(avg_steps_smooth)), avg_steps_smooth, label=f"Moving Avg (window={window})", color="blue")
plt.xlabel("Apple Index")
plt.ylabel("Average Steps Before Eating Apple")
plt.title("Smoothed Average Steps Taken Before Eating Apples")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("avg_steps_before_apple_smooth.png")
print("Saved plot to avg_steps_before_apple_smooth.png")
