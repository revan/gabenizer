import json
import mock
import unittest

import face_detect

JSON_RESPONSE = """{"status": "success",
 "photos": [{"url": "https://i.imgur.com/zKy6YLx.jpg",
   "pid": "F@063bcf2a7f51a2141b85b3f55471e955_71baa0f4ee08f",
   "width": 1280,
   "height": 1920,
   "tags": [{"uids": [],
     "label": null,
     "confirmed": false,
     "manual": false,
     "width": 18.91,
     "height": 11.46,
     "yaw": 8,
     "roll": 0,
     "pitch": -18,
     "attributes": {"face": {"value": "true", "confidence": 81}},
     "points": null,
     "similarities": null,
     "tid": "TEMP_F@063bcf2a7f51a2141b85b3f502da0140_71baa0f4ee08f_57.03_16.67_0_1",
     "recognizable": true,
     "center": {"x": 57.03, "y": 16.67},
     "eye_left": {"x": 60.31, "y": 12.81, "confidence": 98, "id": 449},
     "eye_right": {"x": 51.72, "y": 12.71, "confidence": 97, "id": 450},
     "mouth_center": {"x": 55.7, "y": 18.65, "confidence": 96, "id": 615},
     "nose": {"x": 55.08, "y": 15.83, "confidence": 97, "id": 403}}]}],
 "usage": {"used": 2,
  "remaining": 98,
  "limit": 100,
  "reset_time": 1568517042,
  "reset_time_text": "Sun, 15 September 2019 03:10:42 +0000"},
 "operation_id": "a736fc67645b46b4a697e11e4cee9e4d"}
"""


class FaceDetectTest(unittest.TestCase):

    def test_parses_json(self):
        with mock.patch.object(face_detect, '_make_detect_call') as fake_api:
            fake_api.return_value = json.loads(JSON_RESPONSE)

            returned_faces = face_detect.run_face_detect('unused_url')

            self.assertListEqual(
                returned_faces,
                [face_detect.Face(roll=0, yaw=8, center_x=57.03, center_y=16.67, size=18.91, height=1920, width=1280)]
            )


if __name__ == '__main__':
    unittest.main()
