#!/usr/bin/env bash
set -euo pipefail

IMAGE_TAG="${1:-wordle-solver-worker:local}"
docker build -f Dockerfile.worker -t "${IMAGE_TAG}" .
