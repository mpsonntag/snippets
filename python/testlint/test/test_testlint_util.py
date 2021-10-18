import testlint


def test_add_yourself_success():
    assert testlint.util.add_yourself(1) == 2


def test_add_yourself_fail():
    assert testlint.util.add_yourself(1) == 3
