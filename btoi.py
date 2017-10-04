import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
from scipy.misc import imsave
from scipy.misc import imread
from scipy.interpolate import interp1d
def converttoimage(pixelarray,filename):
    imsave(filename,pixelarray)
    print 'Image saved as',filename


def readimagetoarray(filename):
    im=imread(filename)
    res=np.zeros((im.shape[0],im.shape[1]))
    f=sc.interpolate.interp1d([0,255],[-1,1])
    res=f(im)
    return res

