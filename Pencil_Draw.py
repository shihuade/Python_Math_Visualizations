#coding = utf-8

import numpy as np
import Image as im
import scipy.sparse as sps
from scipy.misc import imrotate
from scipy.signal import convolve2d as conv2

Input_Image = "house.jpg"
Pencil_Texture = "pencil01.jpg"

def img_to_np(img):
    return np.array(img).astype(np.float)/255

def np_to_img(I):
    return im.fromarray((255*I).round().astype(np.uint8))
