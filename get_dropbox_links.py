import dropbox, os
from dotenv import load_dotenv
import sys

load_dotenv()

dirname = os.path.abspath(sys.argv[1])
dropbox_path = dirname.split('Dropbox')[1]
outfile = os.path.join('nft_data', f'dropbox_links_{sys.argv[2]}.csv')

if not os.path.exists(outfile):
	os.system(f'touch {outfile}')

dbx = dropbox.Dropbox(os.getenv('dropbox_key'))

for filename in os.listdir(dirname):
	if not filename or not filename.split('.')[-1] == 'gif':
		continue

	with open(outfile, 'r') as f:
		filenames = [l.rstrip().split(',')[0] for l in f.readlines()]
		if filename in filenames:
			continue

	path = os.path.join(dropbox_path, filename)
	print(path)
	try:
		shared_link_metadata = dbx.sharing_create_shared_link_with_settings(path).url
	except Exception:
		shared_link_metadata = dbx.sharing_list_shared_links(path, direct_only=True).links[0].url

	shared_link_metadata = shared_link_metadata.replace('dl=0', 'dl=1')

	with open(outfile, 'a') as f:
		f.write(f'{filename},{shared_link_metadata}\n')