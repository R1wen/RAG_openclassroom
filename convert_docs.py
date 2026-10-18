from pathlib import Path

DATA_DIR = Path("data")

for path in DATA_DIR.rglob("*"):
    if path.is_file():
        print(path, path.suffix.lower())
