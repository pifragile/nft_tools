import csv
import os
import random
import sys
import time

import twitter
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

    with open(shared_nfts_file, 'a') as f:
        f.write(f'{filename}\n')

    with open(os.path.join('nft_data', f'dropbox_links_{series_name}.csv')) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        rows = list(reader)

        # second element of first row
        dropbox_link = [row for row in rows if row[0] == filename][0][1]

    status = globals().get(f'get_post_text_{series_name}', get_post_text_generic)(name, opensea_link)

    media_category = 'tweet_gif' if filename.split('.')[1] == 'gif' else None
    api.PostUpdate(status, media=dropbox_link, media_category=media_category)



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


def post_random_nft():
    series_names = ['kin', 'kin', 'kin', 'cfd', 'csc', 'hca', 'cwp', 'csu']
    num_tries = 0
    while num_tries < 3:
        try:
            post_nft(random.choice(series_names))
            break
        except Exception as e:
            print(e)
            time.sleep(10)
            num_tries += 1


last_interaction_id = None
if not os.path.exists('community_interactions.txt'):
    os.system('touch community_interactions.txt')
while True:
    if interact:
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
        time.sleep(random.randint(int(0.5 * 3600), int(2.75 * 3600)))
    post_random_nft()
    time.sleep(60 * 15)
