import random

from tile import Tile

# Terrain types
GRASS = 0
SAND = 1
ROCK = 2

# Symbols for visualization
TERRAIN_SYMBOLS = {
    GRASS: "🌿",
    SAND: "🏜️",
    ROCK: "⛰️",
}


def generate_terrain(_width, _height):
    """
    Generates a grid mostly filled with sand and rock,
    with small connected grass clusters.
    Exactly 5 food items placed on grass tiles.
    """
    tiles = [[Tile() for _ in range(_height)] for _ in range(_width)]

    # Step 1: Fill the map with sand and rock (no food yet)
    for x in range(_width):
        for y in range(_height):
            terrain = random.choice([SAND, ROCK])
            tiles[x][y] = Tile(terrain=terrain, has_food=False)

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
                if 0 <= nx < _width and 0 <= ny < _height and (nx, ny) not in visited:
                    cluster.append((nx, ny))
                    visited.add((nx, ny))
                    if len(cluster) >= size:
                        break

        for gx, gy in cluster:
            tiles[gx][gy].terrain = GRASS

    # Step 3: Add 3 to 6 grass clusters
    for _ in range(random.randint(2, 4)):
        cx = random.randint(0, _width - 1)
        cy = random.randint(0, _height - 1)
        cluster_size = random.randint(5, 10)
        create_grass_cluster(cx, cy, cluster_size)

    # Step 4: Put food on exactly 5 random grass tiles
    grass_tiles = [(x, y) for x in range(_width) for y in range(_height) if tiles[x][y].terrain == GRASS]

    if len(grass_tiles) >= 5:
        food_positions = random.sample(grass_tiles, 5)
        for fx, fy in food_positions:
            tiles[fx][fy].has_food = True
    else:
        print("⚠️ Warning: Not enough grass tiles to place 5 food items!")

    return tiles


def print_terrain(grid, _width, _height, agent_pos=None):
    food_symbol = "🍎"

    print("Terrain map:\n")
    for y in range(_height):
        row = ""
        for x in range(_width):
            tile = grid[x][y]
            if agent_pos is not None and agent_pos[0] == x and agent_pos[1] == y:
                row += "🤖 "
            elif tile.has_food:
                row += food_symbol + " "
            else:
                row += TERRAIN_SYMBOLS[tile.terrain] + " "
        print(row)


if __name__ == "__main__":
    width, height = 10, 10
    terrain_grid = generate_terrain(width, height)

    print_terrain(terrain_grid, width, height)
