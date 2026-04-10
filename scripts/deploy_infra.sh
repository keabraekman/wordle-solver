#!/usr/bin/env bash
set -euo pipefail

python3 scripts/build_lambda_package.py
terraform -chdir=infra/terraform init
terraform -chdir=infra/terraform apply "$@"
