# Importing libraries
import matplotlib.pyplot as plt
import numpy as np
import math
  
# Using Numpy to create an array X
X = np.arange(0, math.pi*2, 0.05)
  
# Assign variables to the y axis part of the curve
y = np.sin(X)
z = np.cos(X)

print(y)
  
# Plotting both the curves simultaneously
plt.plot(X, y, color='r', label='sin')
plt.plot(X, z, color='g', label='cos')
  
# Naming the x-axis, y-axis and the whole graph
plt.xlabel("Angle")
plt.ylabel("Magnitude")
plt.title("Sine and Cosine functions")
  
# Adding legend, which helps us recognize the curve according to it's color
plt.legend()
  
# To load the display window
plt.show()