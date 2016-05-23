#coding=utf-8

import numpy as np
import matplotlib.pyplot as plt
from numpy import sqrt, sin, cos, pi
from matplotlib.colors import hsv_to_rgb

def Klein(z):
    #Klein j-函数
    return 1728*(z*(z**10+11*z**5-1))**5 / (-(z**20+1)+228*(z**15-z**5)-494*z**10)**3

def RiemannSphere(z):
    #将复平面上的点利用球极投影对应到Riemann球面上
    t = 1 + z.real**2 + z.imag**2
    return 2*z.real/t, 2*z.imag/t,2/t-1

def Mobius(z):
    #用一个mobius变换扭曲图像
    return (z-20)/(3*z+1j)

x,y = np.ogrid[-5:5:800j,-5:5:800j]
z = x + y*1j
z = Klein(z)
z = Mobius(z)
z = Klein(z)
w = RiemannSphere(z)

H = sin(w[0]*pi)**2
S = cos(w[1]*pi)**2
V = abs(sin(w[2]*pi) * cos(w[2]*pi))**0.2

HSV = np.dstack((H,S,V))
rgb = hsv_to_rgb(HSV)

fig = plt.figure(figsize=(8,8))
ax = fig.add_axes([0,0,1,1],aspect=1)
ax.axis('off')
plt.imshow(rgb)
plt.show()
#plt.savefig('Icosa_Symmetry.png')
