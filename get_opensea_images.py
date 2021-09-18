import os
import time

import requests

image_urls_file_unsold = 'open_sea_image_urls_unsold.csv'
image_urls_file_sold = 'open_sea_image_urls_sold.csv'
collection_slugs_file = 'collections.txt'
latest_offset_file = 'latest_offset.txt'
latest_offset_file_collections = 'latest_offset_collections.txt'


def create_file_if_not_exists(path):
    if not os.path.exists(path):
        os.system(f'touch {path}')


create_file_if_not_exists(image_urls_file_unsold)
create_file_if_not_exists(image_urls_file_sold)
create_file_if_not_exists(latest_offset_file)
create_file_if_not_exists(latest_offset_file_collections)
create_file_if_not_exists(collection_slugs_file)

with open(latest_offset_file_collections, 'r') as f:
    try:
        i = int(f.readline().rstrip())
    except Exception:
        i = 0


while True:
    try:
        url = 'https://api.opensea.io/api/v1/collections'
        querystring = {'offset': i, 'limit': '300'}
        res = requests.request('GET', url, params=querystring)
    except Exception as e:
        print(e)
        continue

    if not res.ok:
        print(res.text)
        print(res.status_code)
        time.sleep(10)
        continue

    data = res.json()
    if 'collections' not in data:
        print(data)

    for collection in data['collections']:
        try:
            if 'slug' in collection.keys() and collection['slug']:
                with open(collection_slugs_file, 'a') as f:
                    f.write(f"{collection['slug']}\n")
        except Exception:
            continue

    i += 300
    with open(latest_offset_file_collections, 'w') as f:
        f.write(f'{i}\n')
    time.sleep(1)



# with open(latest_offset_file, 'r') as f:
#     try:
#         i = int(f.readline().rstrip())
#     except Exception:
#         i = 0
# # offset has to be < 10000
# # need to find another way, maybe go over collections
# while i < 10000000:
#     try:
#         res = requests.get(f'https://api.opensea.io/api/v1/assets?order_direction=desc&offset={i}&limit=50')
#     except Exception as e:
#         print(e)
#         continue
#
#     if not res.ok:
#         print(res.text)
#         print(res.status_code)
#         time.sleep(10)
#         continue
#
#     data = res.json()
#     if 'assets' not in data:
#         print(data)
#
#     for nft in data['assets']:
#         try:
#             if 'image_url' in nft.keys() and nft['image_url']:
#                 if 'num_sales' in nft.keys() and int(nft['num_sales']) > 0:
#                     with open(image_urls_file_sold, 'a') as f:
#                         f.write(f"{nft['id']},{nft['image_url']}\n")
#                 else:
#                     with open(image_urls_file_unsold, 'a') as f:
#                         f.write(f"{nft['id']},{nft['image_url']}\n")
#         except Exception:
#             continue
#
#     i += 50
#     with open(latest_offset_file, 'w') as f:
#         f.write(f'{i}\n')
#     time.sleep(1)
