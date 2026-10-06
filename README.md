# Crash Lab

Projeto de **aprendizado** full-stack: análise estatística de velas de um jogo crash **simulado**,
com bot local de automação, painel web instalável (PWA), licenças e gestão de risco.

> Aviso: em jogos crash cada rodada é independente. O histórico de velas **não prevê** a próxima.
> Este projeto existe para estudar engenharia de software e estatística, não para obter lucro.
> Todo o desenvolvimento acontece contra um jogo simulado local, sem dinheiro real.

## Estrutura

| Pasta | Conteúdo | Fase |
|---|---|---|
| `analysis/` | Biblioteca Python do motor de análise de velas | 1 |
| `simulator/` | Jogo crash simulado (servidor + página) | 2 |
| `backend/` | API FastAPI + PostgreSQL | 3 e 4 |
| `frontend/` | PWA React + Vite | 5 |
| `agent/` | Agente local Python + Playwright | 6 e 7 |
| `docs/` | Requisitos, arquitetura, ameaças, convenções, roadmap | 0 |
| `scripts/` | Utilitários de ambiente | 0 |

## Começando

```bash
bash scripts/check_env.sh      # confere ferramentas instaladas
cp .env.example .env           # ajuste os valores
docker compose up -d db        # sobe o PostgreSQL local
git init && git add . && git commit -m "chore: estrutura inicial (fase 0)"
```

Acompanhe o progresso em `docs/05-roadmap.md`.
