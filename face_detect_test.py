import unittest

import api_module
import face_detect

EXPECTED_FACE = face_detect.Face(
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


class FaceDetectTest(unittest.TestCase):

    def setUp(self):
        api_module.use_mocks = True

    def test_parses_json(self):
        detector = face_detect.FaceDetect()
        returned_faces = detector.run_face_detect('unused_url')
        self.assertEqual(len(returned_faces), 1)
        self.assertEqual(returned_faces[0], EXPECTED_FACE)


if __name__ == '__main__':
    unittest.main()
