import numpy as np
from card_constants import *
from PIL import Image, ImageFilter, ImageDraw


def extract_card(image):
    img_array = np.array(image, dtype=np.uint8)
    (left, right) = process_horisontal(img_array)
    p_left,p_right = fit_polynomial(left, right)

    (top, bottom) = process_vertical(img_array)
    p_left,p_right = fit_polynomial(top, bottom)



    img1 = ImageDraw.Draw(image)
    
    img1.line([p_left(0),0, p_left(image.size[1]), image.size[1]], fill="red", width=0)
    img1.line([p_right(0),0, p_right(image.size[1]), image.size[1]], fill="red", width=0)
    
    return image


def fit_polynomial(p_1, p_2):

    # top_line = np.polyfit([p[1] for p in points_top], [p[0] for p in points_top], 1)
    # bottom_line = np.polyfit([p[1] for p in points_bottom], [p[0] for p in points_bottom], 1)

    coef_1 = np.polyfit([p[0] for p in p_1], [p[1] for p in p_1], 1)
    coef_2 = np.polyfit([p[0] for p in p_2], [p[1] for p in p_2], 1)

    common_slope = (coef_1[0] + coef_2[0])/2

    coef_1[0] = common_slope
    coef_2[0] = common_slope

    line_1 = np.poly1d(coef_1)
    line_2 = np.poly1d(coef_2)

    return (line_1, line_2)

def process_horisontal(img_array):
    # Row 1
    start_h = 18

    top_h = 188
    bottom_h = 400

    horisontal_lines = []

    horisontal_lines.append(start_h + int(top_h/2))
    horisontal_lines.append(start_h + card_h - int(bottom_h/2))

    points_left = []
    points_right = []
    for line in horisontal_lines:
        line_slice = img_array[line, :]
        (px1,px2) = find_line_in_slice(line_slice)
        points_left.append([line, px1])
        points_right.append([line, px2])

    return (points_left, points_right)

def process_vertical(img_array):
    # Row 1

    vertical_lines = []

    vertical_lines.append(int(card_w/3))
    vertical_lines.append(int(2*card_w/3))

    points_top = []
    points_bottom = []
    for line in vertical_lines:
        line_slice = img_array[:, line]
        (px1,px2) = find_line_in_slice(line_slice)
        points_top.append([px1, line])
        points_bottom.append([px2, line])

    return (points_top, points_bottom)



def find_line_in_slice(img_slice):
    threshold = 100
    target_color = np.array(minor_border_color)

    idx = []
    for i in range(len(img_slice)):
        color = img_slice[i]
        diff = target_color - color
        d = np.linalg.norm(diff)
        if(d < threshold):
            idx.append(i)

    df = 3
    dl = 5
    first = idx[0]-df
    last = idx[-1]+dl

    return (first, last)


if __name__ == '__main__':
    path = 'img_src\\card_split\\card-1.png'
    img = extract_card(Image.open(path))

    img.save('test.png')