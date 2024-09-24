import matplotlib.pyplot as plt
from collections import deque
import random

# Constants for grid elements
GRID_SIZE = 5
EMPTY = 0
MOUSE = 1
CHEESE = 2
CAT = 3
END = 4

# Initialize the grid with mouse, cheese, cats, and end
def initialize_grid():
    grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    # Place the mouse at the starting position
    mouse_pos = (0, 0)
    grid[mouse_pos[0]][mouse_pos[1]] = MOUSE
    
    # Place the end point at the bottom-right corner
    end_pos = (GRID_SIZE - 1, GRID_SIZE - 1)
    grid[end_pos[0]][end_pos[1]] = END
    
    # Place some cheese at random positions
    cheese_positions = []
    for _ in range(3):  # Limit the number of cheese to avoid blockages
        while True:
            pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if grid[pos[0]][pos[1]] == EMPTY:
                grid[pos[0]][pos[1]] = CHEESE
                cheese_positions.append(pos)
                break

    # Place cats (obstacles) at random positions
    for _ in range(5):  # Limit the number of cats
        while True:
            pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if grid[pos[0]][pos[1]] == EMPTY:
                grid[pos[0]][pos[1]] = CAT
                break

    # Ensure there's at least one valid path from mouse to end
    if not find_path(grid, mouse_pos, end_pos):
        # If no path exists, reset the grid and try again
        return initialize_grid()
    
    return grid, mouse_pos, end_pos, cheese_positions

# Function to check if a path exists using DFS
def find_path(grid, start, end):
    stack = [start]
    visited = set()

    while stack:
        current = stack.pop()
        if current == end:
            return True
        if current in visited:
            continue
        visited.add(current)
        
        x, y = current
        # Explore all four directions
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if grid[nx][ny] == EMPTY or grid[nx][ny] == END:
                    stack.append((nx, ny))
    
    return False

# BFS Algorithm to find the shortest path while collecting all cheese
def bfs_visualized(grid, start, end, cheese_positions):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    total_cheese = len(cheese_positions)
    
    queue = deque([(start, [], set())])  # (current_position, path, collected_cheese)
    visited = set()
    full_path = []

    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots(figsize=(8, 8))
    
    while queue:
        (x, y), current_path, collected_cheese = queue.popleft()
        current_path.append((x, y))
        
        # Visualize the current position of the mouse
        visualize_path(ax, grid, current_path, len(collected_cheese), end)
        plt.pause(0.5)

        # Add cheese position if collected
        if grid[x][y] == CHEESE:
            collected_cheese.add((x, y))

        # Check if we've reached the end with all the cheese collected
        if (x, y) == end and len(collected_cheese) == total_cheese:
            full_path = current_path
            break
        
        # Explore all four directions
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] == EMPTY or grid[nx][ny] == CHEESE or (nx, ny) == end:
                    state = (nx, ny)
                    if (state, frozenset(collected_cheese)) not in visited:
                        visited.add((state, frozenset(collected_cheese)))
                        queue.append(((nx, ny), list(current_path), set(collected_cheese)))

    plt.ioff()  # Turn off interactive mode
    visualize_path(ax, grid, full_path, len(collected_cheese), end)
    print("Path found:", full_path)
    plt.show()

# Visualization function
def visualize_path(ax, grid, path, cheese_count, end):
    ax.clear()
    ax.set_facecolor('black')

    # Set grid lines and ticks
    ax.set_xticks(range(GRID_SIZE))
    ax.set_yticks(range(GRID_SIZE))
    ax.grid(True, which='both', color='orange', linewidth=0.5)

    # Draw the elements inside the grid
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == MOUSE:
                ax.text(j + 0.5, i + 0.5, "M", ha='center', va='center', fontsize=12, fontweight='bold', color='red')
            elif grid[i][j] == CHEESE:
                ax.text(j + 0.5, i + 0.5, "C", ha='center', va='center', fontsize=12, fontweight='bold', color='yellow')
            elif grid[i][j] == CAT:
                ax.text(j + 0.5, i + 0.5, "X", ha='center', va='center', fontsize=12, fontweight='bold', color='darkgreen')
            elif grid[i][j] == END:
                ax.text(j + 0.5, i + 0.5, "E", ha='center', va='center', fontsize=12, fontweight='bold', color='green')

    # Draw the path if it exists
    if path:
        for (x, y) in path:
            ax.plot([y + 0.5], [x + 0.5], marker='o', markersize=8, color='pink')  # Trailing line
            if path.index((x, y)) != 0:  # Skip the first point
                prev_x, prev_y = path[path.index((x, y)) - 1]
                ax.plot([prev_y + 0.5, y + 0.5], [prev_x + 0.5, x + 0.5], color='pink', linewidth=2)

    # Draw current position of the mouse
    if path:
        current_pos = path[-1]
        ax.text(current_pos[1] + 0.5, current_pos[0] + 0.5, "M", ha='center', va='center', fontsize=12, fontweight='bold', color='red')

    # Legend
    ax.legend(['Mouse', 'Cheese', 'Cat', 'End'], loc='upper left', fontsize=10, frameon=False)
    
    ax.set_xlim(0, GRID_SIZE)
    ax.set_ylim(0, GRID_SIZE)
    ax.invert_yaxis()  # Invert Y axis to match the grid layout

# Main function to run everything
def run_mice_and_cheese():
    grid, mouse_pos, end_pos, cheese_positions = initialize_grid()
    bfs_visualized(grid, mouse_pos, end_pos, cheese_positions)

run_mice_and_cheese()
