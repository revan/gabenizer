"""Module handling contact with facial recognition APIs."""

import collections
import os
from typing import Dict

import requests

CLOUD_KEY = os.environ.get('CLOUD_KEY')


Face = collections.namedtuple(
    'Face',
    ('roll', 'yaw', 'vertices', 'left_eye', 'right_eye',  'mouth_left', 'mouth_right'))


class Coordinate(collections.namedtuple('Coordinate', ('x', 'y', 'z'))):

    def xy(self):
        return self.x, self.y

# Google Vision APIs return strings instead of confidences.
LIKELIHOODS = {v: i for i, v in enumerate(
    ['VERY_UNLIKELY', 'UNLIKELY', 'UNKNOWN', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY']
)}

def likelihood_at_least(value: str, threshold: str):
    return LIKELIHOODS[value] >= LIKELIHOODS[threshold]

def run_face_detect(url: str):
    face_json = _make_detect_call(url)['responses'][0]

    xyz_to_coord = lambda p: Coordinate(p['x'], p['y'], p['z'])
    get_type = lambda lm, t: next(xyz_to_coord(l['position']) for l in lm if l['type'] == t)

    return [
        Face(
            roll=fa['rollAngle'],
            yaw=fa['panAngle'],
            vertices=[Coordinate(x=v['x'], y=v['y'], z=0) for v in fa['fdBoundingPoly']['vertices']],
            left_eye=get_type(fa['landmarks'], 'LEFT_EYE'),
            right_eye=get_type(fa['landmarks'], 'RIGHT_EYE'),
            mouth_left=get_type(fa['landmarks'], 'MOUTH_LEFT'),
            mouth_right=get_type(fa['landmarks'], 'MOUTH_RIGHT'),
        )
        for fa in face_json['faceAnnotations']
        if not likelihood_at_least(fa["blurredLikelihood"], "LIKELY")
    ]


def _make_detect_call(url: str) -> Dict:
    assert CLOUD_KEY
    payload = {
                 'requests': [
                     {
                         'image': {
                             'source': {'imageUri': url}
                         },
                         'features': [{'type': 'FACE_DETECTION','maxResults': 10}],
                     }
                 ]
    }

    response = requests.post(
        'https://vision.googleapis.com/v1/images:annotate',
        json=payload,
        headers={'Authorization': 'Bearer %s' % CLOUD_KEY}
    )
    response.raise_for_status()

    return response.json()
