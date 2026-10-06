from crashlab_analysis import Color, sequence_stats

G, R = Color.GREEN, Color.RED


def test_empty():
    s = sequence_stats([])
    assert s.current_color is None and s.current_length == 0
    assert s.max_green == 0 and s.max_red == 0


def test_current_and_max_runs():
    s = sequence_stats([G, G, R, R, R, G, R, R])
    assert s.current_color is R and s.current_length == 2
    assert s.max_green == 2 and s.max_red == 3


def test_distribution_counts_runs_including_current():
    s = sequence_stats([R, R, G, R, R, R, R])
    assert s.distribution[R] == {2: 1, 4: 1}
    assert s.distribution[G] == {1: 1}


def test_single_color():
    s = sequence_stats([G, G, G])
    assert s.current_length == 3 and s.max_green == 3 and s.max_red == 0
