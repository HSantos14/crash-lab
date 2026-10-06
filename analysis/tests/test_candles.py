import pytest

from crashlab_analysis import Color, classify, classify_all


def test_green_when_reaches_target():
    assert classify(2.0, 2.0) is Color.GREEN
    assert classify(5.3, 2.0) is Color.GREEN


def test_red_when_below_target():
    assert classify(1.99, 2.0) is Color.RED
    assert classify(1.0, 2.0) is Color.RED


def test_classify_all_keeps_order():
    assert classify_all([1.2, 3.0, 1.5], 2.0) == [Color.RED, Color.GREEN, Color.RED]


@pytest.mark.parametrize("target", [1.0, 0.5, -2])
def test_invalid_target(target):
    with pytest.raises(ValueError):
        classify(2.0, target)


def test_invalid_multiplier():
    with pytest.raises(ValueError):
        classify(0.9, 2.0)
