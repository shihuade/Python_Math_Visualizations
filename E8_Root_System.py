#coding = utf-8

# This script draws the figure of the E8 root system projected to its Coxeter plane.
# The main steps are outlined in the comments below.
# A nice explanation of the math behind this script can be find in Humphreys's book
# "Reflection Groups and Coxeter Groups", section 17, chapter 3.
# Casselman also writes a nice expository paper on this topic, see
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
            
#--- Step One Finished ---#



