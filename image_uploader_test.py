import os
from PIL import Image
import unittest

import api_module
import image_uploader

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'testdata', 'in.jpg')

class ImageUploaderTest(unittest.TestCase):

    def setUp(self):
        api_module.use_mocks = True

    def test_parses_json(self):
        img = Image.open(INPUT_FILE)

        uploader = image_uploader.ImageUploader()
        url = uploader.upload_image(img, 'Title')
        self.assertEqual(url, 'https://i.imgur.com/ZClFAdK.jpg')


if __name__ == '__main__':
    unittest.main()
