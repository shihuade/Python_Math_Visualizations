# coding = utf-8

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import convolve

dt = 1.0  # one hour as time step
infection_rate = 0.2
incubation_rate = 0.8
dispersion_rates = [0, 0.3, 0.12]
dispersion_kernel = np.array([[0, 1.0 , 0],
                                [1, -4.0, 1],   
                                [0, 1, 0]]) /4.0
                                
usa = plt.imread("usa_density.png")
SIR = np.zeros((3,)+usa.shape)
SIR[0] = usa
SIR[1,200,512] = 1.0  # patient zero


def infection(SIR, infection_rate, incubation_rate):
    S,I,R = SIR
    newly_infected = infection_rate*R*S
    newly_rampaging = incubation_rate*I
    dS = - newly_infected
    dI = newly_infected - newly_rampaging
    dR = newly_rampaging
    return np.array([dS, dI, dR])


def dispersion(SIR, dispersion_kernel, dispersion_rates):
    return np.array( [convolve(e, dispersion_kernel, mode="constant", cval=0)*r
                       for (e,r) in zip(SIR, dispersion_rates)])
                       

def update(SIR, dt):
    infect = infection(SIR, infection_rate, incubation_rate)
    SIR += dt*infect
    disperse = dispersion(SIR, dispersion_kernel, dispersion_rates)
    SIR += dt*disperse
    
days = 300
fig = plt.figure(figsize=(6,4.8), dpi=100)   
for i in range(days*24):
    update(SIR, dt)
    if (i%24==0):
        ax = fig.add_axes([0,0,1,1], aspect=1)
        ax.axis("off")
        I, R = SIR[1:]
        M = np.zeros_like(I)
        img = np.dstack((R**0.1, I**0.2, M, R**0.2))
        plt.imshow(usa, cmap="Greys_r", interpolation="nearest")
        plt.imshow(img, interpolation="nearest")
        plt.savefig("zombie%03d.png"%(i/24))
        plt.clf()
