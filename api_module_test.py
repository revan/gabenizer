import unittest

import api_module


class ApiModuleTest(unittest.TestCase):

    def setUp(self):
        api_module.use_mocks = False

    def test_no_mock(self):
        class A(api_module.ApiModule):
            def initialize(self):
                pass

            def call(self, unused_a):
                return 1

        a = A()
        self.assertEqual(a.call(1), 1)

    def test_call_required(self):
        class A(api_module.ApiModule):
            def initialize(self):
                pass

        with self.assertRaises(TypeError):
            A()

    def test_mock_signature_must_match(self):
        class A(api_module.ApiModule):
            def initialize(self):
                pass

            def call(self, unused_a):
                return 1

            def mocked_call(self):
                return 2

        with self.assertRaises(AssertionError):
            A()

    def test_mock_off_by_default(self):
        class A(api_module.ApiModule):
            def initialize(self):
                pass

            def call(self):
                return 1

            def mocked_call(self):
                return 2

        self.assertEqual(A().call(), 1)

    def test_mock_opt_in(self):
        class A(api_module.ApiModule):
            def initialize(self):
                pass

            def call(self):
                return 1

            def mocked_call(self):
                return 2

        api_module.use_mocks = True

        self.assertEqual(A().call(), 2)


if __name__ == '__main__':
    unittest.main()
