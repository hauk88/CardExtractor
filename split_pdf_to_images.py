from pdf2image import convert_from_path
import logging
from PIL import Image, ImageFilter, ImageDraw
import os

def split_pdf_to_pages(path, target):
    # Store Pdf with convert_from_path function
    logging.debug(f'reading from path {target}')

    images = convert_from_path(path)
    logging.debug(f'found {len(images)} pages')
    
    for i in range(len(images)):
        target_path = f'{target}page-{str(i)}.jpg'
        logging.debug(f'saving in path {target_path}')
        # Save pages as images in the pdf
        images[i].save(target_path, 'JPEG')


def split_pdf_to_cards(path, target, names):
    # Store Pdf with convert_from_path function
    logging.debug(f'reading from path {target}')

    images = convert_from_path(path, poppler_path=os.getenv('POPPLER_PATH'))
    logging.debug(f'found {len(images)} pages')
    
    total_count = 0
    for i in range(len(images)):
        c = split_page_to_card(images[i], target, total_count, i+1, names)

        total_count = total_count + c


def split_page_to_card(image, target, total_count, page, names):
    cols = [160, 628, 1093, 1558, image.size[0]]
    rows = [0, 719, image.size[1]]

    if(page == 20 or page == 28):
        return 0

    counter = 0
    for i in range(len(rows)-1):
        for j in range(len(cols)-1):
            if(page == 16 and (j == 0 or i == 1)):
                continue
            # crop image between loop idx
            counter = counter + 1
            shape = (cols[j], rows[i], cols[j+1],rows[i+1])
            cropped = image.crop(shape)
            name = names[total_count + counter-1]
            path = get_unique_path(target,name, 'png')
            cropped.save(path)
            
    return counter

def get_unique_path(target, name, ext):
    path = f'{target}{name}.{ext}'
    counter = 1
    while os.path.exists(path):
        path = f'{target}{name}({counter}).{ext}'
        counter += 1
    
    return path

def parse_card_names(path):
    with open(path) as file:
        lines = [line.rstrip() for line in file]
    return lines

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    path = 'img_src\\AgricolaFrWm.pdf'
    target = 'img_src\\card_split\\'
    card_name_path = 'card_to_name.txt'

    if not os.path.exists(target):
        os.mkdir(target)

    names = parse_card_names(card_name_path)
    split_pdf_to_cards(path, target, names)