"""Draw 404's tray glyphs and overlay badges in the monochrome palette.

Tray naming (see src-tauri/src/tray.rs): the unsuffixed file is shown on a DARK
taskbar, so it is drawn white; the `_dark` variant is shown on a LIGHT taskbar,
so it is drawn black.

State is carried by shape, not colour, since there is no hue left to spend:
  idle        the 404 wordmark
  warning     an exclamation mark (model not ready)
  recording   a filled disc
  transcribing three dots

Glyphs are drawn on transparency, the way a tray icon is expected to be: the
taskbar supplies the background and we only supply the ink.
"""

import pathlib

from PIL import Image, ImageDraw, ImageFont

RES = pathlib.Path("src-tauri/resources")
SIZE = 64
SCALE = 8  # supersample, then downscale for clean edges
WHITE = (255, 255, 255, 255)
BLACK = (10, 10, 10, 255)

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
]


def load_font(size):
    for path in FONT_CANDIDATES:
        if pathlib.Path(path).exists():
            return ImageFont.truetype(path, size)
    raise SystemExit("no bold font found")


def fit_text(draw, text, max_width, max_height):
    """Largest bold size at which `text` fits the given box."""
    size = int(max_height)
    while size > 4:
        font = load_font(size)
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        if right - left <= max_width and bottom - top <= max_height:
            return font
        size -= 1
    return load_font(4)


def glyph(fg, text):
    """`text` set to fill the tray square, on transparency."""
    img = Image.new("RGBA", (SIZE * SCALE, SIZE * SCALE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = fit_text(draw, text, 56 * SCALE, 40 * SCALE)
    draw.text(
        (SIZE * SCALE / 2, SIZE * SCALE / 2),
        text,
        font=font,
        fill=fg,
        anchor="mm",
    )
    return img.resize((SIZE, SIZE), Image.LANCZOS)


def disc(fg):
    img = Image.new("RGBA", (SIZE * SCALE, SIZE * SCALE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    inset = 5 * SCALE
    draw.ellipse(
        (inset, inset, SIZE * SCALE - inset - 1, SIZE * SCALE - inset - 1), fill=fg
    )
    return img.resize((SIZE, SIZE), Image.LANCZOS)


def dots(fg):
    img = Image.new("RGBA", (SIZE * SCALE, SIZE * SCALE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    radius = 6 * SCALE
    cy = SIZE * SCALE / 2
    for cx in (14, 32, 50):
        draw.ellipse(
            (
                cx * SCALE - radius,
                cy - radius,
                cx * SCALE + radius,
                cy + radius,
            ),
            fill=fg,
        )
    return img.resize((SIZE, SIZE), Image.LANCZOS)


for name, fg in (("tray_idle", WHITE), ("tray_idle_dark", BLACK)):
    glyph(fg, "404").save(RES / (name + ".png"))
    print("ecrit", name)

for name, fg in (
    ("tray_idle_warning", WHITE),
    ("tray_idle_warning_dark", BLACK),
):
    glyph(fg, "!").save(RES / (name + ".png"))
    print("ecrit", name)

for name, fg in (("tray_recording", WHITE), ("tray_recording_dark", BLACK)):
    disc(fg).save(RES / (name + ".png"))
    print("ecrit", name)

for name, fg in (("tray_transcribing", WHITE), ("tray_transcribing_dark", BLACK)):
    dots(fg).save(RES / (name + ".png"))
    print("ecrit", name)

# Legacy "colored theme" assets: same glyphs, white, so the code path keeps
# working without shipping a second visual language.
glyph(WHITE, "404").save(RES / "handy.png")
glyph(WHITE, "!").save(RES / "handy_warning.png")
disc(WHITE).save(RES / "recording.png")
dots(WHITE).save(RES / "transcribing.png")
print("ecrit handy.png / handy_warning.png / recording.png / transcribing.png")
