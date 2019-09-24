#!/bin/python3
import requests
import urllib
from io import StringIO
import os
from PIL import Image

import image_operations
import face_detect


def process_image(url, gaben_path):
    """ The core of the application. Takes a URL, returns a processed image. """

    faces = face_detect.run_face_detect(url)
    original = Image.open(StringIO(urllib.urlopen(url).read()))

    image_operations.create_before_and_after(
        recipient_faces=faces,
        recipient_image=original
    )
