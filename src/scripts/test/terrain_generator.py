import random
import sys
import os

# Add the src/scripts directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tile import Tile

# Terrain types
GRASS = 0
SAND = 1
ROCK = 2

# Optional symbols for visualization
TERRAIN_SYMBOLS = {
    GRASS: "🌿",
    SAND: "🏖️",
    ROCK: "⛰️",
}

# Directions for the flood-fill (up, down, left, right)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def generate_terrain(width, height):
    """
    Generates a grid of tiles with connected clusters of grass (5-10 connected grass tiles).
    """
    tiles = [[Tile() for _ in range(height)] for _ in range(width)]

    # Start with all tiles as grass
    for x in range(width):
        for y in range(height):
            tiles[x][y] = Tile(terrain=GRASS, has_food=random.choice([True, False, False]))  # Default to grass

    def in_bounds(x, y):
        return 0 <= x < width and 0 <= y < height

    def flood_fill(x, y, max_size):
        """Flood-fill to create a cluster of connected grass tiles of random size (5-10)."""
        stack = [(x, y)]
        visited = set(stack)
        size = 0
        tiles[x][y].terrain = GRASS  # Start with grass at the initial point

        while stack and size < max_size:
            cx, cy = stack.pop()
            size += 1

            # Try all 4 directions
            random.shuffle(DIRECTIONS)  # Randomize direction order for variety
            for dx, dy in DIRECTIONS:
                nx, ny = cx + dx, cy + dy
                if in_bounds(nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    tiles[nx][ny].terrain = GRASS
                    stack.append((nx, ny))

        return size

    def place_grass_clusters(num_clusters):
        """Place connected clusters of grass tiles (5-10)."""
        for _ in range(num_clusters):
            # Pick a random starting point for the cluster
            start_x = random.randint(0, width - 1)
            start_y = random.randint(0, height - 1)
            cluster_size = random.randint(5, 10)  # Size of the cluster (5-10 tiles)
            flood_fill(start_x, start_y, cluster_size)

    # Place connected clusters of grass
    place_grass_clusters(num_clusters=5)

    # Add patches of other terrain types (SAND, ROCK) outside the grass clusters
    def make_patch(center_x, center_y, radius, terrain_type):
        for x in range(center_x - radius, center_x + radius + 1):
            for y in range(center_y - radius, center_y + radius + 1):
                if in_bounds(x, y) and tiles[x][y].terrain == GRASS:  # Replace only grass
                    if random.random() < 0.5:  # fuzzy edge
                        tiles[x][y].terrain = terrain_type

    # Create some terrain clusters (SAND and ROCK)
    num_patches = 3
    for _ in range(num_patches):
        cx = random.randint(0, width - 1)
        cy = random.randint(0, height - 1)
        radius = random.randint(1, 3)
        terrain_type = random.choice([SAND, ROCK])
        make_patch(cx, cy, radius, terrain_type)

    return tiles


if __name__ == "__main__":
    width, height = 10, 10
    terrain_grid = generate_terrain(width, height)

    print("Terrain map:\n")
    for y in range(height):
        row = ""
        for x in range(width):
            tile = terrain_grid[x][y]
            row += TERRAIN_SYMBOLS[tile.terrain] + " "
        print(row)
