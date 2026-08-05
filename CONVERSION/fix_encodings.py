#!/usr/bin/env python3
from pathlib import Path
from tkinter import Tk, filedialog

root = Tk()
root.withdraw()
folder = filedialog.askdirectory(title="Select script folder")
root.destroy()

if not folder:
    raise SystemExit

ROOT = Path(folder)

EXTENSIONS = {".d"}


POLISH_CHARS = set(
    "ąćęłńóśźżĄĆĘŁŃÓŚŹŻ"
)

BAD_MOJIBAKE = (
    "Ä",
    "Å",
    "Ă",
    "Ĺ",
    "â€",
    "Ã",
    "Â",
    "Ð",
    "Ø",
    "œ",
    "ž",
    "š",
)


def score_text(text):
    score = 0

    # Correct Polish letters are good
    score += sum(text.count(c) for c in POLISH_CHARS) * 5

    # Mojibake markers are bad
    score -= sum(text.count(c) for c in BAD_MOJIBAKE) * 10

    # Replacement characters are very bad
    score -= text.count("�") * 100

    return score


def repair_utf8_mojibake(text):
    """
    Fix:
    UTF-8 bytes interpreted as CP1252 and saved as UTF-8
    """
    try:
        fixed = text.encode("cp1252").decode("utf-8")

        if score_text(fixed) > score_text(text):
            return fixed

    except (UnicodeEncodeError, UnicodeDecodeError):
        pass

    return text


def decode_best(raw):
    candidates = []

    encodings = (
        "utf-8",
        "cp1250",
        "cp1252",
        "latin1",
    )

    for enc in encodings:
        try:
            text = raw.decode(enc)
            text = repair_utf8_mojibake(text)

            candidates.append(
                (score_text(text), text, enc)
            )

        except UnicodeDecodeError:
            pass

    if not candidates:
        raise UnicodeDecodeError(
            "unknown",
            raw,
            0,
            1,
            "No usable encoding"
        )

    candidates.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return candidates[0]


for path in ROOT.rglob("*"):

    if not path.is_file():
        continue

    if path.suffix.lower() not in EXTENSIONS:
        continue

    raw = path.read_bytes()

    try:
        score, fixed, encoding = decode_best(raw)
        print("FILE:", path)
        print("ENCODING CHOSEN:", encoding)
        print("BEFORE:", raw.decode("utf-8", errors="replace")[:200])
        print("AFTER :", fixed[:200])
        current = None
        try:
            current = raw.decode("utf-8")
        except:
            pass

        if current != fixed:
            backup = path.with_suffix(path.suffix + ".bak")
            backup.write_bytes(raw)

            path.write_text(
                fixed,
                encoding="utf-8",
                newline=""
            )

            print(
                f"[FIXED] {path} ({encoding}, score {score})"
            )
        else:
            print(f"[OK] {path}")

    except Exception as e:
        print(f"[FAILED] {path}: {e}")