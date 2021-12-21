import csv
import os
import random
import sys
import time
import urllib

import requests
import twitter
from PIL import Image
from dotenv import load_dotenv

interact = len(sys.argv) > 1 and sys.argv[1] == 'interact'

load_dotenv()

my_followers = []

# Consumer keys and access tokens, used for OAuth
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')
bearer_token = os.getenv('bearer_token')

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_token_secret,
                  tweet_mode='extended')


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


def get_post_text_csu(name, opensea_link):
    return f'''{name}
0.01 ETH, minted on @0xPolygon, NO FEES🥳

Generative Art by pifragile.

Check it out on @opensea:
{opensea_link}

#NFT #NFTCommunity #opensea #nftcollector #nftart #Polygon'''


def get_post_text_cfd(name, opensea_link):
    return f'''{name}
0.01 ETH, now available on @0xPolygon, NO FEES🥳

Check it out on @opensea:
{opensea_link}

#NFT #NFTCommunity #opensea #nftcollector #nftart #Polygon'''


def get_post_text_kin(name, opensea_link):
    return f'''{name}

Check it out on @opensea:
{opensea_link}

#generativeArt #NFT #NFTCommunity #opensea #nftcollector #nftart #Polygon'''


def get_nft_data(series_name):
    shared_nfts_file = f'shared_nfts_{series_name}.txt'
    if not os.path.exists(shared_nfts_file):
        os.system(f'touch {shared_nfts_file}')

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
    with open(shared_nfts_file, 'a') as f:
        f.write(f'{filename}\n')
    return filename, name, opensea_link


def get_twitter_media(series_name, dropbox_link):
    if series_name == 'kin':
        urllib.request.urlretrieve(
            dropbox_link,
            "img.png")

        img = Image.open("img.png")
        img = img.resize((1600, 1600))
        img.save('img.png')
        media = open('img.png', 'rb')
    else:
        media = dropbox_link
    return media


def get_dropbox_link(series_name, filename):
    with open(os.path.join('nft_data', f'dropbox_links_{series_name}.csv')) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        rows = list(reader)

        # second element of first row
        dropbox_link = [row for row in rows if row[0] == filename][0][1]
        return dropbox_link


def get_status_text(series_name, nft_name, opensea_link=None):
    status_text_fn = globals().get(f'get_post_text_{series_name}', get_post_text_generic)
    return status_text_fn(nft_name, opensea_link)


def post_nft(series_name):
    filename, name, opensea_link = get_nft_data(series_name)

    dropbox_link = get_dropbox_link(series_name, filename)
    status = get_status_text(series_name, name, opensea_link)

    media_category = 'tweet_gif' if filename.split('.')[1] == 'gif' else None

    media = get_twitter_media(series_name, dropbox_link)

    api.PostUpdate(status, media=media, media_category=media_category)


def validate_hashtags(hashtags):
    accepted_hashtags = ['nftartist', 'nftartists', 'nft', 'nftcollector', 'nftart', 'nftcommunity']
    for hashtag in hashtags:
        if hashtag.text.lower() in accepted_hashtags:
            return True
    return False


def validate_text(text):
    text = text.lower()

    forbidden_texts = ['shill', 'below', 'buy']

    for forbidden_text in forbidden_texts:
        if forbidden_text in text:
            return False
    return True


def validate_user(user_id):
    global my_followers
    # do not retweet own tweets
    if user_id == '1370329500442054657':
        return False
    with open('community_interactions.txt', 'r') as f:
        rows = f.read().splitlines()
        count = 0
        for row in rows:
            if row == user_id:
                count += 1
        if count > 10:
            print(f'User id: {id}, count: {count}')
            return False

    if int(user_id) in my_followers:
        print('Do not retweet for followers')
        return False
    return True


def update_community_interactions(user_id):
    with open('community_interactions.txt', 'a') as f:
        f.write(f'{user_id}\n')


def interact_with_community(last_interaction_id=None):
    statuses = api.GetHomeTimeline(since_id=last_interaction_id, exclude_replies=True)
    num_interactions = 0
    last_interaction_id = None

    for status in statuses:
        if not status.lang == 'en':
            continue

        if not validate_hashtags(status.hashtags):
            continue

        if hasattr(status, 'retweeted_status') and status.retweeted_status:
            statuses.append(status.retweeted_status)
            continue

        if not (hasattr(status, 'media') and status.media or hasattr(status, 'urls') and status.urls):
            continue

        if not validate_text(status.full_text):
            continue

        user_id = status.user.id_str
        if validate_user(user_id):
            status_id = status.id
            try:
                api.PostRetweet(status_id)
            except twitter.error.TwitterError as e:
                continue
            # like with 33% probability
            if not random.randint(0, 3):
                try:
                    api.CreateFavorite(status_id=status_id)
                except twitter.error.TwitterError as e:
                    continue

            print(f'processed status {status_id}')
            update_community_interactions(user_id)
            last_interaction_id = status_id
            time.sleep(5)
            num_interactions += 1

            if num_interactions > 4:
                break

    return last_interaction_id


def try_and_sleep(fn, args):
    num_tries = 0
    while num_tries < 3:
        try:
            fn(*args)
            break
        except Exception as e:
            print(e)
            time.sleep(10)
            num_tries += 1


def post_random_nft():
    series_names = ['kin', 'kin', 'kin', 'cfd', 'csc', 'hca', 'cwp', 'csu']
    try_and_sleep(post_nft, [random.choice(series_names)])


def get_file_extension(link):
    return link.split('?')[0].split('.')[-1]


def get_nft(collection):
    shared_nfts_file = f'shared_nfts_{collection["identifier"]}.txt'
    if not os.path.exists(shared_nfts_file):
        os.system(f'touch {shared_nfts_file}')

    with open(shared_nfts_file, 'r') as f:
        shared_nfts = [l.rstrip() for l in f.readlines()]

    available_nfts = [nft for nft in collection['nft_set'] if not str(nft['id']) in shared_nfts]

    if available_nfts == []:
        available_nfts = collection['nft_set']
        os.system(f'rm {shared_nfts_file}')

    nft = available_nfts[0]
    with open(shared_nfts_file, 'a') as f:
        f.write(f'{nft["id"]}\n')

    return nft


def post_nft_2():
    nft_data = requests.get('https://space.pifragile.com/pifragile/get-nfts').json()
    priorities = [collection['priority'] for collection in nft_data]
    collection = random.choices(nft_data, weights=priorities, k=1)[0]
    nft = get_nft(collection)
    status = collection['twitter_text']
    status = status.format(**{'collection': collection, 'nft': nft})
    media = nft['media']
    file_extension = get_file_extension(media)

    media_category =  None
    if file_extension == 'gif':
        media_category = 'tweet_gif'
    elif file_extension in ['mp4']:
        media_category = 'tweet_video'
        urllib.request.urlretrieve(
            media,
            "vid.mp4")
        media = open('vid.mp4', 'rb')
        media = api.UploadMediaChunked(media, media_category=media_category)
        time.sleep(60)
    api.PostUpdate(status, media=media, media_category=media_category)


def post_random_nft_2():
    try_and_sleep(post_nft_2, [])


last_interaction_id = None
if not os.path.exists('community_interactions.txt'):
    os.system('touch community_interactions.txt')
while True:
    if interact:
        time.sleep(60 * 15)
        try:
            my_followers = [u.id for u in api.GetFollowers(1370329500442054657)]
        except Exception:
            pass

        num_interactions = random.randint(3, 13)
        for _ in range(num_interactions):
            try:
                last_interaction_id = interact_with_community(last_interaction_id)
                time.sleep(10 * 60)
            except Exception as e:
                print(e)
    else:
        time.sleep(random.randint(int(0.5 * 3600), int(1.3 * 3600)))
    if random.random() < 0.8:
        post_random_nft_2()
    else:
        post_random_nft()
