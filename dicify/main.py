import cv2 
import numpy as np

from utils import pairwise
from dice.dice_arrays import dice_units

class Dicifier:
    
    _DICE_UNITS = dice_units
    
    def __init__(self, img_path: str, output_height: int, output_width: int, invert: bool = False):
        self.img_path = img_path
        self.output_height = output_height
        self.output_width = output_width
        self.invert = invert

    @property
    def img(self):
        img = cv2.imread(img_path, 0)
        h, w = img.shape
        self.input_height = h
        self.input_width = w
        return img
    
    @property
    def unit_size(self):
        return self._DICE_UNITS[0].shape[0]
    
    def dicify(self):
        # * load image
        # * rescale to output dimensions
        # * invert colours (so high values correspond to darker pixels in matplotlib)
        # * convert to six grayscale bins
        # * convert each pixel to dice template (keep separate so we can substitute templates)
        img = self.img
        rescaled_img = self._rescale_img(img)
        if not self.invert:
            rescaled_img = cv2.bitwise_not(rescaled_img)
        senarised_img = self.senarise_array(rescaled_img)
        dicified_img = self.convert_to_dice_array(senarised_img)
        return dicified_img
    
    def _rescale_img(self, img: np.ndarray):
        dim = (self.output_width, self.output_height)
        return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    
    @staticmethod
    def senarise_array(array: np.ndarray):
        hist, edges = np.histogram(array, bins=6)
        for i, (lower, upper) in enumerate(pairwise(edges)):
            if i == 0:
                array = np.where((array >= lower) & (array <= upper), i + 1, array)
            else:
                array = np.where((array > lower) & (array <= upper), i + 1, array)
        return array
        
    def convert_to_dice_array(self, array: np.ndarray):
        output_array = np.zeros((self.output_height * self.unit_size, self.output_width * self.unit_size), dtype=int)
        for i, row in enumerate(array):
            for j, col in enumerate(row):
                value = array[i][j]
                output_array = self._update_output_array(output_array, i, j, value)
        return output_array
    
    def _update_output_array(self, output_array: np.ndarray, row: int, col: int, value: int):
        s = int(self.unit_size)
        if self.invert:
            die_array = self._DICE_UNITS[value]
        else:
            die_array = 1 - self._DICE_UNITS[value]
        output_array[s * row: s * row + s, s * col: s * col + s] = die_array
        return output_array


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
    INVERT = True
    img_path = './images/duke.jpg'
    d = Dicifier(img_path, 65, 50, invert=INVERT)
    dicified = d.dicify()
    plt.imshow(1 - dicified, cmap='binary')    
    plt.show()
    cv2.imwrite('./images/duke_output_invert.jpg', 255 * dicified)
    