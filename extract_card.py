import numpy as np
from card_constants import *
from PIL import Image, ImageFilter, ImageDraw, ImageTransform
from enum import Enum

def extract_card(image):
    img_array = np.array(image, dtype=np.uint8)
    (left, right) = process_horisontal(img_array, EdgeMode.COLOR)
    (top, bottom) = process_vertical(img_array, EdgeMode.COLOR)

    d = 10
    box = [min(left[0][1], left[1][1])-d, 
           min(top[0][0], top[1][0])-d,
           max(right[0][1],right[1][1])+d,
           max(bottom[0][0], bottom[1][0])+d]
    
    image_box = image.crop(box)

    imgw = image_box.convert("L")
 
    # Detecting Edges on the Image using the argument ImageFilter.FIND_EDGES
    imgw = imgw.filter(ImageFilter.FIND_EDGES)
    box_1px = [1,1,imgw.size[0]-1, imgw.size[1]-1]
    imgw = imgw.crop(box_1px)

    img_array = np.array(imgw, dtype=np.uint8)    
    
    (left, right) = process_horisontal(img_array, EdgeMode.BW)
    (top, bottom) = process_vertical(img_array, EdgeMode.BW)

    image_box = image_box.crop(box_1px)

    def find_cross_t(p1,p2,q1,q2):
        x = find_cross(p1,p2,q1,q2)
        return [x[1],x[0]]

    top_left = find_cross_t(left[0], left[1], top[0],top[1])
    top_right = find_cross_t(right[0], right[1], top[1],top[0])
    bottom_left = find_cross_t(left[1], left[0], bottom[0],bottom[1])
    bottom_right = find_cross_t(right[1], right[0], bottom[1],bottom[0])  

    # Use this https://stackoverflow.com/questions/71724403/crop-an-image-in-pil-using-the-4-points-of-a-rotated-rectangle
    
    # Define 8-tuple with x,y coordinates of top-left, bottom-left, bottom-right and top-right corners and apply
    transform=[*top_left,*bottom_left,*bottom_right, *top_right]
    size = (card_w,card_h)

    result = image_box.transform(size, ImageTransform.QuadTransform(transform), resample=Image.Resampling.BICUBIC)
    
    return result

def extract_card_draw(image):
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

    draw_points(corners)
    
    return image

def find_cross(p1,p2,q1,q2):
    # p(t) = a*t + b
    a = p1-p2
    b = p2

    # q(t) = c*t + d
    c = q1-q2
    d = q2

    # Solve p(t1) = q(t2), i.e. At = bm
    A = np.array([a, -c]).T
    bm = d-b

    t = np.linalg.solve(A,bm)

    # Calculate point using p(t1)
    x = a*t[0] + b

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

def process_horisontal(img_array, mode):
    start_h = 18

    top_h = 188
    bottom_h = 400

    horisontal_lines = []

    horisontal_lines.append(start_h + int(top_h/2))
    horisontal_lines.append(start_h + card_h - int(bottom_h/2))
    return process_horisontal_lines(img_array, horisontal_lines, mode)

def process_horisontal_lines(img_array, lines, mode):
    points_left = []
    points_right = []
    for line in lines:
        line_slice = img_array[line, :]
        (px1,px2) = find_line_in_slice(line_slice, mode)
        points_left.append(np.array([line, px1]))
        points_right.append(np.array([line, px2]))

    return (points_left, points_right)

def process_vertical(img_array,mode):
    vertical_lines = []

    vertical_lines.append(int(card_w/3))
    vertical_lines.append(int(2*card_w/3))

    points_top = []
    points_bottom = []
    for line in vertical_lines:
        line_slice = img_array[:, line]
        (px1,px2) = find_line_in_slice(line_slice, mode)
        points_top.append(np.array([px1, line]))
        points_bottom.append(np.array([px2, line]))

    return (points_top, points_bottom)

class EdgeMode(Enum):
    COLOR = 1
    BW = 2

def find_line_in_slice(img_slice, mode):
    threshold = 100
    if(mode == EdgeMode.COLOR):
        target_color = np.array(minor_border_color)
    if(mode == EdgeMode.BW):
        target_color = 255

    idx = []
    for i in range(len(img_slice)):
        color = img_slice[i]
        diff = target_color - color
        d = np.linalg.norm(diff)
        if(d < threshold):
            idx.append(i)

    first = idx[0]
    last = idx[-1]

    return (first, last)


if __name__ == '__main__':
    path = 'img_src\\card_split\\card-168.png'
    img = extract_card(Image.open(path))

    img.save('test.png')