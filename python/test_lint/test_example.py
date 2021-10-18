def i_am_ignored():
    assert "a" == "b"


def test_i_am_included_success():
    assert 1 == 1


def test_i_am_included_fail():
    assert 1 == 2
