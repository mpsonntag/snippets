def add_up(a, b):
    return a + b


def test_add_up_succeed():
    assert add_up(1, 2) == 3


def test_add_up_fail():
    assert add_up(1, 2) == 4


def ignore_me():
    assert "I will be" == "completely ignored"
