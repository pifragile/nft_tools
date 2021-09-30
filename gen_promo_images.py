import argparse
import os
import random

import imageio
from PIL import Image

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('imagepath', type=str, help='image path')
parser.add_argument('outputpath', type=str, help='output path path')
parser.add_argument('numimages', type=int, help='number of generated images')
parser.add_argument('-l', '--logo', action='store_true', help='create logos')
parser.add_argument('-f', '--featured', action='store_true', help='create featured images')
parser.add_argument('-b', '--banner', action='store_true', help='create banners')

args = parser.parse_args()

image_folder = args.imagepath
output_path = args.outputpath
num_images = args.numimages

filename_list = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.split('.')[1] == 'png']

images = []
for filename in filename_list:
    img = Image.open(filename)
    images.append(img)

if args.logo:
    # logo
    for i in range(num_images):
        image_choice = random.sample(images, 5)

        if image_choice[0].mode == 'RGBA':
            images_on_white = []
            for image in image_choice:
                background = Image.new('RGBA', (2000, 2000), (255, 255, 255, 255))
                background.paste(image, (0, 0), image)
                images_on_white.append(background)
            image_choice = images_on_white
        imageio.mimsave(os.path.join(output_path, f'logo{i}.gif'), image_choice, duration=0.3)

if args.featured:
    # featured image 600 x 400
    for i in range(num_images):
        header = Image.new('RGBA', (1200, 800))
        image_choice = random.sample(images, 6)

        for idx, img in enumerate(image_choice):
            img = img.convert('RGBA')
            x = (idx % 3) * 400
            y = (idx // 3) * 400
            img = img.resize((400, 400))
            header.paste(img, (x, y), img)

        header.save(os.path.join(output_path, f'featured_image_{i}.png'))

if args.banner:
    # banner 1400 x 400
    for i in range(num_images):
        header = Image.new('RGBA', (1400, 400))
        image_choice = random.sample(images, 14 * 4)

        for idx, img in enumerate(image_choice):
            x = (idx % 14) * 100
            y = (idx // 14) * 100
            img = img.resize((100, 100))
            header.paste(img, (x, y), img)

        header.save(os.path.join(output_path, f'banner_{i}.png'))
