from pdf2image import convert_from_path
import logging

def split_pdf(path, target):
    # Store Pdf with convert_from_path function
    logging.debug(f'reading from path {target}')

    images = convert_from_path(path)
    logging.debug(f'found {len(images)} pages')
    
    for i in range(len(images)):
        target_path = f'{target}page-{str(i)}.jpg'
        logging.debug(f'saving in path {target_path}')
        # Save pages as images in the pdf
        images[i].save(target_path, 'JPEG')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    path = 'img_src\\AgricolaFrWm.pdf'
    target = 'img_src\\page_split\\'

    split_pdf(path, target)