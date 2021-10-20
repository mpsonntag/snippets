### Using the Python `unittest` package

pytest supports the `unittest` package that gives many many additional options to write sophisticated tests.

Some of the nice features:
- gain more sophisticated `asserts`, test exceptions raised
- while writing code, run only specific tests
- set up specific conditions before every test
- clean up after every test

Lets update our example again:

```
touch test/test_unittest_example.py
```

`test_unittest_example.py` content:

```
import unittest

import testlint


class TestUtilAddYourself(unittest.TestCase):
    def setUp(self):
        self.setupvar = 2

    def test_add_yourself_success(self):
        self.assertEqual(testlint.util.add_yourself(self.setupvar), 4)

    def test_add_yourself_fail(self):
        self.assertEqual(testlint.util.add_yourself(self.setupvar), 3)
```

Run all tests including all tests from this class:

```
pytest
```

Run all tests from this class only

```
pytest test/test_unittest.py::testutiladdyourself
```
<table>
<tr>
<th>Method</th>
<th>Checks that</th>
<th>New in</th>
</tr>
<tr>
<td>assertEqual(a, b)
</td>
<td>a == b</td>
<td></td>
</tr>
<tr>
<td>
    assertNotEqual(a, b)
</td>
<td>a != b</td>
<td></td>
</tr>
<tr>
<td>assertTrue(x)
</td>
<td>bool(x) is True</td>
<td></td>
</tr>
<tr>
<td>assertFalse(x)
</td>
<td>bool(x) is False</td>
<td></td>
</tr>
<tr>
<td>assertIs(a, b)
</td>
<td>a is b</td>
<td>3.1</td>
</tr>
<tr>
<td>assertIsNot(a, b)
</td>
<td>a is not b</td>
<td>3.1</td>
</tr>
<tr>
<td>assertIsNone(x)
</td>
<td>x is None</td>
<td>3.1</td>
</tr>
<tr>
<td>assertIsNotNone(x)
</td>
<td>x is not None</td>
<td>3.1</td>
</tr>
<tr>
<td>assertIn(a, b)
</td>
<td>a in b</td>
<td>3.1</td>
</tr>
<tr>
<td>assertNotIn(a, b)
</td>
<td>a not in b</td>
<td>3.1</td>
</tr>
<tr>
<td>assertIsInstance(a, b)
</td>
<td>isinstance(a, b)</td>
<td>3.2</td>
</tr>
<tr>
<td>assertNotIsInstance(a, b)
</td>
<td>not isinstance(a, b)</td>
<td>3.2</td>
</tr>
</table>


- For more details on what the `unittest` can do, check out the unittest documentation: https://docs.python.org/3/library/unittest.html
- For a list of available asserts, check here: https://docs.python.org/3/library/unittest.html#test-cases:
