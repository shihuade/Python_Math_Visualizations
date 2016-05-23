#coding=utf-8

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb

def Klein(z):
    #Klein j-function
    return 1728*(z*(z**10+11*z**5-1))**5 / (-(z**20+1)+228*(z**15-z**5)-494*z**10)**3

def RiemannSphere(z):
    #mapping to Riemann Sphere via stereographic projection
    t = 1 + z.real**2 + z.imag**2
    return 2*z.real/t, 2*z.imag/t, 2/t-1

def Mobius(z):
    #distort the result image by a mobius transformation
    return (z-20)/(3*z+1j)

x,y = np.ogrid[-5:5:800j,-5:5:800j]
z = x + y*1j
z = RiemannSphere(Klein(Mobius(Klein(z))))

H = np.sin(z[0]*np.pi)**2
S = np.cos(z[1]*np.pi)**2
V = abs(np.sin(z[2]*np.pi) * np.cos(z[2]*np.pi))**0.2

HSV = np.dstack((H,S,V))
RGBImage = hsv_to_rgb(HSV)

fig = plt.figure(figsize=(8,8))
ax = fig.add_axes([0,0,1,1], aspect=1)
ax.axis('off')
plt.imshow(RGBImage)
#plt.show()
plt.savefig('Icosa_Symmetry.png')
