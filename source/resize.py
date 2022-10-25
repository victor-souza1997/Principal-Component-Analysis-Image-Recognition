from images import Image
import numpy as np
from images import Imageprocessing

class ImageResize():
    def __init__(self, image, width, height, imagewidth, imageheight):
        self.image  = image
        self.width = width
        self.height = height
        self.imagewidth = imagewidth
        self.imageheight = imageheight
    #def vectorizeMatrix(M):    #este método servirá para transformar uma matrix NxN em um vetor (NxN)x1
    #def subSample():           #essa função irá transformar uma imagem de tamanho NxN para um tamnho nxn, para que assim se possa comparar
    #def reSize(self):
        #for i in range(0,(self.imagewidth-self.height),1):
        #    for j in range(0,(self.imageheight-self.width),1):
            #    newimage = self.image[0+i:self.height+i, 0+j:self.width+j]
            #    return newimage.reshape(self.width*self.height,1)

                #print(i,j, newimage.shape)
    def getSmallsection(self):
         newimage = self.image[0+i:self.height+i, 0+j:self.width+j]
         return newimage.reshape(self.width*self.height,1)






#img = Imageprocessing("placas", "placas")
#imag = img.readImagevector(1, 1, 1512*1344).reshape(1512, 1344)
#reImag = ImageResize(imag, 300, 400, 1344, 1512)
#reImag.reSize()
#print("end")
