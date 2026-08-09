#!/usr/bin/env python3
"""
guard-project-boundary.py — PreToolUse hook para t3rzo-landing.

Bloquea cualquier Edit / Write / NotebookEdit cuyo archivo destino caiga fuera
de la raiz de este proyecto. Implementa la Regla 1 de
docs/metodologia-de-trabajo.md (aislamiento total entre proyectos).

El limite se deriva de la ubicacion de este mismo archivo
(<raiz>/.claude/hooks/guard-project-boundary.py), asi que la carpeta se puede
mover o renombrar sin tener que tocar nada.

Entrada:  JSON del hook por stdin.
Salida:   JSON con permissionDecision "deny" para bloquear; nada para permitir.
"""

import json
import os
import sys
from pathlib import Path

# <raiz>/.claude/hooks/guard-project-boundary.py -> parents[2] == <raiz>
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Unica excepcion al limite: el scratchpad temporal de la sesion de Claude Code.
# No es codigo de ningun proyecto, es area de borradores descartables.
SCRATCHPAD_ROOT = Path(os.environ.get("LOCALAPPDATA", r"C:\Users\Marcos\AppData\Local")) / "Temp" / "claude"

ALLOWED_ROOTS = [PROJECT_ROOT, SCRATCHPAD_ROOT]


def allow():
    sys.exit(0)


def deny(reason: str):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def normalize(raw: str) -> Path:
    """Lleva un path a forma absoluta y resuelta, tolerando el formato /c/Users
    que usa Git Bash ademas del C:\\Users nativo de Windows."""
    text = raw.strip().strip('"')
    # Git Bash / MSYS: /c/Users/... -> C:/Users/...
    if len(text) > 2 and text[0] == "/" and text[2] in "/\\" and text[1].isalpha():
        text = f"{text[1].upper()}:{text[2:]}"
    p = Path(text)
    if not p.is_absolute():
        p = Path.cwd() / p
    # resolve(strict=False): el archivo puede no existir todavia (caso Write)
    return Path(os.path.normpath(str(p.resolve() if p.exists() else p)))


def inside(path: Path, root: Path) -> bool:
    try:
        # normcase: en Windows la comparacion de paths no distingue mayusculas
        a = os.path.normcase(str(path))
        b = os.path.normcase(str(root))
        return a == b or a.startswith(b + os.sep)
    except Exception:
        return False


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception as exc:
        # Fail-closed: si no se entiende la entrada, no se sabe que archivo se
        # va a tocar, y un limite que "no sabe" no puede dejar pasar. Bloquear
        # es visible y recuperable; dejar pasar es silencioso.
        deny(
            f"[limite de proyecto] No se pudo leer la entrada del hook ({exc}). "
            "Se bloquea por precaucion. Si esto se repite, avisale a Marcos: el "
            "limite vive en .claude/hooks/guard-project-boundary.py y se "
            "desactiva borrando el bloque hooks de .claude/settings.json."
        )

    tool_input = payload.get("tool_input") or {}
    target = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not target:
        allow()

    path = normalize(str(target))

    for root in ALLOWED_ROOTS:
        if inside(path, root):
            allow()

    deny(
        f"[limite de proyecto] Bloqueado: {path} esta fuera de {PROJECT_ROOT}. "
        "Regla 1 de docs/metodologia-de-trabajo.md: cada proyecto se trabaja "
        "aislado. Si el cambio hace falta de verdad, abri una sesion de Claude "
        "Code en el repositorio que corresponde."
    )


if __name__ == "__main__":
    main()
