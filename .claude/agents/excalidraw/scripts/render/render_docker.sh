#!/usr/bin/env bash
# Helper script to run Excalidraw renderer via Docker.
# Accepts an input .excalidraw file from ANY directory by mounting its parent
# as /input. The excalidraw agent dir is also mounted read-only at /excalidraw
# so relative asset paths (e.g. icons/foo.png) remain resolvable via the
# EXCALIDRAW_ASSETS_DIR env var.

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
GLOBAL_EXCALIDRAW_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
IMAGE_NAME="excalidraw-renderer"

if [[ -z "${1:-}" ]]; then
    echo "Usage: $0 <path_to_file.excalidraw> [extra args...]" >&2
    exit 1
fi

# Build the image if it doesn't exist
if [[ "$(docker images -q "${IMAGE_NAME}" 2>/dev/null)" == "" ]]; then
    echo "Building Docker image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" "${SCRIPT_DIR}"
fi

# Resolve absolute path of input file, canonicalising any ../ components via cd/pwd.
INPUT_FILE="$1"
if [[ ! "${INPUT_FILE}" = /* ]]; then
    INPUT_FILE="$(cd "$(dirname "${INPUT_FILE}")" && pwd)/$(basename "${INPUT_FILE}")"
fi

if [[ ! -f "${INPUT_FILE}" ]]; then
    echo "ERROR: File not found: ${INPUT_FILE}" >&2
    exit 1
fi

INPUT_DIR="$(cd "$(dirname "${INPUT_FILE}")" && pwd)"
INPUT_BASENAME="$(basename "${INPUT_FILE}")"

# Mount:
#  - input file's directory at /input (rw — output PNG written as sibling)
#  - excalidraw agent dir at /excalidraw (ro) — so icons/*.png resolve via EXCALIDRAW_ASSETS_DIR
docker run --rm \
    -v "${INPUT_DIR}:/input" \
    -v "${GLOBAL_EXCALIDRAW_DIR}:/excalidraw:ro" \
    -e "EXCALIDRAW_ASSETS_DIR=/excalidraw" \
    -w /input \
    "${IMAGE_NAME}" "/input/${INPUT_BASENAME}" "${@:2}"
