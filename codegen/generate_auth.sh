#!/usr/bin/env bash
set -e

# Move to root of project
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

OUT_DIR=./auth/app/generated

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

uv run --project auth python -m grpc_tools.protoc \
    -Iapp/generated=./proto \
    --python_out=./auth \
    --pyi_out=./auth \
    --grpc_python_out=./auth \
    app/generated/auth/v1/auth.proto

find "$OUT_DIR" -type d -exec touch {}/__init__.py \;
