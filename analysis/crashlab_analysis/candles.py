"""Classificação de velas: verde ou vermelha conforme o alvo de cashout."""
from __future__ import annotations

from collections.abc import Iterable
from enum import Enum


class Color(str, Enum):
    GREEN = "green"  # multiplicador final >= alvo
    RED = "red"      # multiplicador final < alvo


def validate_target(target: float) -> None:
    if target <= 1.0:
        raise ValueError("o alvo de cashout deve ser maior que 1.0")


def validate_multiplier(multiplier: float) -> None:
    if multiplier < 1.0:
        raise ValueError(f"multiplicador inválido: {multiplier} (mínimo 1.0)")


def classify(multiplier: float, target: float) -> Color:
    """Verde se o multiplicador final atingiu o alvo, vermelha caso contrário."""
    validate_target(target)
    validate_multiplier(multiplier)
    return Color.GREEN if multiplier >= target else Color.RED


def classify_all(multipliers: Iterable[float], target: float) -> list[Color]:
    return [classify(m, target) for m in multipliers]
