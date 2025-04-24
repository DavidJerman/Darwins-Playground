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

# Symbols for visualization
TERRAIN_SYMBOLS = {
    GRASS: "🌿",
    SAND: "🏖️",
    ROCK: "⛰️",
}


def generate_terrain(width, height):
    """
    Generates a grid mostly filled with sand and rock,
    with small connected grass clusters.
    """
    tiles = [[Tile() for _ in range(height)] for _ in range(width)]

    # Step 1: Fill the map with sand and rock
    for x in range(width):
        for y in range(height):
            terrain = random.choice([SAND, ROCK])
            tiles[x][y] = Tile(terrain=terrain, has_food=random.choice([True, False, False]))

    # Step 2: Create connected grass clusters
    def create_grass_cluster(center_x, center_y, size):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        cluster = [(center_x, center_y)]
        visited = set(cluster)

        while len(cluster) < size:
            x, y = random.choice(cluster)
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                    cluster.append((nx, ny))
                    visited.add((nx, ny))
                    if len(cluster) >= size:
                        break

        for gx, gy in cluster:
            tiles[gx][gy].terrain = GRASS

    # Step 3: Add 3 to 6 grass clusters
    for _ in range(random.randint(2, 4)):
        cx = random.randint(0, width - 1)
        cy = random.randint(0, height - 1)
        cluster_size = random.randint(5, 10)
        create_grass_cluster(cx, cy, cluster_size)

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
