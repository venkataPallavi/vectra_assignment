import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

# ------------------------------
# STEP 1: Polygon Vertices
# ------------------------------
# A polygon is formed by joining points (vertices).
# Here we define 5 points. The order matters (go around the shape in sequence).
vertices = np.array([
    (9.05, 7.76),   # V1
    (12.5, 3.0),    # V2
    (10.0, 0.0),    # V3
    (5.0, 0.0),     # V4
    (2.5, 3.0)      # V5
])

# Number of corners (vertices)
n = len(vertices)

# ------------------------------
# STEP 2: Edges of Polygon
# ------------------------------
# An edge is the line between two consecutive vertices.
# We create vectors for each edge by subtracting coordinates of two vertices.
edges = []
for i in range(n):
    p1 = vertices[i]                 # current vertex
    p2 = vertices[(i + 1) % n]       # next vertex (wrap to first after last)
    edge = p2 - p1                   # vector = (x2-x1, y2-y1)
    edges.append(edge)

# ------------------------------
# STEP 3: Area of Polygon
# ------------------------------
# Formula used = Shoelace Formula
# area = 1/2 * |(x1y2 + x2y3 + ... + xn y1) - (y1x2 + y2x3 + ... + yn x1)|
def polygon_area(points):
    area = 0.0
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        area += (x1 * y2 - x2 * y1)
    return abs(area) / 2

area_calc = polygon_area(vertices)

# Compare with Shapely (a library that does geometry for us)
poly = Polygon(vertices)
area_shapely = poly.area

# ------------------------------
# STEP 4: Length of Edges
# ------------------------------
# Length of a vector (edge) = √(x² + y²)
edge_lengths = [np.linalg.norm(e) for e in edges]

# ------------------------------
# STEP 5: Interior Angles
# ------------------------------
# Angle at a vertex is found using dot product formula:
# cosθ = (u · v) / (|u||v|)
# where u and v are vectors from current vertex to previous and next.
angles = []
for i in range(n):
    p_prev = vertices[i - 1]       # previous vertex
    p_curr = vertices[i]           # current vertex
    p_next = vertices[(i + 1) % n] # next vertex
    
    v1 = p_prev - p_curr   # vector pointing to previous vertex
    v2 = p_next - p_curr   # vector pointing to next vertex
    
    dot = np.dot(v1, v2)   # dot product
    norm = np.linalg.norm(v1) * np.linalg.norm(v2)  # |v1||v2|
    cos_theta = dot / norm
    cos_theta = np.clip(cos_theta, -1.0, 1.0)       # avoid rounding issues
    theta = np.degrees(np.arccos(cos_theta))        # convert to degrees radiens --> degrees 
    
    angles.append(theta)

# Polygon is convex if all interior angles < 180
is_convex = all(a < 180 for a in angles)

# ------------------------------
# STEP 6: Centroid of Polygon
# ------------------------------
# Simple centroid = average of all x-coordinates and y-coordinates
centroid_simple = np.mean(vertices, axis=0)

# Shapely's centroid (geometrical one)
centroid_shapely = np.array([poly.centroid.x, poly.centroid.y])

# ------------------------------
# STEP 7: Print Results
# ------------------------------
print("Polygon Area (Shoelace):", area_calc)
print("Polygon Area (Shapely):", area_shapely)
print("Edge Lengths:", edge_lengths)
print("Interior Angles (degrees):", angles)
print("Is Convex:", is_convex)
print("Centroid (Average of Vertices):", tuple(centroid_simple))
print("Centroid (Shapely):", tuple(centroid_shapely))

# ------------------------------
# STEP 8: Visualization
# ------------------------------
plt.figure(figsize=(6,6))

# Draw filled polygon
plt.fill(vertices[:,0], vertices[:,1], alpha=0.3, color="lightblue", edgecolor="black")

# Mark and label vertices
for i, (x, y) in enumerate(vertices):
    plt.plot(x, y, "bo")                      # blue dots for vertices
    plt.text(x+0.1, y+0.1, f"V{i+1}", fontsize=10)  # label V1, V2, ..., shifts the label slightly so it doesn’t overlap the dot.

# Mark centroid
plt.plot(centroid_simple[0], centroid_simple[1], "ro", label="Centroid")

# Show angle values near vertices
for i, (x, y) in enumerate(vertices):
    plt.text(x-0.3, y-0.3, f"{angles[i]:.1f}°", fontsize=8, color="green")

plt.title("Polygon Geometry Visualization")
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.show()
