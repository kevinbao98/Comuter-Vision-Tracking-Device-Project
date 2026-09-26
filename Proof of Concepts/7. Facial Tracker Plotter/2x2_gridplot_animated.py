from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

# 1. Setup figure and subplots (2 rows, 2 columns)
fig, axes = plt.subplots(4, 1, figsize=(10, 8)) # Divides canvas into two row and two columns
ax1, ax2, ax3, ax4 = axes.flatten()

# 2. Set static limits and labesl so they don't change during animation
ax1.set_xlim(0, 2 * np.pi)
ax1.set_ylim(-1.5, 1.5)
ax1.set_title("Moving Sine Wave")

ax2.set_xlim(0, 2 * np.pi)
ax2.set_ylim(-1.5, 1.5)
ax2.set_title("Moving Cosine Wave")

ax3.set_xlim(0, 2 * np.pi)
ax3.set_ylim(-10, 10)
ax3.set_title("Moving Tangent Wave")

ax4.set_xlim(0, 2 * np.pi)
ax4.set_ylim(-10, 10)
ax4.set_title("Moving Cotangent Wave")

# 3. Initialize empty line objects for each subplot
line1, = ax1.plot([], [], lw=2)
line2, = ax2.plot([], [], lw=2)
line3, = ax3.plot([], [], lw=2)
line4, = ax4.plot([], [], lw=2)

# 4. The init function to set the data of each line to empty lists
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    line4.set_data([], [])
    return line1, line2, line3, line4

# 5. The update function to animate the lines
def update(i):
    x = np.linspace(0, 2 *np.pi, 200)
    y1 = np.sin(x + i * 0.1)
    y2 = np.cos(x + i * 0.1)
    y3 = np.tan(x + i * 0.1)
    y4 = 1 / np.tan(x + i * 0.1)

    # Update the data inside the line objects
    line1.set_data(x, y1)
    line2.set_data(x, y2)
    line3.set_data(x, y3)
    line4.set_data(x, y4)
    return line1, line2, line3, line4

# 6. Create the animation object
'''
frames = how many steps before it loops
interval = delay between frames in milliseconds
blit = speeds up rendering by only drawing what has changed
'''
ani = FuncAnimation(fig, update, init_func=init, frames=200, interval=20, blit=True)

plt.tight_layout()
plt.show()