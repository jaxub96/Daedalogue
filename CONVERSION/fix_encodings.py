#!/usr/bin/env python3
"""
Normalize text files to UTF-8.

Handles three cases:
1. Already valid UTF-8            -> leave unchanged
2. Windows-1250 encoded           -> convert to UTF-8
3. UTF-8 mojibake from CP1250     -> repair and save as UTF-8

The script processes all matching files recursively from the directory
where this script is located.

A .bak backup is created before any file is modified.
"""

from pathlib import Path
from tkinter import Tk, filedialog

# Hide the main Tk window
root = Tk()
root.withdraw()
root.attributes("-topmost", True)

folder = filedialog.askdirectory(
    title="Select the folder containing the script files"
)

root.destroy()

if not folder:
    print("No folder selected.")
    raise SystemExit

ROOT = Path(folder)

# File types to process
EXTENSIONS = {
    ".d"
}

# Characters commonly seen when CP1250 text was misinterpreted as CP1252
MOJIBAKE_CHARS = set("³œ¿¹æêñÆ£ÐØ")



def looks_like_mojibake(text: str) -> bool:
    """Heuristic for Polish CP1250 mojibake."""
    count = sum(text.count(c) for c in MOJIBAKE_CHARS)

    # Common broken fragments
    patterns = (
        "siê",
        "k³",
        "³a",
        "¿",
        "œ",
        "¹",
        "ê",
        "æ",
        "ñ",
    )

    count += sum(text.count(p) for p in patterns)

    return count >= 2


def repair_mojibake(text: str) -> str:
    """Undo CP1250 -> CP1252 mojibake."""
    return text.encode("cp1252").decode("cp1250")


converted = 0
repaired = 0
unchanged = 0
failed = 0

for path in ROOT.rglob("*"):
    if not path.is_file():
        continue

    if path.suffix.lower() not in EXTENSIONS:
        continue

    try:
        raw = path.read_bytes()

        # Case 1: Valid UTF-8
        try:
            text = raw.decode("utf-8")

            if looks_like_mojibake(text):
                fixed = repair_mojibake(text)

                if fixed != text:
                    path.with_suffix(path.suffix + ".bak").write_bytes(raw)
                    path.write_text(fixed, encoding="utf-8", newline="")
                    repaired += 1
                    print(f"[REPAIRED ] {path}")
                else:
                    unchanged += 1
                    print(f"[UNCHANGED] {path}")
            else:
                unchanged += 1
                print(f"[UTF-8    ] {path}")

            continue

        except UnicodeDecodeError:
            pass

        # Case 2: Assume CP1250
        text = raw.decode("cp1250")

        path.with_suffix(path.suffix + ".bak").write_bytes(raw)
        path.write_text(text, encoding="utf-8", newline="")

        converted += 1
        print(f"[CONVERTED] {path}")

    except Exception as e:
        failed += 1
        print(f"[FAILED   ] {path}: {e}")

print()
print("Summary")
print("-------")
print(f"UTF-8 unchanged : {unchanged}")
print(f"CP1250 converted: {converted}")
print(f"Mojibake fixed  : {repaired}")
print(f"Failed          : {failed}")