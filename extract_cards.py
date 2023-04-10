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

top_h = 188
bottom_h = 400

vert_line1 = start_h + int(top_h/2)
vert_line2 = start_h + card_h - int(bottom_h/2)

h = 1

start_boarder_w = start_w - card_boarder
end_boarder_w = start_w + card_w + card_boarder


crop1 = img_array[vert_line1:vert_line1+h, start_boarder_w:end_boarder_w]
crop2 = img_array[vert_line2:vert_line2+h, start_boarder_w:end_boarder_w]

threshold = 200
_, idx = np.where(crop1 > threshold)

v_left_top = idx[0]-1
v_right_top = idx[-1]+1

threshold = 200
_, idx = np.where(crop2 > threshold)

v_left_bottom = idx[0]-1
v_right_bottom = idx[-1]+1


print((v_left_top, v_left_bottom))

print((v_right_top, v_right_bottom))


im1 = Image.fromarray(crop1)
im1.save('crop_test1.png')

im2 = Image.fromarray(crop2)
im2.save('crop_test2.png')