#!/usr/bin/env bash
# 从任意工作目录运行：bash /path/to/scripts/audit.sh aspi
set -euo pipefail
AUDITOR_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 -B "$AUDITOR_ROOT/audit.py" audit "$@"
