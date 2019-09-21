import json
import mock
import unittest

import face_detect

JSON_RESPONSE = """{
  "responses": [
    {
      "faceAnnotations": [
        {
          "boundingPoly": {
            "vertices": [
              {
                "x": 556,
                "y": 59
              },
              {
                "x": 904,
                "y": 59
              },
              {
                "x": 904,
                "y": 464
              },
              {
                "x": 556,
                "y": 464
              }
            ]
          },
          "fdBoundingPoly": {
            "vertices": [
              {
                "x": 586,
                "y": 160
              },
              {
                "x": 849,
                "y": 160
              },
              {
                "x": 849,
                "y": 423
              },
              {
                "x": 586,
                "y": 423
              }
            ]
          },
          "landmarks": [
            {
              "type": "LEFT_EYE",
              "position": {
                "x": 663.3227,
                "y": 240.71407,
                "z": -0.00046655923
              }
            },
            {
              "type": "RIGHT_EYE",
              "position": {
                "x": 769.8674,
                "y": 243.05531,
                "z": -16.996552
              }
            },
            {
              "type": "LEFT_OF_LEFT_EYEBROW",
              "position": {
                "x": 631.4321,
                "y": 217.67667,
                "z": 14.487795
              }
            },
            {
              "type": "RIGHT_OF_LEFT_EYEBROW",
              "position": {
                "x": 687.31775,
                "y": 220.58365,
                "z": -25.22449
              }
            },
            {
              "type": "LEFT_OF_RIGHT_EYEBROW",
              "position": {
                "x": 737.8382,
                "y": 222.12057,
                "z": -33.320004
              }
            },
            {
              "type": "RIGHT_OF_RIGHT_EYEBROW",
              "position": {
                "x": 809.9754,
                "y": 225.43134,
                "z": -11.456075
              }
            },
            {
              "type": "MIDPOINT_BETWEEN_EYES",
              "position": {
                "x": 709.9058,
                "y": 240.42616,
                "z": -30.41169
              }
            },
            {
              "type": "NOSE_TIP",
              "position": {
                "x": 702.9012,
                "y": 302.47394,
                "z": -58.629253
              }
            },
            {
              "type": "UPPER_LIP",
              "position": {
                "x": 708.04175,
                "y": 342.0102,
                "z": -33.182705
              }
            },
            {
              "type": "LOWER_LIP",
              "position": {
                "x": 709.00134,
                "y": 373.034,
                "z": -24.91017
              }
            },
            {
              "type": "MOUTH_LEFT",
              "position": {
                "x": 669.7916,
                "y": 356.6787,
                "z": 1.9067118
              }
            },
            {
              "type": "MOUTH_RIGHT",
              "position": {
                "x": 756.4295,
                "y": 355.22052,
                "z": -10.647221
              }
            },
            {
              "type": "MOUTH_CENTER",
              "position": {
                "x": 708.97577,
                "y": 355.6766,
                "z": -25.090591
              }
            },
            {
              "type": "NOSE_BOTTOM_RIGHT",
              "position": {
                "x": 737.41125,
                "y": 313.6604,
                "z": -23.207363
              }
            },
            {
              "type": "NOSE_BOTTOM_LEFT",
              "position": {
                "x": 683.06256,
                "y": 314.27448,
                "z": -13.738989
              }
            },
            {
              "type": "NOSE_BOTTOM_CENTER",
              "position": {
                "x": 707.37836,
                "y": 321.35675,
                "z": -34.26255
              }
            },
            {
              "type": "LEFT_EYE_TOP_BOUNDARY",
              "position": {
                "x": 662.99347,
                "y": 236.57849,
                "z": -7.2923765
              }
            },
            {
              "type": "LEFT_EYE_RIGHT_CORNER",
              "position": {
                "x": 684.85345,
                "y": 246.36765,
                "z": -2.968449
              }
            },
            {
              "type": "LEFT_EYE_BOTTOM_BOUNDARY",
              "position": {
                "x": 661.8343,
                "y": 251.28755,
                "z": -0.570343
              }
            },
            {
              "type": "LEFT_EYE_LEFT_CORNER",
              "position": {
                "x": 644.8487,
                "y": 243.09045,
                "z": 12.795195
              }
            },
            {
              "type": "LEFT_EYE_PUPIL",
              "position": {
                "x": 661.8876,
                "y": 243.88103,
                "z": -2.462793
              }
            },
            {
              "type": "RIGHT_EYE_TOP_BOUNDARY",
              "position": {
                "x": 766.13086,
                "y": 240.09073,
                "z": -23.864216
              }
            },
            {
              "type": "RIGHT_EYE_RIGHT_CORNER",
              "position": {
                "x": 789.7249,
                "y": 247.92853,
                "z": -10.33867
              }
            },
            {
              "type": "RIGHT_EYE_BOTTOM_BOUNDARY",
              "position": {
                "x": 769.9315,
                "y": 252.81372,
                "z": -17.33489
              }
            },
            {
              "type": "RIGHT_EYE_LEFT_CORNER",
              "position": {
                "x": 744.8743,
                "y": 247.01517,
                "z": -12.873353
              }
            },
            {
              "type": "RIGHT_EYE_PUPIL",
              "position": {
                "x": 767.6582,
                "y": 247.39655,
                "z": -19.585327
              }
            },
            {
              "type": "LEFT_EYEBROW_UPPER_MIDPOINT",
              "position": {
                "x": 658.6823,
                "y": 206.54358,
                "z": -12.903436
              }
            },
            {
              "type": "RIGHT_EYEBROW_UPPER_MIDPOINT",
              "position": {
                "x": 770.6021,
                "y": 210.35391,
                "z": -30.791904
              }
            },
            {
              "type": "LEFT_EAR_TRAGION",
              "position": {
                "x": 617.4541,
                "y": 289.4087,
                "z": 139.47903
              }
            },
            {
              "type": "RIGHT_EAR_TRAGION",
              "position": {
                "x": 852.4276,
                "y": 297.1511,
                "z": 102.15734
              }
            },
            {
              "type": "FOREHEAD_GLABELLA",
              "position": {
                "x": 712.1764,
                "y": 219.9592,
                "z": -33.38018
              }
            },
            {
              "type": "CHIN_GNATHION",
              "position": {
                "x": 709.29333,
                "y": 423.03915,
                "z": -8.77119
              }
            },
            {
              "type": "CHIN_LEFT_GONION",
              "position": {
                "x": 619.99194,
                "y": 357.44647,
                "z": 97.815186
              }
            },
            {
              "type": "CHIN_RIGHT_GONION",
              "position": {
                "x": 831.5262,
                "y": 364.99774,
                "z": 63.719833
              }
            }
          ],
          "rollAngle": 1.6886017,
          "panAngle": -9.137291,
          "tiltAngle": -1.7422112,
          "detectionConfidence": 0.9999341,
          "landmarkingConfidence": 0.8033745,
          "joyLikelihood": "VERY_UNLIKELY",
          "sorrowLikelihood": "VERY_UNLIKELY",
          "angerLikelihood": "VERY_UNLIKELY",
          "surpriseLikelihood": "VERY_UNLIKELY",
          "underExposedLikelihood": "VERY_UNLIKELY",
          "blurredLikelihood": "VERY_UNLIKELY",
          "headwearLikelihood": "VERY_UNLIKELY"
        }
      ]
    }
  ]
}
"""

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

    def test_parses_json(self):
        with mock.patch.object(face_detect, '_make_detect_call') as fake_api:
            fake_api.return_value = json.loads(JSON_RESPONSE)

            returned_faces = face_detect.run_face_detect('unused_url')

            self.assertEqual(len(returned_faces), 1)

            self.assertEqual(returned_faces[0], EXPECTED_FACE)


if __name__ == '__main__':
    unittest.main()
