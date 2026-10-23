"""Generate the 404 icon set: a black rounded square with a white wordmark."""

import pathlib

from PIL import Image, ImageDraw, ImageFont

ICONS = pathlib.Path("src-tauri/icons")
BG = (10, 10, 10, 255)
FG = (255, 255, 255, 255)
TEXT = "404"

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\seguisb.ttf",
]


def load_font(size):
    for path in FONT_CANDIDATES:
        if pathlib.Path(path).exists():
            return ImageFont.truetype(path, size)
    raise SystemExit("no bold font found")


def wordmark(size, tracking_ratio=-0.04):
    """The digits as a tightly tracked image, cropped to their ink box."""
    font = load_font(size)
    tracking = int(size * tracking_ratio)
    advances = [font.getlength(ch) for ch in TEXT]
    total = sum(advances) + tracking * (len(TEXT) - 1)

    canvas = Image.new("RGBA", (int(total) + size, size * 3), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    x = size / 2
    for ch, advance in zip(TEXT, advances):
        draw.text((x, size * 1.5), ch, font=font, fill=FG, anchor="ls")
        x += advance + tracking
    return canvas.crop(canvas.getbbox())


def render(size, radius_ratio=0.22, width_ratio=0.68):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle(
        (0, 0, size - 1, size - 1), radius=int(size * radius_ratio), fill=BG
    )

    # Render big once, then scale the ink box to the target width so every
    # size gets the same optical weight and stays dead centred.
    mark = wordmark(max(size * 2, 64))
    target_w = size * width_ratio
    target_h = mark.height * target_w / mark.width
    mark = mark.resize((round(target_w), round(target_h)), Image.LANCZOS)
    img.alpha_composite(
        mark, (round((size - mark.width) / 2), round((size - mark.height) / 2))
    )
    return img


targets = {
    "icon.png": 1024,
    "128x128@2x.png": 256,
    "128x128.png": 128,
    "64x64.png": 64,
    "32x32.png": 32,
    "Square310x310Logo.png": 310,
    "Square284x284Logo.png": 284,
    "Square150x150Logo.png": 150,
    "Square142x142Logo.png": 142,
    "Square107x107Logo.png": 107,
    "Square89x89Logo.png": 89,
    "Square71x71Logo.png": 71,
    "Square44x44Logo.png": 44,
    "Square30x30Logo.png": 30,
    "StoreLogo.png": 50,
}

for name, size in targets.items():
    render(size).save(ICONS / name)
    print("ecrit", name, size)

# Windows .ico: every size Explorer and the installer ask for.
ico_sizes = [256, 128, 64, 48, 32, 24, 16]
render(256).save(ICONS / "icon.ico", format="ICO", sizes=[(s, s) for s in ico_sizes])
print("ecrit icon.ico", ico_sizes)

# logo.png keeps the same square mark, just larger, for docs/README.
render(1024).save(ICONS / "logo.png")
print("ecrit logo.png")
