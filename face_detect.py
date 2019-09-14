"""Module handling contact with facial recognition APIs."""

import os
import requests

SKYBIO_ID = os.environ['SKYBIO_ID']
SKYBIO_SECRET = os.environ['SKYBIO_SECRET']

def run_face_detect(url):
    response = requests.get(
        'http://api.skybiometry.com/fc/faces/detect.json'
        + '?api_key=%s&api_secret=%s&detector=aggressive&attributes=none&urls=%s' % (SKYBIO_ID, SKYBIO_SECRET, url))
    response.raise_for_status()

    return response.json()['photos'][0]
