"""One public API for six repeatable fictional signature forms."""
from __future__ import annotations

import hashlib
import random
import re

from . import gesture, handwriting, style_a, style_b

PLANS = ("full", "surname", "initial_surname", "monogram", "personal_short", "gesture")
PENS = (("fine ballpoint", .64), ("ballpoint", .84),
        ("ballpoint", .84), ("fine ballpoint", .64))

def writer_style(name: str) -> str:
    """Assign one repeatable handwriting style to each name."""
    key = hashlib.sha256(name.casefold().strip().encode("utf-8")).digest()
    return ("A", "B", "C")[key[3] % 3]

def profile(name: str, variant: int = 0) -> tuple[str, str, float, bool, int]:
    """Fixed design and pen habits for one fictional person."""
    if not name.strip():
        raise ValueError("Podaj imię lub nazwisko")
    key = hashlib.sha256(name.casefold().strip().encode("utf-8")).digest()
    plan = PLANS[key[0] % len(PLANS)]
    pen_name, pen_scale = PENS[key[1] % len(PENS)]
    underline = key[2] % 64 == 0 and plan != "gesture"
    seed = int.from_bytes(hashlib.sha256(key + str(variant).encode("ascii")).digest()[:8], "big")
    return plan, pen_name, pen_scale, underline, seed

def _underline(svg: str, name: str, sample: int, scale: float) -> str:
    width = float(re.search(r'viewBox="0 0 ([\d.]+) 170"', svg).group(1))
    ink = re.search(r'<g fill="(#[0-9a-f]+)"', svg).group(1)
    key = hashlib.sha256(f"{name.casefold().strip()}|underline|{sample}".encode()).digest()
    motion = random.Random(int.from_bytes(key[:8], "big"))
    start = width * .11 + motion.uniform(-5, 5)
    end = width * .83 + motion.uniform(-10, 10)
    low = 137 + motion.uniform(-3, 3)
    path = (f'<path data-mark="underline" d="M{start:.1f},{low:.1f} '
            f'C{start+(end-start)*.22:.1f},{low+motion.uniform(7, 12):.1f} '
            f'{start+(end-start)*.70:.1f},{low+motion.uniform(7, 13):.1f} '
            f'{end:.1f},{low+motion.uniform(-2, 3):.1f}" fill="none" '
            f'stroke="{ink}" stroke-width="{1.15*scale:.2f}" '
            f'stroke-linecap="round" opacity=".9"/>')
    return svg.replace("</svg>", path + "\n</svg>")

def render(name: str, sample: int = 0, variant: int = 0,
           plan: str = "auto") -> str:
    if sample < 0:
        raise ValueError("Numer próbki musi być nieujemny")
    person_plan, _, pen_scale, underline, seed = profile(name, variant)
    chosen = person_plan if plan == "auto" else plan
    if chosen not in PLANS:
        raise ValueError(f"Plan musi być jednym z: auto, {', '.join(PLANS)}")
    # Keep the handwriting engine fixed for this name across all samples.
    pen_jitter = random.Random(hashlib.sha256(f"{seed}|{sample}|pen".encode()).digest()).uniform(.96, 1.04)
    if chosen == "gesture":
        return gesture.render_gesture(name, seed, sample, pen_scale * pen_jitter)
    style = writer_style(name)
    if style == "A":
        return style_a.render(name, seed, "auto", sample, pen_scale * pen_jitter, chosen)
    if style == "B":
        return style_b.generate(name, seed, "auto", sample, chosen, pen_scale * pen_jitter)
    svg = handwriting.render_letters(name, seed, chosen, sample, pen_scale * pen_jitter)
    return _underline(svg, name, sample, pen_scale) if underline else svg
