#coding = utf-8

# This script draws the figure of the E8 root system projected to its Coxeter plane.
# The main steps are outlined in the comments below.
# A nice explanation of the math behind this script can be found in Humphreys's book
# "Reflection Groups and Coxeter Groups", section 17, chapter 3.
# Casselman has also written a nice expository paper on this topic, see
# https://www.math.ubc.ca/~cass/research/pdf/Element.pdf

import numpy as np
import cairo
from itertools import product, combinations


#--- Step One: generate all roots and edges ---#

# There are 240 roots in the root system.
# Mutiply them by a factor 2 to be handy for computations. 
roots = []

# Roots of the form (+-1,+-1,0,0,0,0,0,0).
# Signs can be chosen independently and the two non-zeros can be anywhere.
for i,j in combinations(range(8),2):
    for x,y in product([-2,2], repeat=2):
        v = np.zeros(8)
        v[i] = x
        v[j] = y
        roots.append(v)
        
# Roots of the form 1/2 * (+-1, +-1, ..., +-1).
# Signs can be chosen indenpendently except that there must be an even numer of -1s.
for v in product([-1,1], repeat=8):
    if sum(v) % 4 == 0:
        roots.append(v)
        
roots = np.array(roots, dtype=int)

# Two roots are connected by an edge if and only if the angle between them is pi/3.
edges = []
for i in range(240):
    for j in range(i+1, 240):
        if np.sum((roots[i]-roots[j])**2) == 8:
            edges.append([i,j])
            

#--- Step Two: compute a basis of the Coxeter plane ---#

# Firstly let's write down explicitly a complete set of simple roots.
# Any choice of the set of simple roots would suffice.
# In the following the simple roots are given by the rows of the matrix "delta"
delta = np.eye(8)
for i in range(5):
    delta[i,i+1] = -1
delta[5,6] = 1
delta[6] = -0.5
delta[7,5] = 1
delta[7,6] = -1
delta[7,7] = 0

# Then the Cartan matrix will be:
cartan = np.dot(delta,delta.transpose())

# The Dynkin graph:
# 1---2---3---4---5---6---7
#                 |
#                 8
# Where label i corresponding to the i-th row of delta.

# Now we split the simple roots into two disjoint sets I and J
# such that the simple roots in I are pairwise orthogonal (as well as the roots in J).
# It's obvious to see how to find such a splitting given the Dynkin graph above:
# I = [1,3,5,7] and J = [2,4,6,8]
# since roots are not connected by an edge if and only if they are orthogonal.
# Then a basis of the Coxeter plane is given by
# u = sum (c[i] * delta[i]) for i in I
# v = sum (c[j] * delta[j]) for j in J
# Where c is the eigenvector corresponding to the maximal eigenvalue of the Cartan matrix.

# The eigenvalues returned by eigh() are in ascending order and the eigenvectors are listed by columns. 
I = [0,2,4,6]
J = [1,3,5,7]
eigenvals,eigenvecs= np.linalg.eigh(cartan)
c = eigenvecs[:,7]
u = np.sum([ c[i]*delta[i] for i in I ], axis=0)
v = np.sum([ c[j]*delta[j] for j in J ], axis=0)

# Gram-Schimdt and normalize to unit vectors.
u /= np.linalg.norm(u)
v = v - np.dot(u,v)*u
v /= np.linalg.norm(v)


#--- Step Three: project to the Coxeter plane ---#

roots_2d = np.zeros((240,2))
modulus = np.zeros(240)
colors = np.zeros((240,3))

def edge_color_map(x):
    if x < 0.6:
        return (0, 1, 1)  
    elif x < 0.8:
        return (0, 0, 1)
    elif x < 1.0:
        return (1, 0, 1)
    elif x < 1.2:
        return (0.25, 0.75, 0.5)
    elif x < 1.5:
        return (1, 1, 0)
    elif x < 1.6:
        return (0.5, 0.25, 0.75)
    elif x < 2.0:
        return (0, 1, 0)
    else:
        return (1, 0, 0)
        
for i in range(240):
    x = np.dot(roots[i],u)
    y = np.dot(roots[i],v)
    roots_2d[i] = [x,y]
    modulus[i] = np.linalg.norm([x,y])
    colors[i] = edge_color_map(modulus[i])

# Set the point size and line width.
size = 0.025
LineWidth = size/10.0
FIGSIZE = 600
surface = cairo.SVGSurface("E8_Root_System.svg", FIGSIZE, FIGSIZE)
cr = cairo.Context(surface)
cr.translate(FIGSIZE/2.0, FIGSIZE/2.0)
cr.scale(FIGSIZE/4.8, FIGSIZE/4.8)
cr.set_source_rgb(1,1,1)
cr.paint()

#draw edges:
for e in edges:
    x = roots_2d[e[0]]
    y = roots_2d[e[1]]
    a, b = x
    c, d = y
    if modulus[e[0]] > modulus[e[1]]:
        color = colors[e[0]]
    else:
        color = colors[e[1]]
    cr.move_to(a,b)
    cr.line_to(c,d)
    cr.set_source_rgb(*color)
    cr.set_line_width(LineWidth)            
    cr.stroke()

#draw vertices:
for i in range(240):
    x,y = roots_2d[i]
    color = colors[i]
    cr.arc(x,y,size,0, 2*np.pi)
    cr.set_source_rgb(*color)
    cr.fill_preserve()
    cr.set_source_rgb(0,0,0)
    cr.set_line_width(size/5)
    cr.stroke()

surface.show_page()
