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
