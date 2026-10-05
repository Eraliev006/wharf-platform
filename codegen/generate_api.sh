#!/usr/bin/env bash
set -e

# Move to root of project
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

uv run --project api python -m grpc_tools.protoc \
    -I./proto \
    --python_out=./api/app/generated \
    --pyi_out=./api/app/generated \
    --grpc_python_out=./api/app/generated \
    ./proto/api/v1/api.proto
