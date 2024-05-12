import pandas as pd
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2)

data = pd.read_csv('./results/2024-05-12_07-30-00/results.csv')
deflect_x = data['deflect_x']
deflect_y = data['deflect_y']

axes[0].plot(deflect_x, label='Tmax=4, Tmin=3')
axes[1].plot(deflect_y, label='Tmax=4, Tmin=3')

data = pd.read_csv('./results/2024-05-12_07-46-10/results.csv')
deflect_x = data['deflect_x']
deflect_y = data['deflect_y']

axes[0].plot(deflect_x, label='Tmax=5, Tmin=2')
axes[1].plot(deflect_y, label='Tmax=5, Tmin=2')

fig.suptitle('Deflection Analysis (x and y direction)', fontsize=16)
axes[0].legend()
axes[1].legend()

plt.show()
