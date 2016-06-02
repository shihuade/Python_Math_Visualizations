
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import numpy as np
import moviepy.editor as mpy
from scipy.ndimage.filters import convolve

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
    newly_infected = infection_rate*S*R
    newly_rampaging = incubation_rate*I
    dS = - newly_infected
    dI = newly_infected - newly_rampaging
    dR = newly_rampaging
    return np.array([dS,dI,dR])
    
def Dispersion(SIR, dispersion_rate, dispersion_kernel):
    return np.array( [convolve(e, dispersion_kernel, mode="constant", cval=0)*r
                        for (e,r) in zip(SIR, dispersion_rates)])

  
