import numpy as np
from PIL import Image
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os, sys
import time

class Imageprocessing():

    def __init__(self, folder, files):
        self.folder = folder
        self.files = files
        path = os.getcwd()
        self.fileDir = os.path.abspath(os.path.join(path, os.pardir))
    def getImgVector(self, face_set, img):
        """Return a raster of integers from a PGM as a list of lists."""
        path =self.fileDir+'/utils/conteudo/'+str(face_set)+'/'+str(img)+'.pgm'
        pgmf = open(path, 'rb')
        header = pgmf.readline()
        assert header[:2] == b'P5'
        (width, height) = [int(i) for i in pgmf.readline().split()]
        depth = int(pgmf.readline())
        assert depth <= 255
        print(str(width) +" "+ str(height)+" "+str(width*height))
        M = np.fromfile(pgmf, dtype = np.uint8)
        pgmf.close()
        vetorimg = read_pgm(2)
        print(vetorimg)
        return M[0:width*height:4]
    def addVectorImg(self, face_set,img):
        #f=open("C:/Users/victo/OneDrive/Documentos/Codigos/Drone Tracker/Image analysis/utils/imagens/faces/face1.txt", "a+")
        with open(self.fileDir+"/utils/imagens/"+self.folder+"/"+self.files+str(face_set)+".txt", "a") as myfile:
            np.savetxt(myfile,img)
        myfile.close()
    def readImagevector(self, face_set, n, length):
        return np.loadtxt(self.fileDir+"/utils/imagens/"+self.folder+"/"+self.files+str(face_set)+".txt",delimiter="\n")[(n-1)*length:length*n]
    def showImage(self, img, length, width):
        im = img.reshape(length, width)
        plt.gray()
        plt.imshow(im)
        plt.show()

    def setWholeSet(self, setN):
        for i in range(1,setN+1):
            img = np.loadtxt(self.fileDir+"/utils/imagens/"+self.folder+"/"+self.files+str(face_set)+".txt",delimiter="\n")
            with open(self.fileDir+"/utils/imagens/faces/face.txt", "a") as myfile:
                np.savetxt(myfile,img)
            myfile.close()
