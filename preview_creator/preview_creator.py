import argparse
import multiprocessing as mp
import os
import time

from fpdf import FPDF
from selenium import webdriver

parser = argparse.ArgumentParser(description='Compress NFTs')
parser.add_argument('html_path', type=str, help='html path')
parser.add_argument('num_images', type=int, help='number of images')

args = parser.parse_args()

html_path = os.path.abspath(args.html_path)
num_images = args.num_images

path = os.path.dirname(os.path.abspath(__file__))

tmp_path = os.path.join(path, 'tmp')
img_path = os.path.join(path, 'images')


def reset_tmp():
    os.system(f'rm -rf {tmp_path}')
    os.system(f'mkdir {tmp_path}')


def reset_images():
    os.system(f'rm -rf {img_path}')
    os.system(f'mkdir {img_path}')


opt = webdriver.ChromeOptions()
prefs = {'download.default_directory': tmp_path,
         'profile.default_content_setting_values.automatic_downloads': 1
         }
opt.add_experimental_option('prefs', prefs)


def get_tmp_file_names():
    files = os.listdir(tmp_path)
    return [f for f in files if len(f.split('.')) > 1 and f.split('.')[1] == 'png']


def get_downloaded_file_name():
    file_names = get_tmp_file_names()
    if len(file_names):
        return file_names[0]
    else:
        return None


base_url = f'file://{html_path}/preview.html?num=16'


def download():
    driver = webdriver.Chrome('./chromedriver-2', chrome_options=opt)
    driver.get(base_url)


def download_images():
    reset_images()
    reset_tmp()
    num_processes = num_images // 16
    processes = []
    for i in range(num_processes):
        p = mp.Process(target=download)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    
    while True: 
        if len(get_tmp_file_names()) == num_processes * 16:
            break
    time.sleep(5)


def create_pdf():
    pdf_width = 210
    pdf_height = 297
    pdf = FPDF()
    imagelist = get_tmp_file_names()[:num_images]
    for lst in [imagelist[i:i + 35] for i in range(0, len(imagelist), 35)]:
        margin = 2

        actual_size = (pdf_width - 6 * margin) / 5
        pdf.add_page()
        for idx, image in enumerate(lst):
            x = idx % 5
            y = idx // 5

            x = x * actual_size + (x + 1) * margin
            y = y * actual_size + + (y + 1) * margin
            pdf.image(os.path.join(tmp_path, image), x, y, actual_size, actual_size)

    pdf.output(f"preview_{round(time.time())}.pdf", "F")
    os.system('pkill -f Chrome')



download_images()
create_pdf()