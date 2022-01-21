import napari
import skimage

from skimage import io

img = io.imread('C:\Bachelor Oppgave\Datasets\Qanats Iran-Afghanistan\Id-1-Iran-58.58042-34.35781-58.60262-34.33726-zoom=17\ID_1_composite.png')

viewer = napari.Viewer()
new_layer = viewer.add_image(img, rgb=True)
napari.run()

#if __name__ == '__main__':
#    pass