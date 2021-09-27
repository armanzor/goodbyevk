#!/usr/bin/env python3
# Author: 9tudeptb@duck.com
# Date: 2021-09-27
# Modified: 2021-09-27

import sys, requests, os

API_URL = "https://api.vk.com/method/"
API_VERSION = "5.81"
METHOD_NAME = "photos.get"                # https://vk.com/dev/photos.get
OWNER_ID = str(sys.argv[1])               # Your VK ID
ACCESS_TOKEN = str(sys.argv[2])           # https://vk.com/dev/first_guide, https://vk.com/dev/implicit_flow_user
ALBUM_ID = "-15"                          # https://vk.com/dev/photos.get
PHOTO_SIZES = "1"                         # https://vk.com/dev/objects/photo_sizes
PHOTO_TYPES = ['w', 'z', 'y', 'x']        # https://vk.com/dev/objects/photo_sizes
REV = "1"                                 # https://vk.com/dev/photos.get start from last
COUNT = "1000"                              # https://vk.com/dev/photos.get
PICTURES_DIR = "./pictures/"

def usage():
    if len(sys.argv) == 1:
        print('Usage:',  str(sys.argv[0]), 'OWNER_ID', 'ACCESS_TOKEN')
        sys.exit(1)

def get_photos_list(offset):
    photos_list = requests.get(API_URL + METHOD_NAME +
                              '?' + 'owner_id=' + OWNER_ID +
                              '&v=' + API_VERSION +
                              '&access_token=' + ACCESS_TOKEN +
                              '&album_id=' + ALBUM_ID +
                              '&photo_sizes=' + PHOTO_SIZES +
                              '&rev=' + REV +
                              '&count=' + COUNT +
                              '&offset=' + str(offset)).json()
    return photos_list

def main():
    usage()
    offset = 0                              # https://vk.com/dev/photos.get
    print('Offset:', offset)
    os.makedirs(PICTURES_DIR, exist_ok=True)
    photos_list = get_photos_list(offset)
    while photos_list['response']['items'] != []:
        photo_url_list = []
        for photo in photos_list['response']['items']:
            exitFlag = False
            for type in PHOTO_TYPES:
                for size in photo['sizes']:
                    if size['type'] == type:
                        photo_url_list.append(size['url'])
                        exitFlag = True
                        break
                if exitFlag == True:
                    break
        for url in photo_url_list:
            file_name = url.split('/')[-1].split('?')[0]
            if os.path.exists(PICTURES_DIR + file_name):
                break
            with open(PICTURES_DIR + file_name, 'wb') as photo:
                photo.write(requests.get(url).content)
        offset += 1
        print('Offset:', offset)
        photos_list = get_photos_list(offset)

if __name__ == "__main__":
    main()
