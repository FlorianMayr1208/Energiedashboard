#!/usr/bin/env python3
"""
Icon Generator für PWA
Generiert 192x192 und 512x512 PNG Icons
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    """Erstellt ein Icon mit Blitz-Symbol"""
    # Erstelle Bild mit Gradient-Hintergrund
    img = Image.new('RGB', (size, size), color='#667eea')
    draw = ImageDraw.Draw(img)

    # Zeichne Kreis als Hintergrund
    margin = size // 10
    draw.ellipse([margin, margin, size-margin, size-margin], fill='#667eea', outline='#4a5dc7', width=size//50)

    # Zeichne Blitz-Symbol (vereinfacht als Polygon)
    bolt_width = size // 3
    bolt_height = size // 2
    center_x = size // 2
    center_y = size // 2

    # Blitz-Koordinaten (vereinfachte Form)
    bolt = [
        (center_x, center_y - bolt_height//2),  # Oben
        (center_x + bolt_width//4, center_y),   # Mitte rechts
        (center_x - bolt_width//8, center_y),   # Mitte links
        (center_x, center_y + bolt_height//2),  # Unten
        (center_x - bolt_width//4, center_y),   # Mitte links
        (center_x + bolt_width//8, center_y),   # Mitte rechts
    ]

    draw.polygon(bolt, fill='#FFD700', outline='#FFA500', width=size//100)

    # Speichere
    img.save(output_path, 'PNG', quality=95)
    print(f"✓ Icon erstellt: {output_path} ({size}x{size})")

def main():
    """Generiert alle benötigten Icons"""
    static_dir = os.path.join(os.path.dirname(__file__), 'static')

    # Erstelle Icons
    create_icon(192, os.path.join(static_dir, 'icon-192.png'))
    create_icon(512, os.path.join(static_dir, 'icon-512.png'))

    print("\n✅ Alle Icons erfolgreich generiert!")
    print("Icons befinden sich in: static/")

if __name__ == '__main__':
    main()
