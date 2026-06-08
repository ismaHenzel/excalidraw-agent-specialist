import json
import sys
import os
import re
from pathlib import Path


MONOSPACE_ADVANCE_RATIO = 0.6
ENDPOINT_TOLERANCE_PX = 8

EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "☀-➿"
    "\U0001F1E6-\U0001F1FF"
    "]"
)

EMOJI_TO_ICON = {
    "✅": "success_icon.png",
    "❌": "failure_icon.png",
    "⚠": "failure_icon.png",
}


def issue(check, element_id, severity, detail, suggested_fix):
    return {
        "check": check,
        "element_id": element_id,
        "severity": severity,
        "detail": detail,
        "suggested_fix": suggested_fix,
    }


def _bbox_contains_point(sx, sy, sw, sh, px, py):
    return sx <= px <= sx + sw and sy <= py <= sy + sh


def _on_rectangle_border(px, py, sx, sy, sw, sh, tol):
    outer = _bbox_contains_point(sx - tol, sy - tol, sw + 2 * tol, sh + 2 * tol, px, py)
    if not outer:
        return False
    if sw - 2 * tol <= 0 or sh - 2 * tol <= 0:
        return True
    inner = _bbox_contains_point(sx + tol, sy + tol, sw - 2 * tol, sh - 2 * tol, px, py)
    return not inner


def _on_ellipse_border(px, py, sx, sy, sw, sh, tol):
    if sw <= 0 or sh <= 0:
        return False
    cx = sx + sw / 2.0
    cy = sy + sh / 2.0
    a = sw / 2.0
    b = sh / 2.0
    if a == 0 or b == 0:
        return False
    nx = (px - cx) / a
    ny = (py - cy) / b
    d = (nx * nx + ny * ny) ** 0.5
    return abs(d - 1.0) * min(a, b) <= tol


def _distance_point_to_segment(px, py, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5
    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    if t < 0:
        t = 0
    elif t > 1:
        t = 1
    qx = x1 + t * dx
    qy = y1 + t * dy
    return ((px - qx) ** 2 + (py - qy) ** 2) ** 0.5


def _on_diamond_border(px, py, sx, sy, sw, sh, tol):
    top = (sx + sw / 2.0, sy)
    right = (sx + sw, sy + sh / 2.0)
    bottom = (sx + sw / 2.0, sy + sh)
    left = (sx, sy + sh / 2.0)
    segments = [(top, right), (right, bottom), (bottom, left), (left, top)]
    dmin = float("inf")
    for (x1, y1), (x2, y2) in segments:
        d = _distance_point_to_segment(px, py, x1, y1, x2, y2)
        if d < dmin:
            dmin = d
    return dmin <= tol


def _shape_bbox(el):
    return (
        el.get("x", 0),
        el.get("y", 0),
        el.get("width", 0),
        el.get("height", 0),
    )


def _find_containing_shape(text_el, elements):
    tx = text_el.get("x", 0)
    ty = text_el.get("y", 0)
    tw = text_el.get("width", 0)
    th = text_el.get("height", 0)
    candidates = []
    for el in elements:
        if el.get("type") not in ("rectangle", "ellipse", "diamond"):
            continue
        sx, sy, sw, sh = _shape_bbox(el)
        if sx <= tx and sy <= ty and sx + sw >= tx + tw and sy + sh >= ty + th:
            candidates.append((sw * sh, el))
    if not candidates:
        return None
    candidates.sort(key=lambda pair: pair[0])
    return candidates[0][1]


def check_raw_emoji_in_text(elements):
    issues = []
    for el in elements:
        if el.get("type") != "text":
            continue
        if el.get("fontFamily") != 3:
            continue
        text = el.get("text", "")
        el_id = el.get("id", "unknown")
        for match in EMOJI_RE.finditer(text):
            ch = match.group(0)
            cp = ord(ch)
            if ch in EMOJI_TO_ICON:
                fix = (
                    "Prefer an image element pointing to .claude/agents/excalidraw/icons/"
                    + EMOJI_TO_ICON[ch]
                    + " for text element id: "
                    + el_id
                    + " (an icon exists for U+"
                    + format(cp, "04X")
                    + "); keep the raw emoji only if no icon matches and the user did not opt out of emojis."
                )
            else:
                fix = (
                    "Raw emoji U+"
                    + format(cp, "04X")
                    + " in text element id: "
                    + el_id
                    + " is an allowed fallback when no matching icon exists; use it sparingly (titles / topic markers, not plain body text). If an icon under .claude/agents/excalidraw/icons/ matches, prefer it."
                )
            issues.append(
                issue(
                    "raw_emoji_in_text",
                    el_id,
                    "warning",
                    "Text element contains raw emoji codepoint U+"
                    + format(cp, "04X")
                    + " (allowed as an icon fallback; the visual missing_glyph_box check is the hard gate if it fails to render).",
                    fix,
                )
            )
    return issues


def check_text_missing_dimensions(elements):
    issues = []
    for el in elements:
        if el.get("type") != "text":
            continue
        if el.get("width") and el.get("height"):
            continue
        el_id = el.get("id", "unknown")
        issues.append(
            issue(
                "text_missing_dimensions",
                el_id,
                "error",
                "Text element has no width/height. It renders in the PNG export (exportToSvg measures text on the fly) "
                "but collapses to a zero-size, invisible box when the .excalidraw is opened in the Excalidraw editor.",
                "Add explicit width and height to text element id: "
                + el_id
                + " (monospace: width = len(longest line) * fontSize * 0.6, height = lines * fontSize * lineHeight), "
                + "plus lineHeight, textAlign, verticalAlign, and originalText.",
            )
        )
    return issues


def check_text_overflow_static(elements):
    issues = []
    for el in elements:
        if el.get("type") != "text":
            continue
        if el.get("containerId"):
            continue
        text = el.get("text", "")
        font_size = el.get("fontSize", 20)
        estimated_width = len(text) * MONOSPACE_ADVANCE_RATIO * font_size
        container = _find_containing_shape(el, elements)
        if container is None:
            continue
        shape_width = container.get("width", 0)
        if estimated_width <= shape_width:
            continue
        text_id = el.get("id", "unknown")
        shape_id = container.get("id", "unknown")
        threshold = int(estimated_width) + 20
        issues.append(
            issue(
                "text_overflow_static",
                text_id,
                "error",
                "Text '"
                + text
                + "' (~"
                + str(int(estimated_width))
                + "px @ fontSize "
                + str(font_size)
                + ") exceeds container '"
                + shape_id
                + "' width ("
                + str(shape_width)
                + "px).",
                "Increase rectangle id: "
                + shape_id
                + " width from "
                + str(shape_width)
                + " to >="
                + str(threshold)
                + ", or shorten the label in text element id: "
                + text_id
                + ".",
            )
        )
    return issues


def check_arrow_endpoint_unanchored(elements):
    issues = []
    shapes = [el for el in elements if el.get("type") in ("rectangle", "ellipse", "diamond")]
    for el in elements:
        if el.get("type") != "arrow":
            continue
        points = el.get("points", [])
        if len(points) < 1:
            continue
        last = points[-1]
        ax = el.get("x", 0)
        ay = el.get("y", 0)
        px = ax + last[0]
        py = ay + last[1]
        anchored = False
        for shape in shapes:
            sx, sy, sw, sh = _shape_bbox(shape)
            stype = shape.get("type")
            if stype == "rectangle":
                if _on_rectangle_border(px, py, sx, sy, sw, sh, ENDPOINT_TOLERANCE_PX):
                    anchored = True
                    break
            elif stype == "ellipse":
                if _on_ellipse_border(px, py, sx, sy, sw, sh, ENDPOINT_TOLERANCE_PX):
                    anchored = True
                    break
            elif stype == "diamond":
                if _on_diamond_border(px, py, sx, sy, sw, sh, ENDPOINT_TOLERANCE_PX):
                    anchored = True
                    break
        if anchored:
            continue
        arrow_id = el.get("id", "unknown")
        issues.append(
            issue(
                "arrow_endpoint_unanchored",
                arrow_id,
                "error",
                "Arrow last point ("
                + format(px, ".0f")
                + ", "
                + format(py, ".0f")
                + ") is not within "
                + str(ENDPOINT_TOLERANCE_PX)
                + "px of any shape border.",
                "Adjust arrow id: "
                + arrow_id
                + " last point to land on the border of an existing rectangle/ellipse/diamond within "
                + str(ENDPOINT_TOLERANCE_PX)
                + "px.",
            )
        )
    return issues


def _resolve_image_path(raw_path, excalidraw_parent_dir):
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate if candidate.exists() else None
    direct = excalidraw_parent_dir / candidate
    if direct.exists():
        return direct
    assets_env = os.environ.get("EXCALIDRAW_ASSETS_DIR")
    if assets_env:
        fallback = Path(assets_env) / candidate
        if fallback.exists():
            return fallback
    return None


def check_image_path_unresolvable(elements, excalidraw_parent_dir):
    issues = []
    for el in elements:
        if el.get("type") != "image":
            continue
        raw_path = el.get("file_path")
        if not raw_path:
            continue
        resolved = _resolve_image_path(raw_path, excalidraw_parent_dir)
        if resolved is not None:
            continue
        image_id = el.get("id", "unknown")
        issues.append(
            issue(
                "image_path_unresolvable",
                image_id,
                "error",
                "Image element file_path '"
                + str(raw_path)
                + "' does not resolve to any existing file.",
                "Update image element id: "
                + image_id
                + " file_path to a valid PNG under .claude/agents/excalidraw/icons/.",
            )
        )
    return issues


def check_roughness_nonzero(elements):
    issues = []
    for el in elements:
        if "roughness" not in el:
            continue
        if el.get("roughness") == 0:
            continue
        el_id = el.get("id", "unknown")
        issues.append(
            issue(
                "roughness_nonzero",
                el_id,
                "warning",
                "Element has roughness="
                + str(el.get("roughness"))
                + ", expected 0 (Architect's Precision).",
                "Set element id: " + el_id + " roughness to 0.",
            )
        )
    return issues


def check_fontfamily_nonmonospace(elements):
    issues = []
    for el in elements:
        if el.get("type") != "text":
            continue
        if "fontFamily" not in el:
            continue
        if el.get("fontFamily") == 3:
            continue
        el_id = el.get("id", "unknown")
        issues.append(
            issue(
                "fontfamily_nonmonospace",
                el_id,
                "warning",
                "Text element has fontFamily="
                + str(el.get("fontFamily"))
                + ", expected 3 (monospace).",
                "Set text element id: "
                + el_id
                + " fontFamily to 3 (Cascadia Code monospace).",
            )
        )
    return issues


def check_arrow_points_too_few(elements):
    issues = []
    for el in elements:
        if el.get("type") != "arrow":
            continue
        points = el.get("points", [])
        if len(points) >= 3:
            continue
        el_id = el.get("id", "unknown")
        issues.append(
            issue(
                "arrow_points_too_few",
                el_id,
                "warning",
                "Arrow has "
                + str(len(points))
                + " points, expected >=3 for elbow routing.",
                "Add an intermediate point to arrow id: "
                + el_id
                + " to form a 90-degree elbow per kb/feedback-loop.md and the Architect's Precision rules.",
            )
        )
    return issues


def check_arrow_not_elbow(elements):
    issues = []
    for el in elements:
        if el.get("type") != "arrow":
            continue
        el_id = el.get("id", "unknown")
        roundness = el.get("roundness")
        rounded = isinstance(roundness, dict) and roundness.get("type") == 2
        elbowed = el.get("elbowed") is True
        if elbowed and not rounded:
            continue
        problems = []
        if rounded:
            problems.append("has roundness {type:2} which curves the corner")
        if not elbowed:
            problems.append("is missing elbowed:true")
        issues.append(
            issue(
                "arrow_not_elbow",
                el_id,
                "warning",
                "Arrow " + " and ".join(problems) + "; it is not a sharp 90-degree elbow connector.",
                "Set arrow id: "
                + el_id
                + " to \"elbowed\": true with \"roundness\": null and orthogonal right-angle points "
                + "(e.g. [[0,0],[dx,0],[dx,dy]]). Never use roundness {type:2} on an arrow.",
            )
        )
    return issues


def check_sequence_activation_center_x(elements):
    """Check that each activation-bar rectangle is centered on its nearest lifeline line.

    Heuristic:
    - Lifeline candidates: `line` elements with strokeStyle == "dashed" and width == 0
    - Activation-bar candidates: `rectangle` elements with 10 <= width <= 16
    For each bar, find lifelines whose x is within 8px of the bar center. If any such
    lifeline's x differs from the bar center by more than 1px, report an error.

    Issue key: activation_bar_center_x_mismatch
    """
    issues = []
    line_elements = [
        e for e in elements
        if e.get("type") == "line"
        and e.get("strokeStyle") == "dashed"
        and e.get("width", 0) == 0
    ]
    activation_bars = [
        e for e in elements
        if e.get("type") == "rectangle"
        and 10 <= e.get("width", 0) <= 16
    ]
    for bar in activation_bars:
        bar_center_x = bar["x"] + bar["width"] / 2
        nearby_lines = [
            ln for ln in line_elements
            if abs(ln["x"] - bar_center_x) < 8
        ]
        for ln in nearby_lines:
            if abs(ln["x"] - bar_center_x) > 1:
                issues.append(
                    issue(
                        "activation_bar_center_x_mismatch",
                        bar.get("id", "unknown"),
                        "error",
                        "Activation bar center x "
                        + format(bar_center_x, ".1f")
                        + " != nearest lifeline x "
                        + format(ln["x"], ".1f")
                        + " (bar id: "
                        + bar.get("id", "unknown")
                        + ").",
                        "Set bar x to "
                        + format(ln["x"] - bar["width"] / 2, ".1f")
                        + " so that bar center ("
                        + format(ln["x"], ".1f")
                        + ") aligns with lifeline x. "
                        + "Formula: bar.x = lifeline_center_x - bar.width / 2.",
                    )
                )
    return issues


def main():
    try:
        if len(sys.argv) < 2:
            print(json.dumps([issue(
                "verifier_internal_error",
                "—",
                "error",
                "Argument missing: expected absolute path to .excalidraw file.",
                "Investigate; this is a verifier bug, not a diagram bug.",
            )]))
            sys.exit(0)

        path = sys.argv[1]

        if not os.path.exists(path):
            print(json.dumps([issue(
                "verifier_internal_error",
                "—",
                "error",
                "File not found: " + path + ".",
                "Investigate; this is a verifier bug, not a diagram bug.",
            )]))
            sys.exit(0)

        try:
            with open(path, "r") as f:
                data = json.load(f)
        except (IOError, OSError) as exc:
            print(json.dumps([issue(
                "verifier_internal_error",
                "—",
                "error",
                "Could not read file " + path + ": " + str(exc) + ".",
                "Investigate; this is a verifier bug, not a diagram bug.",
            )]))
            sys.exit(0)
        except json.JSONDecodeError:
            print(json.dumps([issue(
                "verifier_internal_error",
                "—",
                "error",
                "Not valid JSON: " + path + ".",
                "Investigate; this is a verifier bug, not a diagram bug.",
            )]))
            sys.exit(0)

        elements = data.get("elements", [])
        parent_dir = Path(path).parent

        issues = []
        issues.extend(check_raw_emoji_in_text(elements))
        issues.extend(check_text_missing_dimensions(elements))
        issues.extend(check_text_overflow_static(elements))
        issues.extend(check_arrow_endpoint_unanchored(elements))
        issues.extend(check_image_path_unresolvable(elements, parent_dir))
        issues.extend(check_roughness_nonzero(elements))
        issues.extend(check_fontfamily_nonmonospace(elements))
        issues.extend(check_arrow_points_too_few(elements))
        issues.extend(check_arrow_not_elbow(elements))
        issues.extend(check_sequence_activation_center_x(elements))

        print(json.dumps(issues))
        sys.exit(0)
    except Exception as exc:
        print(json.dumps([issue(
            "verifier_internal_error",
            "—",
            "error",
            "Uncaught helper exception: " + str(exc) + ".",
            "Investigate; this is a verifier bug, not a diagram bug.",
        )]))
        sys.exit(0)


if __name__ == "__main__":
    main()
