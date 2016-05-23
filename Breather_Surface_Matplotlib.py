#coding=utf-8

import numpy as np
from numpy import sinh, cosh, sin, cos, sqrt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(6,6))
ax = fig.gca(projection='3d', xlim=(-3,3), ylim=(-3,3), zlim=(-3,3), aspect=1)
#ax.axis('off')

x = np.linspace(-10,10,100)
y = np.linspace(0,50,200)
u,v = np.meshgrid(x,y)

a = 0.5
w = sqrt(1-a**2)

def breather(u,v):
    denom = a*((w*cosh(a*u))**2 + (a*sin(w*v))**2)
    x = -u+2*w**2*cosh(a*u)*sinh(a*u) / denom
    y = 2*w*cosh(a*u)*(-w*cos(v)*cos(w*v)-sin(v)*sin(w*v)) /denom
    z = 2*w*cosh(a*u)*(-w*sin(v)*cos(w*v)+cos(v)*sin(w*v)) /denom
    return x,y,z

Z = breather(u,v)
surface = ax.plot_surface(Z[0],Z[1],Z[2],rstride=1,cstride=1,lw=0.1,cmap='jet')
#plt.show()
plt.savefig('Breather_Surface_Matplotlib.png')
