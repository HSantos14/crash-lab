import pytest

from crashlab_analysis import window_stats


def test_counts_and_percentages():
    stats = window_stats([1.1, 2.5, 3.0, 1.5], target=2.0)
    assert (stats.total, stats.greens, stats.reds) == (4, 2, 2)
    assert stats.green_pct == 50.0
    assert stats.red_pct == 50.0


def test_only_last_n_candles_are_used():
    stats = window_stats([5.0] * 10 + [1.1] * 3, target=2.0, size=3)
    assert (stats.total, stats.greens, stats.reds) == (3, 0, 3)


def test_window_smaller_than_size():
    assert window_stats([2.0, 1.0], target=2.0, size=100).total == 2


def test_empty_history():
    stats = window_stats([], target=2.0)
    assert stats.total == 0 and stats.green_pct == 0.0 and stats.red_pct == 0.0


def test_invalid_size():
    with pytest.raises(ValueError):
        window_stats([2.0], target=2.0, size=0)
