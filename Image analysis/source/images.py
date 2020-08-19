import numpy as np
from PIL import Image
from PIL import Image
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os, sys

class Image():
    def getImgVector(self, img):
        ##"""Return a raster of integers from a PGM as a list of lists."""
        path ='C:/Users/victo/OneDrive/Documentos/Codigos/Drone Tracker/Image analysis/utils/conteudo/s1/'+str(img)+'.pgm'
        pgmf = open(path, 'rb')
        header = pgmf.readline()
        assert header[:2] == b'P5'
        (width, height) = [int(i) for i in pgmf.readline().split()]
        depth = int(pgmf.readline())
        assert depth <= 255
        print(str(width) +" "+ str(height)+" "+str(width*height))
        M = np.fromfile(pgmf, dtype = np.uint8)
        pgmf.close()
        return M
        vetorimg = read_pgm(2)
        print(vetorimg)
    def addVectorImg(self, img):
        #f=open("C:/Users/victo/OneDrive/Documentos/Codigos/Drone Tracker/Image analysis/utils/imagens/faces/face1.txt", "a+")
        with open("C:/Users/victo/OneDrive/Documentos/Codigos/Drone Tracker/Image analysis/utils/imagens/faces/face1.txt", "a+") as myfile:
            np.savetxt(myfile,img)
        myfile.close()
    def readImage(self, n, length):
        #with open("C:/Users/victo/OneDrive/Documentos/Codigos/Drone Tracker/Image analysis/utils/imagens/faces/face1.txt", "r") as myfile:
        return np.loadtxt("C:/Users/victo/OneDrive/Documentos/Codigos/Drone Tracker/Image analysis/utils/imagens/faces/face1.txt",delimiter="\n")[(n-1)*length:length*n]
    def showImage(self, img, length, width):
        im = img.reshape(width, length)
        plt.gray()
        plt.imshow(im)
        plt.show()

#width = 112 and length = 92 in all the imagens
n = 10
length = 92
width = 112
img = Image()
#for i in range(1,11):
#    img.addVectorImg(img.getImgVector(i))
#x = img.readImage(n, width*length)
#img.showImage(x, length,width)

#def reScaleImage(self, M, resize):
