import requests
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from shutil import copyfile

with open('allsky.jpg', 'wb') as f:
    resp = requests.get('http://staernwarten.de/wp-content/uploads/webcam/1/ImageLastFTP_AllSKY-COPY.jpg', verify=False)
    if resp.status_code != 200:
        copyfile("fehler.png", "allsky_final.png")
        exit(1)
    f.write(resp.content)

img = Image.open('allsky.jpg')
image_width = 1950
img = ImageChops.offset(img, 75, 0)


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


img_thumb = crop_center(img, image_width, image_width)


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


img_square = crop_max_square(img).resize((image_width, image_width), Image.LANCZOS)
img_thumb = mask_circle_transparent(img_square, 4)
img_thumb.save('allsky_final.png')
