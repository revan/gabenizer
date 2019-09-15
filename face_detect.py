"""Module handling contact with facial recognition APIs."""

import collections
import os
import requests

SKYBIO_ID = os.environ.get('SKYBIO_ID')
SKYBIO_SECRET = os.environ.get('SKYBIO_SECRET')


Face = collections.namedtuple('Face', ('roll', 'yaw', 'center_x', 'center_y', 'size', 'height', 'width'))


def run_face_detect(url: str):
    face_json = _make_detect_call(url)['photos'][0]

    return [
        Face(
            roll=t['roll'],
            yaw=t['yaw'],
            center_x=t['center']['x'],
            center_y=t['center']['y'],
            size=t['width'],
            height=face_json['height'],
            width=face_json['width'],
    )
        for t in face_json['tags']
    ]


def _make_detect_call(url: str):
    assert SKYBIO_ID and SKYBIO_SECRET

    response = requests.get(
        'http://api.skybiometry.com/fc/faces/detect.json'
        + '?api_key=%s&api_secret=%s&detector=aggressive&attributes=none&urls=%s' % (SKYBIO_ID, SKYBIO_SECRET, url))
    response.raise_for_status()

    return response.json()
