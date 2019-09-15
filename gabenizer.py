#!/bin/python3
import requests
import time
import urllib
from io import StringIO
import os
from pprint import pprint
from PIL import Image, ImageStat

import image_operations
import face_detect

IMGUR_KEY = os.environ['IMGUR_KEY']
IMGUR_DELETE = os.environ['IMGUR_DELETE']


def process_image(url, gaben_path):
    """ The core of the application. Takes a URL, returns a processed image. """

    faces = face_detect.run_face_detect(url)
    original = Image.open(StringIO(urllib.urlopen(url).read()))

    image_operations.create_before_and_after(
        recipient_faces=faces,
        recipient_image=original
    )


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
    print(imgururl)

    return imgururl

