import numpy as np
from PIL import Image, ImageFilter

path = 'img_src\\page_split\\page-0.jpg'


# Opening the image (R prefixed to string
# in order to deal with '\' in paths)
image = Image.open(path)
 
# Converting the image to grayscale, as edge detection
# requires input image to be of mode = Grayscale (L)
image = image.convert("L")
 
# Detecting Edges on the Image using the argument ImageFilter.FIND_EDGES
image = image.filter(ImageFilter.FIND_EDGES)
 

card_boarder = 19

start_w = 184
start_h = 18

card_w = 423
card_h = 678


img_array = np.array(image, dtype=np.uint8)

cords = (start_w,start_h,start_w+card_w,start_h+card_h)


vert_line1 = start_h + int(card_h/3)
vert_line2 = start_h + int(2*card_h/3)

crop1 = img_array[:,vert_line1]
crop2 = img_array[:,vert_line2]


im1 = Image.fromarray(crop1)
im1.save('crop_test1.png')

im2 = Image.fromarray(crop2)
im2.save('crop_test2.png')