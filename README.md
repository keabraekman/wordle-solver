# Wordle Solver

Minimal MVP website for solving Wordle from prior guesses and feedback.

Users can:

- enter previous guesses,
- mark each letter as absent (`0`), present (`1`), or correct (`2`),
- submit the board,
- get the best next guess, top 10 ranked guesses, and the remaining candidate count.

This app keeps the original repo's solver ideas, but wraps them behind a clean Python API and a small static frontend.

## What Changed

The old repo was a set of exploratory Python scripts:

- `wordle-solver.py` for a letter-frequency heuristic
- `wordle-solver-2.py` and `test.py` for more experimental ranking approaches
- `word-scraper.py` for generating word lists

Those legacy files are still in the repo as references. The production-ish MVP now lives under `app/`, `frontend/`, `infra/`, `scripts/`, and `tests/`.

## Architecture

### Local development

```text
Browser
  -> local_api.py
    -> solve_next_guess(...)
      -> legacy solver adapter
```

### Production

```text
Browser
  -> S3 static website
    -> Lambda Function URL
      -> validates request
      -> launches one-off ECS/Fargate task
        -> worker loads bundled solver data
        -> runs solver
        -> writes result JSON to S3
      -> Lambda polls task + reads result JSON
      -> returns JSON to browser
```

## Why This Architecture

- The frontend is just static files, so hosting is cheap and simple.
- Solver compute only runs when a user submits a solve request.
- ECS/Fargate tasks give near-zero idle compute cost because there is no always-on app server.
- The solver data is small, so it is bundled directly into the Python package and worker image.
- S3 is only used as the short-lived handoff for worker results.
- There is no database, no ALB, no auth layer, and no permanent background service.

## Repo Layout

```text
app/
  api/
    local_api.py
    lambda_handler.py
    service.py
  solver/
    adapter.py
    legacy_solver1.py
    legacy_solver2.py
    models.py
    resources.py
    validation.py
    data/
  worker/
    main.py
frontend/
  index.html
  styles.css
  app.js
  config.js
infra/
  terraform/
scripts/
tests/
Dockerfile.worker
pyproject.toml
```

## Solver Behavior

- Input shape:

```json
{
  "guesses": [
    {"word": "raise", "feedback": "01020"},
    {"word": "clout", "feedback": "20000"}
  ]
}
```

- Validation rules:
  - every word must be exactly 5 letters
  - every word must exist in the allowed guess list
  - every feedback string must be exactly 5 characters of `0`, `1`, or `2`
  - if the guess history leaves no valid official Wordle answers, the request is rejected

- Strategy selection:
  - no guesses yet: use the legacy precomputed opening-word ranking
  - 1 candidate left: return that candidate
  - small remaining candidate set: use the stronger expected-remaining ranking
  - larger remaining candidate set: fall back to the legacy letter-frequency heuristic

## Local Development

### 1. Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Run tests

```bash
python3 -m unittest discover -s tests
```

### 3. Start the local site

```bash
./scripts/run_local.sh
```

Then open:

```text
http://127.0.0.1:8000
```

The local server:

- serves the static frontend,
- exposes `POST /api/solve`,
- runs the solver directly in-process.

## Frontend Build

For local mode you do not need a build step.

For deployment, generate a static bundle with the production API URL:

```bash
python3 scripts/build_frontend.py --api-base-url "https://your-function-url-id.lambda-url.us-west-2.on.aws"
```

Output goes to:

```text
dist/frontend/
```

## Worker Image Build

Build the ECS worker image locally:

```bash
./scripts/build_worker.sh
```

Or with a custom tag:

```bash
./scripts/build_worker.sh wordle-solver-worker:dev
```

## Lambda Package Build

Build the Lambda deployment zip:

```bash
python3 scripts/build_lambda_package.py
```

Output goes to:

```text
dist/lambda/wordle-solver-lambda.zip
```

## Terraform Deployment

### 1. Review variables

Start with:

```bash
cp infra/terraform/terraform.tfvars.example infra/terraform/terraform.tfvars
```

The key variables are:

- `aws_region`
- `project_name`
- `environment`
- `worker_image_uri` (optional; defaults to the Terraform-created ECR repo with `:latest`)

### 2. Apply infrastructure

```bash
./scripts/deploy_infra.sh
```

This script:

- builds the Lambda zip,
- runs `terraform init`,
- runs `terraform apply`.

Terraform provisions:

- ECR repository for the worker image
- ECS cluster
- Fargate task definition
- IAM roles and policies
- Lambda control plane
- Lambda Function URL
- S3 bucket for short-lived worker results with lifecycle cleanup
- public S3 website bucket for the frontend
- small public VPC/subnets for Fargate, with no NAT gateway

### 3. Push the worker image

After the first apply, get the ECR repo URL:

```bash
ECR_REPO="$(terraform -chdir=infra/terraform output -raw ecr_repository_url)"
```

Build and push:

```bash
./scripts/build_worker.sh
./scripts/push_worker.sh "$ECR_REPO"
```

### 4. Upload the frontend

Get the frontend bucket and Lambda URL:

```bash
FRONTEND_BUCKET="$(terraform -chdir=infra/terraform output -raw frontend_bucket_name)"
API_URL="$(terraform -chdir=infra/terraform output -raw lambda_function_url)"
```

Build and upload the static frontend:

```bash
./scripts/upload_frontend.sh "$FRONTEND_BUCKET" "${API_URL%/}"
```

### 5. Open the site

```bash
terraform -chdir=infra/terraform output -raw frontend_website_url
```

## API Endpoints

### Local API

- `GET /api/health`
- `POST /api/solve`

### Lambda Function URL

The frontend calls:

- `POST <function-url>/solve`

The Lambda handler also supports:

- `GET <function-url>/health`

## Important Assumptions

- This app uses the official Wordle answer list bundled in the repo.
- The worker image bundles the solver data directly instead of pulling it from storage at runtime.
- The production frontend is a plain S3 website endpoint, which is HTTP-only. If you want HTTPS and a nicer public edge setup, add CloudFront later.
- ECS tasks run in public subnets with public IPs so the stack can stay NAT-free and cheap.
- Result objects in S3 are short-lived and automatically expire after 1 day.
- The old root-level experimental scripts are intentionally left in place as historical references.

## Practical Follow-Ups

Useful next improvements if you want to keep pushing this:

- replace the frequency fallback with a stronger but still bounded ranking strategy for larger candidate sets
- add a small job status endpoint instead of synchronous Lambda polling if solve times grow
- add CloudFront in front of the S3 website for HTTPS
- tighten Lambda IAM from broad ECS permissions to more granular resource constraints
- add CI for tests, Lambda package build, and Terraform formatting/validation
