# Eurion PDF Protection Tool

Eurion PDF Protection is a Python tool that overlays a PDF with a grid of **Eurion constellations**, an anti-counterfeiting measure commonly found on banknotes. This tool helps prevent unauthorized photocopying by making the document harder to reproduce using scanners.

## Features
- **Customizable density**: Separate control for horizontal (`-dx`) and vertical (`-dy`) spacing.
- **Adjustable size**: Modify the size of each Eurion constellation (`-s`).
- **Transparency control**: Set the opacity of the constellations (`-t`).
- **Custom color**: Specify any hex color for the Eurion stars (`-c`).
- **Command-line interface**: Simple arguments for full customization.

## Installation
Ensure you have Python 3 installed, then install the required dependencies:
```sh
pip install pymupdf reportlab argparse
```

## Usage
Run the script with the desired settings:
```sh
python eurion.py -i input.pdf -o output.pdf
```
### Example with Custom Settings
```sh
python eurion.py -i input.pdf -o protected.pdf -dx 50 -dy 80 -s 5 -t 0.3 -c FFCCDD
```
- `-dx 50`: 50 constellations across the width
- `-dy 80`: 80 constellations down the page
- `-s 5`: Size of each constellation
- `-t 0.3`: 30% opacity
- `-c FFCCDD`: Light pink stars

## Options
| Option | Description | Default |
|--------|-------------|---------|
| `-i`, `--input` | Input PDF file | Required |
| `-o`, `--output` | Output PDF file | Required |
| `-dx`, `--density-x` | Horizontal density | 25 |
| `-dy`, `--density-y` | Vertical density | 55 |
| `-s`, `--size` | Size of Eurion constellations | 5 |
| `-t`, `--transparency` | Opacity (0.0 - 1.0) | 0.1 |
| `-c`, `--color` | Hex color of constellations | `A0A0A0` (light grey) |

## Example Output
This tool applies a **subtle, yet scanner-detectable** Eurion pattern across the PDF pages, making it more resistant to unauthorized reproduction.

## Repository
[GitHub Repository](https://github.com/conorarmstrong/eurion)

## Author
Developed by **Conor Armstrong**
📧 Email: [conorarmstrong@gmail.com](mailto:conorarmstrong@gmail.com)
