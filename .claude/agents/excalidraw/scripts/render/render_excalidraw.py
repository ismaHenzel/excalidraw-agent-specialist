"""Render Excalidraw JSON to PNG using Playwright + headless Chromium.

Usage:
    uv run python render_excalidraw.py <path-to-file.excalidraw> [--output path.png] [--scale 2] [--width 1920]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import base64
import mimetypes
from pathlib import Path


def validate_excalidraw(data: dict) -> list[str]:
    """Validate Excalidraw JSON structure. Returns list of errors (empty = valid)."""
    errors: list[str] = []

    if data.get("type") != "excalidraw":
        errors.append(f"Expected type 'excalidraw', got '{data.get('type')}'")

    if "elements" not in data:
        errors.append("Missing 'elements' array")
    elif not isinstance(data["elements"], list):
        errors.append("'elements' must be an array")
    elif len(data["elements"]) == 0:
        errors.append("'elements' array is empty — nothing to render")

    return errors


def compute_bounding_box(elements: list[dict]) -> tuple[float, float, float, float]:
    """Compute bounding box (min_x, min_y, max_x, max_y) across all elements."""
    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")

    for el in elements:
        if el.get("isDeleted"):
            continue
        x = el.get("x", 0)
        y = el.get("y", 0)
        w = el.get("width", 0)
        h = el.get("height", 0)

        # For arrows/lines, points array defines the shape relative to x,y
        if el.get("type") in ("arrow", "line") and "points" in el:
            for px, py in el["points"]:
                min_x = min(min_x, x + px)
                min_y = min(min_y, y + py)
                max_x = max(max_x, x + px)
                max_y = max(max_y, y + py)
        else:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x + abs(w))
            max_y = max(max_y, y + abs(h))

    if min_x == float("inf"):
        return (0, 0, 800, 600)

    return (min_x, min_y, max_x, max_y)


def embed_images(data: dict, excalidraw_dir: Path):
    """Embed local images from 'file_path' into the 'files' object as Base64.

    Relative image paths are resolved in this order:
      1. Against the input .excalidraw file's directory.
      2. Against $EXCALIDRAW_ASSETS_DIR (used by render_docker.sh to expose the
         agent's icons/ folder regardless of where the input file lives).
    """
    if "files" not in data:
        data["files"] = {}

    assets_dir_env = os.environ.get("EXCALIDRAW_ASSETS_DIR")
    assets_dir = Path(assets_dir_env) if assets_dir_env else None

    elements = data.get("elements", [])
    for el in elements:
        if el.get("type") == "image" and "file_path" in el:
            raw_path = Path(el["file_path"])
            if raw_path.is_absolute():
                file_path = raw_path
            else:
                file_path = excalidraw_dir / raw_path
                if not file_path.exists() and assets_dir is not None:
                    fallback = assets_dir / raw_path
                    if fallback.exists():
                        file_path = fallback

            if file_path.exists():
                try:
                    # Create a unique fileId if not present
                    file_id = el.get("fileId") or f"file_{file_path.stem}_{hash(str(file_path)) % 10000}"
                    el["fileId"] = file_id
                    
                    mime_type, _ = mimetypes.guess_type(file_path)
                    mime_type = mime_type or "image/png"
                    
                    with open(file_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
                        dataURL = f"data:{mime_type};base64,{encoded_string}"
                        
                    data["files"][file_id] = {
                        "mimeType": mime_type,
                        "id": file_id,
                        "dataURL": dataURL,
                        "created": 123456789
                    }
                except Exception as e:
                    print(f"WARNING: Failed to embed image {file_path}: {e}", file=sys.stderr)
            else:
                print(f"WARNING: Image file not found: {file_path}", file=sys.stderr)


def render(
    excalidraw_path: Path,
    output_path: Path | None = None,
    scale: int = 2,
    max_width: int = 1920,
) -> Path:
    """Render an .excalidraw file to PNG. Returns the output PNG path."""
    # Import playwright here so validation errors show before import errors
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed.", file=sys.stderr)
        sys.exit(1)

    # Read and validate
    raw = excalidraw_path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {excalidraw_path}: {e}", file=sys.stderr)
        sys.exit(1)

    errors = validate_excalidraw(data)
    if errors:
        print(f"ERROR: Invalid Excalidraw file:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    # Embed local images
    embed_images(data, excalidraw_path.parent)

    # Compute viewport size from element bounding box
    elements = [e for e in data["elements"] if not e.get("isDeleted")]
    min_x, min_y, max_x, max_y = compute_bounding_box(elements)
    padding = 80
    diagram_w = max_x - min_x + padding * 2
    diagram_h = max_y - min_y + padding * 2

    # Cap viewport width, let height be natural
    vp_width = min(int(diagram_w), max_width)
    vp_height = max(int(diagram_h), 600)

    # Output path
    if output_path is None:
        output_path = excalidraw_path.with_suffix(".png")

    # Template path (same directory as this script)
    template_path = Path(__file__).parent / "render_template.html"
    if not template_path.exists():
        print(f"ERROR: Template not found at {template_path}", file=sys.stderr)
        sys.exit(1)

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        except Exception as e:
            print(f"ERROR: Failed to launch browser: {e}", file=sys.stderr)
            sys.exit(1)

        page = browser.new_page(
            viewport={"width": vp_width, "height": vp_height},
            device_scale_factor=scale,
        )
        page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))
        page.on("requestfailed", lambda request: print(f"REQUEST FAILED: {request.url}"))

        # Load the template
        template_content = template_path.read_text(encoding="utf-8")
        page.set_content(template_content, wait_until="load")

        # Wait for the ES module to load
        try:
            page.wait_for_function("window.__moduleReady === true", timeout=30000)
        except Exception:
            print(f"ERROR: Module ready timeout.", file=sys.stderr)
            raise

        # Inject the diagram data and render
        json_str = json.dumps(data)
        result = page.evaluate(f"window.renderDiagram({json_str})")

        if not result or not result.get("success"):
            error_msg = result.get("error", "Unknown render error") if result else "renderDiagram returned null"
            print(f"ERROR: Render failed: {error_msg}", file=sys.stderr)
            browser.close()
            sys.exit(1)

        # Wait for render completion signal
        page.wait_for_function("window.__renderComplete === true", timeout=15000)

        # Screenshot the SVG element
        svg_el = page.query_selector("#root svg")
        if svg_el is None:
            print("ERROR: No SVG element found after render.", file=sys.stderr)
            browser.close()
            sys.exit(1)

        svg_el.screenshot(path=str(output_path))
        browser.close()

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Excalidraw JSON to PNG")
    parser.add_argument("input", type=Path, help="Path to .excalidraw JSON file")
    parser.add_argument("--output", "-o", type=Path, default=None, help="Output PNG path (default: same name with .png)")
    parser.add_argument("--scale", "-s", type=int, default=2, help="Device scale factor (default: 2)")
    parser.add_argument("--width", "-w", type=int, default=1920, help="Max viewport width (default: 1920)")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"ERROR: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    png_path = render(args.input, args.output, args.scale, args.width)
    print(str(png_path))


if __name__ == "__main__":
    main()
