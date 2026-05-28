#!/usr/bin/env python3
"""Generate professional author avatars for NewTrekko."""

from PIL import Image, ImageDraw, ImageFont
import os, math

OUTPUT_DIR = "/home/user/NewTrekko/images/autores"

AUTHORS = [
    {"slug": "rafael-dias",     "name": "Rafael Dias",     "initial": "R"},
    {"slug": "marcos-rodrigues","name": "Marcos Rodrigues","initial": "M"},
    {"slug": "leticia-campos",  "name": "Letícia Campos",  "initial": "L"},
]

BG_COLOR    = (21, 128, 61)   # #15803d
RING_COLOR  = (134, 239, 172) # #86efac
INNER_COLOR = (22, 101, 52)   # slightly darker for depth
WHITE       = (255, 255, 255)
SIZE        = 200


def draw_avatar(initial: str) -> Image.Image:
    img = Image.new("RGB", (SIZE, SIZE), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    # outer ring
    draw.ellipse([2, 2, SIZE - 3, SIZE - 3], fill=RING_COLOR)
    # inner gradient approximation — two circles
    draw.ellipse([8, 8, SIZE - 9, SIZE - 9], fill=BG_COLOR)
    # subtle inner shadow at bottom
    for i in range(8):
        alpha = int(30 * (i / 8))
        y_off = SIZE // 2 + 10 + i * 5
        r_off = SIZE // 2 - 9 - i * 3
        if r_off > 0:
            draw.arc(
                [SIZE // 2 - r_off, y_off - r_off // 2,
                 SIZE // 2 + r_off, y_off + r_off // 2],
                start=0, end=180,
                fill=(15, 90, 40),
                width=2,
            )

    # letter — use a large truetype font if available, else default
    font = None
    for fp in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    ]:
        if os.path.exists(fp):
            font = ImageFont.truetype(fp, size=96)
            break
    if font is None:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), initial, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (SIZE - tw) // 2 - bbox[0]
    ty = (SIZE - th) // 2 - bbox[1] - 4

    # subtle drop shadow
    draw.text((tx + 2, ty + 3), initial, font=font, fill=(10, 70, 30))
    # main letter
    draw.text((tx, ty), initial, font=font, fill=WHITE)

    # circular mask (round the image)
    mask = Image.new("L", (SIZE, SIZE), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([0, 0, SIZE - 1, SIZE - 1], fill=255)
    img.putalpha(mask)

    # white background composite (for JPG which has no alpha)
    bg = Image.new("RGB", (SIZE, SIZE), (248, 250, 252))
    bg.paste(img, mask=img.split()[3])
    return bg


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for author in AUTHORS:
        img = draw_avatar(author["initial"])
        jpg_path = os.path.join(OUTPUT_DIR, f"{author['slug']}-avatar.jpg")
        webp_path = os.path.join(OUTPUT_DIR, f"{author['slug']}-avatar.webp")
        img.save(jpg_path, "JPEG", quality=90, optimize=True)
        img.save(webp_path, "WEBP", quality=85)
        print(f"Created {jpg_path}")
        print(f"Created {webp_path}")


if __name__ == "__main__":
    main()
