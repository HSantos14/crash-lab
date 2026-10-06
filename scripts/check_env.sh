#!/usr/bin/env bash
# Verifica as ferramentas necessárias para o projeto.
ok=0
check() {
  local name="$1" cmd="$2"
  if command -v "$cmd" >/dev/null 2>&1; then
    printf "[ok]    %-8s %s\n" "$name" "$($cmd --version 2>&1 | head -n1)"
  else
    printf "[FALTA] %-8s instale antes de continuar\n" "$name"; ok=1
  fi
}
check git git
check python python3
check node node
check npm npm
check docker docker
py=$(python3 -c 'import sys;print(sys.version_info >= (3,11))' 2>/dev/null || echo False)
[ "$py" = "True" ] || { echo "[AVISO] Python 3.11+ recomendado"; ok=1; }
exit $ok
