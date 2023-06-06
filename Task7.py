import matplotlib.pyplot as plt
import numpy as np


def find_clusters(hits):
    clusters = []
    visited = set()

    def dfs(cell):
        x, y = cell
        cluster = {(x, y)}
        visited.add((x, y))

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Up, Left, Down
            nx, ny = x + dx, y + dy
            if (nx, ny) in hits and (nx, ny) not in visited:
                cluster.update(dfs((nx, ny)))
        return cluster

    for hit in hits:
        if hit not in visited:
            clusters.append(dfs(hit))
    return clusters


def find_cluster_status(clusters, misses, board_size):
    status = []

    for cluster in clusters:
        # If all cells are hit, count the cluster as a "sunk" ship
        if len(cluster) == total_ship_cells:
            status.append('sunk')
            continue

            # Else, if the number of hit cells equals the total number of ship cells, count the cluster as a "sunk" ship
        elif len(cluster) <= total_ship_cells and len(hits) == total_ship_cells:
            status.append('sunk')
            continue

        uncertain = False
        for x, y in cluster:
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Up, Left, Down
                nx, ny = x + dx, y + dy
                if 0 <= nx < board_size and 0 <= ny < board_size and (nx, ny) not in hits and (nx, ny) not in misses:
                    uncertain = True
                    break
            if uncertain:
                break
        status.append('sunk' if not uncertain else 'uncertain')

    return status


def find_ship_status(hits, misses, board_size, total_ship_cells):
    # Edge case: if all cells are hit and the total number of hit cells equals the total number of cells occupied by ships
    if len(hits) == total_ship_cells:
        print(f"All {len(find_clusters(hits))} ships are sunk. No uncertain clusters.")
        return

    clusters = find_clusters(hits)
    status = find_cluster_status(clusters, misses, board_size)

    sunk_ships = status.count('sunk')
    uncertain_clusters = status.count('uncertain')

    print(f"Sunk ships: {sunk_ships}, Uncertain clusters: {uncertain_clusters}")

    for i, cluster in enumerate(clusters):
        print(f"Cluster {i + 1}: {cluster} - {status[i]}")

    for i, cluster in enumerate(clusters):
        if status[i] == 'uncertain':
            print(f"Uncertain cluster {i + 1} missing cells:")
            for x, y in cluster:
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Up, Left, Down
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < board_size and 0 <= ny < board_size and (nx, ny) not in hits and (
                            nx, ny) not in misses:
                        print(f"({nx}, {ny})")


game_states = [
    {
        'hits': {(2, 2), (2, 3), (2, 4)},
        'misses': {(1, 2), (1, 3), (1, 4), (3, 2), (3, 3), (3, 4), (2, 1), (2, 5)}
    },
    {
        'hits': {(7, 5), (8, 5), (9, 5)},
        'misses': {(7, 4), (7, 6), (8, 4), (8, 6), (9, 4), (9, 6), (6, 5)}
    },
    {
        'hits': {(7, 5)},
        'misses': {(9, 9)}
    },

    {
        'hits': {(5, 0), (6, 0), (7, 0), (8, 0), (9, 0)},
        'misses': {(5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (4, 0)}
    },
    {
        'hits': {(2, 7), (3, 7), (4, 7), (5, 7)},
        'misses': {(2, 6), (2, 8), (3, 6), (3, 8), (4, 6), (4, 8), (5, 6), (5, 8), (1, 7), (6, 7)}
    },
    {
        'hits': {(1, 1), (2, 1), (3, 1), (1, 2), (3, 2)},
        'misses': {(0, 1), (4, 1), (1, 0), (1, 3), (2, 0), (2, 3), (3, 0), (3, 3), (0, 2), (2, 2), (4, 2)}
    },
    {
        'hits': {(7, 2), (8, 2), (7, 3), (8, 3)},
        'misses': {(6, 2), (6, 3), (9, 2), (9, 3), (7, 1), (7, 4), (8, 1), (8, 4)}
    },
    {
        'hits': {(3, 6), (4, 6), (5, 6), (6, 6), (7, 6)},
        'misses': {(3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (2, 6), (8, 6)}
    },
    {
        'hits': {(6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5)},
        'misses': {(5, 3), (5, 4), (5, 5), (8, 3), (8, 4), (8, 5), (6, 2), (6, 6), (7, 2), (7, 6)}
    },
    {
        'hits': {(0, 9), (1, 9), (2, 9), (3, 9)},
        'misses': {(0, 8), (1, 8), (2, 8), (3, 8), (4, 9)}
    },
    {
        'hits': {(6, 8), (7, 8), (8, 8), (9, 8)},
        'misses': {(6, 7), (7, 7), (8, 7), (9, 7), (6, 9), (7, 9), (8, 9), (9, 9), (5, 8)}
    },
    {
        'hits': {(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)},
        'misses': {(5, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)}
    },
    {
        'hits': {(9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8)},
        'misses': {(8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (9, 2), (9, 9)}
    },
    {
        'hits': {(3, 0), (4, 0), (5, 0), (6, 0), (6, 1), (6, 2)},
        'misses': {(2, 0), (7, 0), (3, 1), (4, 1), (5, 1), (7, 1), (6, 3), (5, 2), (7, 2)}
    },
    {
        'hits': {(5, 9), (6, 9), (7, 9), (8, 9), (6, 7), (6, 8)},
        'misses': {(4, 9), (9, 9), (5, 8), (7, 8), (8, 8), (5, 7), (7, 7), (6, 6)}
    },
    {
        'hits': {(5, 4), (5, 5), (5, 6), (4, 5), (6, 5)},
        'misses': {(4, 4), (6, 4), (4, 6), (6, 6), (3, 5), (7, 5), (5, 3), (5, 7)}
    },
    {
        'hits': {(0, 0), (0, 1), (1, 0), (1, 1)},
        'misses': {(2, 0), (0, 2), (2, 1), (1, 2)}
    },
    {
        'hits': {(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1), (5, 0), (5, 1), (6, 0),
                 (6, 1), (7, 0), (7, 1), (8, 0), (8, 1), (9, 0), (9, 1)},
        'misses': {}
    },
    {
        'hits': {(0, 0), (0, 1), (2, 2), (2, 3), (4, 0), (4, 1), (6, 2), (6, 3), (8, 0), (8, 1), (1, 4), (1, 5), (3, 6),
                 (3, 7), (5, 4), (5, 5), (7, 6), (7, 7), (9, 4), (9, 5)},
        'misses': {}
    },

    # One horizontal and one vertical ship
    {
        'hits': {(1, 5), (2, 5), (3, 5), (6, 2), (6, 3)},
        'misses': {(4, 5), (6, 1), (6, 4), (0, 5), (1, 4), (2, 4), (3, 4), (1, 6), (2, 6), (3, 6), (5, 2), (5, 3),
                   (7, 2), (7, 3)}
    },


    # Two horizontal and two vertical ships
    {
        'hits': {(3, 2), (3, 3), (7, 6), (7, 7), (1, 9), (2, 9), (3, 9), (8, 2), (8, 3)},
        'misses': {(3, 1), (3, 4), (7, 5), (7, 8), (0, 9), (4, 9), (7, 2), (8, 1), (8, 4), (9, 2), (9, 3), (7, 3),
                   (8, 6), (8, 7), (6, 6), (6, 7), (2, 2), (2, 3), (4, 2), (4, 3), (1, 8), (2, 8), (3, 8)}
    },

    # Two L-shaped and two vertical ships
    {
        'hits': {(1, 1), (1, 2),  (5, 5), (5, 6), (6, 5), (8, 8), (8, 9), (9, 8), (3, 2), (4, 2)},
        'misses': {(0, 1), (0, 2), (2, 1), (4, 5), (4, 6), (6, 4), (7, 8), (7, 9), (9, 7), (2, 2), (5, 2), (9, 9),
                   (8, 7), (5, 4), (6, 6), (1, 0), (3, 1), (4, 1), (1, 3), (3, 3), (4, 3), (7, 5), (5, 7)}
    },

    # Four T-shaped ships
    {
        'hits': {(2, 2), (3, 2), (2, 3), (5, 5), (6, 5), (7, 5),  (9, 8), (9, 9), (8, 9), (1, 7), (2, 7),
                 (1, 8)},
        'misses': {(1, 2), (4, 2), (2, 1), (2, 4), (4, 5), (8, 5), (5, 4), (5, 6), (7, 4), (7, 6), (8, 8), (9, 7),
                   (0, 7),
                   (3, 7), (1, 6), (1, 9), (7, 9), (6, 4), (6, 6), (3, 1), (3, 3), (1, 3), (0, 8), (2, 8), (2, 6)}
    }
]

game_states_uncertain = [
    {
        'hits': {(2, 2), (2, 3), (2, 4)},
        'misses': {(1, 2), (1, 3), (1, 4), (3, 2), (3, 4), (2, 1), (2, 5)}
    },
    {
        'hits': {(7, 5), (8, 5), (9, 5)},
        'misses': {(7, 4), (7, 6), (8, 4), (8, 6), (9, 6), (6, 5)}
    },
    {
        'hits': {(5, 0), (6, 0), (7, 0), (8, 0), (9, 0)},
        'misses': {(5, 1), (6, 1), (7, 1), (8, 1), (9, 1), }
    },
    {
        'hits': {(2, 7), (3, 7), (4, 7), (5, 7)},
        'misses': {(2, 6), (2, 8), (3, 6), (3, 8), (5, 8), (1, 7), (6, 7)}
    },
    {
        'hits': {(1, 1), (2, 1), (3, 1), (1, 2), (3, 2)},
        'misses': {(0, 1), (4, 1), (1, 0), (3, 0), (3, 3), (0, 2), (2, 2), (4, 2)}
    },
    {
        'hits': {(7, 2), (8, 2), (7, 3), (8, 3)},
        'misses': {(6, 2), (6, 3), (9, 2), (9, 3), (7, 1), (8, 1), (8, 4)}
    },
    {
        'hits': {(3, 6), (4, 6), (5, 6), (6, 6), (7, 6)},
        'misses': {(4, 5), (5, 5), (6, 5), (7, 5), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (2, 6), (8, 6)}
    },
    {
        'hits': {(6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5)},
        'misses': {(5, 3), (5, 4), (5, 5), (8, 5), (6, 2), (6, 6), (7, 2), (7, 6)}
    },
    {
        'hits': {(0, 9), (1, 9), (2, 9), (3, 9)},
        'misses': {(0, 8), (1, 8), (3, 8), (4, 9)}
    },
    {
        'hits': {(6, 8), (7, 8), (8, 8), (9, 8)},
        'misses': {(6, 7), (7, 7), (8, 7), (6, 9), (7, 9), (8, 9), (9, 9), (5, 8)}
    },
    {
        'hits': {(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)},
        'misses': {(5, 1), (0, 0), (1, 0), (2, 0), (4, 0), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)}
    },
    {
        'hits': {(9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8)},
        'misses': {(8, 3), (8, 4), (8, 5), (8, 8), (9, 2), (9, 9)}
    },
    {
        'hits': {(3, 0), (4, 0), (5, 0), (6, 0), (6, 1), (6, 2)},
        'misses': {(2, 0), (7, 0), (3, 1), (4, 1), (6, 3), (5, 2), (7, 2)}
    },
    {
        'hits': {(5, 9), (6, 9), (7, 9), (8, 9), (6, 7), (6, 8)},
        'misses': {(4, 9), (9, 9), (5, 8), (7, 8), (8, 8), (7, 7), (6, 6)}
    },
    {
        'hits': {(5, 4), (5, 5), (5, 6), (4, 5), (6, 5)},
        'misses': {(4, 4), (6, 4), (6, 6), (3, 5), (7, 5), (5, 3), (5, 7)}
    },
    {
        'hits': {(0, 0), (0, 1), (1, 0), (1, 1)},
        'misses': {(0, 2), (2, 1), (1, 2)}
    },
    {
        'hits': {(0, 0), (0, 1), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1), (5, 0), (5, 1), (6, 0),
                 (6, 1), (7, 0), (7, 1), (8, 0), (8, 1), (9, 0), (9, 1)},
        'misses': {}
    },
    {
        'hits': {(0, 0), (0, 1), (2, 3), (4, 0), (4, 1), (6, 2), (8, 0), (8, 1), (1, 4), (1, 5), (3, 6),
                 (3, 7), (5, 4), (5, 5), (7, 6), (7, 7), (9, 4), (9, 5)},
        'misses': {}
    },

    # One horizontal and one vertical ship
    {
        'hits': {(1, 5), (2, 5), (3, 5), (6, 2), (6, 3)},
        'misses': {(4, 5), (6, 1), (6, 4), (0, 5), (1, 4), (2, 4), (3, 4), (1, 6)}
    },

    # Two horizontal and two vertical ships
    {
        'hits': {(3, 2), (3, 3), (7, 6), (7, 7), (1, 9), (2, 9), (3, 9), (8, 2), (8, 3)},
        'misses': {(3, 1), (3, 4), (7, 5), (7, 8), (0, 9), (4, 9)}
    },

    # Two L-shaped and two vertical ships
    {
        'hits': {(1, 1), (1, 2), (5, 5), (5, 6), (6, 5), (8, 8), (8, 9), (9, 8), (3, 2), (4, 2)},
        'misses': {(0, 1), (0, 2), (2, 1), (4, 5), (4, 6), (6, 4), (7, 8), (7, 9), (9, 7), (2, 2), (5, 2), (9, 9),
                   (8, 7), (5, 4), (6, 6), (1, 0), (3, 1), (4, 1), (1, 3)}
    },

    # Four T-shaped ships
    {
        'hits': {(2, 2), (3, 2), (2, 3), (5, 5), (6, 5), (7, 5), (9, 8), (9, 9), (8, 9), (1, 7), (2, 7),
                 (1, 8)},
        'misses': {(1, 2), (4, 2), (2, 1), (2, 4), (4, 5), (8, 5), (5, 4), (5, 6), (7, 4), (7, 6), (8, 8), (9, 7),
                   (0, 7),
                   (3, 7), (1, 6), (1, 9), (7, 9), (6, 4), (6, 6), (3, 1)}
    }
]

board_size = 10
total_ship_cells = 20

import matplotlib.patches as patches

colors = ["red", "white", "green"]
bounds = [-1.5, -0.5, 0.5, 1.5]
cmap = plt.cm.colors.ListedColormap(colors)
norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)


def draw_boundaries(ax, cluster, color):
    x_vals, y_vals = zip(*cluster)
    left, right = min(x_vals), max(x_vals)
    bottom, top = min(y_vals), max(y_vals)
    # Need to subtract the coordinates from board size
    rectangle = patches.Rectangle((left - 0.5, board_size - 1 - top - 0.5), right - left + 1, top - bottom + 1,
                                  linewidth=5, edgecolor=color, facecolor='none')
    ax.add_patch(rectangle)


for i, game_state in enumerate(game_states + game_states_uncertain):
    hits, misses = game_state['hits'], game_state['misses']
    clusters = find_clusters(hits)
    status = find_cluster_status(clusters, misses, board_size)

    # Initialize a 10x10 board
    board = np.zeros((board_size, board_size))

    # Mark hits with 1 and misses with -1
    for hit in hits:
        # Invert y-coordinates here
        board[board_size - 1 - hit[1]][hit[0]] = 1
    for miss in misses:
        # Invert y-coordinates here
        board[board_size - 1 - miss[1]][miss[0]] = -1

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.imshow(board, cmap=cmap, norm=norm)
    ax.invert_yaxis()  # Keep this line to maintain the correct orientation in the plot
    ax.set_title(f'Case {i + 1}')
    im = ax.imshow(board, cmap=cmap, norm=norm)

    # Draw boundaries around clusters
    for i, cluster in enumerate(clusters):
        color = 'lime' if status[i] == 'sunk' else 'orange'  # green for sunk, orange for uncertain
        draw_boundaries(ax, cluster, color)

    # Show the color bar
    cbar = plt.colorbar(im, ticks=[-1, 0, 1])  # Pass the imshow output to colorbar
    cbar.ax.set_yticklabels(['Miss', 'Unknown', 'Hit'])

    # Show the grid
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=0.5)
    ax.set_xticks(np.arange(-.5, board_size, 1));
    ax.set_yticks(np.arange(-.5, board_size, 1));

    # Add labels for sunk and uncertain counts
    sunk_count = status.count('sunk')
    uncertain_count = status.count('uncertain')
    ax.text(0.02, 0.95, f'Sunk: {sunk_count}', transform=ax.transAxes, color='lime', fontsize=12, fontweight='bold')
    ax.text(0.02, 0.9, f'Uncertain: {uncertain_count}', transform=ax.transAxes, color='orange', fontsize=12,
            fontweight='bold')

    # Display the plot
    plt.show()
