
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import numpy as np
import moviepy.editor as mpy
from scipy.signal import convolve2d as conv2

usa = mpy.ImageClip("usa_density.png").resize(width=600)
SIR = np.zeros((3, usa.h, usa.w)).astype(np.float)
SIR[0] = usa.get_frame(0) / 255

dispersion_rates = [0, 0.5, 0.3]
dispersion_kernel = np.array([[0.5, 1 , 0.5],
                              [1, -6, 1],
                              [0.5, 1, 0.5]]) / 6

infection_rate = 0.5
incubation_rate = 0.8

def Infection(SIR, infection_rate, incubation_rate):
  
