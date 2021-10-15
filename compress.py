import argparse
import os

from PIL import Image, ImageSequence

import multiprocessing as mp

from mp_utils import proc_wrapper

parser = argparse.ArgumentParser(description='Compress NFTs')
parser.add_argument('source', type=str, help='image path')
parser.add_argument('destination', type=str, help='output path path')
parser.add_argument('fileextension', type=str, help='file extension')

args = parser.parse_args()

source = os.path.abspath(args.source)
dest = os.path.abspath(args.destination)
file_extension = args.fileextension
if not os.path.isdir(dest):
    os.system(f'mkdir {dest}')


all_filenames = [fn for fn in os.listdir(source) if fn.split('.')[-1] == file_extension]
all_filenames_processed = [fn for fn in os.listdir(dest) if fn.split('.')[-1] == file_extension]


def compress_file(fn, source, dest):
    if file_extension == 'gif':
        size = 400, 400
        # Open source
        im = Image.open(os.path.join(source, fn))

        # Get sequence iterator
        frames = ImageSequence.Iterator(im)


        def thumbnails(frames):
            thumbnails = []
            durations = []
            for frame in frames:
                thumbnail = frame.copy()
                thumbnail.thumbnail(size, Image.ANTIALIAS)
                thumbnails.append(thumbnail)
                durations.append(frame.info['duration'])

            return thumbnails, durations
        frames, durations = thumbnails(frames)

        # Save output
        om = frames[0]  # Handle first frame separately
        om.info = im.info  # Copy sequence info
        om.save(os.path.join(dest, fn), save_all=True, append_images=frames[1:], duration=durations, loop=0)
    else:
        size = 600, 600
        im = Image.open(os.path.join(source, fn))
        im = im.resize(size)
        im.save(os.path.join(dest, fn))
    print(f'processed {fn}')


num_workers = mp.cpu_count()
pool = mp.Pool(num_workers)
results = []
for fn in all_filenames:
    if fn in all_filenames_processed:
        continue
    results.append(pool.apply_async(proc_wrapper, args=(compress_file, fn, source, dest)))

res = [result.get() for result in results]
