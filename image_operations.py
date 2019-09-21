"""Functions for modifying images."""

import os
from typing import List

from PIL import Image, ImageStat
import face_detect


GABEN_FACE = face_detect.Face(
    roll=0.06490052, yaw=1.1396244,
    vertices=[
        face_detect.Coordinate(34, 9, 0),
        face_detect.Coordinate(455, 9, 0),
        face_detect.Coordinate(455, 430, 0),
        face_detect.Coordinate(34, 430, 0)
    ],
    left_eye=face_detect.Coordinate(149.74083, 144.1833, 0.0023378613),
    right_eye=face_detect.Coordinate(337.4488, 145.49677, 3.5483594),
    mouth_left=face_detect.Coordinate(181.15941, 329.88702, 1.5182021),
    mouth_right=face_detect.Coordinate(326.6459, 329.2062, 8.069958)
)
GABEN_FILE = os.path.join(os.path.dirname(__file__), 'gabenface.png')
GABEN_IMAGE = Image.open(GABEN_FILE)

COLOR_CUTOFF = 100


def create_before_and_after(
        recipient_faces: List[face_detect.Face],
        recipient_image: Image,
        donor_face: face_detect.Face = GABEN_FACE,
        donor_image: Image = GABEN_IMAGE):

    after_image = recipient_image

    assert len(recipient_faces) > 0
    for recipient_face in recipient_faces:
        after_image = _paste_donor_on_recipient(recipient_face, after_image, donor_face, donor_image)

    width, height = recipient_image.size
    final = Image.new("RGB", (width * 2, height))
    final.paste(recipient_image, (0, 0))
    final.paste(after_image, (width, 0))

    # if original image was grayscale, convert final
    colors = ImageStat.Stat(recipient_image).var
    if len(colors) == 3 and abs(max(colors) - min(colors)) < COLOR_CUTOFF:
        final = final.convert('L')

    return final


def _paste_donor_on_recipient(
        recipient_face: face_detect.Face,
        recipient_image: Image,
        donor_face: face_detect.Face,
        donor_image: Image):

    # TODO: rewrite with like, math and stuff
    return recipient_image

