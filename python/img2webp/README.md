# img2webp

Converts JPG/PNG images to lossless WebP format via clipboard.

## Usage

1. Select image files in Explorer and copy their paths (`Ctrl+C`)
2. Run the script via Listary or terminal
3. Confirm whether to delete originals

## Setup

```bash
uv venv
uv pip install -r requirements.txt
```

## Compile to exe

```bash
pyinstaller --onefile convert.py
```

Point Listary to `dist\convert.exe`.
