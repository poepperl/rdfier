import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# Setup, and create the data to plot
y = np.random.rand(10)
y[5:] *= 2
y[np.geomspace(1, 5, 4).astype(int)] = -1
mpl.rcParams['path.simplify'] = True

print(y)

mpl.rcParams['path.simplify_threshold'] = 0.0
plt.plot(y)
plt.show()

mpl.rcParams['path.simplify_threshold'] = 1.0
plt.plot(y)
plt.show()