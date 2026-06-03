import json
import sys
import os

def validate_excalidraw(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return False

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {file_path} is not a valid JSON file.")
        return False

    errors = []
    warnings = []

    # 1. Check Metadata
    if data.get("type") != "excalidraw":
        errors.append("Missing or invalid 'type': 'excalidraw' metadata.")
    if "version" not in data:
        errors.append("Missing 'version' metadata.")
    if "elements" not in data:
        errors.append("Missing 'elements' array.")

    elements = data.get("elements", [])
    
    # 2. Check for 'label' property in shapes
    shapes_with_labels = []
    for el in elements:
        if el.get("type") in ["rectangle", "ellipse", "diamond"] and "label" in el:
            shapes_with_labels.append(el.get("id", "unknown"))
    
    if shapes_with_labels:
        errors.append(f"Found 'label' property in shapes: {', '.join(shapes_with_labels)}. Use standalone text elements instead.")

    # 3. Check for standalone text elements
    text_elements = [el for el in elements if el.get("type") == "text"]
    if not text_elements and len(elements) > 2:
        warnings.append("No text elements found. The diagram might be missing labels.")

    # 4. Check for high-contrast colors
    low_contrast_text = []
    for el in text_elements:
        stroke = el.get("strokeColor", "").lower()
        if stroke not in ["#1e1e1e", "#000000", "#000"]:
            low_contrast_text.append(el.get("id", "unknown"))
    
    if low_contrast_text:
        warnings.append(f"Text elements with potentially low contrast strokeColor: {', '.join(low_contrast_text)}. Prefer #1e1e1e.")

    # Report
    print(f"--- Excalidraw Validation Report: {file_path} ---")
    if errors:
        print("ERRORS:")
        for err in errors:
            print(f"  [X] {err}")
    else:
        print("  [✓] Metadata and core structure valid.")

    if warnings:
        print("WARNINGS:")
        for warn in warnings:
            print(f"  [!] {warn}")
    
    print("---------------------------------------------")
    return len(errors) == 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python excalidraw_validator.py <path_to_excalidraw_file>")
        sys.exit(1)
    
    success = validate_excalidraw(sys.argv[1])
    sys.exit(0 if success else 1)
