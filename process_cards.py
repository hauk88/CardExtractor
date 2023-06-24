import os
from card_constants import *
from extract_card import extract_card
from PIL import Image, ImageFilter, ImageDraw


def process_cards():
    path = 'img_src\\card_split\\'
    target_path = 'img_res\\'
    card_paths = os.listdir(path)

    for card_path in card_paths:
        # number=int(card_path.split('-')[1].split('.')[0])
        # is_minor = number <= last_minor
        # if not is_minor:
        #     break
        full_path = path + card_path
        img = extract_card(Image.open(full_path))

        img.save(target_path+card_path)



if __name__ == '__main__':
    process_cards()