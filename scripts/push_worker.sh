#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <ecr-repository-url> [local-image-tag]" >&2
  exit 1
fi

ECR_REPOSITORY_URL="$1"
LOCAL_IMAGE_TAG="${2:-wordle-solver-worker:local}"
REGION="$(echo "${ECR_REPOSITORY_URL}" | cut -d'.' -f4)"

aws ecr get-login-password --region "${REGION}" \
  | docker login --username AWS --password-stdin "$(echo "${ECR_REPOSITORY_URL}" | cut -d'/' -f1)"

docker tag "${LOCAL_IMAGE_TAG}" "${ECR_REPOSITORY_URL}:latest"
docker push "${ECR_REPOSITORY_URL}:latest"
