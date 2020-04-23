import unittest
import warnings

from os import path


def formatted_warnings(msg, category=None, *args, **kwargs):
    final_msg = "%s\n" % str(msg)
    if category:
        final_msg = "%s: %s" % (category.__name__, final_msg)

    return final_msg


class TestUnitTestClass(unittest.TestCase):
    def setUp(self):
        print("set up")
        core_name = path.basename(path.splitext(__file__)[0])
        print("File: %s" % core_name)
        self.warnings = warnings
        self.warnings.formatwarning = formatted_warnings

    def tearDown(self):
        print("tear down")

    def test_some_func(self):
        print("test some func")

    def test_some_method(self):
        print("test some method")

    def test_deprecation_warning(self):
        self.warnings.warn("Method deprecated", DeprecationWarning)
        # warnings.simplefilter("ignore")
        self.warnings.warn("Some other stuff", DeprecationWarning)


if __name__ == "__main__":
    unittest.main()
