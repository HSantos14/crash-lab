# 03. Modelo de ameaças (simples)

## Ativos
Contas de usuário, tokens, configurações do bot, histórico, chaves de licença.

## Atores
Usuário legítimo, usuário malicioso (tenta burlar licença), atacante externo, erro humano.

## Ameaças e mitigações
| # | Ameaça | Mitigação | Fase |
|---|---|---|---|
| T1 | Força bruta no login | Rate limit, bloqueio temporário, argon2 | 9 |
| T2 | Roubo de JWT | Expiração curta, refresh rotativo, HTTPS | 4, 9 |
| T3 | Injeção SQL | ORM com parâmetros, validação Pydantic | 3, 4 |
| T4 | XSS/CSRF no painel | Escape padrão do React, CORS restrito, cabeçalhos de segurança | 5, 9 |
| T5 | Vazamento de segredos | `.env` fora do git, chaves em `keys/` ignorado | 0, 9 |
| T6 | Cópia/pirataria do agente | Token assinado, vínculo de dispositivo, lógica sensível no servidor | 8 |
| T7 | Adulteração da configuração do bot | Validação no servidor, limites máximos de risco | 4, 7 |
| T8 | Bot fora de controle (perda da banca simulada) | Stops, limites, kill switch local e remoto | 7 |
| T9 | Acesso a dados de outro usuário | Autorização por dono em todo endpoint | 4 |
| T10 | Dependências vulneráveis | Auditoria periódica (pip-audit, npm audit) | 11 |

## Limite conhecido
Nenhuma proteção em código que roda na máquina do usuário é definitiva.
