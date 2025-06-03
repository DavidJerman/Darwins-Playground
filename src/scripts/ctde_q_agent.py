from collections import defaultdict

import numpy as np


class CTDEQLearningAgent:
    def __init__(self, agent_id, action_space, lr=0.1, gamma=0.9, epsilon=1.0, epsilon_min=0.05, epsilon_decay=0.999):
        self.agent_id = agent_id
        self.q_table = defaultdict(lambda: np.zeros(action_space.n))
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.action_space = action_space

    def get_state_key(self, global_obs):
        obs = global_obs[self.agent_id]
        pos = tuple((obs["agent_position"] * 10).astype(int))
        food = tuple((obs["food_position"] * 10).astype(int))
        return pos + food + (obs["terrain"],)

    def select_action(self, local_obs):
        pos = tuple((local_obs["agent_position"] * 10).astype(int))
        food = tuple((local_obs["food_position"] * 10).astype(int))
        state = pos + food + (local_obs["terrain"],)
        if np.random.rand() < self.epsilon:
            return self.action_space.sample()
        return int(np.argmax(self.q_table[state]))

    def update(self, global_obs, action, reward, global_next_obs, done):
        state = self.get_state_key(global_obs)
        next_state = self.get_state_key(global_next_obs)
        max_next_q = 0 if done else np.max(self.q_table[next_state])
        td_target = reward + self.gamma * max_next_q
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.lr * td_error

    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def set_epsilon(self, value):
        self.epsilon = value
