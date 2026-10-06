"""QA previews adapted from OpenAI hatch-pet (Apache-2.0).

Modified by KidsCharacterKit, 2026-10-06: explicit timing/loop, full-alpha APNG;
removed fixed pet states, GIF quantization and inferred frame ordering.
See SOURCE.json and LICENSE.txt alongside this file.
"""


def save_preview(frames, durations, output, loop):
    if not frames or len(frames) != len(durations):
        raise ValueError("one duration per explicit frame required")
    if any(type(value) is not int or not 1 <= value <= 65535 for value in durations):
        raise ValueError("durations must be integer milliseconds in 1..65535")
    if type(loop) is not int or loop not in (0, 1):
        raise ValueError("loop must be 0 (repeat) or 1 (once)")
    if any(frame.mode != "RGBA" or frame.size != frames[0].size for frame in frames):
        raise ValueError("preview frames must have one RGBA canvas")
    if len(frames) < 2:
        raise ValueError("animation preview requires at least two frames")
    if all(frame.tobytes() == frames[0].tobytes() for frame in frames[1:]):
        raise ValueError("all frames identical; use a static raster for a hold")
    frames[0].save(output, format="PNG", save_all=True, append_images=frames[1:],
                   duration=durations, loop=loop, disposal=0, blend=0, optimize=False)
