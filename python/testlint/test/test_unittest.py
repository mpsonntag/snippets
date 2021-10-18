import unittest

import testlint


class testutiladdyourself(unittest.TestCase):
    def setUp(self):
        self.setupvar = 2

    def test_add_yourself_success(self):
        self.assertEqual(testlint.util.add_yourself(self.setupvar), 4)

    def test_add_yourself_fail(self):
        self.assertEqual(testlint.util.add_yourself(self.setupvar), 3)
