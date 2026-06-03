#!/usr/bin/env bash
# Master script for Excalidraw Validation and Rendering

set -euo pipefail

EXCALIDRAW_FILE="${1:-}"

if [[ -z "${EXCALIDRAW_FILE}" ]]; then
    echo "Usage: bash scripts/render/validate_and_render.sh <path_to_file.excalidraw>" >&2
    exit 1
fi

if [[ ! -f "${EXCALIDRAW_FILE}" ]]; then
    echo "ERROR: File not found: ${EXCALIDRAW_FILE}" >&2
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "--- Phase 1: Technical Validation ---"
if ! python3 "${SCRIPT_DIR}/excalidraw_validator.py" "${EXCALIDRAW_FILE}"; then
    echo "ERROR: Technical validation failed. Please fix the JSON before rendering." >&2
    exit 1
fi

printf '\n--- Phase 2: Visual Rendering ---\n'
if ! bash "${SCRIPT_DIR}/render_docker.sh" "${EXCALIDRAW_FILE}"; then
    echo "ERROR: Rendering failed." >&2
    exit 1
fi

PNG_FILE="${EXCALIDRAW_FILE%.excalidraw}.png"
printf '\n--- Phase 3: Visual Analysis ---\n'
echo "SUCCESS: Rendering complete. Image saved to: ${PNG_FILE}"
echo "INSTRUCTION: Now use 'read_file' on the .png to visually verify the diagram."
