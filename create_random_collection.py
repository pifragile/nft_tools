import argparse
import os
import random

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('source', type=str, help='image path')
parser.add_argument('destination', type=str, help='output path path')
parser.add_argument('fileextension', type=str, help='file extension')

args = parser.parse_args()

source = os.path.abspath(args.source)
dest = os.path.abspath(args.destination)
file_extension = args.fileextension

all_filenames = [fn for fn in os.listdir(source) if fn.split('.')[-1] == file_extension]
randomized_files = sorted(all_filenames, key=lambda x: random.random())

current_number = len(os.listdir(dest))

for filename in randomized_files:
    command = f'cp {source}/{filename} {dest}/{current_number:04d}.{file_extension}'
    print(command)
    os.system(command)
    current_number += 1
