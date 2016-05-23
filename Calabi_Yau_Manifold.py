#coding=utf-8

import numpy as np
from numpy import exp, pi, sinh, cosh, sin, cos
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(6,6))
ax = fig.add_axes([0,0,1,1], projection='3d', xlim=(-1,1), ylim=(-1,1), zlim=(-1,1))
ax.axis('off')
#ax.view_init(0, 60)

x = np.linspace(-1, 1, 30)
y = np.linspace(0, 0.5*pi, 30)
X,Y = np.meshgrid(x,y)

n = 5  
alpha = 0.5 * pi

def CalabiYau(z,k1,k2):
    z1 = exp(2*pi*1j*k1/n) * cosh(z)**(2.0/n)
    z2 = exp(2*pi*1j*k2/n) * sinh(z)**(2.0/n)
    return np.array([z1.real, z2.real, cos(alpha)*z1.imag + sin(alpha)*z2.imag])

for k1 in range(n):
    for k2 in range(n):
        Z = CalabiYau(X+Y*1j,k1,k2)
        surface = ax.plot_surface(Z[0] ,Z[1], Z[2], rstride=1, cstride=1, lw=0.1, cmap='jet')

#plt.show()
plt.savefig('Calabi_Yau_Manifold.png')
