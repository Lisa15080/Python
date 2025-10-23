import matplotlib.pyplot as plt
import numpy as np
import math

x = np.linspace(0, 2 * np.pi, 200)
print(type(x ))
y = np.tan(x)

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()