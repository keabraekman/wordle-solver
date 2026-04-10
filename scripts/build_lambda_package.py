from __future__ import annotations

from pathlib import Path
import zipfile


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "dist" / "lambda"
OUTPUT_PATH = OUTPUT_DIR / "wordle-solver-lambda.zip"


def iter_source_files() -> list[Path]:
    files: list[Path] = []
    for path in (PROJECT_ROOT / "app").rglob("*"):
        if path.is_dir():
            continue
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        files.append(path)
    return files


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUTPUT_PATH, "w", zipfile.ZIP_DEFLATED) as archive:
        for source_path in iter_source_files():
            archive.write(source_path, source_path.relative_to(PROJECT_ROOT))
    print(f"Built Lambda package at {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
