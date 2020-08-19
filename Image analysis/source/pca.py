
from images import Image
import numpy as np

#esta classe tem como objetivo de processar às imagens
class PCA():
    def __init__(self):
        self.img = Image()

    def getMatrix(self, M):   #função que retorna matrix de covariancia
        return np.outer(M,M)

    def getEignValues(self, M): #função que retorna o valor dos autovalores da matrix
        V, D = np.linalg.eig(M)
        return np.diagonal(D)

    def meanVector(self, length, N):
        F = np.array([0]*length)
        for n in range(1,N+1):
            F = F+np.array(self.img.readImage(n, length))
        return F/N


img = PCA()
#M = img.getMatrix(np.array([1,2,3]))
M = (img.meanVector(112*92, 10))
print(img.getMatrix(M))
