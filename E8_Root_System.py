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

#--- Step Two: compute a basis of the Coxeter plane ---#

# Firstly let's write down explicitly a complete set of simple roots.
# Any choice of the set of simple roots would surfice.
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
u = np.sum([ c[i]*delta[i] for i in I ],axis=0)
v = np.sum([ c[j]*delta[j] for j in J ],axis=0)

# Gram-Schimdt and normalize to unit vectors.
u /= np.linalg.norm(u)
v = v - np.dot(u,v)*u
v /= np.linalg.norm(v)

#--- Step Two Finished ---#



   
