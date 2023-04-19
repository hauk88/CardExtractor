import numpy as np
from card_constants import *
from PIL import Image, ImageFilter, ImageDraw


def extract_card(image):
    img_array = np.array(image, dtype=np.uint8)
    (left, right) = process_horisontal(img_array)
    c_left,c_right = fit_polynomial(left, right)

    (top, bottom) = process_vertical(img_array)
    c_top,c_bottom = fit_polynomial(swap_points(top), swap_points(bottom))

    p_left = np.poly1d(c_left)
    p_right = np.poly1d(c_right)
    p_top = np.poly1d(c_top)
    p_bottom = np.poly1d(c_bottom)


    img1 = ImageDraw.Draw(image)



    img1.line([p_left(0),0, p_left(image.size[1]), image.size[1]], fill="red", width=0)
    img1.line([p_right(0),0, p_right(image.size[1]), image.size[1]], fill="red", width=0)

    img1.line([0,p_top(0), image.size[1], p_top(image.size[1])], fill="red", width=0)
    img1.line([0,p_bottom(0), image.size[1], p_bottom(image.size[1])], fill="red", width=0)

    def draw_points(points):
        w = 2
        for p in points:
            img1.ellipse((round(p[1])-w, round(p[0])-w,round(p[1])+w,round(p[0])+w), fill='green')

    draw_points(left)
    draw_points(right)
    draw_points(top)
    draw_points(bottom)

    corners = [find_cross(left[0], left[1], top[0],top[1]),
               find_cross(right[0], right[1], top[1],top[0]),
               find_cross(left[1], left[0], bottom[0],bottom[1]),
               find_cross(right[1], right[0], bottom[1],bottom[0])]

    print(corners)

    draw_points(corners)
    
    return image


def find_cross(p1,p2,q1,q2):
    pdiff = (p1-p2).T
    qdiff = (q1-q2).T

    A = np.array([pdiff, -qdiff])
    b = q2-p2

    t = np.linalg.solve(A,b)

    x = p2 + t*pdiff

    return x

def swap_points(p):
    res = []
    for i in range(len(p)):
        res.append([p[i][1], p[i][0]])
    return res

def fit_polynomial(p_1, p_2):
    coef_1 = np.polyfit([p[0] for p in p_1], [p[1] for p in p_1], 1)
    coef_2 = np.polyfit([p[0] for p in p_2], [p[1] for p in p_2], 1)

    common_slope = (coef_1[0] + coef_2[0])/2

    coef_1[0] = common_slope
    coef_2[0] = common_slope

    return (coef_1, coef_2)

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
        points_left.append(np.array([line, px1]))
        points_right.append(np.array([line, px2]))

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
        points_top.append(np.array([px1, line]))
        points_bottom.append(np.array([px2, line]))

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