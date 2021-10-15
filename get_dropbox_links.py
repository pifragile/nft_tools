import argparse
import multiprocessing as mp

import dropbox
import os
from dotenv import load_dotenv

from mp_utils import proc_wrapper

load_dotenv()

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('source', type=str, help='image path')
parser.add_argument('collectionidentifier', type=str, help='output path path')
parser.add_argument('fileextension', type=str, help='file extension')

args = parser.parse_args()

dirname = os.path.abspath(args.source)
dropbox_path = dirname.split('Dropbox')[1]
outfile = os.path.join('nft_data', f'dropbox_links_{args.collectionidentifier}.csv')

if not os.path.exists(outfile):
    os.system(f'touch {outfile}')

dbx = dropbox.Dropbox(os.getenv('dropbox_key'))


def get_link(filename, dropbox_path):
    path = os.path.join(dropbox_path, filename)
    print(path)
    try:
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(path).url
    except Exception:
        shared_link_metadata = dbx.sharing_list_shared_links(path, direct_only=True).links[0].url

    return filename, shared_link_metadata.replace('dl=0', 'dl=1')


with open(outfile, 'r') as f:
    processed_filenames = [l.rstrip().split(',')[0] for l in f.readlines()]

num_workers = mp.cpu_count()
pool = mp.Pool(num_workers)
results = []

for filename in os.listdir(dirname):
    if not filename or not filename.split('.')[-1] == args.fileextension:
        continue

    if filename in processed_filenames:
        continue

    results.append(pool.apply_async(proc_wrapper, args=(get_link, filename, dropbox_path)))

res = [result.get() for result in results]
with open(outfile, 'a') as f:
    for filename, link in res:
        f.write(f'{filename},{link}\n')
