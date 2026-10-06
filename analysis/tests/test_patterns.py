import pytest

from crashlab_analysis import (
    Color,
    PatternRule,
    evaluate_rule,
    should_enter,
    wilson_interval,
)

# alvo 2.0: abaixo de 2.0 é vermelha
RULE = PatternRule(prior_count=2, prior_color=Color.RED, next_min=1.6)


def test_rule_validation():
    with pytest.raises(ValueError):
        PatternRule(0, Color.RED, 1.6)
    with pytest.raises(ValueError):
        PatternRule(2, Color.RED, 0.9)


def test_counts_occurrences_and_hits():
    # R R -> 1.7 (acerto), R R -> 1.2 (erro)
    history = [1.1, 1.3, 1.7, 3.0, 1.1, 1.4, 1.2]
    # i=2: [1.1,1.3] RR -> 1.7>=1.6 acerto
    # i=3: [1.3,1.7] RR -> 3.0 acerto
    # i=4: [1.7,3.0] não
    # i=5: [3.0,1.1] não
    # i=6: [1.1,1.4] RR -> 1.2 erro
    r = evaluate_rule(history, 2.0, RULE)
    assert (r.occurrences, r.hits) == (3, 2)
    assert r.hit_rate == pytest.approx(2 / 3)


def test_no_occurrences():
    r = evaluate_rule([3.0, 4.0, 5.0], 2.0, RULE)
    assert r.occurrences == 0 and r.hit_rate is None
    assert r.confidence_interval is None


def test_break_even_rate():
    r = evaluate_rule([1.1, 1.2, 2.0], 2.0, RULE)
    assert r.break_even_rate == pytest.approx(1 / 1.6)


def test_wilson_interval_bounds():
    low, high = wilson_interval(6, 10)
    assert 0 <= low < 0.6 < high <= 1
    assert wilson_interval(0, 0) is None
    low, high = wilson_interval(10, 10)
    assert high == pytest.approx(1.0) and low < 1.0


def test_should_enter_true():
    history = [1.1, 1.3, 2.5] * 5 + [1.1, 1.2]  # termina com RR; 2.5 é acerto
    d = should_enter(history, 2.0, RULE, min_occurrences=3, min_hit_rate=0.5)
    assert d.should_enter is True


def test_should_enter_pattern_inactive():
    d = should_enter([1.1, 1.3, 3.0], 2.0, RULE, min_occurrences=0)
    assert d.should_enter is False and "não está ativo" in d.reason


def test_should_enter_short_history():
    d = should_enter([1.1], 2.0, RULE)
    assert d.should_enter is False


def test_should_enter_small_sample():
    history = [1.1, 1.3, 1.7, 1.1, 1.2]
    d = should_enter(history, 2.0, RULE, min_occurrences=10)
    assert d.should_enter is False and "amostra pequena" in d.reason


def test_should_enter_low_hit_rate():
    history = [1.1, 1.3, 1.2] * 5 + [1.1, 1.2]  # sempre erra depois de RR
    d = should_enter(history, 2.0, RULE, min_occurrences=3, min_hit_rate=0.5)
    assert d.should_enter is False and "abaixo do mínimo" in d.reason
