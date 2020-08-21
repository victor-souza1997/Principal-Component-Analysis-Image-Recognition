
from images import Image
import numpy as np
import time
import matplotlib.pyplot as plt
import scipy.linalg as la
#import cupy as cp
#from skcuda import linalg

#esta classe tem como objetivo de processar às imagens
class PCA():
    def __init__(self, width, height):
        self.img = Image()
        self.width = width
        self.height = height
        self.length = self.height*self.width
        self.A = 0  #matrix variância
        self.m = 0  #vetor média
    def show(self, img):
        self.img.showImage(img, self.height, self.width)
    def getLength(self):
        return self.length
    def getMatrix(self, M):
        A = np.zeros((self.length,self.length))
        M = M.T
        for i in range(0,10):   #função que retorna matrix de covariancia
            A = A + np.outer(M[:,i],M[:,i])#np.outer(M[i,:],M[i,:]) #para a múltiplicação da matrix MxM^T eu utilizei uma função pronta de Python
        return A
    def getEignValues(self, M): #função que retorna o valor dos autovalores da matrix
        V, D = np.linalg.eig(M)
        return np.diagonal(D)
    def meanVector(self, image_set, N):
        F = np.zeros(self.length)
        self.A = np.zeros((10, self.length))
        for n in range(1,N+1):
            D = np.array(self.img.readImage(image_set,n, self.length))
            F = F + D
            self.A[n-1,:] = D
            #self.show(D)
        self.m = F/N
    def getMean(self):
        return self.m
    def setVariance(self):
        self.m = np.outer(np.ones(10),self.m)
        self.A = self.A - self.m
        return self.A
    def getVariance(self):
        return self.A
    def getPCA(self, eig, threshold):
        total = sum(eig)
        for i in range(self.length):
            if(threshold < sum(eig[self.length-i:self.length])/total):
                return i
            elif(i == self.length):
                return 0
    def getWeights(self, eigvector):
        print(eigvector.shape, self.A[1,:].shape)
        return eigvector.T.dot(self.A[1,:])

img = PCA(23,112)
img.meanVector(1,10)
t0 = time.time()
img.setVariance()

M = (img.getVariance())
C = (img.getMatrix(M))
#print(C.shape)
#C = (np.random.rand(10000,10000))
V, D = np.linalg.eigh(C)#linalg.eig(C)
#V, D = la.eig(C)
#print(V.shape, D.shape)
#plt.plot(V)
stop = img.getPCA(V,0.7)#vr_gpu, w_gpu = linalg.eig(C, 'N', 'V')
Base = D[:,img.getLength()-stop:img.getLength()]
print(img.getWeights(Base).shape)
#plt.plot(D)
#plt.show()
t1 = time.time()

total = t1-t0
print(total)
