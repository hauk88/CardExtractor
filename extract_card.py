import numpy as np
from card_constants import *
from PIL import Image, ImageFilter, ImageDraw


def extract_card(image):
    img_array = np.array(image, dtype=np.uint8)
    print(img_array)

    print(minor_border_color)

    return image



def find_line_in_slice(img_slice):
    threshold = 200
    
    idx = np.where(img_slice > threshold)[0]

    first = idx[0]-1
    last = idx[-1]+1

    return (first, last)


if __name__ == '__main__':
    path = 'img_src\\card_split\\card-1.png'
    img = extract_card(Image.open(path))

    img.save('test.png')