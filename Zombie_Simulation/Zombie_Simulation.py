
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.ndimage.filters import convolve

infection_rate = 0.4
incubation_rate = 1.0

dispersion_rates = [0, 0.5, 0.8]
dispersion_kernel = np.array([[0.5, 1 , 0.5],
                                [1, -6, 1],   
                                [0.5, 1, 0.5]]) /6.0
                                
t = 0
dt = 1.0
days = 300

usa = plt.imread("usa_density.png")
SIR = np.zeros((3,)+usa.shape)
SIR[0] = usa
SIR[1,200,512] = 0  # patient zero

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

def update():
    global SIR, t, dt
    infect = infection(SIR, infection_rate, incubation_rate)
    disperse = dispersion(SIR, dispersion_kernel, dispersion_rates)
    SIR += dt*( infect + disperse)
    t += dt

fig = plt.figure(figsize=(6,4.8), dpi=100)   
myCM = cm.get_cmap("Reds")
myCM._init()
alphas = np.linspace(0,1,myCM.N)
myCM._lut[:-3,-1] = alphas

for i in range(days*24):
    update()
    if (i%24==0):
        R = SIR[2]
        ax = fig.add_axes([0,0,1,1], aspect=1)
        plt.imshow(usa, cmap="Greys_r", interpolation="nearest")
        plt.imshow(R, cmap=myCM, interpolation="nearest")
        plt.savefig()
        plt.clf()
