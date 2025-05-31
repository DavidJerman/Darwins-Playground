import numpy as np
from collections import defaultdict


class QLearningAgent:
    def __init__(self, action_space, lr=0.1, gamma=0.9, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        self.q_table = defaultdict(lambda: np.zeros(action_space.n))
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.action_space = action_space

    def get_state_key(self, obs):
        pos = tuple((obs["agent_position"] * 10).astype(int))
        food = tuple((obs["food_position"] * 10).astype(int))
        return pos + food + (obs["terrain"],)

    def select_action(self, obs):
        state = self.get_state_key(obs)
        if np.random.rand() < self.epsilon:
            return self.action_space.sample()
        return int(np.argmax(self.q_table[state]))

    def update(self, obs, action, reward, next_obs, done):
        state = self.get_state_key(obs)
        next_state = self.get_state_key(next_obs)

        max_next_q = 0 if done else np.max(self.q_table[next_state])
        td_target = reward + self.gamma * max_next_q
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.lr * td_error

    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def set_epsilon(self, value):
        self.epsilon = value
