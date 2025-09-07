# room_tiling_spiral.py
"""
Room Tiling with Squares (Spiral Fill Visualization)

- Fill the room using the minimum number of tiles (always try to place bigger tiles first)
- The tiling should proceed in a circular/spiral motion starting from the center
- If after placing larger tiles, there is some empty space left in the center, that space must be filled only with 1×1 tiles
- Visualize the result with matplotlib (different colors for each tile size)

Input:
- width and height of room (dimensions in x and y direction)
- The sizes of the tiles are fixed: 1x1 (Red), 2x2 (Blue), 3x3 (Yellow), 4x4 (Green)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation

TILE_SIZES = [4, 3, 2, 1]  # Prioritize larger tiles
TILE_COLORS = {
    4: 'green',   # 4x4
    3: 'yellow',  # 3x3
    2: 'blue',    # 2x2
    1: 'red'      # 1x1
}

def spiral_tile_anchors(m, n, tile_size):
    spiral = []
    top, bottom, left, right = 0, m - tile_size, 0, n - tile_size
    while left <= right and top <= bottom:
        # Bottom row: left to right
        for j in range(left, right + 1, tile_size):
            print(right,j)
            spiral.append((bottom, j))
        # Right col: bottom-tile_size up to top
        for i in range(bottom - tile_size, top - 1, -tile_size):
            print(i,right)
            spiral.append((i, right))
        # Top row: right-tile_size to left, only if there is more than one row
        if top < bottom:
            for j in range(right - tile_size, left - 1, -tile_size):
                print(top,j)
                spiral.append((top, j))
        # Left col: top+tile_size to bottom-tile_size, only if there is more than one col
        if left < right:
            for i in range(top + tile_size, bottom, tile_size):
                print(i,left)
                spiral.append((i, left))
        left += tile_size
        right -= tile_size
        top += tile_size
        bottom -= tile_size
    return spiral

def fill_room_spiral_tile_anchors_animated(m, n):
    grid = np.zeros((m, n), dtype=int)
    steps = []
    for size in TILE_SIZES:
        spiral = spiral_tile_anchors(m, n, size)
        for x, y in spiral:
            if size == 1:
                if grid[x, y] == 0:
                    grid[x, y] = 1
                    steps.append(grid.copy())
            else:
                if grid[x, y] == 0:
                    if x + size <= m and y + size <= n and np.all(grid[x:x+size, y:y+size] == 0):
                        grid[x:x+size, y:y+size] = size
                        steps.append(grid.copy())
    return steps

def animate_tiling(steps):
    grid = steps[-1]
    m, n = grid.shape
    fig, ax = plt.subplots(figsize=(n/2 + 2, m/2 + 1))  # Extra space for legend
    ax.set_xlim(0, n)
    ax.set_ylim(0, m)
    ax.set_aspect('equal')
    ax.set_xticks(np.arange(0, n+1, 1))
    ax.set_yticks(np.arange(0, m+1, 1))
    ax.set_yticklabels(np.arange(0, m+1, 1))
    ax.grid(True, which='both', color='gray', linewidth=0.5, linestyle='--', alpha=0.5)
    
    # Create legend handles and labels
    legend_handles = []
    legend_labels = []
    
    # Count tiles of each size
    tile_counts = {1: 0, 2: 0, 3: 0, 4: 0}
    for i in range(m):
        for j in range(n):
            size = grid[i, j]
            if size > 0:
                tile_counts[size] += 1
    
    # Create legend entries
    for size in sorted(tile_counts.keys()):
        if tile_counts[size] > 0:  # Only show sizes that exist
            color = TILE_COLORS[size]
            legend_handles.append(plt.Rectangle((0,0),1,1, facecolor=color, edgecolor='black', alpha=0.7))
            legend_labels.append(f'{size}x{size}: {tile_counts[size]//(size*size)}')
    
    # Add legend
    ax.legend(legend_handles, legend_labels, loc='upper left', bbox_to_anchor=(1.05, 1), 
              title='Tile Counts', borderaxespad=0.)
    
    drawn = np.zeros_like(grid, dtype=bool)
    patches = []

    def init():
        for patch in patches:
            patch.remove()
        patches.clear()
        return patches

    def update(frame):
        nonlocal drawn
        for patch in patches:
            patch.remove()
        patches.clear()
        drawn = np.zeros_like(grid, dtype=bool)
        grid_frame = steps[frame]
        
        # Update tile counts for current frame
        tile_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for i in range(m):
            for j in range(n):
                size = grid_frame[i, j]
                if size > 0 and not drawn[i, j]:
                    tile_counts[size] += 1
                    color = TILE_COLORS[size]
                    rect = Rectangle((j, i), size, size, facecolor=color, edgecolor='black', lw=1, alpha=0.7)
                    ax.add_patch(rect)
                    patches.append(rect)
                    drawn[i:i+size, j:j+size] = True
        
        # Update title with current step
        ax.set_title(f'Step {frame + 1}/{len(steps)}', pad=20)
        return patches

    anim = FuncAnimation(fig, update, frames=len(steps), init_func=init, 
                        blit=False, interval=500, repeat=False)
    plt.tight_layout()
    plt.subplots_adjust(right=0.8)  # Make room for legend
    plt.show()
    

def main():
    try:
        width = int(input("Enter room width (number of columns): "))
        height = int(input("Enter room height (number of rows): "))
    except ValueError:
        print("Invalid input. Please enter integer values.")
        return
    steps = fill_room_spiral_tile_anchors_animated(height, width)
    animate_tiling(steps)
if __name__ == "__main__":
    main()
