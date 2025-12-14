#!/usr/bin/env bash
set -euo pipefail

# Creates a single ZIP you can upload to the LMS.
# Output: m7/cs499_module7_submission.zip

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_ZIP="$ROOT_DIR/m7/cs499_module7_submission.zip"

cd "$ROOT_DIR"

rm -f "$OUT_ZIP"

# zip is widely available; if it isn't, install it or switch to tar.
zip -r "$OUT_ZIP" \
  m7/README.md \
  m7/final_submission_manifest.md \
  m7/final_submission_checklist.md \
  m7/submission_files \
  grazioso-dashboard \
  -x "**/.git/**" \
  -x "**/node_modules" \
  -x "**/node_modules/**" \
  -x "**/dist" \
  -x "**/dist/**" \
  -x "**/__pycache__/**" \
  -x "**/.pytest_cache/**" \
  -x "**/.mypy_cache/**" \
  -x "**/.ruff_cache/**" \
  -x "**/.venv" \
  -x "**/.venv/**" \
  -x "**/logs/**" \
  -x "**/.coverage" \
  -x "**/coverage.xml" \
  -x "**/.env" \
  -x "**/*.pyc" \
  -x "**/*.pyo" \
  -x "**/*.pyd" \
  -x "**/*.DS_Store" \
  -x "**/Thumbs.db"

echo "Created: $OUT_ZIP"