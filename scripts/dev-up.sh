#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root"
docker compose up -d postgres
echo "PostgreSQL đang chạy tại localhost:5432."
