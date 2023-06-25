import numpy as np
from card_constants import *
from PIL import Image

def rotate(l, n):
    return l[n:] + l[:n]

def rotate_card(image):
    ds = [i*0.01 for i in range(100)]
    for d in ds:
        r = image.rotate(d)
        r.save('img_test\\test_r_{:.2f}.png'.format(d))
    return image

def rotate_card_order(image):
    d = 0.7
    for o in [Image.Resampling.NEAREST, Image.Resampling.BILINEAR, Image.Resampling.BICUBIC]:
        r = image.rotate(d, resample=o)
        r.save('img_test\\test_r_{:.2f}_o_{:}.png'.format(d,o))
    return image