import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.ticker as plticker
from PIL import Image

class Image_Classification:
    def __init__(self, file, grid_size):
        self.file = file
        self.grid_size = grid_size


    def classify_image(self):
        img = mpimg.imread(self.file)
        plt.imshow(img)
        plt.show()

        #plt.imshow(self.img)
        #plt.show()
















if __name__ == '__main__':
    temp = Image_Classification('C:\Bachelor Oppgave\Datasets\Qanats Iran-Afghanistan\Id-1-Iran-58.58042-34.35781-58.60262-34.33726-zoom=17\ID_1_composite.png',256)
    temp.classify_image()