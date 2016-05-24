#coding = utf-8

import numpy as np
import matplotlib.pyplot as plt

max_iterations = 100

def escape(c):
    z = 0
    for i in range(max_iterations):
        if abs(z) > 10:
            break
        z = z*z + c
    # Smooth the coloring
    if abs(z) > 2:
        i = i - np.log2(np.log2(abs(z)))
    return i
    
y,x = np.ogrid[-1.4:1.4:500j,-2:1:500j]
z = x+y*1j
mandelbrot = np.frompyfunc(escape,1,1)(z).astype(np.float)
fig = plt.figure(figsize=(6,6))
ax = fig.add_axes([0,0,1,1], aspect=1)
ax.axis("off")
plt.imshow(mandelbrot, cmap="Blues_r")
plt.savefig("Mandelbrot.png")
