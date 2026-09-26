import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)

# Create a 2x2 grid of subplots

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))

# Top-left subplot: Sine wave
axes[0,0].plot(x, np.sin(x), color='g')
axes[0,0].set_title('Sine Wave')

# Top-right subplot: Cosine wave
axes[0, 1].plot(x, np.cos(x), color='b')
axes[0, 1].set_title('Cosine Wave')

# Bottom-left subplot: Tangent wave
axes[1, 0].plot(x, np.tan(x), color='r')
axes[1, 0].set_title('Tangent Wave')

plt.tight_layout()
plt.show()