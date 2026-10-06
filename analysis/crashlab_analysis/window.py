"""Estatísticas de uma janela das últimas N velas."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from .candles import Color, classify_all


@dataclass(frozen=True)
class WindowStats:
    total: int
    greens: int
    reds: int

    @property
    def green_pct(self) -> float:
        return 100.0 * self.greens / self.total if self.total else 0.0

    @property
    def red_pct(self) -> float:
        return 100.0 * self.reds / self.total if self.total else 0.0


def window_stats(multipliers: Iterable[float], target: float, size: int = 100) -> WindowStats:
    """Conta verdes e vermelhas nas últimas `size` velas (ou menos, se houver menos)."""
    if size <= 0:
        raise ValueError("o tamanho da janela deve ser positivo")
    recent = list(multipliers)[-size:]
    colors = classify_all(recent, target)
    greens = sum(1 for c in colors if c is Color.GREEN)
    return WindowStats(total=len(colors), greens=greens, reds=len(colors) - greens)
