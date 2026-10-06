# analysis

Biblioteca pura (sem I/O) do motor de análise de velas. Fase 1 do Crash Lab.

## Módulos
| Módulo | Função |
|---|---|
| `candles` | Classifica velas em verde/vermelha conforme o alvo de cashout |
| `window` | Contagem e percentuais nas últimas N velas (padrão 100) |
| `sequences` | Sequência atual, máximas e distribuição de sequências |
| `patterns` | Regra "após N velas da cor X, a próxima >= Y": ocorrências, acertos, intervalo de confiança de Wilson, ponto de equilíbrio e decisão de entrada |

## Instalar e testar
```bash
cd analysis
python -m venv .venv
.venv\Scripts\activate          # Windows (Git Bash: source .venv/Scripts/activate)
pip install -e ".[dev]"
pytest
python examples/experimento_padroes.py
```

## Aviso
O histórico descreve o passado. Cada rodada é independente, então nada aqui prevê a próxima vela.
