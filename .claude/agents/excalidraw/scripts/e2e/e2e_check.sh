#!/usr/bin/env bash
# End-to-end artefact-side check runner for the Excalidraw closed-loop specialist.
#
# Validates the loop's OUTPUTS after an operator-driven specialist run. Does NOT
# spawn the specialist or the verifier itself — those run inside an interactive
# Claude Code session per fixtures/e2e/README.md.
#
# Modes:
#   success         — assert sibling PNG + verifier-report exist and passed=true;
#                      no suffixed siblings; report fresh (>= source mtime).
#   honest-failure  — assert sibling PNG + report exist, passed=false + issues
#                      non-empty; no suffixed siblings; if --final-message <path>
#                      is provided, assert it contains the LOOP-02 honest-failure
#                      tokens and lacks forbidden success tokens.
#
# Exit codes:
#   0 — all asserts hold
#   1 — at least one assert failed
#   2 — bad invocation (missing args, unknown mode, path doesn't end in .excalidraw)
#
# NOTE: set -e is intentionally ABSENT. This script uses a FAIL-counter pattern
# where every assert must run regardless of prior failures. pipefail is included
# so any failed pipeline stage is surfaced rather than silently swallowed.

set -uo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# shellcheck disable=SC2034  # AGENT_DIR is intentionally retained for future asserts that reference agent-level fixtures
AGENT_DIR="$( cd "${SCRIPT_DIR}/../.." && pwd )"

usage() {
    echo "Usage: bash scripts/e2e/e2e_check.sh <path-to-.excalidraw> --mode {success|honest-failure} [--final-message <path>]" >&2
}

SOURCE=""
MODE=""
FINAL_MSG=""

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --mode)
            if [[ "$#" -lt 2 ]] || [[ -z "$2" ]]; then usage; exit 2; fi
            MODE="$2"; shift 2 ;;
        --final-message)
            if [[ "$#" -lt 2 ]] || [[ -z "$2" ]]; then usage; exit 2; fi
            FINAL_MSG="$2"; shift 2 ;;
        --help|-h)
            usage; exit 0 ;;
        --*)
            usage; exit 2 ;;
        *)
            if [[ -z "${SOURCE}" ]]; then
                case "$1" in
                    *.excalidraw) SOURCE="$1"; shift ;;
                    *) usage; exit 2 ;;
                esac
            else
                usage; exit 2
            fi
            ;;
    esac
done

if [[ -z "${SOURCE}" ]]; then usage; exit 2; fi
if [[ -z "${MODE}" ]]; then usage; exit 2; fi
case "${MODE}" in
    success|honest-failure) ;;
    *) usage; exit 2 ;;
esac

# Derive BASE and BASENAME directly from SOURCE for clarity.
BASE="${SOURCE%.excalidraw}"
PNG="${BASE}.png"
REPORT="${BASE}.verifier-report.json"
DIR="$(dirname "${SOURCE}")"
BASENAME="$(basename "${BASE}")"

FAIL=0
pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAIL=$(( FAIL + 1 )); }

# Source presence — early hard exit if missing (later asserts depend on it).
if [[ ! -f "${SOURCE}" ]]; then
    fail "source not found: ${SOURCE}"
    echo "Summary: ${FAIL} fail"
    exit 1
fi

if jq empty "${SOURCE}" >/dev/null 2>&1; then
    pass "source is valid JSON"
else
    fail "source is not valid JSON: ${SOURCE}"
fi

# Sibling PNG presence + non-empty.
if [[ -f "${PNG}" ]] && [[ -s "${PNG}" ]]; then
    pass "sibling PNG present and non-empty: ${PNG}"
else
    fail "sibling PNG missing or empty: ${PNG}"
fi

# Sibling verifier-report presence, validity, schema, passed value, issue count.
if [[ -f "${REPORT}" ]] && jq empty "${REPORT}" >/dev/null 2>&1; then
    pass "verifier report present and valid JSON: ${REPORT}"

    if jq -e 'has("passed") and has("checked_at") and has("source") and has("png") and has("issues")' "${REPORT}" >/dev/null; then
        pass "verifier report has all 5 top-level keys (passed, checked_at, source, png, issues)"
    else
        fail "verifier report missing one of the 5 top-level keys"
    fi

    case "${MODE}" in
        success)
            if jq -e '.passed == true' "${REPORT}" >/dev/null; then
                pass "verifier reports passed=true"
            else
                fail "verifier reports passed != true (mode=success expects true)"
            fi
            ;;
        honest-failure)
            if jq -e '.passed == false' "${REPORT}" >/dev/null; then
                pass "verifier reports passed=false"
            else
                fail "verifier reports passed != false (mode=honest-failure expects false)"
            fi
            if jq -e '(.issues | length) > 0' "${REPORT}" >/dev/null; then
                pass "verifier report has at least one issue"
            else
                fail "verifier report has zero issues (mode=honest-failure expects >= 1)"
            fi
            ;;
    esac

    # Staleness: report's checked_at must be at least as recent as the source's mtime.
    # Soft assert — if the timestamp cannot be parsed (e.g., synthetic test fixture),
    # warn and skip rather than failing.
    #
    # NOTE: date -d and stat -c are GNU coreutils extensions (Linux-only).
    # They are used here only for a soft/warn-and-skip assert; the script remains
    # functional on macOS but this staleness check will silently skip there.
    CHECKED_AT="$(jq -r '.checked_at // empty' "${REPORT}")"
    if [[ -n "${CHECKED_AT}" ]]; then
        REPORT_EPOCH="$(date -d "${CHECKED_AT}" +%s 2>/dev/null || echo "")"
        SOURCE_EPOCH="$(stat -c %Y "${SOURCE}" 2>/dev/null || echo "")"
        if [[ -n "${REPORT_EPOCH}" ]] && [[ -n "${SOURCE_EPOCH}" ]]; then
            if [[ "${REPORT_EPOCH}" -ge "${SOURCE_EPOCH}" ]]; then
                pass "report checked_at (${CHECKED_AT}) is not older than source mtime"
            else
                fail "STALE: report checked_at (${CHECKED_AT}) is older than source mtime — re-run the specialist on this scenario"
            fi
        else
            echo "WARN: could not compare report checked_at to source mtime (parse failure); skipping staleness assert"
        fi
    fi
else
    fail "verifier report missing or not valid JSON: ${REPORT}"
fi

# Artefact discipline — no suffixed siblings allowed.
# grep -iEn '\b(done|completed|successfully|ready)\b' is the forbidden-token regex below;
# here we glob for known forbidden artefact suffixes per LOOP-03.
#
# Save and restore the caller's prior nullglob state so we do not silently change
# the shell option for the remainder of the script or any sourcing context.
_nullglob_was_set=0
shopt -q nullglob && _nullglob_was_set=1
shopt -s nullglob
BAD=(
    "${DIR}/${BASENAME}".v[0-9]*.excalidraw
    "${DIR}/${BASENAME}"_iter*.excalidraw
    "${DIR}/${BASENAME}"_iter*.png
    "${DIR}/${BASENAME}".bak*
    "${DIR}/${BASENAME}".report-[0-9]*.json
)
if [[ "${_nullglob_was_set}" -eq 0 ]]; then
    shopt -u nullglob
fi

if [[ "${#BAD[@]}" -eq 0 ]]; then
    pass "no suffixed siblings present (artefact discipline)"
else
    fail "suffixed siblings present (artefact discipline violated):"
    for f in "${BAD[@]}"; do
        echo "  - ${f}"
    done
fi

# Honest-failure: optional --final-message file contains required tokens
# and lacks forbidden success tokens (case-insensitive, word-bounded).
if [[ "${MODE}" = "honest-failure" ]]; then
    if [[ -n "${FINAL_MSG}" ]]; then
        if [[ -f "${FINAL_MSG}" ]] && [[ -s "${FINAL_MSG}" ]]; then
            pass "final-message file present and non-empty: ${FINAL_MSG}"
            for TOKEN in "Failed PNG:" "Source:" "Report:" "Outstanding issues:"; do
                if grep -F -q "${TOKEN}" "${FINAL_MSG}"; then
                    pass "final-message contains honest-failure token: ${TOKEN}"
                else
                    fail "final-message missing honest-failure token: ${TOKEN}"
                fi
            done
            # Word-bounded, case-insensitive forbidden-token scan.
            FORBIDDEN="$(grep -iEn '\b(done|completed|successfully|ready)\b' "${FINAL_MSG}" || true)"
            if [[ -z "${FORBIDDEN}" ]]; then
                pass "final-message contains no forbidden success tokens"
            else
                fail "final-message contains forbidden success token(s):"
                echo "${FORBIDDEN}"
            fi
        else
            fail "final-message file missing or empty: ${FINAL_MSG}"
        fi
    else
        echo "WARN: --final-message not provided; skipping H5 (operator must inspect the message manually for the LOOP-02 honest-failure template)"
    fi
fi

echo "Summary: ${FAIL} fail"
[[ "${FAIL}" -eq 0 ]] && exit 0 || exit 1
