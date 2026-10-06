"""Regras de padrão: "após N velas da cor X, a próxima foi >= Y?".

Importante: este módulo mede o que ACONTECEU no histórico. Não prevê a próxima vela.
Cada rodada de um jogo crash é independente, então use o resultado como informação
de risco, nunca como garantia.
"""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from math import sqrt

from .candles import Color, classify_all


@dataclass(frozen=True)
class PatternRule:
    prior_count: int   # N: quantas velas seguidas formam o gatilho
    prior_color: Color  # X: cor dessas velas
    next_min: float    # Y: multiplicador mínimo da vela seguinte para contar como acerto

    def __post_init__(self) -> None:
        if self.prior_count < 1:
            raise ValueError("prior_count deve ser >= 1")
        if self.next_min < 1.0:
            raise ValueError("next_min deve ser >= 1.0")


@dataclass(frozen=True)
class PatternResult:
    occurrences: int
    hits: int
    next_min: float

    @property
    def hit_rate(self) -> float | None:
        return self.hits / self.occurrences if self.occurrences else None

    @property
    def confidence_interval(self) -> tuple[float, float] | None:
        return wilson_interval(self.hits, self.occurrences)

    @property
    def break_even_rate(self) -> float:
        """Taxa de acerto necessária para empatar ao sair em `next_min`: 1 / Y."""
        return 1.0 / self.next_min


@dataclass(frozen=True)
class EntryDecision:
    should_enter: bool
    reason: str
    result: PatternResult


def wilson_interval(hits: int, n: int, z: float = 1.96) -> tuple[float, float] | None:
    """Intervalo de confiança de Wilson (95% por padrão) para uma proporção."""
    if n == 0:
        return None
    p = hits / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def evaluate_rule(multipliers: Iterable[float], target: float, rule: PatternRule) -> PatternResult:
    """Conta quantas vezes o gatilho ocorreu no histórico e quantas vezes a vela seguinte
    atingiu `rule.next_min`. Ocorrências sobrepostas são contadas separadamente."""
    mults = list(multipliers)
    colors = classify_all(mults, target)
    n = rule.prior_count
    occurrences = hits = 0
    for i in range(n, len(mults)):
        if all(c is rule.prior_color for c in colors[i - n:i]):
            occurrences += 1
            if mults[i] >= rule.next_min:
                hits += 1
    return PatternResult(occurrences=occurrences, hits=hits, next_min=rule.next_min)


def should_enter(
    multipliers: Iterable[float],
    target: float,
    rule: PatternRule,
    min_occurrences: int = 10,
    min_hit_rate: float = 0.0,
) -> EntryDecision:
    """Decide se o gatilho está ativo agora e se o histórico atende aos mínimos do usuário."""
    mults = list(multipliers)
    result = evaluate_rule(mults, target, rule)
    n = rule.prior_count

    tail = classify_all(mults[-n:], target) if len(mults) >= n else []
    if len(tail) < n or not all(c is rule.prior_color for c in tail):
        return EntryDecision(False, "padrão não está ativo agora", result)
    if result.occurrences < min_occurrences:
        return EntryDecision(False, "amostra pequena: poucas ocorrências no histórico", result)
    rate = result.hit_rate or 0.0
    if rate < min_hit_rate:
        return EntryDecision(False, "taxa de acerto histórica abaixo do mínimo configurado", result)
    return EntryDecision(True, "padrão ativo e histórico dentro dos mínimos", result)
