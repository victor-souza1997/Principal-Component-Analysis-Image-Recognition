from pca import AppPCA
import time
from images import Imageprocessing
import numpy as np
import matplotlib.pyplot as plt
from convertImage import ConvertImage
from scipy import ndimage



def eliminate_overlappped(M): #nessa função elimamos a janelas que sobrepõe a outras. Tentando deixar apenas a janela que represente o caractere da melhor forma
    height, width = M.shape

    for i in range(0, width-1):
        for j in range(1, width-i):

            if(M[1,i] == 'None' or M[1,i+j] == 'None'):
                continue
            if(M[0,i] == M[0,i+j] ):
                a = 0.3
            else:
                a = .6
            if((M[1,i]+M[2,i]>M[1,i+j]) & ((M[2,i+j]*a<M[2,i]+(M[1,i])-(M[1,i+j])))):
                if(M[3,i]<M[3,i+j]):
                    M[:,i+j] = None
                else:
                    M[:,i] = None
    return M
def pre_processamento_PCA():     #esta função chama o método que calcula as PCAs
    img_faces.runPCA()
def getRegion(picture, o, parameter):   #este método recorta a uma área que contenha suspeitas de encontrar o objeto desejado.
    y, x = np.where(o >= parameter)
    return picture[y,x].reshape(len(np.unique(y)),len(np.unique(x)))
def zero_surrounded(a, localizacao):
    return a[np.min(np.nonzero(localizacao)[0]):np.max(np.nonzero(localizacao)[0])+1,np.min(np.nonzero(localizacao)[1]):np.max(np.nonzero(localizacao)[1])+1]

def find_plate(arquivo, complemento):       #nesta função iremos procurar a localização da placa, recortar a imagem e depois indentificar cada um dos caracteres
    img = Imageprocessing("placas", arquivo) #"placas" e "placas" são respectivamente pasta e arquivo. Se você quiser alterar o arquivo, basta colocar a imagem nesta pasta e substituir o nome nessa função
    imag = img.readImagevector(complemento, 1,  900*1500).reshape( 900, 1500)   #aqui o método está chamando o arquivo imagem, chamado de teste, para ser utilizado.
    plt.imshow(imag)
    plt.title("Imagem a ser testada")
    plt.gray()
    plt.show()
    placa, o, smallest_error = img_faces.janelamento(imag, 300, 100,  1500, 900, 34,10, 49, 0, None)    #este método do janelamento irá escanear a imagem teste para tentar localizar a posição da placa na imagem
    plt.imshow(imag+o)
    imag = zero_surrounded(imag,o)
    plt.title('Posição da Placa')
    plt.gray()
    plt.show()
    placa, o, smallest_error = img_faces.janelamento(imag, 300, 100, imag.shape[1],imag.shape[0] , 34,10, 49, 0, None)#novamente, repetindo o processo. Isso não é necessário, mas é apenas para garantir que a imagem fique centralizada
    max = np.unique(o)[-1] #aqui estou pegando apenas os maiores valores do mapa de erro
    imag = zero_surrounded(imag,o) #aqui irei recortar a posição na imagem, utilizando o mapa de erro como parametro, para localizar a posição da placa

    plt.imshow(imag+o) #aqui estou imprimindo a imagem recortada da placa, junto com a imagem de erro
    plt.title('Imagem da placa localizada')
    plt.gray()
    plt.show()
    #As listas c, threshold, PCs e amostras serão utilizadas para no mesmo método de escaneamento. Porém como dessa vez precisamos localizar mais de uma coisa, precisaremos também de mais informações
    c = ['K', 'N', 'V', '8', '5', '0']
    threshold = [68256583459.865265,  879451037858.7833, 1534171.745237128, 4962382,31325435.7039992, 4417664.6045767395]
    PCs = [3, 4, 9, 33, 14, 23]
    amostras = [6, 6, 13, 55, 21, 42]
    error_map = np.zeros((imag.shape[0],imag.shape[1]))
    analise = np.array([[],[],[],[]])
    for i in range(0    ,6):
        #imag = np.where(imag>30, 255, 0)
        numeros, erro, x = img_faces.janelamento(imag, 20, 20,  imag.shape[1],imag.shape[0], int(PCs[i]),1,amostras[i], int(threshold[i]),c[i])
        error_map = error_map+erro
        analise = np.hstack((analise, x))

    analise = analise[:,np.argsort(analise[1,:])]
    x = (eliminate_overlappped(analise))
    x = x[:,~np.isnan(x).any(axis=0),]
    print("A placa da imagem possui os seguintes caracteres:", ' '.join(str(chr(int(i))) for i in x[0,:]))

    plt.imshow(error_map+imag)
    plt.gray()
    plt.title('Caracteres localizados')
    plt.show()
if __name__ == "__main__":
    t0 = time.time()
    width = 300     #estas informações servem para encontrar a pasta que contenha o arquivo de texto de uma classe de imagens. Essas que podem ser: placas, caracteres. Com esses arquivos selecionados,
    height = 100    #podemos calcular às bases, médias e pesos de uma determinada classe. Essas informações calculadas também serão salvas em arquivos de texto.
    set = "0"       #o set representa o tipo de arquivo que será usado para o cálculo. Deixe 0 se quiser selecionar o arquivo que contenha todas as imagens vetorizas
    Nset = 49       #é de extram importância que o número de imagens do arquivo vetor esteja correto, pois o código não irá rodar
    folder = "placas"   #arquivo em que o programa irá buscar o arquivo. Para facilitar o processo, o arquivo e a pasta cotém o mesmo nome.
    file = "placas"     #para selcionar o arquivo que contenha placas, digita placas. Para selecionar arquivos que contenham caracteres, escreva caracteres

    img_faces = AppPCA(width, height, set, Nset, folder, file) #nesta classe está contida todos os métodos necessários para o cálculo de PCA

    #pre_processamento_PCA()   #esta parte representa o pré-processamento de uma imagem. Aqui serão calculadas às bases, médias e pesos da PCA, e serão salvos num arquivo

    print("Iniciando o processo de reconhecimento de caracteres.\nIsso pode levar um tempo...\nPara avançar, feche as imagens que forem aparecendo. No fim aparecerá por escrito os caracteres da placa")
    find_plate("placa", "teste")       #para alterar o arquivo imagem q está sendo analisado, basta ir na pasta placas e colocar o nome e o complemento da placa desejada por aqui
    t1 = time.time()
    print("time of code: ", t1-t0)

    k=input("Fim do processo.\nAperte alguma tecla para sair")
