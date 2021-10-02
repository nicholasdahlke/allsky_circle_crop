import os
import glob
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import urllib.request
import ssl
import requests
import numpy as np

with open('allsky.jpg', 'wb') as f:
    resp = requests.get('http://staernwarten.de/wp-content/uploads/webcam/1/ImageLastFTP_AllSKY-COPY.jpg', verify=False)
    f.write(resp.content)

im = Image.open('allsky.jpg')
image_width = 1950
im = ImageChops.offset(im, 75, 0)


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


im_thumb = crop_center(im, image_width, image_width)
im_thumb.save('allsky_cropped.jpg', quality=95)
def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

def mask_circle_transparent(pil_img, blur_radius, offset=0):
    offset = blur_radius * 2 + offset
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

    result = pil_img.copy()
    result.putalpha(mask)

    return result


im_square = crop_max_square(im).resize((image_width, image_width), Image.LANCZOS)
im_thumb = mask_circle_transparent(im_square, 4)
im_thumb.save('allsky_circle.png')