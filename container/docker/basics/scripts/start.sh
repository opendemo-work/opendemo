#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if command -v docker-compose &>/dev/null; then
    docker-compose up -d
else
    docker compose up -d
fi

echo "NGINX container started at http://localhost:8080"
