"""Sequências (corridas) de velas da mesma cor."""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from .candles import Color


@dataclass(frozen=True)
class SequenceStats:
    current_color: Color | None
    current_length: int
    max_green: int
    max_red: int
    # distribution[cor][tamanho] = quantas sequências desse tamanho ocorreram
    # (a sequência em andamento no fim da lista também é contada)
    distribution: dict[Color, dict[int, int]]


def sequence_stats(colors: Sequence[Color]) -> SequenceStats:
    runs: list[list] = []  # cada item: [cor, tamanho]
    for color in colors:
        if runs and runs[-1][0] is color:
            runs[-1][1] += 1
        else:
            runs.append([color, 1])

    distribution: dict[Color, dict[int, int]] = {Color.GREEN: {}, Color.RED: {}}
    for color, length in runs:
        distribution[color][length] = distribution[color].get(length, 0) + 1

    def longest(color: Color) -> int:
        return max(distribution[color], default=0)

    current_color = runs[-1][0] if runs else None
    current_length = runs[-1][1] if runs else 0
    return SequenceStats(
        current_color=current_color,
        current_length=current_length,
        max_green=longest(Color.GREEN),
        max_red=longest(Color.RED),
        distribution=distribution,
    )
