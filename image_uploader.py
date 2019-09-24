import base64
import io
import os
from typing import Dict

import requests
from PIL import Image

IMGUR_KEY = os.environ.get('IMGUR_KEY')

IMAGE_DESCRIPTION = 'https://reddit.com/r/gentlemangabers'


def upload_image(final: Image, title: str) -> str:
    """ Uploads an Image to imgur."""
    final_bytes = _image_to_base64(image=final)
    result = _make_upload_call(encoded=final_bytes, title=title, description=IMAGE_DESCRIPTION)

    return result['data']['link']


def _image_to_base64(image: Image) -> base64.bytes_types:
    bytes_buffer = io.BytesIO()
    image.save(bytes_buffer, format='PNG')
    return base64.b64encode(bytes_buffer.getvalue())


def _make_upload_call(encoded: base64.bytes_types, title: str, description: str) -> Dict:
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
