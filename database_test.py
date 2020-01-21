import datetime
import unittest.mock

import api_module
import database


_FIXED_DATETIME = datetime.datetime.now()


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        api_module.use_mocks = True

    def test_contains(self):
        db = database.Database()
        self.assertTrue(
            db.contains('https://i.imgur.com/ZClFAdK.jpg')
        )

    @unittest.mock.patch('datetime.datetime')
    def test_record_post(self, mock_dt):
        mock_dt.now.return_value = _FIXED_DATETIME

        db = database.Database()
        record = db.record_post(
            source_url='https://i.imgur.com/source.jpg',
            uploaded_url='https://i.imgur.com/upload.jpg'
        )

        self.assertEqual(
            record,
            database.Record(
                source_url='https://i.imgur.com/source.jpg',
                uploaded_url='https://i.imgur.com/upload.jpg',
                success=True,
                date=_FIXED_DATETIME
            )
        )

    @unittest.mock.patch('datetime.datetime')
    def test_record_failure(self, mock_dt):
        mock_dt.now.return_value = _FIXED_DATETIME

        db = database.Database()
        record = db.record_failure('https://i.imgur.com/failed.png')

        self.assertEqual(
            record,
            database.Record(
                source_url='https://i.imgur.com/failed.png',
                uploaded_url='',
                success=False,
                date=_FIXED_DATETIME
            )
        )


if __name__ == '__main__':
    unittest.main()
