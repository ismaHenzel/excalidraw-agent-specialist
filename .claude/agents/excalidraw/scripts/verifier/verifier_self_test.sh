#!/usr/bin/env bash
# Helper-level self-test for the Excalidraw verifier's structural pre-check.
#
# Loops over the committed fixtures under fixtures/verifier/, runs
# scripts/verifier/verifier_structural.py on each, and diffs its stdout
# against the `issues` field of the fixture's expected-report.json
# (jq-normalized).
#
# Tests the HELPER only (structural issues). The subagent's visual half is
# validated by the manual end-to-end checkpoint, not this script.

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
AGENT_DIR="$( cd "${SCRIPT_DIR}/../.." && pwd )"
FIXTURES_DIR="${AGENT_DIR}/fixtures/verifier"
HELPER="${SCRIPT_DIR}/verifier_structural.py"

ALL_FIXTURES=(good raw-emoji text-overflow)

usage() {
    echo "Usage: bash scripts/verifier/verifier_self_test.sh [good|raw-emoji|text-overflow]" >&2
}

# Preflight: require python3, jq, diff
for dep in python3 jq diff; do
    if ! command -v "${dep}" >/dev/null 2>&1; then
        echo "ERROR: required dependency not found: ${dep}" >&2
        exit 1
    fi
done

if [[ "$#" -gt 1 ]]; then
    usage
    exit 1
fi

if [[ "$#" -eq 1 ]]; then
    SELECTED="$1"
    VALID=0
    for f in "${ALL_FIXTURES[@]}"; do
        if [[ "${f}" = "${SELECTED}" ]]; then
            VALID=1
            break
        fi
    done
    if [[ "${VALID}" -eq 0 ]]; then
        usage
        exit 1
    fi
    FIXTURES=("${SELECTED}")
else
    FIXTURES=("${ALL_FIXTURES[@]}")
fi

PASS=0
FAIL=0

for fixture in "${FIXTURES[@]}"; do
    echo "--- Fixture: ${fixture} ---"
    EXCALIDRAW_FILE="${FIXTURES_DIR}/${fixture}/${fixture}.excalidraw"
    EXPECTED_FILE="${FIXTURES_DIR}/${fixture}/expected-report.json"

    if [[ ! -f "${EXCALIDRAW_FILE}" ]]; then
        echo "FAIL: ${fixture}"
        echo "  missing fixture: ${EXCALIDRAW_FILE}"
        FAIL=$(( FAIL + 1 ))
        continue
    fi
    if [[ ! -f "${EXPECTED_FILE}" ]]; then
        echo "FAIL: ${fixture}"
        echo "  missing expected-report: ${EXPECTED_FILE}"
        FAIL=$(( FAIL + 1 ))
        continue
    fi

    # Run helper — capture output; guard with || so set -e doesn't abort the loop.
    GEN=""
    HELPER_RC=0
    GEN="$(python3 "${HELPER}" "${EXCALIDRAW_FILE}")" || HELPER_RC=$?
    if [[ "${HELPER_RC}" -ne 0 ]]; then
        echo "FAIL: ${fixture}"
        echo "  helper exited ${HELPER_RC} (expected 0)"
        FAIL=$(( FAIL + 1 ))
        continue
    fi

    # Validate helper output is JSON before diffing.
    if ! echo "${GEN}" | jq empty >/dev/null 2>&1; then
        echo "FAIL: ${fixture}"
        echo "  helper output is not valid JSON"
        FAIL=$(( FAIL + 1 ))
        continue
    fi

    # Extract expected issues field; guard with || so set -e doesn't abort on jq error.
    EXP=""
    EXP_RC=0
    EXP="$(jq '.issues' "${EXPECTED_FILE}")" || EXP_RC=$?
    if [[ "${EXP_RC}" -ne 0 ]]; then
        echo "FAIL: ${fixture}"
        echo "  could not extract .issues from expected-report"
        FAIL=$(( FAIL + 1 ))
        continue
    fi

    DIFF=""
    DIFF="$(diff <(echo "${EXP}" | jq .) <(echo "${GEN}" | jq .))" || true

    if [[ -z "${DIFF}" ]]; then
        echo "PASS: ${fixture}"
        PASS=$(( PASS + 1 ))
    else
        echo "FAIL: ${fixture}"
        echo "${DIFF}"
        FAIL=$(( FAIL + 1 ))
    fi
done

echo "Summary: ${PASS} pass / ${FAIL} fail"
# Normalise exit code to 0/1 rather than the raw FAIL count (avoids
# confusing callers when FAIL > 1, since exit codes > 125 have special meanings).
[[ "${FAIL}" -eq 0 ]] && exit 0 || exit 1
