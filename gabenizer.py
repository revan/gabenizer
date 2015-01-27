#!/bin/python2
import unirest
import requests
import time
import urllib
import cStringIO
import os
from pprint import pprint
from PIL import Image, ImageStat

SKYBIO_ID = os.environ['SKYBIO_ID']
SKYBIO_SECRET = os.environ['SKYBIO_SECRET']
IMGUR_KEY = os.environ['IMGUR_KEY']
IMGUR_DELETE = os.environ['IMGUR_DELETE']


def process_image(url, gaben_path):
    """ The core of the application. Takes a URL, returns a processed image. """

    # detect face, get x,y
    response = unirest.get('http://api.skybiometry.com/fc/faces/detect.json'
        + '?api_key='+SKYBIO_ID
        + '&api_secret='+SKYBIO_SECRET
        + '&detector=aggressive'
        + '&attributes=none'
        + '&urls='+url)
    pprint(vars(response))

    photos = response.body['photos']
    for photo in photos:
        original = Image.open(cStringIO.StringIO(urllib.urlopen(url).read()))
        gabenized = original.copy()
        if not photo['tags']:
            continue
        unprocessed = True
        for face in photo['tags']:
            # get image values
            original_roll = face['roll']
            original_yaw = face['yaw']
            original_center_x = face['center']['x']
            original_center_y = face['center']['y']
            original_size = face['width']
            original_height = photo['height']
            original_width = photo['width']

            # if yaw is too great, skip
            MAX_YAW = 30
            if abs(original_yaw) > MAX_YAW:
                continue

            # hardcoded values for gabenface
            gaben_roll = -1
            gaben_center_x = 51.24
            gaben_center_y = 47.53
            gaben_size = 67.15
            gaben_height = 465
            gaben_width = 484

            # calculate values for scale and position
            scale = (original_size * original_width) / (gaben_size * gaben_width)
            scale_height = gaben_height * scale
            scale_width = gaben_width * scale
            place_x = (0.01 * original_center_x * original_width) - (0.01 * gaben_center_x * scale_width)
            place_y = (0.01 * original_center_y * original_height) - (0.01 * gaben_center_y * scale_height)

            print scale
            print scale_height
            print scale_width
            print place_x
            print place_y

            # open image
            gaben = Image.open(gaben_path)

            # rotate gaben to match roll
            gaben = gaben.rotate(int(-1*original_roll))

            # resize gaben
            gaben = gaben.resize((int(scale_width), int(scale_height)))

            gabenized.paste(gaben, (int(place_x), int(place_y)), gaben)
            unprocessed = False
        if unprocessed:
            continue

        # arrange both images
        final = Image.new("RGB", (original_width * 2, original_height))
        final.paste(original, (0,0))
        final.paste(gabenized, (original_width, 0))

        # if original image was grayscale, convert final
        COLOR_CUTOFF = 100
        colors = ImageStat.Stat(original).var
        if len(colors) == 3 and abs(max(colors) - min(colors)) < COLOR_CUTOFF:
            final = final.convert('L')

        return final


def imgur_upload(final, filepath, filename, title, URL_STATIC):
    """ Uploads a locally hosted image to imgur.
        TODO: upload the file directly. """
    # save image
    fullpath = os.path.join(filepath, filename)
    final.save(fullpath)

    # upload to imgur
    dataupload = {
        'image': URL_STATIC + filename,
        'type': 'URL',
        'name': filename,
        'title': title,
        'album': IMGUR_DELETE
    }
    url = 'https://api.imgur.com/3/image'
    headers = {'Authorization': 'Client-ID ' + IMGUR_KEY}
    req = requests.post(url, data=dataupload, headers=headers)
    imgururl = req.json()['data']['link']
    print imgururl

    return imgururl

