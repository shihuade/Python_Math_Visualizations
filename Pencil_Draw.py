#coding = utf-8

# A Python implementation of the algorithm depicted in CeWu Lu, Li Xu, JiaYa Jia's paper 
# "Combining Sketch and Tone for Pencil Drawing Production".

# There are three main steps:
# 1. Generate the stroke map S of the image.
# 2. Generate the tone map T of the image.
# 3. Combine S and T to get the final output.
# For detailed explanations of these steps see the comments below.

import numpy as np
import Image as im
import scipy.sparse as sps
from scipy.misc import imrotate
from scipy.signal import convolve2d as conv2

# The Input_Image is the image that to be processed.
# The Pencil_Texture is a suitably chosen texture image that determines the style of the output.
Input_Image = "house.jpg"
Pencil_Texture = "texture.jpg"

# Now the global parameters:
Line_Len = 19  # must be an odd
kr = Line_Len // 2  # kernel radius
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
    The output S is also a numpy 2d-array within [0,1] and has the same shape with I.
    """
    # Compute the gradient image by the forward difference.
    G = np.sqrt(dx**2 + dy**2)
    
