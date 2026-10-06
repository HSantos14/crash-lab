"""Experimento: regras de padrão vencem a margem da casa?

Gera rodadas crash sintéticas (independentes, com margem da casa) e compara:
  A) apostar em toda rodada, saindo em `next_min`;
  B) apostar só quando a regra de padrão manda entrar.
Se padrões tivessem poder preditivo, B teria ROI melhor que A. Rode e veja.

Uso: python examples/experimento_padroes.py --rodadas 30000 --seed 42
"""
from __future__ import annotations

import argparse
import random
from math import sqrt
from statistics import pstdev

from crashlab_analysis import Color, PatternRule, should_enter


def gerar_rodadas(n: int, edge: float, rng: random.Random) -> list[float]:
    """P(multiplicador >= x) = (1 - edge) / x, truncado em 2 casas e mínimo 1.00."""
    out = []
    for _ in range(n):
        u = 1.0 - rng.random()  # (0, 1]
        out.append(max(1.0, int(((1 - edge) / u) * 100) / 100))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rodadas", type=int, default=30000)
    ap.add_argument("--edge", type=float, default=0.03)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--janela", type=int, default=100)
    args = ap.parse_args()

    target, next_min = 2.0, 1.6
    rule = PatternRule(prior_count=2, prior_color=Color.RED, next_min=next_min)
    rng = random.Random(args.seed)
    mults = gerar_rodadas(args.rodadas, args.edge, rng)

    def payoff(m: float) -> float:
        return (next_min - 1) if m >= next_min else -1.0

    base, pat = [], []
    for i in range(args.janela, len(mults)):
        base.append(payoff(mults[i]))
        d = should_enter(mults[i - args.janela:i], target, rule,
                         min_occurrences=5, min_hit_rate=0.65)
        if d.should_enter:
            pat.append(payoff(mults[i]))

    def resumo(nome: str, pagamentos: list[float]) -> float | None:
        if not pagamentos:
            print(f"{nome} o padrão nunca disparou com esses filtros.")
            return None
        n = len(pagamentos)
        roi = sum(pagamentos) / n
        se = pstdev(pagamentos) / sqrt(n)
        print(f"{nome} {n:6d} apostas | ROI {roi:+.2%} (erro padrão {se:.2%})")
        return (roi + args.edge) / se  # distância da teoria, em erros padrão

    print(f"Rodadas: {args.rodadas} | margem da casa: {args.edge:.1%} | saída em {next_min}x")
    print(f"ROI esperado (teoria): {-args.edge:+.2%}")
    resumo("A) toda rodada:  ", base)
    z = resumo("B) só com padrão:", pat)
    if z is not None:
        if abs(z) < 2:
            print(f"B está a {abs(z):.1f} erros padrão da teoria: diferença dentro do ruído estatístico.")
        else:
            print(f"B está a {abs(z):.1f} erros padrão da teoria: rode com outra seed e mais rodadas.")
    print("Dica: aumente --rodadas e troque --seed para ver o ROI de B convergir para a teoria.")


if __name__ == "__main__":
    main()
