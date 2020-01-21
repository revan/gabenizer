import base64
import io
import os
from typing import Dict

import requests
from PIL import Image

import api_module

IMGUR_KEY = os.environ.get('IMGUR_KEY')

IMAGE_DESCRIPTION = 'https://reddit.com/r/gentlemangabers'


class ImageUploader:

    def upload_image(self, final: Image, title: str) -> str:
        """ Uploads an Image to imgur."""
        final_bytes = ImageUploader._image_to_base64(image=final)
        result = self.upload_bytes(encoded=final_bytes, title=title, description=IMAGE_DESCRIPTION)

        return result['data']['link']

    @staticmethod
    def _image_to_base64(image: Image) -> base64.bytes_types:
        bytes_buffer = io.BytesIO()
        image.save(bytes_buffer, format='JPEG')
        # TODO: check image size against imgur limits? Too large files will be rejected.
        return base64.b64encode(bytes_buffer.getvalue())


    @api_module.register
    def upload_bytes(self, encoded: base64.bytes_types, title: str, description: str) -> Dict:
        assert IMGUR_KEY

        dataupload = {
            'image': encoded,
            'type': 'base64',
            'title': title,
            'description': description,
        }
        url = 'https://api.imgur.com/3/image'
        headers = {'Authorization': 'Client-ID %s' % IMGUR_KEY}
        req = requests.post(url, data=dataupload, headers=headers)
        req.raise_for_status()

        return req.json()

    def mocked_upload_bytes(self, encoded: base64.bytes_types, title: str, description: str) -> Dict:
        return {
            'data': {
                'id': 'ZClFAdK',
                'title': 'Title',
                'description': 'https://reddit.com/r/gentlemangabers',
                'datetime': 1569827115,
                'type': 'image/jpeg',
                'animated': False,
                'width': 1280,
                'height': 1920,
                'size': 215749,
                'views': 0,
                'bandwidth': 0,
                'vote': None,
                'favorite': False,
                'nsfw': None,
                'section': None,
                'account_url': None,
                'account_id': 0,
                'is_ad': False,
                'in_most_viral': False,
                'has_sound': False,
                'tags': [],
                'ad_type': 0,
                'ad_url': '',
                'edited': '0',
                'in_gallery': False,
                'deletehash': 'jHumAibcPBlZoVb',
                'name': '',
                'link': 'https://i.imgur.com/ZClFAdK.jpg'
            },
            'success': True,
            'status': 200
        }
