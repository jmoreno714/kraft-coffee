"""
Generate AI food images via Pollinations.ai (free, no API key required).
Downloads images to brand_assets/ai-images/ and updates index.html paths.
"""

import requests
import time
import shutil
from pathlib import Path
from urllib.parse import quote

ROOT       = Path(__file__).parent.parent
OUTPUT_DIR = ROOT / "brand_assets" / "ai-images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

IMAGES = [
    {
        "filename": "hero.jpg",
        "prompt": "professional food photography croissant and latte coffee cup marble table cafe morning light warm tones elegant",
        "width": 1600, "height": 900, "seed": 101,
    },
    {
        "filename": "about.jpg",
        "prompt": "avocado toast poached egg artisan sourdough bread sesame seeds cafe plate white ceramic overhead shot professional food photography warm light",
        "width": 900, "height": 1100, "seed": 202,
    },
    {
        "filename": "gallery-1.jpg",
        "prompt": "fresh croissants plate cafe table coffee cup morning breakfast professional food photography golden light",
        "width": 900, "height": 700, "seed": 303,
    },
    {
        "filename": "gallery-2.jpg",
        "prompt": "smoothie berry drink glass straw cafe table elegant food photography vibrant red pink colors",
        "width": 700, "height": 700, "seed": 404,
    },
    {
        "filename": "gallery-3.jpg",
        "prompt": "gourmet burger brioche bun fries basket cafe restaurant food photography professional warm tones",
        "width": 800, "height": 700, "seed": 505,
    },
    {
        "filename": "gallery-4.jpg",
        "prompt": "slice tart mixed berries raspberry blueberry cream cheese dessert plate cafe professional food photography",
        "width": 700, "height": 700, "seed": 606,
    },
    {
        "filename": "gallery-5.jpg",
        "prompt": "chocolate lava cake molten dark chocolate ice cream scoop dessert plate restaurant elegant food photography",
        "width": 900, "height": 700, "seed": 707,
    },
]


def download_image(img: dict) -> bool:
    prompt_enc = quote(img["prompt"])
    url = (
        f"https://image.pollinations.ai/prompt/{prompt_enc}"
        f"?width={img['width']}&height={img['height']}"
        f"&seed={img['seed']}&nologo=true&model=flux"
    )
    dest = OUTPUT_DIR / img["filename"]
    print(f"  Generando {img['filename']}...")

    try:
        r = requests.get(url, timeout=90, stream=True)
        r.raise_for_status()
        with open(dest, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        size_kb = dest.stat().st_size // 1024
        print(f"    Guardado ({size_kb} KB)")
        return True
    except Exception as e:
        print(f"    ERROR: {e}")
        return False


def update_html():
    html_path = ROOT / "index.html"
    html = html_path.read_text(encoding="utf-8")

    replacements = {
        "brand_assets/Fotos- recursos/unnamed.jpg": "brand_assets/ai-images/hero.jpg",
        "brand_assets/Fotos- recursos/2.jpg":       "brand_assets/ai-images/about.jpg",
        "brand_assets/Fotos- recursos/3.jpg":       "brand_assets/ai-images/gallery-2.jpg",
        "brand_assets/Fotos- recursos/4.jpg":       "brand_assets/ai-images/gallery-3.jpg",
        "brand_assets/Fotos- recursos/5.jpg":       "brand_assets/ai-images/gallery-4.jpg",
    }

    # hero background in CSS uses url()
    html = html.replace(
        "url('brand_assets/Fotos- recursos/unnamed.jpg')",
        "url('brand_assets/ai-images/hero.jpg')"
    )
    # about floating image (also unnamed.jpg)
    # replace remaining occurrences
    for old, new in replacements.items():
        html = html.replace(old, new)

    # swap gallery items to use all generated images
    html = html.replace(
        'src="brand_assets/ai-images/hero.jpg" alt="Croissants y café"',
        'src="brand_assets/ai-images/gallery-1.jpg" alt="Croissants y café"'
    )

    html_path.write_text(html, encoding="utf-8")
    print("  index.html actualizado.")


def main():
    print("=" * 50)
    print("  Generando imagenes con IA (Pollinations.ai)")
    print("=" * 50)

    failed = []
    for img in IMAGES:
        ok = download_image(img)
        if not ok:
            failed.append(img["filename"])
        time.sleep(1)

    print()
    if failed:
        print(f"Fallaron: {', '.join(failed)}")
    else:
        print("Todas las imagenes generadas correctamente.")

    print("Actualizando index.html...")
    update_html()
    print()
    print("Listo. Ahora correr deploy_github_pages.py para publicar.")


if __name__ == "__main__":
    main()
