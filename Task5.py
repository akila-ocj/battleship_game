def find_clusters(H):
    clusters = []
    visited = set()

    def dfs(cell):
        x, y = cell
        cluster = {(x, y)}
        visited.add((x, y))

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Up, Left, Down
            nx, ny = x + dx, y + dy
            if (nx, ny) in H and (nx, ny) not in visited:
                cluster.update(dfs((nx, ny)))
        return cluster

    for hit in H:
        if hit not in visited:
            clusters.append(dfs(hit))
    return clusters


def find_sunk_ships(H, ships, announced_sunk_ship_count):
    clusters = find_clusters(H)

    if len(clusters) != announced_sunk_ship_count:
        return f"Error: Announced sunk ship count ({announced_sunk_ship_count}) does not match identified clusters ({len(clusters)})"

    sunk_ships = []
    for cluster in clusters:
        min_x = min(cluster, key=lambda x: x[0])[0]
        max_x = max(cluster, key=lambda x: x[0])[0]
        min_y = min(cluster, key=lambda x: x[1])[1]
        max_y = max(cluster, key=lambda x: x[1])[1]

        width = max_x - min_x + 1
        height = max_y - min_y + 1
        size = len(cluster)

        for ship in ships:
            # Check the size of the ship and the maximum of width and height to match with the ship's width and height.
            # As ships can be oriented differently, we need to take the max of width and height to consider both orientations.
            if ship["size"] == size and max(ship["width"], ship["height"]) in [width, height]:
                sunk_ships.append(ship["name"])

    return sunk_ships


# Assume board size is 6x6
ships = [
    {"name": "KoKo", "width": 2, "height": 1, "size": 2},
    {"name": "Cruiser", "width": 2, "height": 2, "size": 4},
    {"name": "Submarine", "width": 1, "height": 3, "size": 3},
    {"name": "Frigate", "width": 1, "height": 4, "size": 4},
    {"name": "Aircraft Carrier", "width": 2, "height": 3, "size": 6},
    {"name": "Unicorn", "width": 3, "height": 3, "size": 5}
    # The Unicorn is assumed to be in a '+' shape but its size is 5
]

H = {(0, 0), (0, 1), (0, 4), (0, 5), (1, 4), (1, 5)}  # H on the board
print(find_sunk_ships(H, ships, 2))  # ['KoKo', 'Cruiser']

H = {(0, 0), (0, 1), (3, 2), (3, 3), (3, 4), (3, 5)}  # H on the board
print(find_sunk_ships(H, ships, 2))  # ['KoKo', 'Frigate']
