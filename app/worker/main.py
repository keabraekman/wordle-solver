from __future__ import annotations

import json
import os
import sys
import traceback
from typing import Any

from app.api.service import solve_payload


def _result_key(request_id: str, prefix: str) -> str:
    normalized_prefix = prefix.strip("/")
    if not normalized_prefix:
        return f"{request_id}.json"
    return f"{normalized_prefix}/{request_id}.json"


def _write_result(bucket: str, key: str, payload: dict[str, Any]) -> None:
    import boto3

    s3 = boto3.client("s3")
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(payload).encode("utf-8"),
        ContentType="application/json",
    )


def main() -> int:
    request_json = os.environ.get("WORDLE_SOLVER_REQUEST_JSON")
    if not request_json:
        raise RuntimeError("WORDLE_SOLVER_REQUEST_JSON is required.")

    request_id = os.environ.get("WORDLE_SOLVER_REQUEST_ID", "local-request")
    result_bucket = os.environ.get("WORDLE_SOLVER_RESULT_BUCKET")
    result_prefix = os.environ.get("WORDLE_SOLVER_RESULT_PREFIX", "results")
    result_key = _result_key(request_id, result_prefix)

    try:
        payload = json.loads(request_json)
        result = solve_payload(payload)
        result["request_id"] = request_id

        if result_bucket:
            _write_result(result_bucket, result_key, result)

        print(json.dumps(result))
        return 0
    except Exception as exc:
        error_payload = {
            "request_id": request_id,
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }
        if result_bucket:
            _write_result(result_bucket, result_key, error_payload)
        print(json.dumps(error_payload), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
