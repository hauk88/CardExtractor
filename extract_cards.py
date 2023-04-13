import numpy as np
from PIL import Image, ImageFilter, ImageDraw

path = 'img_src\\page_split\\page-0.jpg'


# Opening the image (R prefixed to string
# in order to deal with '\' in paths)
image = Image.open(path)
 
# Converting the image to grayscale, as edge detection
# requires input image to be of mode = Grayscale (L)
image = image.convert("L")
 
# Detecting Edges on the Image using the argument ImageFilter.FIND_EDGES
image = image.filter(ImageFilter.FIND_EDGES)

img_array = np.array(image, dtype=np.uint8)
 
card_boarder = 19
card_w = 423
card_h = 678
start_h = 18

def find_line_in_slice(img_slice):
    threshold = 200
    
    idx = np.where(img_slice > threshold)[0]

    first = idx[0]-1
    last = idx[-1]+1

    return (first, last)


def process_horisontal(start_w):
    # Row 1
    start_h = 18

    top_h = 188
    bottom_h = 400

    horisontal_lines = []

    horisontal_lines.append(start_h + int(top_h/2))
    horisontal_lines.append(start_h + card_h - int(bottom_h/2))

    start_boarder_w = start_w - card_boarder
    end_boarder_w = start_w + card_w + card_boarder

    points_left = []
    points_right = []
    for line in horisontal_lines:
        line_slice = img_array[line, start_boarder_w:end_boarder_w]
        (px1,px2) = find_line_in_slice(line_slice)
        points_left.append([line, px1 + start_boarder_w])
        points_right.append([line, px2 + start_boarder_w])
    left_line = np.polyfit([p[0] for p in points_left], [p[1] for p in points_left], 1)
    right_line = np.polyfit([p[0] for p in points_right], [p[1] for p in points_right], 1)

    return (left_line, right_line)

def process_vertical(start_w):
    # Row 1
    start_h = 18

    vertical_lines = []

    vertical_lines.append(start_w + int(card_w/3))
    vertical_lines.append(start_w + int(2*card_w/3))

    start_boarder_h = int(start_h/2)
    end_boarder_h = start_h + card_h + card_boarder

    points_top = []
    points_bottom = []
    for line in vertical_lines:
        line_slice = img_array[start_boarder_h:end_boarder_h, line]
        (px1,px2) = find_line_in_slice(line_slice)
        points_top.append([px1 + start_boarder_h, line])
        points_bottom.append([px2 + start_boarder_h, line])
    top_line = np.polyfit([p[1] for p in points_top], [p[0] for p in points_top], 1)
    bottom_line = np.polyfit([p[1] for p in points_bottom], [p[0] for p in points_bottom], 1)

    return (top_line, bottom_line)


start_w = 184
image = Image.open(path)

img1 = ImageDraw.Draw(image)
for i in range(4):
    start_w_1 = start_w + (card_w + 2*card_boarder + 2)*i
    (left, right) = process_horisontal(start_w_1)

    p_left = np.poly1d(left)
    p_right = np.poly1d(right)

    (top, bottom) = process_vertical(start_w_1)

    p_top = np.poly1d(top)
    p_bottom = np.poly1d(bottom)

    img1.line([p_left(start_h),start_h, p_left(start_h+card_h), start_h+card_h], fill="red", width=0)
    img1.line([p_right(start_h),start_h, p_right(start_h+card_h), start_h+card_h], fill="red", width=0)

    img1.line([start_w_1,p_top(start_w_1), start_w_1+card_w, p_top(start_w_1+card_w)], fill="red", width=0)
    img1.line([start_w_1,p_bottom(start_w_1), start_w_1+card_w, p_bottom(start_w_1+card_w)], fill="red", width=0)

image.save('draw_test.png')