'''
if d-file is corrupted with mojibake, put it into this directory, and run to fix it. It will convert the file from cp1252 to cp1250 and save it back as utf-8.
'''
from pathlib import Path

script_dir = Path(__file__).parent

for path in script_dir.glob("*.D"):
    try:
        text = path.read_text(encoding="utf-8")
        fixed = text.encode("cp1252").decode("cp1250")
        path.write_text(fixed, encoding="utf-8")
        print("Fixed:", path)
    except Exception as e:
        print("Skipped:", path, e)