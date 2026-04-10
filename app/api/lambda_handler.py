from __future__ import annotations

import base64
import json
import os
import time
import uuid
from http import HTTPStatus
from typing import Any

from app.api.service import handle_payload
from app.solver import ValidationError, validate_payload


def _cors_headers() -> dict[str, str]:
    origin = os.getenv("WORDLE_SOLVER_CORS_ORIGIN", "*")
    return {
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
        "Content-Type": "application/json",
    }


def _json_response(status_code: int, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "statusCode": int(status_code),
        "headers": _cors_headers(),
        "body": json.dumps(payload),
    }


def _decode_body(event: dict[str, Any]) -> dict[str, Any]:
    raw_body = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        raw_body = base64.b64decode(raw_body).decode("utf-8")
    return json.loads(raw_body or "{}")


def _run_via_ecs(payload: dict[str, Any]) -> dict[str, object]:
    import boto3

    validated_guesses = validate_payload(payload)
    normalized_payload = {"guesses": [guess.to_dict() for guess in validated_guesses]}
    request_id = uuid.uuid4().hex

    cluster_arn = os.environ["WORDLE_SOLVER_CLUSTER_ARN"]
    task_definition_arn = os.environ["WORDLE_SOLVER_TASK_DEFINITION_ARN"]
    container_name = os.environ.get("WORDLE_SOLVER_CONTAINER_NAME", "worker")
    result_bucket = os.environ["WORDLE_SOLVER_RESULT_BUCKET"]
    result_prefix = os.environ.get("WORDLE_SOLVER_RESULT_PREFIX", "results").strip("/")
    subnets = [
        value.strip()
        for value in os.environ["WORDLE_SOLVER_SUBNET_IDS"].split(",")
        if value.strip()
    ]
    security_groups = [
        value.strip()
        for value in os.environ["WORDLE_SOLVER_SECURITY_GROUP_IDS"].split(",")
        if value.strip()
    ]
    wait_timeout_seconds = int(os.environ.get("WORDLE_SOLVER_WAIT_TIMEOUT_SECONDS", "60"))

    ecs = boto3.client("ecs")
    s3 = boto3.client("s3")

    run_response = ecs.run_task(
        cluster=cluster_arn,
        taskDefinition=task_definition_arn,
        launchType="FARGATE",
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": subnets,
                "securityGroups": security_groups,
                "assignPublicIp": "ENABLED",
            }
        },
        overrides={
            "containerOverrides": [
                {
                    "name": container_name,
                    "environment": [
                        {"name": "WORDLE_SOLVER_REQUEST_ID", "value": request_id},
                        {
                            "name": "WORDLE_SOLVER_REQUEST_JSON",
                            "value": json.dumps(normalized_payload),
                        },
                        {"name": "WORDLE_SOLVER_RESULT_BUCKET", "value": result_bucket},
                        {"name": "WORDLE_SOLVER_RESULT_PREFIX", "value": result_prefix},
                    ],
                }
            ]
        },
    )

    failures = run_response.get("failures", [])
    if failures:
        failure = failures[0]
        raise RuntimeError(f"ECS task failed to start: {failure.get('reason', 'unknown error')}")

    tasks = run_response.get("tasks", [])
    if not tasks:
        raise RuntimeError("ECS task failed to start: no task information returned.")

    task_arn = tasks[0]["taskArn"]
    deadline = time.time() + wait_timeout_seconds

    while time.time() < deadline:
        task = ecs.describe_tasks(cluster=cluster_arn, tasks=[task_arn])["tasks"][0]
        if task.get("lastStatus") == "STOPPED":
            break
        time.sleep(1)
    else:
        raise TimeoutError("Timed out waiting for the solver task to finish.")

    task = ecs.describe_tasks(cluster=cluster_arn, tasks=[task_arn])["tasks"][0]
    container = task["containers"][0]
    result_key = f"{result_prefix}/{request_id}.json"

    result_object = s3.get_object(Bucket=result_bucket, Key=result_key)
    result_payload = json.loads(result_object["Body"].read().decode("utf-8"))

    exit_code = container.get("exitCode", 1)
    if exit_code != 0:
        error_message = result_payload.get(
            "error",
            container.get("reason") or task.get("stoppedReason") or "Worker task failed.",
        )
        raise RuntimeError(str(error_message))

    return result_payload


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    del context

    method = (
        event.get("requestContext", {})
        .get("http", {})
        .get("method", "POST")
        .upper()
    )
    raw_path = event.get("rawPath") or "/api/solve"

    if method == "OPTIONS":
        return _json_response(HTTPStatus.NO_CONTENT, {})

    if method == "GET" and raw_path.endswith("/health"):
        return _json_response(HTTPStatus.OK, {"status": "ok"})

    if method != "POST":
        return _json_response(HTTPStatus.METHOD_NOT_ALLOWED, {"error": "Method not allowed."})

    try:
        payload = _decode_body(event)
    except json.JSONDecodeError:
        return _json_response(
            HTTPStatus.BAD_REQUEST,
            {"error": "Request body must be valid JSON."},
        )

    mode = os.getenv("WORDLE_SOLVER_MODE", "direct").lower()

    try:
        if mode == "ecs":
            result = _run_via_ecs(payload)
            return _json_response(HTTPStatus.OK, result)

        status_code, body = handle_payload(payload)
        return _json_response(status_code, body)
    except ValidationError as exc:
        return _json_response(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
    except TimeoutError as exc:
        return _json_response(HTTPStatus.GATEWAY_TIMEOUT, {"error": str(exc)})
    except Exception as exc:  # pragma: no cover - infrastructure failure path
        return _json_response(HTTPStatus.BAD_GATEWAY, {"error": str(exc)})
