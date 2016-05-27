#coding = utf-8

import numpy as np
import Image as im
import scipy.sparse as sps
from scipy.misc import imrotate
from scipy.signal import convolve2d as conv2

# The Input_Image is the image that to be processed,
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
    
    
