#coding = utf-8

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
from scipy.misc import imrotate
from scipy.signal import convolve2d as conv2


# The Input_Image is the image that to be processed.
# The Pencil_Texture is a suitably chosen texture image that determines the style of the output.
Input_Image = "house.jpg"
Pencil_Texture = "texture.jpg"

# Global parameters:
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
    dx = np.zeros_like(I)
    dy = np.zeros_like(I)
    dx[:,1:] = I[:,1:] - I[:,:-1]
    dy[1:] = I[1:] - I[:-1]
    G = np.sqrt(dx**2 + dy**2)
    
    L = np.zeros((dirnum, Line_Len, Line_Len))
    
    for i in range(dirnum):
        L[i] = 
        
    response = np.zeros((dirnum,)+I.shape)
        for i in range(dirnum):
            response[i] = conv2(G, L[i], mode="same")
            
    index = np.argmax(response, axis=0)
    
    # C[i] is the set of pixels in G with their responses attained maximals at the i-th direction.
    # S[i] is the set if lines toward the i-th direction. It's just the convolution of C[i] and L[i].
    C = np.zeros_like(response)
    Sp = np.zeros_like(response)
    for i in range(dirnum):
        ind = np.where(index==i)
        C[i][ind] = G[ind]
        Sp[i] = conv2(C[i], L[i], mode="same")
    S = np.sum(Sp, axis=0)    
    S = S / np.max(S)  # map back to [0,1]
    S = 1-S   # invert pixels. Since the lines in G are white.
    return S
    
def GetTone(I):
    """
    Perform histogram matching so that the distribution of the result image matches the 
    empirical distributions learned from artist-drawn images.
    The input I should be a numpy 2d-array within [0,255] and dtype 'np.unit8'.
    The output J has the same shape with I but with values within [0,1].
    """
    
    return J
    
def StitchTexture(texture, I):
    
    
    return P

  
def Combine(S, J, P):
    """
    S is the stroke image
    J is the tone image
    P is the pencil texture
    S,J,P are numpy 2d-arrays with the same shape and have values within [0,1]
    """
    r, c = S.shape
    epsilon = 1e-8
    size = r*c
    
    # add epsilon to avoid invalid log inputs 
    logJ = np.log(J.ravel() + epsilon)
    logP = sps.spdiags( np.log(P.ravel()+epsilon), 0, size, size)
    
    e = np.ones(size)
    Dx = sps.spdiags([-e,e], [0,c], size, size)
    Dy = sps.spdiags([-e,e], [0,1], size, size)
    
    A = Lambda * (Dx * Dx.T + Dy * Dy.T) + logP * logP
    b = logP * logJ
    beta1d, _ = sps.linalg.cg(A, b, tol=1e-6, maxiter=80)
    beta = beta1d.reshape(S.shape)
    
    T = np.power(P, beta)
    T = (T-np.min(T)) / (np.max(T)-np.min(T))
    return S*T
    
    
def PencilDraw(filename, texture):
    img = im.open(filename)
    if img.size[2] > 1:
        Y, Cb, Cr = img.convert("YCbCr").split()
        mode = "color"
    else:
        Y = img.convert("L")
        mode = "gray"
        
    I = img_to_np(Y)
    
    texture = im.open(texture).convert("L")
    texture = img_to_np(texture)

    S = GetStroke(I)
    J = GetTone(I)
    P = StitchTexture(texture, I)
    
    result = Combine(S, J, P)
    result = np_to_img(result)
    result.save("result_gray.jpg")
    
    if mode == "color":
        result = im.merge("YCbCr", (result, Cb, Cr))
        result.save("result_color.jpg")
        
        
PencilDraw(Input_Image, Pencil_Texture)
