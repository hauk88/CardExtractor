import os
from add_border import add_border
from card_constants import *
from extract_card import extract_card
from PIL import Image, ImageFilter, ImageDraw


def process_cards():
    path = 'img_src\\card_split\\'
    target_path = 'img_res\\'
    card_paths = os.listdir(path)

    for card_path in card_paths:
        print(f'Processing {card_path}')
        full_path = path + card_path
        img = extract_card(Image.open(full_path))
        img = add_border(img, card_border)

        img.save(target_path+card_path)

if __name__ == '__main__':
    process_cards()