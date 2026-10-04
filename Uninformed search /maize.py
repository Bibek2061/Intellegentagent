# import numpy as np
# import matplotlib.pyplot as plt
# # 0 = path (white), 1 = wall (black)
# maze = np.array([
#     [1,0,1,1,1,1,1,1,1,0,1,1],
#     [1,0,1,1,1,1,1,1,1,0,1,1],
#     [1,0,0,0,0,0,0,0,0,0,0,1],
#     [1,0,1,1,1,1,1,1,1,1,0,1],
#     [1,0,1,0,0,0,0,0,0,1,1,1],
#     [1,0,0,0,1,1,1,1,1,1,1,1],
#     [1,0,1,0,1,1,1,0,1,1,1,1],
#     [1,0,1,0,0,0,1,0,1,1,1,1],
#     [1,0,1,1,1,0,0,0,0,0,0,1],
#     [1,0,1,1,1,1,1,1,1,1,0,1],
#     [0,0,1,1,1,1,1,0,0,0,0,1]
# ], dtype=int)
# # Start (A) and Goal (B)
# start = (10, 0)
# goal  = (6, 7)
# fig, ax = plt.subplots(figsize=(8, 7))
# ax.imshow(maze, cmap="gray_r", interpolation="nearest")
# # Draw borders around every cell
# rows, cols = maze.shape
# ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
# ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
# ax.grid(which="minor", color="gray", linestyle="-", linewidth=0.8)
# ax.text(start[1], start[0], "A", ha="center", va="center", color="blue", fontsize=16)
# ax.text(goal[1],  goal[0],  "B", ha="center", va="center", color="red",  fontsize=16)
# plt.show()



#Using BFS and DFS to find a path in the maze

import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# 0 = path (white), 1 = wall (black)
maze = np.array([
    [1,0,1,1,1,1,1,1,1,0,1,1],
    [1,0,1,1,1,1,1,1,1,0,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,1,1,1],
    [1,0,0,0,1,1,1,1,1,1,1,1],
    [1,0,1,0,1,1,1,0,1,1,1,1],
    [1,0,1,0,0,0,1,0,1,1,1,1],
    [1,0,1,1,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,0,1],
    [0,0,1,1,1,1,1,0,0,0,0,1]
], dtype=int)

start = (10, 0)
goal = (6, 7)

# Explore in this order: Up, Right, Down, Left
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def get_neighbors(position):
    row, col = position
    rows, cols = maze.shape

    for dr, dc in directions:
        nr, nc = row + dr, col + dc

        if 0 <= nr < rows and 0 <= nc < cols:
            if maze[nr, nc] == 0:
                yield (nr, nc)


def reconstruct_path(parent, end):
    path = []
    current = end

    while current is not None:
        path.append(current)
        current = parent[current]

    return path[::-1]


def bfs(start, goal):
    queue = deque([start])
    parent = {start: None}
    explored = []

    while queue:
        current = queue.popleft()
        explored.append(current)

        if current == goal:
            return reconstruct_path(parent, goal), explored

        for neighbor in get_neighbors(current):
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)

    return None, explored


def dfs(start, goal):
    visited = set()
    parent = {start: None}
    explored = []

    def visit(current):
        visited.add(current)
        explored.append(current)

        if current == goal:
            return True

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                parent[neighbor] = current

                if visit(neighbor):
                    return True

        return False

    if visit(start):
        return reconstruct_path(parent, goal), explored

    return None, explored


def draw_result(ax, path, explored, name, path_color):
    ax.imshow(maze, cmap="gray_r", vmin=0, vmax=1,
              interpolation="nearest")

    rows, cols = maze.shape
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which="minor", color="gray", linewidth=0.8)
    ax.tick_params(which="minor", bottom=False, left=False)

    # Light blue cells show explored positions.
    ax.scatter(
        [pos[1] for pos in explored],
        [pos[0] for pos in explored],
        color="lightskyblue",
        marker="s",
        s=180,
        alpha=0.5
    )

    if path:
        ax.plot(
            [pos[1] for pos in path],
            [pos[0] for pos in path],
            color=path_color,
            linewidth=3,
            marker="o",
            markersize=4
        )
        ax.set_title(
            f"{name}: {len(path) - 1} moves | "
            f"{len(explored)} cells explored"
        )
    else:
        ax.set_title(f"{name}: No path found")

    for position, label, color in [
        (start, "A", "blue"),
        (goal, "B", "red")
    ]:
        ax.text(
            position[1], position[0], label,
            ha="center", va="center",
            color=color, fontsize=16, fontweight="bold",
            bbox=dict(facecolor="white", edgecolor="none", pad=1)
        )

    ax.set_xlabel("Column")
    ax.set_ylabel("Row")


bfs_path, bfs_explored = bfs(start, goal)
dfs_path, dfs_explored = dfs(start, goal)

for name, path, explored in [
    ("BFS", bfs_path, bfs_explored),
    ("DFS", dfs_path, dfs_explored)
]:
    print(f"\n{name}")
    print("Path:", path)
    print("Moves:", len(path) - 1 if path else "No path found")
    print("Cells explored:", len(explored))

fig, axes = plt.subplots(1, 2, figsize=(14, 7))

draw_result(axes[0], bfs_path, bfs_explored, "BFS", "green")
draw_result(axes[1], dfs_path, dfs_explored, "DFS", "darkorange")

plt.tight_layout()
plt.show()