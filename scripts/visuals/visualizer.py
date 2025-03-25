import pygame
import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self, environment, live=True, log_interval=10):
        self.environment = environment
        self.live = live
        self.log_interval = log_interval
        self.step_count = 0

        if self.live:
            pygame.init()
            self.screen = pygame.display.set_mode((environment.width * 10, environment.height * 10))
        else:
            self.fig, self.ax = plt.subplots()
            self.data = []

    def update(self):
        self.step_count += 1

        if self.live:
            self._update_pygame()
        elif self.step_count % self.log_interval == 0:
            self._update_matplotlib()

    def _update_pygame(self):
        self.screen.fill((0, 0, 0))
        for agent in self.environment.agents:
            pygame.draw.rect(self.screen, (0, 255, 0), (agent.x * 10, agent.y * 10, 10, 10))
        pygame.display.flip()

    def _update_matplotlib(self):
        self.data.append(len(self.environment.agents))
        self.ax.clear()
        self.ax.plot(self.data)
        plt.draw()
        plt.pause(0.01)
