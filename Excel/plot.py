import numpy as np
import matplotlib.pyplot as plt

size = 0.3
vals = np.array([[60., 32.], [37., 40.], [70., 20.]])

cmap = plt.get_cmap("tab20c")
outer_colors = cmap(np.arange(3)*4)
inner_colors = cmap([1, 2, 5, 6, 9, 20])

print(vals.sum(axis=1))

plt.pie(vals.sum(axis=1), radius=1, colors=outer_colors, wedgeprops=dict(width=size, edgecolor='w'))
print(vals.flatten())

plt.pie(vals.flatten(), radius=1-size, colors=inner_colors, wedgeprops=dict(width=size, edgecolor='w'))

plt.axis('equal')
plt.show()
