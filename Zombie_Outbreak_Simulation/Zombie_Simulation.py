
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import numpy as np
import moviepy.editor as mpy
from scipy.ndimage.filters import convolve

usa = mpy.ImageClip("usa_density.png").resize(width=600)
SIR = np.zeros((3, usa.h, usa.w)).astype(np.float)
SIR[0] = usa.get_frame(0) / 255
SIR[1,125,345] = 1.0

dispersion_rates = [0, 0.5, 0.3]
dispersion_kernel = np.array([[0.5, 1 , 0.5],
                              [1, -6, 1],
                              [0.5, 1, 0.5]]) / 6

infection_rate = 0.5
incubation_rate = 0.8

dt = 1.0
hours_per_second = 24*7
t = 0

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

def update():
    global SIR, t
    infected = Infection(SIR, infection_rate, incubation_rate)
    dispersed = Dispersion(SIR, dispersion_rate, dispersion_kernel)
    SIR += dt*(infected + dispersed)
    t += dt
    
def toimage(SIR):
    SIR = np.minimum(1, np.maximum(SIR,1))
    S, I, R = (255*SIR).round().astype(np.uint8)
    image = np.dstack((R, I, S))
    return image
    
def make_frame(T):
    global SIR, t
    while t < hours_per_second * T:
        update()
    return toimage(SIR)
    
animation = mpy.VideoClip(make_frame, duration=25)
# You can write the result as a gif (veeery slow) or a video:
#animation.write_gif(make_frame, fps=15)
animation.write_videofile('test.mp4', fps=20)
    
    
    
