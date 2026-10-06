"""QA contact sheets adapted from OpenAI hatch-pet (Apache-2.0).

Modified by KidsCharacterKit, 2026-10-06: explicit frames/labels, common canvas
scale and checker/white/black backgrounds; removed fixed pet atlas geometry.
See SOURCE.json and LICENSE.txt alongside this file.
"""
from PIL import Image, ImageDraw


def checker(size: tuple[int, int], square: int = 16) -> Image.Image:
    image = Image.new("RGB", size, "#ffffff")
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], square):
        for x in range(0, size[0], square):
            if (x // square + y // square) % 2:
                draw.rectangle((x, y, x + square - 1, y + square - 1), fill="#e8e8e8")
    return image


def make_sheet(frames, labels, output, extent=280):
    if not frames or len(frames) != len(labels) or extent < 16:
        raise ValueError("explicit frames and one label per frame required")
    factor = extent / max(max(frame.size) for frame in frames)
    cell = extent + 12
    sheet = Image.new("RGB", (len(frames) * cell, 32 + 3 * (extent + 28)), "#f7f7f7")
    draw = ImageDraw.Draw(sheet)
    draw.text((6, 8), "QA ONLY / CANDIDATES - shared canvas scale", fill="black")
    for row, background in enumerate(("checker", "white", "black")):
        y = 32 + row * (extent + 28)
        for column, (frame, label) in enumerate(zip(frames, labels)):
            x = column * cell
            draw.text((x + 6, y + 4), f"{label} / {background}", fill="black")
            bg = checker((extent, extent)) if background == "checker" else Image.new("RGB", (extent, extent), background)
            resized = frame.resize(tuple(max(1, round(v * factor)) for v in frame.size), Image.Resampling.LANCZOS)
            # Canvas centering is for comparison only; it is not a ground anchor.
            bg.paste(resized, ((extent - resized.width) // 2, (extent - resized.height) // 2), resized)
            sheet.paste(bg, (x + 6, y + 24))
    sheet.save(output)
    return {"common_preview_scale": factor, "extent": extent, "anchor_alignment": False}
