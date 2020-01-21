import unittest

import api_module


class ApiModuleTest(unittest.TestCase):

    def setUp(self):
        api_module.use_mocks = False

    def test_mock_signature_must_match(self):
        class A(object):
            def initialize(self):
                pass

            @api_module.register
            def call(self, unused_a):
                return 1

            def mocked_call(self):
                return 2

        api_module.use_mocks = True
        a = A()

        with self.assertRaises(AssertionError):
            a.call()

    def test_mock_off_by_default(self):
        class A(object):
            def initialize(self):
                pass

            @api_module.register
            def call(self):
                return 1

            def mocked_call(self):
                return 2

        self.assertEqual(A().call(), 1)

    def test_mock_opt_in(self):
        class A(object):
            def initialize(self):
                pass

            @api_module.register
            def call(self):
                return 1

            def mocked_call(self):
                return 2

        api_module.use_mocks = True

        self.assertEqual(A().call(), 2)


if __name__ == '__main__':
    unittest.main()
