import os
from PIL import Image, ImageChops
import unittest

import face_detect
import image_operations


INPUT_FILE = os.path.join(os.path.dirname(__file__), 'testdata', 'in.jpg')
SINGLE_PANEL_FILE = os.path.join(os.path.dirname(__file__), 'testdata', 'single.png')
BEFORE_AFTER_FILE = os.path.join(os.path.dirname(__file__), 'testdata', 'double.png')
TMP_DIR = '/tmp/image_test_out'


class ImageOperationsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            os.mkdir(TMP_DIR)
        except FileExistsError:
            pass

    def setUp(self):
        self.input_image = Image.open(INPUT_FILE)
        self.input_faces = [
            face_detect.Face(roll=0, yaw=8, center_x=57.03, center_y=16.67, size=18.91, height=1920, width=1280)
        ]

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
        self.assertFalse(diff.getbbox())



if __name__ == '__main__':
    unittest.main()
