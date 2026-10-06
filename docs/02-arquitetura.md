# 02. Arquitetura

```
 +-----------+   HTTPS/JWT   +------------------+      +------------+
 | Frontend  | <-----------> |  Backend FastAPI | <--> | PostgreSQL |
 |  (PWA)    |               |  auth, config,   |      +------------+
 +-----------+               |  licenças, logs  |
                             +---------^--------+
                                       | HTTPS/JWT + token de licença
                             +---------+--------+   WebSocket   +-----------+
                             |  Agente local    | <-----------> | Simulador |
                             |  Playwright      |   (cliques)   |  crash    |
                             |  + analysis lib  |               +-----------+
                             +------------------+
```

## Decisões
| Decisão | Escolha | Motivo |
|---|---|---|
| Backend | FastAPI + SQLAlchemy + Alembic | Tipagem, OpenAPI automático, ecossistema Python |
| Banco | PostgreSQL 16 | Relacional, índices, padrão de mercado |
| Frontend | React + Vite (PWA) | Instalável, ecossistema amplo |
| Agente | Python + Playwright | Mesma linguagem do motor; WebSocket e iframes |
| Análise | Biblioteca Python pura | Testável e reutilizável por backend e agente |
| Licença | Token assinado (chave assimétrica) | Validação offline curta no agente |

## Princípios
1. O motor de análise é puro: entra lista de velas, sai resultado.
2. O agente roda na máquina do usuário e nunca guarda credenciais de terceiros no backend.
3. Toda ação do bot gera registro auditável.
4. Segurança desde o início, não no fim.
