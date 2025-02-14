import json
from PIL import Image, ImageTransform
from card_constants import *


def exract_card(image, top_left, bottom_left, bottom_right, top_right):
    """
    Extract a card from an image using the card's corners.
    """
    transform = [*top_left, *bottom_left, *bottom_right, *top_right]
    size = (card_w, card_h)

    result = image.transform(
        size, ImageTransform.QuadTransform(transform), resample=Image.Resampling.BICUBIC
    )

    return result


if __name__ == "__main__":
    path = "img_src_r2/card_corners.json"
    c = json.load(open(path))

    safety = 3

    for key in c:
        corners = c[key]
        img = Image.open(f"img_src_r2/{key}.jpg")
        top_left = [corners["top_left"][0] - safety, corners["top_left"][1] - safety]
        bottom_left = [
            corners["bottom_left"][0] - safety,
            corners["bottom_left"][1] + safety,
        ]
        bottom_right = [
            corners["bottom_right"][0] + safety,
            corners["bottom_right"][1] + safety,
        ]
        top_right = [corners["top_right"][0] + safety, corners["top_right"][1] - safety]

        card = exract_card(
            img,
            top_left,
            bottom_left,
            bottom_right,
            top_right,
        )
        card.save(f"img_target_r2/{key}.jpg")
