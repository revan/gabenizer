import urllib.request
import io
from PIL import Image

import image_uploader
import image_operations
import face_detect

detector = face_detect.FaceDetect()
uploader = image_uploader.ImageUploader()


def process_image(url: str, title: str) -> str:
    """For image at URL, returns URL of processed image."""
    faces = detector.run_face_detect(url)
    original = Image.open(io.BytesIO(urllib.request.urlopen(url).read()))

    processed = image_operations.create_before_and_after(
        recipient_faces=faces,
        recipient_image=original
    )
    uploaded_url = uploader.upload_image(processed, title=title)
    return uploaded_url

