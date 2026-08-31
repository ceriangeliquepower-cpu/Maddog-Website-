"""
Resize + compress a raw photo for use on the Maddog site.

Usage:
    py optimize_photo.py raw-photos/myphoto.jpg --type hero
    py optimize_photo.py raw-photos/myphoto.jpg --type card
    py optimize_photo.py raw-photos/myphoto.jpg --type general

Drop your original, unedited photo into raw-photos/ (any size, any format —
JPG, PNG, HEIC-exported-as-JPG, whatever your phone/camera produces). This
script:
  1. Auto-rotates it based on EXIF orientation (fixes sideways phone photos)
  2. Resizes it down to a sensible max width for how it'll actually be
     displayed on the site (no point shipping a 4000px photo for a 400px card)
  3. Flattens transparency onto white and converts to JPEG
  4. Compresses at decreasing quality until it's under the target size,
     matching CLAUDE.md's "≤200KB per image, quality 72-82" rule
  5. Names the output to match the site's existing convention (16-char hash)
     and saves it into images/ — ready to reference as images/HASH.jpg

The raw original in raw-photos/ is left untouched (that folder is gitignored,
so it never gets pushed or deployed — it's just your local working copy).
"""
import argparse
import hashlib
import io
import os
import sys

from PIL import Image, ImageOps

PAGES_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(PAGES_DIR, 'images')

PRESETS = {
    # (max_width, target_kb, start_quality)
    'hero':    (1600, 200, 80),
    'card':    (800,  120, 78),
    'general': (1400, 180, 78),
}


def optimize(input_path, preset):
    max_width, target_kb, start_quality = PRESETS[preset]

    img = Image.open(input_path)
    img = ImageOps.exif_transpose(img)  # fix sideways/upside-down phone photos

    if img.mode in ('RGBA', 'LA', 'P'):
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img.convert('RGBA'), mask=img.convert('RGBA').split()[-1])
        img = bg
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    if img.width > max_width:
        new_height = round(img.height * (max_width / img.width))
        img = img.resize((max_width, new_height), Image.LANCZOS)

    quality = start_quality
    data = None
    while quality >= 40:
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=quality, optimize=True)
        data = buf.getvalue()
        if len(data) <= target_kb * 1024:
            break
        quality -= 6

    img_hash = hashlib.md5(data).hexdigest()[:16]
    out_filename = f'{img_hash}.jpg'
    out_path = os.path.join(IMAGES_DIR, out_filename)

    os.makedirs(IMAGES_DIR, exist_ok=True)
    with open(out_path, 'wb') as f:
        f.write(data)

    return {
        'filename': out_filename,
        'path': out_path,
        'width': img.width,
        'height': img.height,
        'quality': quality,
        'size_kb': round(len(data) / 1024, 1),
        'original_size_kb': round(os.path.getsize(input_path) / 1024, 1),
    }


def main():
    parser = argparse.ArgumentParser(description='Resize + compress a photo for the Maddog site.')
    parser.add_argument('input', help='Path to the raw photo (e.g. raw-photos/myphoto.jpg)')
    parser.add_argument('--type', choices=PRESETS.keys(), default='general',
                         help='hero = blog/page hero banner (max 1600px, ≤200KB), '
                              'card = thumbnail/card image (max 800px, ≤120KB), '
                              'general = anything else (max 1400px, ≤180KB)')
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f'ERROR: file not found: {args.input}', file=sys.stderr)
        sys.exit(1)

    result = optimize(args.input, args.type)

    print(f"Saved: images/{result['filename']}")
    print(f"Dimensions: {result['width']}x{result['height']}")
    print(f"Size: {result['original_size_kb']}KB -> {result['size_kb']}KB (quality {result['quality']})")
    print(f"Use in HTML: images/{result['filename']}")


if __name__ == '__main__':
    main()
