
from images import Imageprocessing
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
from PIL import Image
from convertImage import ConvertImage
import matplotlib
import time
import os
#import cupy as cp
#from skcuda import linalg

#esta classe tem como objetivo de processar às imagens

class AppPCA(): #o objetivo dessa classe é importar todos os métodos da classe PCA para
    def __init__(self, width, height, set, Nset, folder, file):
        self.width = width
        self.height = height
        self.Nset = Nset
        self.pca = PCA(width, height, set, Nset, folder, file)
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        self.fileDir = os.path.join(fileDir, '..')
        print(self.fileDir)

    def runPCA(self):
        self.pca.setPCA()
        self.meanPicture = self.pca.getmeanImage()
        Base = self.pca.getsubspaceBase()
        j = 0
        print(Base.shape)
        print(self.pca.getPC())

        w = np.zeros((self.pca.getPC(),self.Nset))#self.Nset))
        for i in range(0,self.Nset):#
            w[:,i] = self.pca.getWeights(i)
        self.w = w
        A = self.pca.getVariance()
        print(A.shape)
        conv = ConvertImage()
        imagem_teste = conv.getImage(999, "placas", "placas", "PJG")
        """
        h, w = imagem_teste.shape
        imag = conv.downScale(imagem_teste, h, w, 100, 300)
        w_teste = Base.T.dot(imag.reshape(100*300,1))
        imagem_reconstruida = Base.dot(w_teste)
        fig = plt.figure()
        ax1 = fig.add_subplot(2,1,1)
        ax1.imshow(imagem_reconstruida+self.meanPicture)
        ax2 = fig.add_subplot(2,1,2)
        ax2.imshow(imag)
        plt.show()"""



    def setPlates(self):
        w = np.zeros((self.pca.getPC(),self.Nset))#self.Nset))
        for i in range(0,self.Nset):#
            w[:,i] = self.pca.getWeights(i)
        self.w = w
        #self.savePCA("pesos", self.w.reshape(self.pca.getPC()*self.Nset,1))
        #self.savePCA("media", self.pca.getmeanImage())
        #self.savePCA("matrixBase", self.pca.getsubspaceBase().reshape(self.pca.getPC()*len(self.pca.getmeanImage()),1))

    def setCaracteres(self):
        caracteres = ['V']#['5', '6', '8', 'K', 'N', 'V']
        for c in caracteres:
            w = np.zeros((self.pca.getPC(),13))##self.Nset))#self.Nset))
            for i in range(0,13):#self.Nset):#
                w[:,i] = self.pca.getWeights(i+j*6)
            self.w = w
            j+=1
            self.w = self.w.reshape(13*self.pca.getPC(),1)
            #self.savePCA("pesos_teste"+c, self.w)
            #self.savePCA("media_teste"+c, self.pca.getmeanImage())
            #self.savePCA("matrixBase_teste"+c, self.pca.getsubspaceBase().reshape(self.pca.getPC()*len(self.pca.getmeanImage()),1))

    def paintBorder(self, picture): #este método constroi uma borda na região em que seja determinada
        height, width = picture.shape
        picture[0,:] = 250*np.ones(width)
        picture[height-1,:] = 250*np.ones(width)
        picture[:,0] = 250*np.ones(height)
        picture[:,width-1] = 250 * np.ones(height)
        return picture
    def correctScale(self, picture, ideal_height, ideal_width):  #este método corrige a escala da janela que está sendo analisada. Por exemplo: quando uma janela que está sendo analisada é muito grande
        real_height, real_width = picture.shape                  #é necessário que ela seja subamostrada para que possamos analisar suas componentes principais
        iheight = np.round(np.linspace(0, real_height - 1, ideal_height)).astype(int)
        iwidth = np.round(np.linspace(0, real_width - 1, ideal_width)).astype(int)
        picture = picture[iheight]
        picture = picture[:,iwidth]
        return picture
    def readPlate(self,info, caractere, x_position, scale, error):
        return np.hstack((info,np.array([[caractere, int(x_position), scale, error]]).T))
    def squareMean(self, w, w_in): #função para calcular o erro entre a imagem reconstruida e as imagens do banco treinamento
        x = np.sqrt(np.sum(np.asarray(w - w_in.T)**2, axis=1))
        x.sort()
        return x[0]
    def savePCA(self, namefile, content):   #este método salva arquivos
        with open(self.fileDir+"/utils/dados/"+namefile+".txt", "a") as myfile:
            np.savetxt(myfile,content)
        myfile.close()
    def readPCA(self, namefile): #este método ler o arquivos
        return np.loadtxt(self.fileDir+"/utils/dados/"+namefile+".txt")
    def sumMatrix(self, M, position_y, position_x, height, width, error): #este método cria o mapa de errors
        M[position_y:position_y+height,position_x:position_x+width] =  error*np.ones((height, width))+M[position_y:position_y+height,position_x:position_x+width]
        return M

    def janelamento(self, picture, width, height, picture_width, picture_height, w_n, jump, n_imagens, threshold, caractere): #função que realiza a classifição quadrado por quadrado
        file_media = "media"
        file_peso = "pesos"
        file_matrixBase = "matrixBase"

        if caractere is not None:
            file_media = file_media+"_teste"+caractere
            file_peso = file_peso+"_teste"+caractere
            file_matrixBase = file_matrixBase+"_teste"+caractere
        mean_picture = np.array(self.readPCA(file_media))
        wk = self.readPCA(file_peso).reshape(w_n, n_imagens)
        Base = self.readPCA(file_matrixBase).reshape((width*height),w_n)
        x = []
        position_x = []
        position_y = []
        scalar = []
        i = 0
        j = 0
        n = 1
        t0 = time.time()
        while(n<4):
            if(width*n+j > picture_width):
                j = 0
                i += jump
            if( i + height*n > picture_height):
                i = 0
                n += 1
            picture_seg = picture[i:height*n+i, j:width*n+j]
            picture_seg = self.correctScale(picture_seg, height, width)  #caso a seção selecionada seja maior do que a escala desejanda, ela sofrará um downScale
            picture_vector = picture_seg.reshape(width*height,1)  #transformando o janelamento em um vetor para encontrar os pesos
            Thau = picture_vector[:,0] - mean_picture  #achando a variância do vetor imagem do janelamento com a média da classe de objeto
            wi = Base.T.dot(Thau)           #encontrar o peso da projeção da imagem
            y = self.squareMean(wi, wk) #calcular o erro quadrático dos pesos

            position_y.append(i)   #salvar a posição deste erro calculado, que poderá ser usado mais tarde.
            position_x.append(j)
            scalar.append(n)       #junto com a posição, também será salva o aumento da janela
            x.append(y)            #salvando o erro da janela
            j += jump

        info =  np.array([[],[],[],[]])
        sorted_lookup = sorted(enumerate(x), key=lambda i:i[1]) #este método nos permite salvar os erros em ordem crescente, e além disso, retornar a posição de cada erro
        matrix_error = np.zeros((picture_height,picture_width))
        t1 = time.time()
        print("tempo de loop: ", t1-t0)
        for i in range(4): #encontrar os n menores erros
            position, value = sorted_lookup[i] #como mencionado anteriormente, podemos pegar a posição do menor erro
            if(value < threshold & threshold != 0 ): #retornar valores que passam do threshold
                info = self.readPlate(info, ord(caractere), position_x[position], width*scalar[position],  value)
            matrix_error = self.sumMatrix(matrix_error, (position_y[position]), (position_x[position]), (height*scalar[position]), (width*scalar[position]), value)
        position, value = sorted_lookup[0]
        img_cut = picture[position_y[position]:height*scalar[position]+position_y[position], position_x[position]:width*scalar[position]+position_x[position]]
        img_cut_height, img_cut_width = img_cut.shape
        Max = np.max(matrix_error)
        matrix_error = np.divide(matrix_error*255, Max)
        matrix_error = matrix_error.reshape(picture_height, picture_width)
        picture = picture.reshape(picture_height, picture_width)
        return img_cut, matrix_error, info#img_cut, matrix_error#picture[position_y:height*scala+position_y, position_x:width*scala+position_x]



class PCA():
    def __init__(self, width, height, set, N, folder, file):
        self.img = Imageprocessing(folder, file)
        self.width = width
        self.height = height   #altura da imagem quando colocada em uma matrix
        self.length = self.height*self.width #comprimento de cada vetor imagem
        self.A = 0  #matrix variância
        self.m = 0  #vetor média
        self.N = N  #número de imagens dentro do vetor
        self.eigenvalues = 0
        self.eigenvector = [] #vetor de eignvector;
        self.set = set #set de imagens que iremos pegar. Por padrão o set selecionado é o 0, pois representa um vetor com todas as imagens

    def setPCA(self):
        F = np.zeros(self.length) #declarado vetor média
        self.I = np.zeros(( self.length, self.N)) #Criando matrix imagem
        for n in range(1, self.N+1):
            D = np.array(self.img.readImagevector(self.set, n, self.length))
            F = F + D     #somando todos os vetores imagens para o cálculo da média
            self.I[:,n-1] = D       #preenchendo matrix imagem. Cada coluna dela será uma imagem
        self.m = F/self.N      #cálculo da média
        self.A = self.I - np.outer(self.m,np.ones(self.N)) #Criando matrix variância. Resultado da subtração da matrix imagem com o vetor médio
        threshold = 0.95            #definindo o threshold para encontrar as componentes principais
        C = np.cov(self.A.T)        #calculo da matrix covariância MxM ao invés de NxN
        self.eigenvalues, self.eigenvector = np.linalg.eigh(C) #encontrar os autovalores e autovetores da matrix covariância
        self.stop = 0
        i = 0
        while(threshold > sum(self.eigenvalues[self.N-i:self.N])/sum(self.eigenvalues)): #calculo para encontrar o número de componentes principais
            self.stop = i
            i+=1
        self.Base = self.A.dot(self.eigenvector[:,self.N-self.stop:self.N])              #trazer a Base para dimensão correta Nxk. Sendo k o número de autovetores PCs

    def getPC(self):
        return self.stop
    def getmatrixImage(self):
        return self.A + np.outer(self.m,np.ones(self.N))
    def getmeanImage(self):
        return self.m
    def getsubspaceBase(self):
        return self.Base
    def getVariance(self):
        return self.A
    def getWeights(self, n):
        return  self.Base.T.dot(self.A[:,n])#np.outer(self.Base.T,self.A[1,:].T)
    def getImage(self, w):
        #print(self.Base.dot(w).shape, self.m.shape)
        return  self.Base.dot(w)+self.m
