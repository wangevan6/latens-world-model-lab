"""Generates the placeholder PNGs used by README.md.

Run once: `python3 assets/_make_images.py` from the repo root.
Replace the outputs with real artwork when available.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent


def font(size: int) -> ImageFont.ImageFont:
    for path in (
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def gradient(w: int, h: int, top: tuple[int, int, int], bot: tuple[int, int, int]) -> Image.Image:
    img = Image.new("RGB", (w, h), top)
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return img


def banner() -> None:
    img = gradient(1600, 600, (10, 14, 28), (40, 60, 110))
    d = ImageDraw.Draw(img)
    d.text((80, 200), "LATENS", fill=(245, 247, 255), font=font(140))
    d.text((84, 360), "World Model Lab", fill=(180, 200, 240), font=font(56))
    d.text((84, 440), "predictive latent worlds, in your browser", fill=(150, 170, 210), font=font(28))
    for i, x in enumerate(range(1100, 1500, 28)):
        d.ellipse((x, 180 + i * 6, x + 16, 196 + i * 6), fill=(120 + i * 6, 160, 240))
    img.save(OUT / "banner.png", optimize=True)


def architecture() -> None:
    img = Image.new("RGB", (1600, 900), (250, 251, 254))
    d = ImageDraw.Draw(img)
    d.text((60, 40), "Architecture (placeholder)", fill=(20, 24, 40), font=font(40))

    boxes = [
        (120, 180, 380, 320, "Encoder", (220, 232, 255)),
        (520, 180, 780, 320, "Predictor", (210, 245, 230)),
        (920, 180, 1180, 320, "Decoder", (255, 232, 220)),
        (1320, 180, 1480, 320, "Loss", (240, 220, 240)),
        (520, 480, 780, 620, "Latent Memory", (235, 235, 245)),
        (120, 700, 1480, 800, "Browser Runtime (Latens UI)", (245, 245, 250)),
    ]
    for x0, y0, x1, y1, label, color in boxes:
        d.rounded_rectangle((x0, y0, x1, y1), radius=18, fill=color, outline=(40, 50, 80), width=2)
        d.text((x0 + 20, y0 + 20), label, fill=(20, 24, 40), font=font(28))

    arrows = [(380, 250, 520, 250), (780, 250, 920, 250), (1180, 250, 1320, 250), (650, 320, 650, 480)]
    for x0, y0, x1, y1 in arrows:
        d.line((x0, y0, x1, y1), fill=(40, 50, 80), width=3)
        d.polygon(
            [(x1, y1), (x1 - 12, y1 - 6), (x1 - 12, y1 + 6)] if x1 != x0 else [(x1, y1), (x1 - 6, y1 - 12), (x1 + 6, y1 - 12)],
            fill=(40, 50, 80),
        )

    img.save(OUT / "architecture.png", optimize=True)


def screenshot() -> None:
    img = Image.new("RGB", (1600, 1000), (16, 18, 28))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((40, 40, 1560, 960), radius=18, fill=(24, 28, 42), outline=(60, 70, 100), width=1)
    d.text((72, 72), "Latens — demo screen (placeholder)", fill=(220, 230, 250), font=font(28))
    d.rounded_rectangle((72, 130, 480, 920), radius=12, fill=(32, 38, 56))
    d.text((92, 150), "Sessions", fill=(180, 200, 240), font=font(22))
    for i in range(8):
        d.rounded_rectangle((92, 200 + i * 78, 460, 260 + i * 78), radius=8, fill=(40, 48, 70))
        d.text((104, 214 + i * 78), f"world-{i:02d}", fill=(210, 220, 245), font=font(20))
    d.rounded_rectangle((520, 130, 1530, 600), radius=12, fill=(28, 32, 48))
    d.text((540, 150), "Latent flow", fill=(180, 200, 240), font=font(22))
    pts = []
    import math

    for x in range(540, 1520, 8):
        y = 360 + int(120 * math.sin((x - 540) * 0.012)) + int(40 * math.sin((x - 540) * 0.05))
        pts.append((x, y))
    d.line(pts, fill=(120, 200, 255), width=3)
    d.rounded_rectangle((520, 630, 1530, 920), radius=12, fill=(28, 32, 48))
    d.text((540, 650), "Logs", fill=(180, 200, 240), font=font(22))
    sample = [
        "[t=0.00] init world model: latents=256 horizon=16",
        "[t=0.04] encode frame 0 -> z0",
        "[t=0.08] predictor rollout 16 steps, mse=0.0123",
        "[t=0.12] decode ✓",
    ]
    for i, line in enumerate(sample):
        d.text((540, 700 + i * 36), line, fill=(180, 220, 200), font=font(20))
    img.save(OUT / "screenshot.png", optimize=True)


if __name__ == "__main__":
    banner()
    architecture()
    screenshot()
    print("wrote:", *(p.name for p in OUT.glob("*.png")))
