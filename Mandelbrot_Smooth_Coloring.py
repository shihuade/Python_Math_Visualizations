#coding = utf-8

import numpy as np
import matplotlib.pyplot as plt

max_iterations = 500
radius = 50
figsize = (1200, 960)

def escape(c):
    z = 0
    for i in xrange(max_iterations):
        if abs(z) > radius:
            break
        z = z**2 + c
