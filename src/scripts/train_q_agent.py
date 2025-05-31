from q_agent import QLearningAgent
from environment import GridFoodSearchEnv
from terrain_generator import print_terrain

env = GridFoodSearchEnv({"num_agents": 1, "width": 10, "height": 10})
env.set_render_mode(render_mode="human")
agent_id = "agent_0"
agent = QLearningAgent(env.action_spaces[agent_id])

n_episodes = 10000

for episode in range(n_episodes):
    obs, _ = env.reset()
    obs = obs[agent_id]
    total_reward = 0

    for _ in range(env._max_episode_steps):
        action = agent.select_action(obs)
        actions = {agent_id: action}
        new_obs, rewards, dones, truncs, _ = env.step(actions)

        reward = rewards[agent_id]
        done = dones[agent_id] or truncs[agent_id]
        agent.update(obs, action, reward, new_obs[agent_id], done)

        obs = new_obs[agent_id]
        total_reward += reward

        if done:
            break

    agent.decay_epsilon()

    if episode % 50 == 0:
        print(f"Episode {episode}, total reward: {total_reward:.2f}")
        agent_pos = (env.my_agents[agent_id].x, env.my_agents[agent_id].y)
        print_terrain(env.tiles, env.width, env.height, agent_pos)

agent.set_epsilon(0)  # no randomness

n_test_episodes = 10
for episode in range(n_test_episodes):
    obs, _ = env.reset()
    obs = obs[agent_id]
    total_reward = 0

    for _ in range(env._max_episode_steps):
        action = agent.select_action(obs)
        actions = {agent_id: action}
        new_obs, rewards, dones, truncs, _ = env.step(actions)

        reward = rewards[agent_id]
        done = dones[agent_id] or truncs[agent_id]

        obs = new_obs[agent_id]
        total_reward += reward

        if done:
            break

    agent_pos = (env.my_agents[agent_id].x, env.my_agents[agent_id].y)
    print(f"[Test] Episode {episode}, total reward: {total_reward:.2f}")
    print_terrain(env.tiles, env.width, env.height, agent_pos)
