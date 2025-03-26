import matplotlib.pyplot as plt
import numpy as np


class Visualizer:
    def __init__(self, mode='matplotlib'):
        """
        Initialize the visualizer

        :param mode: console, matplotlib, pygame
        """
        self.environment = None
        self.mode = mode

    def set_environment(self, environment):
        """
        Set the environment
        """
        self.environment = environment

    def update(self):
        """
        Update the visual
        """
        if self.environment is None:
            print("Environment is None")
            return

        if self.mode == 'console':
            self._console_visualization()
        elif self.mode == 'matplotlib':
            self._matplotlib_visualization()
        elif self.mode == 'pygame':
            self._pygame_visualization()

    def _console_visualization(self):
        """
        Console visualization
        """
        # Border
        border_row = '#' * (self.environment.width * 2 + 3)
        print(border_row)

        # Loop through environment grid and display agents
        for y in range(self.environment.height):
            row = '# '
            for x in range(self.environment.width):
                if any(agent.x == x and agent.y == y for agent in self.environment.my_agents.values()):
                    row += 'A '
                else:
                    row += '. '
            row += '#'
            print(row)

        # Border
        print(border_row)

    def _matplotlib_visualization(self):
        """
        Matplotlib visualization
        """
        grid = np.zeros((self.environment.height, self.environment.width))

        # Mark terrain types (0: normal, 1: water, 2: mountain)
        for y in range(self.environment.height):
            for x in range(self.environment.width):
                grid[y, x] = self.environment.tiles[x][y].terrain

        # Plot the grid
        plt.imshow(grid, cmap='viridis', interpolation='nearest')
        plt.colorbar(label="Terrain Type")

        # Plot agents
        for agent_id, position in self.environment.my_agents.items():
            agent_x, agent_y = position.x, position.y
            plt.scatter(agent_x, agent_y, c='red', label=agent_id, s=100)

        plt.title("Ecosystem Visualization")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()

    def _pygame_visualization(self):
        """
        Pygame visualization
        """
        # TODO: Pygame visualisation for live demo
        pass
