# 01. Requisitos

## Funcionais
| ID | Requisito | Fase |
|---|---|---|
| RF01 | Classificar velas em verde/vermelha conforme o alvo de cashout | 1 |
| RF02 | Analisar janela de N velas (padrão 100): contagens e percentuais | 1 |
| RF03 | Calcular sequências atual e máxima da mesma cor e sua distribuição | 1 |
| RF04 | Avaliar regra "após N velas de cor X, próxima >= Y": ocorrências e taxa | 1 |
| RF05 | Simular rodadas crash com margem da casa configurável | 2 |
| RF06 | Cadastro, login e perfis (admin e usuário) | 4 |
| RF07 | Usuário configura parâmetros do bot (entrada, alvo, stops, cooldown) | 4, 5 |
| RF08 | Painel com análise, histórico e gestão da banca | 5 |
| RF09 | Painel instalável (PWA) | 5 |
| RF10 | Agente local lê velas, aposta e faz cashout automático | 6 |
| RF11 | Gestão de risco com pausa automática e kill switch | 7 |
| RF12 | Licença por usuário e dispositivo, com revogação remota | 8 |
| RF13 | Alertas (ex.: Telegram) e exportação de relatórios | 10 |

## Não funcionais
| ID | Requisito |
|---|---|
| RNF01 | Motor de análise sem dependência de I/O e com cobertura de testes >= 90% |
| RNF02 | Senhas com argon2; tokens JWT de curta duração |
| RNF03 | Segredos somente em variáveis de ambiente ou arquivos fora do git |
| RNF04 | API documentada via OpenAPI |
| RNF05 | Latência de leitura do multiplicador no agente abaixo de 200 ms (meta) |
| RNF06 | Ambiente reproduzível com Docker Compose |
| RNF07 | Logs estruturados e trilha de auditoria de ações sensíveis |

## Regras de negócio
- Vela verde: multiplicador final >= alvo; vermelha: abaixo do alvo.
- O bot só entra se ocorrências mínimas e percentual mínimo da regra forem atingidos.
- Qualquer limite de risco atingido pausa o bot até ação manual do usuário.
