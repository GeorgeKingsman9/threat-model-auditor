#!/usr/bin/env bash
set -euo pipefail
AUDITOR_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 -B "$AUDITOR_ROOT/scan.py" "$@"
