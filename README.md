# tex2img.py

`tex2img.py` is a Python program that converts LaTeX code into a `.png` image. It supports saving the generated image to a file or copying it directly to the clipboard (Windows only).

## Features

- Converts LaTeX code to a high-resolution PNG image.
- Copies the PNG image to the clipboard (Windows only).
- Saves the PNG image to a specified file.
- Simple and lightweight.

## Requirements

- Python 3.x
- [Pillow](https://pypi.org/project/Pillow/) (Python Imaging Library)
- [pywin32](https://pypi.org/project/pywin32/) (required for clipboard support on Windows)
- LaTeX tools:
  - `latex` (to compile `.tex` files)
  - `dvipng` (to convert `.dvi` files to PNG images)

Make sure the LaTeX tools are installed and accessible in your system's PATH.

## Usage
```bash
python tex2img.py [-h] [-c] [-s filename] [tex code]
```

### Arguments:
- `-h`: Displays usage information.
- `-c`: Copies the generated PNG image to the clipboard (Windows only).
- `-s filename`: Saves the PNG image to the specified file.
- `[tex code]`: The LaTeX code to convert.
