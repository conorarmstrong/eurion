import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
import io
import sys
import argparse

def hex_to_rgb(hex_color):
    """Converts a hex color (e.g., A0A0A0) to an RGB tuple with values between 0 and 1."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError("Invalid color format. Use a 6-character hex code (e.g., FFCCDD).")

    r, g, b = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    return r, g, b

def draw_eurion(canvas_obj, x, y, color_rgb, size, opacity):
    """
    Draws a small Eurion constellation at the given (x, y) position with full transparency support.
    """
    constellation = [
        (x, y), (x + size * 1.5, y - size * 0.5),
        (x + size * 3, y - size * 1), (x + size * 2, y + size),
        (x + size * 4, y + size * 0.5)
    ]

    # Apply transparency to both stroke (lines) and fill
    canvas_obj.setFillAlpha(opacity)
    canvas_obj.setStrokeAlpha(opacity)
    canvas_obj.setFillColorRGB(*color_rgb)
    canvas_obj.setStrokeColorRGB(*color_rgb)

    for cx, cy in constellation:
        canvas_obj.circle(cx, cy, size / 5, stroke=1, fill=1)  # Small dots

def create_eurion_overlay(width, height, color_rgb, density_x, density_y, constellation_size, opacity):
    """
    Generates an overlay PDF with multiple Eurion constellations tiled across the entire page.
    """
    packet = io.BytesIO()
    overlay_canvas = canvas.Canvas(packet, pagesize=(width, height))

    # Convert float dimensions to integers for range() to work
    width = int(width)
    height = int(height)

    spacing_x = max(10, width / density_x)  # Floating point spacing for horizontal
    spacing_y = max(10, height / density_y)  # Floating point spacing for vertical

    # Generate a grid of Eurion constellations using while loops
    x = 0
    while x < width:
        y = 0
        while y < height:
            draw_eurion(overlay_canvas, x, y, color_rgb, constellation_size, opacity)
            y += spacing_y  # Increment using float
        x += spacing_x  # Increment using float

    overlay_canvas.save()
    packet.seek(0)
    return fitz.open("pdf", packet.read())

def overlay_eurion(input_pdf_path, output_pdf_path, color_hex, density_x, density_y, constellation_size, opacity):
    # Convert hex color to RGB
    color_rgb = hex_to_rgb(color_hex)

    # Open the input PDF
    doc = fitz.open(input_pdf_path)

    # Create an empty PDF to store modified pages
    output_pdf = fitz.open()

    for page_num in range(len(doc)):
        page = doc[page_num]
        width, height = page.rect.width, page.rect.height

        # Generate the Eurion overlay for this page
        overlay_pdf = create_eurion_overlay(width, height, color_rgb, density_x, density_y, constellation_size, opacity)

        # Copy the original page into the output document
        new_page = output_pdf.new_page(width=width, height=height)

        # Insert the original page content
        new_page.show_pdf_page(page.rect, doc, page_num)

        # Overlay the Eurion pattern
        new_page.show_pdf_page(page.rect, overlay_pdf, 0)

    # Save the output PDF
    output_pdf.save(output_pdf_path)
    output_pdf.close()
    doc.close()

def main():
    parser = argparse.ArgumentParser(
        description="Overlay a PDF with multiple Eurion constellations to prevent photocopying.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter  # Shows default values in help text
    )

    parser.add_argument("-i", "--input", required=True, help="Path to the input PDF file")
    parser.add_argument("-o", "--output", required=True, help="Path to the output PDF file")
    parser.add_argument("-c", "--color", default="A0A0A0", help="Hex color for the Eurion stars")
    parser.add_argument("-dx", "--density-x", type=int, default=25, help="Horizontal density (number of constellations across the width)")
    parser.add_argument("-dy", "--density-y", type=int, default=55, help="Vertical density (number of constellations along the height)")
    parser.add_argument("-s", "--size", type=int, default=5, help="Size of each Eurion constellation")
    parser.add_argument("-t", "--transparency", type=float, default=0.1, help="Transparency of the constellations (0.0 - fully transparent, 1.0 - fully opaque)")

    args = parser.parse_args()

    try:
        overlay_eurion(args.input, args.output, args.color, args.density_x, args.density_y, args.size, args.transparency)
        print(f"Processed file saved as {args.output} with Eurion color #{args.color}, horizontal density {args.density_x}, vertical density {args.density_y}, size {args.size}, and transparency {args.transparency}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
