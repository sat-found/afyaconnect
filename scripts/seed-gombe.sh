#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

if ! docker compose ps app --status running -q 2>/dev/null | grep -q .; then
  echo "App container is not running. Start the stack first: ./scripts/start.sh"
  exit 1
fi

echo "Seeding Gombe synthetic data..."
docker compose exec app python3 /opt/gnuhealth/seed/seed_gombe.py
