#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if command -v docker-compose &>/dev/null; then
    docker-compose down
else
    docker compose down
fi

echo "NGINX container stopped"
