import numpy as np
import scipy as sc
import math
import btoi
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
def sig(b,wst,yt):
    return 1/float(1+math.exp(2*(b+np.dot(wst,yt))))

def nbr(x,y,mx,my):
    if x==0 and y==0:
        return np.asarray([[0,y+1],[x+1,0]])
    elif x==0 and y==my:
        return np.asarray([[x+1,y],[x,y-1]])
    elif y==0 and x==mx:
        return np.asarray([[x-1,y],[x,y+1]])
    elif x==mx and y==my:
        return np.asarray([[x-1,y],[x,y-1]])
    elif x==0 and y!=0 and y!=my:
        return np.asarray([[x,y-1],[x,y+1],[x+1,y]])
    elif x==mx and y!=0 and y!=my:
        return np.asarray([[x,y-1],[x,y+1],[x-1,y]])
    elif y==0 and x!=0 and x!=mx:
        return np.asarray([[x-1,y],[x+1,y],[x,y+1]])
    elif y==my and x!=0 and x!=mx:
        return np.asarray([[x,y-1],[x-1,y],[x+1,y]])
    else:
        return np.asarray([[x-1,y],[x+1,y],[x,y-1],[x,y+1]])

def change_pixelcolor(nparray):
    tmp=np.zeros((nparray.shape[0],nparray.shape[1]))
    for x in range(nparray.shape[0]):
        for y in range(nparray.shape[1]):
            if nparray[x][y]==1:
                tmp[x][y]=255
            elif nparray[x][y]==(-1):
                tmp[x][y]=0
    return tmp




trials=300
b=0.8
#wst=[0.0,0.1,0.2,0.3,0.4,0.5]
index=0

conversionto255=sc.interpolate.interp1d([-1,1],[0,255])
conversionto1=sc.interpolate.interp1d([0,255],[-1,1])

imagepixels=btoi.readimagetoarray('noisy.png')
print "The size of imagepixels is",imagepixels.shape
print 'The original noisy image is'
for i in range(imagepixels.shape[0]):
    print imagepixels[i]

print

imagepixelsscaled=conversionto255(imagepixels)
print 'The scaled noisy image is'
for i in range(imagepixelsscaled.shape[0]):
    print imagepixelsscaled[i]

print


bs=np.zeros((imagepixels.shape[0],imagepixels.shape[1]))
for i in range(bs.shape[0]):
    for j in range(bs.shape[1]):
        bs[i][j]=np.multiply(imagepixels[i][j],b)




wst=0.6
ys=np.zeros((imagepixels.shape[0],imagepixels.shape[1]))
for i in range(len(ys)):
    for j in range(ys.shape[1]):
        ys[i][j]=(-1.0)

meanys=np.zeros((ys.shape[0],ys.shape[1]))
for t in range(trials):
    for i in range(ys.shape[0]):
        for j in range(ys.shape[1]):
            nys=nbr(i,j,ys.shape[0]-1,ys.shape[1]-1)
            weights=np.zeros((nys.shape[0],))
            yt=np.zeros((nys.shape[0],))
            for k in range(len(weights)):
                weights[k]=wst
                yt[k]=ys[nys[k][0]][nys[k][1]]
            pys=sig(bs[i][j],weights,yt)
            ran=np.random.random()
            if ran>pys:
                ys[i][j]=1.0
            else:
                ys[i][j]=(-1.0)
    meanys+=ys
meanys=meanys/float(trials)


print 'Printing means in [-1,1]'
for i in range(meanys.shape[0]):
    print meanys[i]

print

meanysnew=conversionto255(meanys)


print 'Printing means in [0,255]'
for i in range(meanysnew.shape[0]):
    print meanysnew[i]
btoi.converttoimage(meanysnew,'denoised.png')
diff=0.0
impixnew=conversionto255(btoi.readimagetoarray('original.png'))
for i in range(impixnew.shape[0]):
    for j in range(impixnew.shape[1]):
        diff+=math.fabs(meanysnew[i][j]-impixnew[i][j])
diff/=float(np.multiply(impixnew.shape[0],impixnew.shape[1]))
print 'The Mean Pixelwise Absolute Error is',diff
