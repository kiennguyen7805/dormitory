#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root/src/backend"
python -m dormitory_infrastructure.identity.seed_cli
