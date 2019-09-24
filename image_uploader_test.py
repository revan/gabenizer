import os
from PIL import Image
import json
import mock

import unittest

import image_uploader

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'testdata', 'in.jpg')

JSON_RESPONSE = """{
    "data": {
        "id": "Buv9Bmm",
        "title": "Title",
        "description": "https://reddit.com/r/gentlemangabers",
        "datetime": 1569306724,
        "type": "image/jpeg",
        "animated": false,
        "width": 1280,
        "height": 1920,
        "size": 215749,
        "views": 0,
        "bandwidth": 0,
        "vote": null,
        "favorite": false,
        "nsfw": null,
        "section": null,
        "account_url": null,
        "account_id": 0,
        "is_ad": false,
        "in_most_viral": false,
        "has_sound": false,
        "tags": [],
        "ad_type": 0,
        "ad_url": "",
        "edited": "0",
        "in_gallery": false,
        "deletehash": "zTv7m2WUB22XgCD",
        "name": "",
        "link": "https://i.imgur.com/Buv9Bmm.jpg"
    },
    "success": true,
    "status": 200
}
"""


class ImageUploaderTest(unittest.TestCase):

    def test_parses_json(self):
        img = Image.open(INPUT_FILE)

        with mock.patch.object(image_uploader, '_make_upload_call') as fake_api:
            fake_api.return_value = json.loads(JSON_RESPONSE)

            url = image_uploader.upload_image(img, 'Title')

            self.assertEqual(url, 'https://i.imgur.com/Buv9Bmm.jpg')


if __name__ == '__main__':
    unittest.main()
