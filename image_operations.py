"""Functions for modifying images."""

import os
from typing import List

from PIL import Image, ImageStat
import face_detect


GABEN_FACE = face_detect.Face(roll=0, yaw=2, center_x=52.27, center_y=54.84, size=76.65, height=465, width=484)
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

    final = Image.new("RGB", (recipient_face.width * 2, recipient_face.height))
    final.paste(recipient_image, (0, 0))
    final.paste(after_image, (recipient_face.width, 0))

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
    # calculate values for scale and position
    scale = (recipient_face.size * recipient_face.width) / (donor_face.size * donor_face.width)
    scale_height = donor_face.height * scale
    scale_width = donor_face.width * scale
    place_x = (0.01 * recipient_face.center_x * recipient_face.width) - (0.01 * donor_face.center_x * scale_width)
    place_y = (0.01 * recipient_face.center_y * recipient_face.height) - (0.01 * donor_face.center_y * scale_height)

    working_donor = donor_image.rotate(int(-1 * recipient_face.roll))
    working_donor = working_donor.resize((int(scale_width), int(scale_height)))

    working_recipient = recipient_image.copy()
    working_recipient.paste(working_donor, (int(place_x), int(place_y)), working_donor)

    return working_recipient

