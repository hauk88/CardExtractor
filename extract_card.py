import numpy as np
from card_constants import *
from polynomial_fitters import *
from PIL import Image, ImageFilter, ImageDraw, ImageTransform

def extract_card(image, draw=False):
    img_array = np.array(image, dtype=np.uint8)
    # Find small box around card
    (left, right) = process_horisontal(img_array, np.array(minor_border_color), 100)
    (top, bottom) = process_vertical(img_array, np.array(minor_border_color), 100)

    # Define padding around box
    d_left = 10
    d_top = 10
    d_right = 13
    d_bottom = 15

    left_x = [l[0] for l in left]
    rigt_x = [l[0] for l in right]
    top_y = [l[1] for l in top]
    bottom_y = [l[1] for l in bottom] 

    box = [min(left_x)-d_left, 
           min(top_y)-d_top,
           max(rigt_x)+d_right,
           max(bottom_y)+d_bottom]
    
    image_box = image.crop(box)

    # Use edge detection on boxed card to find edges
    imgw = image_box.convert("L")
    imgw = imgw.filter(ImageFilter.FIND_EDGES)

    # Remove 1 px as this is detected as an edge
    box_1px = [1,1,imgw.size[0]-1, imgw.size[1]-1]
    
    image_box = image_box.crop(box_1px)
    imgw = imgw.crop(box_1px)

    img_array = np.array(imgw, dtype=np.uint8)    
    
    (left, right) = process_horisontal(img_array, 255, 100)
    (top, bottom) = process_vertical(img_array, 255, 100)

    # Edge detection seem to detect 1px before edge on top and left. Shift to correct
    for i in range(len(left)):
        left[i][0] = left[i][0] + 1

    for i in range(len(top)):
        top[i][1] = top[i][1] + 1

    if draw:
        img_test = imgw.convert('RGB')

        img1 = ImageDraw.Draw(img_test)

        def draw_points(points):
            w = 1
            for p in points:
                img1.ellipse((round(p[0])-w, round(p[1])-w,round(p[0])+w,round(p[1])+w), fill='green')

        draw_points(left)
        draw_points(right)
        draw_points(top)
        draw_points(bottom)

    # Find polynomial that fits the points
    # For left and right we need to swap the points to get a well behaved function
    c_left = fit_polynomial_outliers_iterative(swap_points(left))
    c_right = fit_polynomial_outliers_iterative(swap_points(right))
    c_top = fit_polynomial_outliers_iterative(top)
    c_bottom = fit_polynomial_outliers_iterative(bottom)

    p_left = np.poly1d(c_left)
    p_right = np.poly1d(c_right)
    p_top = np.poly1d(c_top)
    p_bottom = np.poly1d(c_bottom)

    # Find two points for each line
    xp = [0, imgw.size[0]]
    yp = [0, imgw.size[1]]

    top = [np.array([x,p_top(x)]) for x in xp]
    bottom = [np.array([x,p_bottom(x)]) for x in xp]

    left = [np.array([p_left(y), y]) for y in yp]
    right = [np.array([p_right(y),y]) for y in yp]

    if draw:
        img1.line([left[0][0], left[0][1],left[1][0], left[1][1]], fill="red", width=0)
        img1.line([right[0][0], right[0][1],right[1][0], right[1][1]], fill="red", width=0)
        img1.line([top[0][0], top[0][1],top[1][0], top[1][1]], fill="red", width=0)
        img1.line([bottom[0][0], bottom[0][1],bottom[1][0], bottom[1][1]], fill="red", width=0)
        return img_test

    # Use points to find corners of the card
    top_left = find_cross(left[0], left[1], top[0],top[1])
    top_right = find_cross(right[0], right[1], top[1],top[0])
    bottom_left = find_cross(left[1], left[0], bottom[0],bottom[1])
    bottom_right = find_cross(right[1], right[0], bottom[1],bottom[0])

    # Rotate and crop card using corners

    # Use this https://stackoverflow.com/questions/71724403/crop-an-image-in-pil-using-the-4-points-of-a-rotated-rectangle
    # Define 8-tuple with x,y coordinates of top-left, bottom-left, bottom-right and top-right corners and apply
    transform=[*top_left,*bottom_left,*bottom_right, *top_right]
    size = (card_w,card_h)

    result = image_box.transform(size, ImageTransform.QuadTransform(transform), resample=Image.Resampling.BICUBIC)
    
    return result

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

def process_horisontal(img_array, target, threshold):
    h = img_array.shape[0]

    border = (h - card_h)
    safety = 5

    # Top
    start = border + card_corner_size + safety
    end = card_top_part_h - safety
    horisontal_lines = [i for i in range(start, end, 1)]

    # Bottom
    start = card_h + border - card_bottom_part_h + safety
    end = card_h - border - card_corner_size - safety
    for i in range(start, end, 1):
        horisontal_lines.append(i)

    return process_horisontal_lines(img_array, horisontal_lines, target, threshold)

def process_horisontal_lines(img_array, lines, target, threshold):
    points_left = []
    points_right = []
    for line in lines:
        line_slice = img_array[line, :]
        (px1,px2) = find_line_in_slice(line_slice, target, threshold)
        points_left.append(np.array([px1, line]))
        points_right.append(np.array([px2, line]))

    return (points_left, points_right)

def process_vertical(img_array,target, threshold):
    w = img_array.shape[1]
    
    border = (w - card_w)
    safety = 5

    start = border + card_corner_size + safety
    end = w - start
    vertical_lines = [i for i in range(start,end,1)]

    points_top = []
    points_bottom = []
    for line in vertical_lines:
        line_slice = img_array[:, line]
        (px1,px2) = find_line_in_slice(line_slice, target, threshold)
        points_top.append(np.array([line, px1 ]))
        points_bottom.append(np.array([line, px2]))

    return (points_top, points_bottom)

def find_line_in_slice(img_slice, target_color, threshold=100):

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
    path = 'img_src\\card_split\\FR003.png'
    img = extract_card(Image.open(path), draw=False)

    img.save('test.png')