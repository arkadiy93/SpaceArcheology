import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
from PIL import Image
import tkinter as tk
from tkinter import messagebox
import csv


class Binary_Image_Classification:
    def __init__(self, composite_file, grid_size,img_tile_folder=None):
        self.file = composite_file
        self.grid_size = grid_size
        self.img_tile_folder = img_tile_folder
        self.tile_dict = {}
        self.image = Image.open(self.file)
        self.im_width = self.image.size[0]
        self.im_height = self.image.size[1]
        self.im_comp = None
        self.im_tile = None
        self.ax1 = None
        self.ax2 = None
        self.classification_dict = {}
        self.classification_loaded = False

    #classify image methods starts the classification. All other class methods does not need to be called outside the class.
    def classify_image(self):
        classification_file = self.find_classification_file()
        self.create_tile_and_classification_dict()
        if classification_file != None:
            self.load_classification(classification_file)
        self.fig, self.ax1, self.ax2 = self.make_plot()
        plt.ion()
        self.fig.canvas.draw_idle()
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('close_event', self.update_data)
        if self.classification_loaded:
            self.update_plot()
        plt.show(block=True)


    def make_plot(self):
        assert os.path.isfile(self.file), "The image file to classify does not exist."
        x, y = self.im_width//self.grid_size, self.im_height//self.grid_size
        fig, (self.ax1,self.ax2) = plt.subplots(nrows=1,ncols=2,figsize=(17, 9), dpi=100)
        fig.suptitle('Binary Classification - Green: Contains Feature, Red: Will be Excluded from Data Set, Blank: Does not Contain Feature', fontsize=12)
        self.ax1.title.set_text('Composite Image')
        self.ax2.title.set_text('Tile: X=0 Y=0')
        self.ax1.set_ylabel('# of pixels')
        self.ax1.set_xlabel('# of pixels')
        self.ax2.set_ylabel('# of pixels')
        self.ax2.set_xlabel('# of pixels')
        self.im_comp = self.ax1.imshow(self.image, interpolation='none', filternorm=False, resample=False, cmap='gray')
        self.im_tile = self.ax2.imshow(self.tile_dict.get((0,0)),interpolation='none', filternorm=False, resample=False, cmap='gray')
        for i in range(x):
            for j in range(y):
                rect = self.draw_rect(i, j, 'yellow', 'none')
                self.ax1.add_patch(rect)
        self.im_comp.set_data(self.image)
        self.im_tile.set_data(self.tile_dict.get((0,0)))
        return fig, self.ax1, self.ax2

    def update_plot(self):
        for key in self.classification_dict:
            tile_x,tile_y = key
            rect_index = (tile_x * (self.im_height//self.grid_size)) + tile_y
            if rect_index <= len(self.ax1.patches):
                if self.classification_dict[key] == 1:
                    self.ax1.patches[rect_index].set_facecolor((0, 1, 0, 0.2))
                if self.classification_dict[key] == 'exclude':
                    self.ax1.patches[rect_index].set_facecolor((1, 0, 0, 0.2))

    #Finds if there is a classification file for the dataset. Need to change code to add more file types than csv.
    def find_classification_file(self):
        if self.img_tile_folder is None:
            self.img_tile_folder = os.path.dirname((os.path.abspath(self.file)))
        temp_id = self.file.split('_')
        id = temp_id[-2]
        classification_file = os.path.join(self.img_tile_folder,'ID=' + str(id) + '_Classification.csv')
        return classification_file


    def load_classification(self,file):
        root = tk.Tk()
        root.withdraw()
        ans = tk.messagebox.askquestion('Load Classification File', 'Would you like to load classification data from existing file?')
        if ans == 'yes':
            root.destroy()
            with open(file, 'r', encoding='UTF8') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    temp = row[0].split('_')
                    x = int(temp[-2][2:])
                    temp_y = temp[-1].split('.')
                    y = int(temp_y[0][2:])
                    if row[1] == 'exclude':
                        self.classification_dict[(x, y)] = row[1]
                    else:
                        self.classification_dict[(x,y)] = int(row[1])
                    self.classification_loaded = True
            f.close()



    def create_tile_and_classification_dict(self):
        #Loads all individual image tiles into dictionary which is used to display these tiles individually, when selected for classification.
        if self.img_tile_folder is None:
            self.img_tile_folder = os.path.dirname((os.path.abspath(self.file)))
        for file in os.listdir(self.img_tile_folder):
            if file.endswith('.png') and file.endswith('composite.png') == False:
                filename = file.split('_')
                x = int(filename[-2][2:])
                temp_y = filename[-1].split('.')
                y = int(temp_y[0][2:])
                temp_image = Image.open(os.path.join(self.img_tile_folder,file))
                self.tile_dict[(x,y)] = temp_image
                self.classification_dict[(x,y)] = 0

    def update_data(self, conformation=True):
        root = tk.Tk()
        root.withdraw()
        ans = tk.messagebox.askquestion('Classification', 'Do you want to update classification file?')
        if ans == 'yes':
            root.destroy()
            self.create_classification_file()

    #Can add more classification file types to create.
    def create_classification_file(self):
        self.create_classification_csv()

    def create_classification_csv(self):
        header = ('filename', 'classification')
        temp_id = self.file.split('_')
        id = temp_id[-2]
        with open(os.path.join(self.img_tile_folder, 'ID=' + id + '_Classification.csv'), 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for key in self.tile_dict:
                x, y = key
                if x < 10:
                    x = '0' + str(x)
                else:
                    x = str(x)
                if y < 10:
                    y = '0' + str(y)
                else:
                    y = str(y)
                classification = str(self.classification_dict[key])
                string = (str('ID=' + id + '_x=' + x + '_y=' + y + '.png'),classification)
                writer.writerow(string)
        f.close()

    def onclick(self, event):
        if self.fig.canvas.manager.toolbar.mode != '':
            return
        rect_index, tile_x, tile_y = self.translate_pixel(event.xdata, event.ydata)
        if self.ax1.patches[rect_index].get_facecolor() == (0, 0, 0, 0):
            self.ax1.patches[rect_index].set_facecolor((0, 1, 0, 0.2))
            self.im_tile.set_data(self.tile_dict.get((tile_x,tile_y)))
            self.ax2.title.set_text('Tile: X=' + str(tile_x) + ' Y=' + str(tile_y))
            self.classification_dict[(tile_x,tile_y)] = 1
            rect = self.draw_rect(tile_x, tile_y, 'blue', 'none')
            self.ax1.add_patch(rect)
        elif self.ax1.patches[rect_index].get_facecolor() == (0, 1, 0, 0.2):
            self.im_tile.set_data(self.tile_dict.get((tile_x,tile_y)))
            self.ax1.patches[rect_index].set_facecolor((1, 0, 0, 0.2))
            self.ax2.title.set_text('Tile: X=' + str(tile_x) + ' Y=' + str(tile_y))
            self.classification_dict[(tile_x, tile_y)] = 'exclude'
            rect = self.draw_rect(tile_x, tile_y, 'blue', 'none')
            self.ax1.add_patch(rect)
        else:
            self.im_tile.set_data(self.tile_dict.get((tile_x,tile_y)))
            self.ax1.patches[rect_index].set_facecolor((0, 0, 0, 0))
            self.ax2.title.set_text('Tile: X=' + str(tile_x) + ' Y=' + str(tile_y))
            self.classification_dict[(tile_x, tile_y)] = 0
            rect = self.draw_rect(tile_x, tile_y, 'blue', 'none')
            self.ax1.add_patch(rect)



    def draw_rect(self, x, y, edgecolor, facecolor):
        x = self.grid_size * x
        y = self.grid_size * y
        rect = patches.Rectangle((x, y), self.grid_size, self.grid_size, linewidth=0.5, edgecolor=edgecolor, facecolor=facecolor)
        return rect


    def translate_pixel(self, x_float, y_float):
        # # Find segment id
        rect_index = int((x_float//self.grid_size) * (self.im_height//self.grid_size) + (y_float//self.grid_size))
        tile_x = int(rect_index//(self.im_height//self.grid_size))
        tile_y = int(rect_index - (tile_x*(self.im_height//self.grid_size)))
        return rect_index, tile_x, tile_y



if __name__ == '__main__':
    temp = Binary_Image_Classification('C:\Bachelor Oppgave\Datasets\Qanats Iran-Afghanistan\Id-1-Iran-58.58042-34.35781-58.60262-34.33726-zoom=17\ID_1_composite.png',256,'C:\Bachelor Oppgave\Datasets\Qanats Iran-Afghanistan\Id-1-Iran-58.58042-34.35781-58.60262-34.33726-zoom=17\Resized_to_256')
    temp.classify_image()