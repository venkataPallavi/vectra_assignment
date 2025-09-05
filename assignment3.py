import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def lattice_point(i, j, side):
    """
    Return coordinates (x,y) of the lattice point P(i,j).
    i, j are integer indices on a triangular lattice.
    side is the side length of each small triangle.
    """
    h = math.sqrt(3) / 2 * side  # height of a small equilateral triangle
    x = j * side + i * (side / 2)
    y = i * h
    return (x, y)

def build_and_draw_pyramid(side=1.0, depth=4, color_upright="tab:blue", color_inverted="tab:orange"):
    """
    Build and draw a big equilateral pyramid made of small equilateral triangles.
    - side  : side length of each small triangle
    - depth : number of small-triangle rows along each side (D)
    
    How it works :
      * We place lattice points P(i,j) = i*v1 + j*v2, where
          v1 = (side/2, height) and v2 = (side, 0).
      * Upright triangles are formed by points:
          P(i,j), P(i,j+1), P(i+1,j)
        for i=0..D-1 and j=0..D-1-i
      * Inverted triangles are formed by points:
          P(i+1,j+1), P(i,j+1), P(i+1,j)
        for i=0..D-2 and j=0..D-2-i
      * This produces exactly D^2 small triangles that tile the larger equilateral triangle.
    """
    h = math.sqrt(3) / 2 * side

    triangles = []  # will hold (vertices, color)

    # Upright triangles
    for i in range(depth):
        for j in range(depth - i):
            A = lattice_point(i, j, side)
            B = lattice_point(i, j + 1, side)
            C = lattice_point(i + 1, j, side)
            triangles.append(([A, B, C], color_upright))

    # Inverted triangles
    for i in range(depth - 1):
        for j in range(depth - 1 - i):
            A = lattice_point(i + 1, j + 1, side)
            B = lattice_point(i, j + 1, side)
            C = lattice_point(i + 1, j, side)
            triangles.append(([A, B, C], color_inverted))

    # Center the big triangle horizontally at x = 0
    x_shift = (depth * side) / 2.0
    shifted_triangles = []
    for verts, col in triangles:
        shifted = [ (x - x_shift, y) for (x,y) in verts ]
        shifted_triangles.append((shifted, col))

    # Draw
    fig_w = max(6, depth * 0.8)
    fig_h = max(6, depth * 0.8)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    for verts, col in shifted_triangles:
        poly = Polygon(verts, closed=True, edgecolor="black", linewidth=0.7, facecolor=col)
        ax.add_patch(poly)

    ax.set_aspect('equal')
    padding = side * 0.2
    ax.set_xlim(-x_shift - padding, x_shift + padding)
    ax.set_ylim(-padding, depth * h + padding)
    ax.axis('off')

    plt.title(f"Pyramid of depth={depth}  (small triangle side={side})", fontsize=14)
    plt.show()

# Example: depth=4, side length=1.0 (same as your sample)
build_and_draw_pyramid(side=1.0, depth=5, color_upright="royalblue", color_inverted="gold")
