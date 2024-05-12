import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)

data = pd.read_csv('./results/2024-05-12_07-46-10/results.csv')
deflect_x = data['deflect_x']
deflect_y = data['deflect_y']

deflect = np.column_stack((deflect_x, deflect_y))

# Normalize each vector in the deflect list
deflect_normalized = deflect / np.linalg.norm(deflect, axis=1)[:, np.newaxis]

X = deflect_normalized[:, 0].copy()
Y = deflect_normalized[:, 1].copy()
zeros = np.zeros_like(X)

print(Y)

# Plot the normalized vectors in the coordinate system
ax.quiver(zeros, zeros, X, Y, scale=2)
# ax.scatter(X, Y)
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_aspect('equal')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Normalized Vectors')

plt.show()

# TODO: complete the rest