import matplotlib.pyplot as plt
import numpy as np


class Visualizer:
    def __init__(self, mode='matplotlib'):
        self.environment = None
        self.mode = mode

    def set_environment(self, environment):
        self.environment = environment

    def update(self):
        if self.environment is None:
            print("Environment is None")
        if self.mode == 'console':
            self._console_visualization()
        elif self.mode == 'matplotlib':
            self._matplotlib_visualization()
        elif self.mode == 'pygame':
            self._pygame_visualization()

    def _console_visualization(self):
        # Display a basic textual visualization of the environment
        for y in range(self.environment.height):
            row = ''
            for x in range(self.environment.width):
                if any(agent['x'] == x and agent['y'] == y for agent in self.environment.agents.values()):
                    row += 'A '  # Representing agents as 'A'
                else:
                    row += '. '  # Empty spaces as '.'
            print(row)

    def _matplotlib_visualization(self):
        # Create a grid for visualization
        grid = np.zeros((self.environment.height, self.environment.width))

        # Mark terrain types (0: normal, 1: water, 2: mountain)
        for y in range(self.environment.height):
            for x in range(self.environment.width):
                grid[y, x] = self.environment.tiles[x][y].terrain

        # Plot the grid
        plt.imshow(grid, cmap='viridis', interpolation='nearest')
        plt.colorbar(label="Terrain Type")

        # Plot agents on the grid (using red dots for agents)
        for agent_id, position in self.environment.agents.items():
            agent_x, agent_y = position['x'], position['y']
            plt.scatter(agent_x, agent_y, c='red', label=agent_id, s=100)

        plt.title("Ecosystem Visualization")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()

    def _pygame_visualization(self):
        # Placeholder for Pygame visualization logic
        pass
