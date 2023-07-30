from PIL import Image

def add_border(image, border_size):
    new_size = [s+border_size*2 for s in image.size] 
    res = Image.new("RGB", new_size, "White")

    box = tuple((n - o) // 2 for n, o in zip(new_size, image.size))

    res.paste(image, box)

    return res


if __name__ == '__main__':
    path = 'img_src\\card_split\\FR003.png'
    img = add_border(Image.open(path), 100)

    img.save('test.png')
