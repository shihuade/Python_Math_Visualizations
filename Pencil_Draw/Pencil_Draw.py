# coding = utf-8

# A Python implementation of the algorithm depicted in CeWu Lu, Li Xu, JiaYa Jia's paper 
# "Combining Sketch and Tone for Pencil Drawing Production".
# I wrapped everything in this single file.

# There are three main steps:
# 1. Generate the stroke map S of the image.
# 2. Generate the tone map T of the image.
# 3. Combine S and T to get the final output.
# For detailed explanations of these steps see the comments below.

import numpy as np
import Image as im
import scipy.sparse as sps
from skimage.transform import rotate
from scipy.signal import convolve2d as conv2

Input_Image = "house.jpg"
Pencil_Texture = "texture.jpg"

# Global parameters:
Line_Len = 15  
kr = Line_Len // 2  # kernel radius
LineWidth = 5
dirnum = 8
Lambda = 0.2

# The following two functions make conversions between image instances and numpy arrays.
def img_to_np(img):
    return np.array(img).astype(np.float)/255

def np_to_img(I):
    return im.fromarray((255*I).round().astype(np.uint8))
    
def GetStroke(I):
    """
    The input I is a numpy 2d-array within [0,1]. 
    The output S has the same shape and data type with I.
    """
    
def GetTone(I, omega=0):
    """
    Perform histogram matching so that the distribution of the result image matches the 
    empirical distributions learned from artist-drawn images.
    The input I should be a numpy 2d-array within [0,1].
    The output J has the same shape and dtype with I.
    """
    I = (255*I).round().astype(np.uint8)
    counts = np.bincount(I.ravel(), minlength=256)
    source_cdf = np.cumsum(counts).astype(np.float)
    source_cdf /= source_cdf[-1]
    
    p = np.zeros(256)
    for i in range(255):
        p1 = np.exp( - (255-i) / 9.0 ) / 9
        p2 = (i>=105 and i<=225) / (225.0-105.0)
        p3 = np.exp( -(i-90)**2 / (2.0*121) ) / np.sqrt(2*np.pi*11) 
        if omega == 0:
            w = [76, 22, 2]
        elif omega == 1:
            w = [52, 37, 11]
        elif omega == 2:
            w = [42, 29, 29]
        else:
            raise ValueError("omega must take values in [0,1,2]")
        p[i] = np.dot([p1,p2,p3], w)
        
    target_cdf = np.cumsum(p)
    target_cdf /= target_cdf[-1]
    
    values, bins = np.unique(I.ravel(), return_inverse = True)
    interp_values = np.interp(source_cdf, target_cdf, range(256))
    J = interp_values[bins].reshape(I.shape)
    J /= 255.0
    return J
    
