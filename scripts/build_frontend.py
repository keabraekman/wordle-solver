from __future__ import annotations

import argparse
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = PROJECT_ROOT / "frontend"
OUTPUT_DIR = PROJECT_ROOT / "dist" / "frontend"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the static frontend bundle.")
    parser.add_argument(
        "--api-base-url",
        default="",
        help="API base URL injected into frontend/config.js.",
    )
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for filename in ("index.html", "styles.css", "app.js"):
      shutil.copy2(FRONTEND_DIR / filename, OUTPUT_DIR / filename)

    config_path = OUTPUT_DIR / "config.js"
    config_path.write_text(
        "window.WORDLE_SOLVER_CONFIG = {\n"
        f'  apiBaseUrl: "{args.api_base_url}",\n'
        "};\n",
        encoding="utf-8",
    )
    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")

    print(f"Built frontend into {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
