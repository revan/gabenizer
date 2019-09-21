import os
from PIL import Image, ImageChops
import unittest

import face_detect
import image_operations


INPUT_FILE = os.path.join(os.path.dirname(__file__), 'testdata', 'in.jpg')
SINGLE_PANEL_FILE = os.path.join(os.path.dirname(__file__), 'testdata', 'single.png')
BEFORE_AFTER_FILE = os.path.join(os.path.dirname(__file__), 'testdata', 'double.png')
TMP_DIR = '/tmp/image_test_out'

RECIPIENT_FACE = face_detect.Face(
    roll=1.6886017, yaw=-9.137291,
    vertices=[
        face_detect.Coordinate(586, 160, 0),
        face_detect.Coordinate(849, 160, 0),
        face_detect.Coordinate(849, 423, 0),
        face_detect.Coordinate(586, 423, 0)
    ],
    left_eye=face_detect.Coordinate(663.3227, 240.71407, -0.00046655923),
    right_eye=face_detect.Coordinate(769.8674, 243.05531, -16.996552),
    mouth_left=face_detect.Coordinate(669.7916, 356.6787, 1.9067118),
    mouth_right=face_detect.Coordinate(756.4295, 355.22052, -10.647221)
)

class ImageOperationsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            os.mkdir(TMP_DIR)
        except FileExistsError:
            pass

    def setUp(self):
        self.input_image = Image.open(INPUT_FILE)
        self.input_faces = [RECIPIENT_FACE]

    def test_pasting_donor(self):
        pasted = image_operations._paste_donor_on_recipient(
            recipient_face=self.input_faces[0],
            recipient_image=self.input_image,
            donor_face=image_operations.GABEN_FACE,
            donor_image=image_operations.GABEN_IMAGE,
        )
        outfile = os.path.join(TMP_DIR, 'single_out.png')
        pasted.save(outfile)
        print('Single panel saved to ', outfile)

        self._assertImagesEqual(pasted, Image.open(SINGLE_PANEL_FILE))

    def test_before_after(self):
        before_after = image_operations.create_before_and_after(
            recipient_faces=self.input_faces,
            recipient_image=self.input_image
        )

        outfile = os.path.join(TMP_DIR, 'double.png')
        before_after.save(outfile)
        print('Before and after saved to ', outfile)

        self._assertImagesEqual(before_after, Image.open(BEFORE_AFTER_FILE))

    def _assertImagesEqual(self, new, expect):
        diff = ImageChops.difference(new, expect)
        self.assertFalse(diff.getbbox(), 'Images differ!')


if __name__ == '__main__':
    unittest.main()
