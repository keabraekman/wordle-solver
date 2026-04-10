#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <frontend-bucket-name> <api-base-url>" >&2
  exit 1
fi

BUCKET_NAME="$1"
API_BASE_URL="$2"

python3 scripts/build_frontend.py --api-base-url "${API_BASE_URL}"
aws s3 sync dist/frontend/ "s3://${BUCKET_NAME}" --delete
