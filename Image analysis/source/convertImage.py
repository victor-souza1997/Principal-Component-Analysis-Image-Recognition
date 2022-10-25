
from images import Imageprocessing
import math
import time
from scipy import ndimage
import os
import math
import numpy as np
from PIL import Image
class ConvertImage():
    
    def __init__(self):
        self.img = Imageprocessing("bordas","bordas")
        path = os.getcwd()
        self.fileDir = os.path.abspath(os.path.join(path, os.pardir))
    
    def getImage(self, n, folder, file, type_file):           
        """method reads image and makes it into a gray scale array"""
        image_file = Image.open(self.fileDir+"\\utils\\conteudo\\"+str(folder)+'\\' + str(file) + ' ('+str(n)+').'+type_file)
        image = image_file.convert('L') # convert image to black and white
        image_file.close()
        return np.array(image)

    def downScale(self, picture, real_height, real_width, ideal_height, ideal_width):  
        """method downscales image"""
        e_height = math.ceil(real_height/ideal_height)
        e_width = math.ceil(real_width/ideal_width)
        iheight = np.round(np.linspace(0, real_height - 1, ideal_height)).astype(int)
        iwidth = np.round(np.linspace(0, real_width - 1, ideal_width)).astype(int)
        picture = picture[iheight]
        picture = picture[:,iwidth]
        return picture

    def show(self, img, height, width):          
        """method prints vector image"""
        self.img.showImage(img, height, width)

    def addVectorImg(self, img, folder, filename): 
        """method saves vector images into a file"""
        with open(self.fileDir+folder+"/"+filename+".txt", "a") as myfile:
            np.savetxt(myfile,img)
        myfile.close()
    
    def imagemTeste(self):
        img1 = self.getImage("teste", "placas", "placa")
        height, width = img1.shape
        a = self.downScale(img1, height, width, 900, 1500)
        print(a.shape)
        self.show(a,  900, 1500)
        self.addVectorImg(a.reshape(900*1500,1), "placas", "placateste") #resolução das imagens 252 x 448

    def setImageVectorCaracteres(self): 
        """Methods makes image of caracters into vector images"""
        caracteres = ['V']#['5', '6', '8', 'K', 'N', 'V']
        for c in caracteres:
            for i in range(1,14):
                conv = ConvertImage()
            #    conv.imagemTeste()
                a = self.getImage(i,"caracteres/"+c, c, "png")
                height, width = a.shape
                #a = np.where(a>80, 255, 0)
                a = self.downScale(a, height, width, 20, 20)
                #print(a.shape)
                conv.show(a, 20 , 20)
                #conv.addVectorImg(a.reshape(20*20, 1), "caracteres", "teste"+c+"0") #resolução das imagens 252 x 448"""

    def setVectorPlates(self):  
        """method converts plate's image into vector images"""
        for i in range(1, 50):
            a = self.getImage(i, "placas", "placas", "JPG")
            height, width = a.shape
            #a = np.where(a>90, 255, 0)
            a = self.downScale(a, height, width,  100,300)
            self.show(a,  100, 300)
            #self.addVectorImg(a.reshape(100*300, 1), "placas", "placas0") #"""#resolução das imagens 252 x 448


#conv = ConvertImage()
#conv.setVectorPlates()
#conv.setImageVectorCaracteres()
