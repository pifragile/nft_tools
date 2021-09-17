import twitter
import os
import csv
import random 
from dotenv import load_dotenv
import time

# sleep 0.5 hour to avoid too many tweets in case of failures
time.sleep(1800)

load_dotenv()

# Consumer keys and access tokens, used for OAuth
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')
bearer_token = os.getenv('bearer_token')
 
api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_token_secret)


def get_post_text_csc(name, opensea_link):
	return f'''{name}
Generative Art by pifragile.

Each piece features a sample of the official source code of Ethereum.

Check it out on @opensea:
{opensea_link}

#NFT #NFTCommunity #opensea #nftcollector #nftart'''

def get_post_text_generic(name, opensea_link):
	return f'''{name}
Generative Art by pifragile.

Check it out on @opensea:
{opensea_link}

#NFT #NFTCommunity #opensea #nftcollector #nftart'''

def get_post_text_hca(name, opensea_link):
	return f'''{name}
Generative Art by pifragile.

1 NFT = 5 color patterns with proof of uniqueness

Check it out on @opensea:
{opensea_link}

#NFT #NFTCommunity #opensea #nftcollector #nftart'''

def get_post_text_cwa(name, opensea_link):
	return f'''{name}
Generative Art by pifragile.

Masses of warriors fighting, and only YOUR warrior survives💕

Check it out on @opensea:
{opensea_link}

#NFT #NFTCommunity #opensea #nftcollector #nftart'''


def get_post_text_cwp(name, opensea_link):
	return f'''{name}
0.01 ETH, minted on @0xPolygon, NO FEES🥳

Masses of warriors fighting, and only YOUR warrior survives💕

Check it out on @opensea:
{opensea_link}

#NFT #NFTCommunity #opensea #nftcollector #nftart #Polygon'''

def post_nft(series_name):
	shared_nfts_file = f'shared_nfts_{series_name}.txt'
	if not os.path.exists(shared_nfts_file):
		os.system(f'touch {shared_nfts_file}')

	shared_nfts = []
	with open(shared_nfts_file, 'r') as f:
		shared_nfts = [l.rstrip() for l in f.readlines()]

	with open(os.path.join('nft_data', f'nfts_{series_name}.csv')) as csv_file:
		reader = csv.reader(csv_file, delimiter=',')
		rows = list(reader)

	available_nfts = [row for row in rows if row[0] not in shared_nfts]

	if available_nfts == []:
		available_nfts = rows
		os.system(f'rm {shared_nfts_file}')

	filename, name, opensea_link = available_nfts[0]


	with open(os.path.join('nft_data', f'dropbox_links_{series_name}.csv')) as csv_file:
		reader = csv.reader(csv_file, delimiter=',')
		rows = list(reader)

		# second element of first row
		dropbox_link = [row for row in rows if row[0] == filename][0][1]


	status = globals().get(f'get_post_text_{series_name}', get_post_text_generic)(name, opensea_link)

	api.PostUpdate(status, media=dropbox_link, media_category='tweet_gif')

	with open(shared_nfts_file, 'a') as f:
		f.write(f'{filename}\n')


series_names = ['cfd', 'csc', 'hca', 'cwp', 'cwp']

while True:
	try:
		post_nft(random.choice(series_names))
		time.sleep(random.randint(int(0.75 * 3600), 3 * 3600))
	except Exception as e:
		print(e)
		time.sleep(60)
	


