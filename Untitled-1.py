import numpy as np
import matplotlib.pyplot as plt

def fractal_flower(n_points=100000, n_iters=100, n_petals=8):
    # Set the initial point
    x, y = 0, 0
    # Initialize arrays to store the points
    x_points = [x]
    y_points = [y]

    # Generate points
    for _ in range(n_points):
        # Randomly choose a transformation and apply it
        theta = np.random.randint(0, n_petals) * (2 * np.pi / n_petals)
        x, y = 0.85 * (x * np.cos(theta) - y * np.sin(theta)), 0.85 * (x * np.sin(theta) + y * np.cos(theta))
        
        # Store the points
        x_points.append(x)
        y_points.append(y)

    return x_points, y_points

# Generate the fractal flower points
x_points, y_points = fractal_flower()

# Plot the fractal flower
plt.figure(figsize=(6, 6))
plt.scatter(x_points, y_points, s=0.1, color='purple')
plt.axis('equal')
plt.axis('off')
plt.show()
