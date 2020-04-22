import unittest


class TestUnitTestClass(unittest.TestCase):
    def setUp(self):
        print("set up")

    def tearDown(self):
        print("tear down")

    def test_some_func(self):
        print("test some func")

    def test_some_method(self):
        print("test some method")


if __name__ == "__main__":
    unittest.main()
