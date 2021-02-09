import cv2 


class Dicifier:
    
    def __init__(self, img_path, output_height, output_width):
        self.img_path = img_path
        self.output_height = output_height
        self.output_width = output_width

    @property
    def img(self):
        img = cv2.imread(img_path, 0)
        h, w = img.shape
        self.input_height = h
        self.input_width = w
        return img


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
    img_path = './images/duke.jpg'
    d = Dicifier(img_path, 100, 100)
    img = d.img
    print(d.input_height)
    plt.imshow(img)
    plt.show()
    
    