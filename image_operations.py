"""Functions for modifying images."""

import os
from typing import List

import numpy as np
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

    get_coords = lambda face: [c.xy() for c in [face.left_eye, face.right_eye, face.mouth_left, face.mouth_right]]
    donor_coords = get_coords(donor_face)
    recipient_coords = get_coords(recipient_face)
    coefficients = _find_coeffs(recipient_coords, donor_coords)

    warped_donor = donor_image.transform(
        recipient_image.size, Image.PERSPECTIVE, coefficients, Image.BICUBIC)

    working_recipient = recipient_image.copy()
    working_recipient.paste(warped_donor, (0, 0), warped_donor)

    return working_recipient


# Adapted from https://stackoverflow.com/questions/14177744/how-does-perspective-transformation-work-in-pil.
def _find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = np.array(matrix, dtype=np.float)
    B = np.array(pb).reshape(8)

    res = np.dot(np.linalg.inv(A.T @ A) @ A.T, B)
    return np.array(res).reshape(8)
