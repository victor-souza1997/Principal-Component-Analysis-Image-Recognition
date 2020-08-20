
from images import Image
import numpy as np
import time
import matplotlib.pyplot as plt
import scipy.linalg as la
#import cupy as cp
#from skcuda import linalg

#esta classe tem como objetivo de processar às imagens
class PCA():
    def __init__(self):
        self.img = Image()
        self.A = 0  #matrix variância
        self.m = 0  #vetor média
    def getMatrix(self, M):
        A = np.zeros((2688,2688))
        M = M.T
        for i in range(0,10):   #função que retorna matrix de covariancia
            A = A + np.outer(M[:,i],M[:,i])#np.outer(M[i,:],M[i,:]) #para a múltiplicação da matrix MxM^T eu utilizei uma função pronta de Python
        return A
    def getEignValues(self, M): #função que retorna o valor dos autovalores da matrix
        V, D = np.linalg.eig(M)
        return np.diagonal(D)

    def meanVector(self, length, N):
        F = np.zeros(length)
        self.A = np.zeros((10, length))
        for n in range(1,N+1):
            D = np.array(self.img.readImage(n, length))
            F = F + D
            self.A[n-1,:] = D
        self.m = F/N

    def getMean(self):
        return self.m

    def setVariance(self):
        self.m = np.outer(np.ones(10),self.m)
        self.A = self.A - self.m
        return self.A

    def getVariance(self):
        return self.A

img = PCA()
img.meanVector(2688, 10)
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
#plt.show()
#vr_gpu, w_gpu = linalg.eig(C, 'N', 'V')
#plt.plot(D)
#plt.show()
t1 = time.time()

total = t1-t0
print(total)
