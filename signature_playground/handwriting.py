"""Procedural letter strokes for fictional SVG signatures (standard library only)."""
from __future__ import annotations

import hashlib
import math
import random
from xml.sax.saxutils import escape

from . import polish

GLYPHS: dict[str, list[tuple[float, float]]] = {
    "a": [(0, 0), (.10, -.40), (.31, -.66), (.57, -.56), (.61, -.27), (.43, -.06), (.19, -.09), (.09, -.37), (.29, -.63), (.57, -.56), (.64, -.22), (.82, .02), (1, -.09)],
    "b": [(0, 0), (.14, -.30), (.19, -.86), (.16, -1.12), (.08, -.90), (.13, -.38), (.35, -.64), (.60, -.66), (.79, -.46), (.76, -.18), (.52, -.03), (.31, -.13), (.50, -.58), (.74, -.46), (.83, -.12), (1, -.07)],
    "c": [(0, -.06), (.11, -.39), (.33, -.62), (.61, -.63), (.72, -.49), (.55, -.53), (.32, -.49), (.24, -.23), (.44, -.04), (.73, -.01), (1, -.15)],
    "d": [(0, 0), (.12, -.40), (.34, -.64), (.59, -.54), (.61, -.25), (.41, -.04), (.20, -.11), (.16, -.40), (.38, -.63), (.62, -.50), (.70, -.90), (.71, -1.12), (.65, -.79), (.70, -.29), (.84, .01), (1, -.10)],
    "e": [(0, -.04), (.17, -.36), (.40, -.54), (.60, -.50), (.57, -.33), (.34, -.32), (.24, -.47), (.40, -.61), (.62, -.55), (.63, -.30), (.45, -.07), (.73, .01), (1, -.12)],
    "f": [(0, 0), (.16, -.28), (.28, -.82), (.38, -1.08), (.56, -1.12), (.62, -.91), (.53, -.76), (.34, -.68), (.16, -.66), (.44, -.73), (.52, -.22), (.54, .14), (.43, .38), (.29, .35), (.43, .04), (.72, -.13), (1, -.10)],
    "g": [(0, -.02), (.15, -.40), (.38, -.64), (.63, -.55), (.64, -.25), (.44, -.04), (.22, -.09), (.14, -.35), (.34, -.62), (.65, -.53), (.71, -.10), (.67, .34), (.54, .57), (.33, .57), (.31, .38), (.56, .23), (1, -.12)],
    "h": [(0, 0), (.15, -.35), (.20, -.84), (.17, -1.10), (.09, -.89), (.17, -.43), (.35, -.64), (.54, -.65), (.65, -.44), (.63, -.20), (.72, -.04), (1, -.12)],
    "i": [(0, 0), (.18, -.47), (.34, -.62), (.39, -.43), (.35, -.20), (.48, -.03), (.70, -.03), (1, -.12)],
    "j": [(0, -.02), (.19, -.42), (.35, -.62), (.40, -.45), (.38, -.12), (.33, .30), (.17, .53), (.03, .46), (.14, .25), (.45, .05), (1, -.12)],
    "k": [(0, 0), (.14, -.35), (.17, -.90), (.13, -1.10), (.08, -.83), (.17, -.35), (.39, -.63), (.63, -.70), (.54, -.44), (.32, -.26), (.53, -.45), (.72, -.10), (1, -.09)],
    "l": [(0, 0), (.16, -.35), (.23, -.89), (.31, -1.12), (.44, -1.05), (.38, -.76), (.25, -.39), (.33, -.10), (.58, .02), (1, -.12)],
    "m": [(0, 0), (.13, -.47), (.30, -.64), (.46, -.58), (.45, -.31), (.40, -.06), (.53, -.47), (.69, -.63), (.84, -.54), (.80, -.29), (.82, -.06), (1, -.12)],
    "n": [(0, 0), (.14, -.47), (.35, -.65), (.58, -.54), (.54, -.27), (.58, -.06), (.79, .02), (1, -.12)],
    "o": [(0, -.03), (.13, -.40), (.37, -.65), (.66, -.58), (.71, -.29), (.54, -.03), (.27, -.04), (.14, -.29), (.36, -.62), (.67, -.54), (.77, -.24), (1, -.10)],
    "p": [(0, 0), (.14, -.42), (.27, -.65), (.31, -.40), (.28, .28), (.30, .44), (.39, .18), (.41, -.29), (.56, -.60), (.76, -.62), (.88, -.43), (.76, -.17), (.52, -.10), (.37, -.27), (.70, -.28), (1, -.10)],
    "q": [(0, -.02), (.15, -.42), (.38, -.65), (.66, -.55), (.70, -.25), (.49, -.03), (.22, -.08), (.14, -.37), (.38, -.64), (.68, -.54), (.75, -.12), (.76, .37), (.91, .45), (1, .25)],
    "r": [(0, 0), (.14, -.43), (.31, -.64), (.47, -.59), (.47, -.42), (.35, -.36), (.43, -.62), (.64, -.66), (.81, -.54), (.68, -.39), (.69, -.14), (1, -.11)],
    "s": [(0, -.02), (.14, -.36), (.36, -.61), (.61, -.65), (.72, -.50), (.56, -.37), (.34, -.28), (.32, -.10), (.52, .02), (.78, -.06), (1, -.13)],
    "t": [(0, 0), (.18, -.28), (.33, -.82), (.48, -1.04), (.50, -.79), (.36, -.33), (.42, -.08), (.67, .01), (1, -.12)],
    "u": [(0, -.03), (.16, -.44), (.34, -.63), (.41, -.43), (.35, -.13), (.47, .00), (.65, -.21), (.81, -.57), (.76, -.33), (.79, -.07), (1, -.11)],
    "v": [(0, -.02), (.16, -.48), (.32, -.64), (.39, -.39), (.44, -.05), (.58, .01), (.79, -.34), (.89, -.59), (.84, -.39), (1, -.11)],
    "w": [(0, -.03), (.13, -.46), (.28, -.64), (.33, -.39), (.31, -.08), (.42, .01), (.55, -.24), (.68, -.57), (.67, -.31), (.74, -.05), (.85, -.13), (1, -.54)],
    "x": [(0, -.03), (.18, -.45), (.38, -.62), (.53, -.42), (.71, -.10), (1, -.08), (.74, -.13), (.57, -.35), (.38, -.54), (.22, -.12), (1, -.11)],
    "y": [(0, -.02), (.17, -.46), (.35, -.65), (.43, -.41), (.39, -.10), (.53, .00), (.73, -.28), (.89, -.59), (.81, -.20), (.72, .26), (.56, .55), (.33, .54), (.35, .34), (.64, .15), (1, -.11)],
    "z": [(0, -.02), (.17, -.48), (.43, -.63), (.70, -.55), (.63, -.38), (.36, -.15), (.29, .01), (.57, -.05), (.84, -.12), (1, -.10)],
}

CAPITALS: dict[str, list[tuple[float, float]]] = {
    "a": [(0, 0), (.28, -.85), (.48, -1.02), (.65, -.93), (.89, -.06), (.76, -.45), (.31, -.43), (.72, -.45), (1, -.05)],
    "b": [(0, -.02), (.22, -1.01), (.18, -.93), (.72, -.91), (.82, -.70), (.56, -.51), (.23, -.49), (.75, -.49), (.88, -.22), (.65, -.01), (1, -.09)],
    "c": [(.88, -.84), (.52, -1.01), (.18, -.81), (.04, -.46), (.20, -.13), (.57, .02), (1, -.16)],
    "d": [(0, 0), (.20, -1.02), (.61, -.97), (.90, -.70), (.90, -.32), (.65, -.05), (.20, 0), (1, -.08)],
    "e": [(.89, -.96), (.21, -.98), (.09, -.48), (.67, -.48), (.12, -.47), (.16, -.02), (1, -.09)],
    "f": [(.92, -.95), (.26, -.99), (.17, -.05), (.06, .08), (.52, -.52), (.12, -.49), (.75, -.49), (1, -.08)],
    "g": [(.89, -.82), (.56, -1.02), (.17, -.82), (.08, -.42), (.26, -.08), (.65, .02), (.88, -.17), (.87, -.46), (.60, -.45), (1, -.07)],
    "h": [(0, -.02), (.15, -.99), (.20, -.51), (.76, -.54), (.83, -.98), (.77, -.05), (1, -.08)],
    "i": [(.19, -.97), (.77, -.99), (.49, -.97), (.45, -.04), (.14, -.02), (.89, -.03), (1, -.10)],
    "j": [(.29, -.97), (.91, -.99), (.66, -.96), (.60, -.16), (.43, .08), (.16, .04), (.06, -.16), (1, -.08)],
    "k": [(0, -.02), (.16, -.99), (.17, -.52), (.82, -.98), (.29, -.48), (.85, -.04), (1, -.10)],
    "l": [(.06, -.99), (.24, -.98), (.20, -.06), (.86, -.04), (1, -.10)],
    "m": [(0, 0), (.14, -.99), (.44, -.31), (.71, -.99), (.87, -.02), (1, -.10)],
    "n": [(0, 0), (.12, -1), (.82, -.05), (.83, -.99), (1, -.10)],
    "o": [(.50, -.99), (.17, -.85), (.04, -.49), (.19, -.12), (.55, .01), (.89, -.17), (.98, -.53), (.78, -.91), (.50, -.99), (1, -.10)],
    "p": [(0, 0), (.18, -1), (.66, -.96), (.91, -.77), (.76, -.52), (.20, -.49), (1, -.08)],
    "q": [(.49, -.99), (.16, -.83), (.06, -.47), (.23, -.11), (.61, .02), (.91, -.20), (.97, -.59), (.78, -.91), (.49, -.99), (.59, -.16), (1, .09)],
    "r": [(0, 0), (.17, -1), (.69, -.95), (.87, -.73), (.72, -.52), (.22, -.49), (.70, -.51), (.96, -.05), (1, -.09)],
    "s": [(.91, -.85), (.57, -1), (.20, -.83), (.18, -.60), (.78, -.39), (.82, -.15), (.50, .02), (.12, -.10), (1, -.09)],
    "t": [(.10, -.98), (.91, -.99), (.51, -.97), (.46, -.05), (1, -.10)],
    "u": [(.08, -.99), (.12, -.31), (.42, .01), (.78, -.17), (.83, -.99), (1, -.10)],
    "v": [(.03, -.99), (.47, .02), (.90, -.99), (1, -.10)],
    "w": [(0, -.99), (.18, .01), (.48, -.64), (.70, .01), (.96, -.99), (1, -.10)],
    "x": [(.04, -.98), (.88, -.02), (.49, -.50), (.87, -.99), (.05, -.02), (1, -.10)],
    "y": [(.04, -.99), (.49, -.50), (.94, -.99), (.49, -.50), (.46, -.03), (1, -.10)],
    "z": [(.04, -.97), (.91, -.99), (.12, -.03), (.94, -.04), (1, -.10)],
}

def _smooth(points: list[tuple[float, float]], steps: int = 8) -> list[tuple[float, float]]:
    """Interpolate pen waypoints with a Catmull-Rom spline."""
    result: list[tuple[float, float]] = []
    for i in range(len(points) - 1):
        p0 = points[max(0, i - 1)]
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[min(len(points) - 1, i + 2)]
        for j in range(steps):
            t = j / steps
            t2, t3 = t * t, t * t * t
            x = .5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = .5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            result.append((x, y))
    result.append(points[-1])
    return result

def _ribbon(points: list[tuple[float, float]], width: float, rng: random.Random, phase: float) -> str:
    """Make an outlined stroke with thicker downward pen motion."""
    if len(points) < 2:
        return ""
    left: list[str] = []
    right: list[str] = []
    pressure_noise = rng.uniform(0, 2 * math.pi)
    for i, (x, y) in enumerate(points):
        x0, y0 = points[max(0, i - 1)]
        x1, y1 = points[min(len(points) - 1, i + 1)]
        dx, dy = x1 - x0, y1 - y0
        d = max(math.hypot(dx, dy), 1e-8)
        nx, ny = -dy / d, dx / d
        t = i / (len(points) - 1)
        taper = min(1.0, .27 + 7.0 * min(t, 1 - t))
        pressure = .68 + .57 * max(0, dy / d)
        pressure *= 1 + .09 * math.sin(13 * t + pressure_noise) + .04 * math.sin(39 * t + phase)
        radius = width * pressure * taper / 2
        left.append(f"{x + radius * nx:.2f},{y + radius * ny:.2f}")
        right.append(f"{x - radius * nx:.2f},{y - radius * ny:.2f}")
    return "M" + " L".join(left + right[::-1]) + " Z"

def _name_words(name: str) -> list[str]:
    normalized = polish.letters(name)
    words = ["".join(c for c in part.lower() if polish.BASE.get(c, c) in GLYPHS)
             for part in normalized.split()]
    words = [word for word in words if word]
    if not words:
        raise ValueError("Name must contain at least one letter")
    return words

def render_letters(name: str, seed: int, legibility: str = "readable", sample: int = 0,
           pen_scale: float = 1.0) -> str:
    identity = hashlib.sha256(f"{name.casefold()}|{seed}".encode("utf-8")).digest()
    rng = random.Random(int.from_bytes(identity[:8], "big"))
    person = hashlib.sha256(name.casefold().encode("utf-8")).digest()
    writer = random.Random(int.from_bytes(person[8:16], "big"))
    style = person[7] % 3  # flowing, compact, or open handwriting
    motion = random.Random(int.from_bytes(hashlib.sha256(identity + str(sample).encode("ascii")).digest()[:8], "big"))
    # A person's proportions and pen habits remain fixed across samples.
    height_factor = writer.uniform(*((1.03, 1.12), (.93, 1.02), (.96, 1.05))[style])
    width_factor = writer.uniform(*((.91, 1.02), (.86, .98), (1.13, 1.25))[style])
    pen_factor = writer.uniform(*((.89, 1.03), (1.00, 1.10), (.79, .93))[style]) * pen_scale * .85
    slant = writer.uniform(*((16, 22), (2, 7), (8, 13))[style])
    initial_factor = writer.uniform(*((1.28, 1.43), (1.09, 1.19), (1.17, 1.29))[style])
    spacing_factor = writer.uniform(*((.93, .99), (.95, 1.01), (1.04, 1.11))[style])
    rhythm = writer.uniform(-1.0, 1.0)
    letter_shape = {letter: (writer.uniform(.94, 1.06), writer.uniform(-.035, .035)) for letter in GLYPHS}
    traits = random.Random(hashlib.sha256(person + b"|traits").digest())
    height_factor *= traits.uniform(.86, 1.14)
    width_factor *= traits.uniform(.88, 1.12)
    pen_factor *= traits.uniform(.83, 1.12)
    slant += traits.uniform(-5.0, 5.0)
    initial_factor *= traits.uniform(.86, 1.14)
    spacing_factor *= traits.uniform(.92, 1.08)
    energy = traits.uniform(.75, 1.15)
    baseline_gain = traits.uniform(.68, 1.28)
    # Samples model consecutive signings, not a new writer.
    sample_amount = 0 if sample == 0 else 1.55 * energy
    sample_slant = sample_amount * motion.uniform(-5.2, 5.2)
    sample_height = 1 + sample_amount * motion.uniform(-.065, .075)
    sample_width = 1 + sample_amount * motion.uniform(-.075, .085)
    sample_pen = 1 + sample_amount * motion.uniform(-.08, .08)
    sample_baseline = sample_amount * motion.uniform(-3.0, 3.0)
    words = _name_words(name)
    plan = legibility
    tail_key = hashlib.sha256(f"{name.casefold().strip()}|tail-habit".encode()).digest()[0] / 255
    fast = plan in ("monogram", "personal_short", "gesture")
    tail_mode = (1 if tail_key < .32 else 2) if fast else (0 if tail_key < .32 else 1 if tail_key < .75 else 2)
    omission = 10 if fast else 32 if tail_mode == 1 else 20
    if sample and tail_mode and hashlib.sha256(
            f"{name.casefold().strip()}|{plan}|{sample}|tail".encode()).digest()[0] < omission:
        tail_mode = 0
    if plan == "full":
        pass
    elif plan == "surname":
        words = [words[-1]]
    elif plan == "initial_surname":
        words = [words[0][0], words[-1]] if len(words) > 1 else [words[0]]
    elif plan == "monogram":
        words = ["".join(word[0] for word in words)]
    elif plan == "personal_short":
        surname = words[-1]
        words = [words[0][0] + surname[:2] + surname[-1]]
    else:
        raise ValueError("Unknown letter form")

    ink = rng.choice(("#17253a", "#1c2b43", "#1d2735", "#1a2540"))
    baseline = 103.0
    scale_y = rng.uniform(47, 55) * height_factor * sample_height
    x = 46.0
    ribbons: list[str] = []
    clear_marks: list[str] = []
    baseline_wave_phase = rng.uniform(0, 6)
    # The writing line wanders smoothly from letter to letter; one person's
    # usual drift stays recognizable, while each signing adds a little motion.
    baseline_rng = random.Random(int.from_bytes(hashlib.sha256(identity + b"|baseline").digest()[:8], "big"))
    baseline_sample_rng = random.Random(int.from_bytes(
        hashlib.sha256(identity + f"|baseline|{sample}".encode()).digest()[:8], "big"))
    baseline_walk = 0.0
    all_centers: list[tuple[float, float]] = []
    word_centers: list[tuple[float, float]] = []

    # Preserve the old random sequence without drawing a detached lead-in.
    rng.random()

    for wi, word in enumerate(words):
        if wi:
            previous_end_x = word_centers[-1][0]
            ribbons.append(_ribbon(word_centers, rng.uniform(2.25, 3.35) * pen_factor * sample_pen, rng, wi))
            word_centers = []
            gap = rng.uniform(39, 45) * sample_width if plan == "initial_surname" else rng.uniform(23, 34) * sample_width
            if plan == "initial_surname" and wi == 1 and len(words) > 1:
                # A visible period belongs to the initial. Its short, sometimes
                # dragged mark varies like a dot made quickly with the same pen.
                # Centre it between the actual end of the initial and the next
                # word's start, rather than near the initial's advance cursor.
                dot_x = (previous_end_x + x + gap) * .5
                dot_y = baseline + sample_baseline - 6 + sample_amount * motion.uniform(-1.5, 1.5)
                drag = 2.0 + sample_amount * motion.uniform(-.4, 1.7)
                dot = _smooth([(dot_x - 1.0, dot_y - .2), (dot_x + drag * .35, dot_y + 1.2),
                               (dot_x + drag, dot_y + .7)], 5)
                ribbons.append(_ribbon(dot, 2.6 * pen_factor * sample_pen, rng, .5))
            x += gap
        for li, letter in enumerate(word):
            if li == 1 and plan in ("full", "surname", "initial_surname") and word_centers:
                ribbons.append(_ribbon(word_centers, rng.uniform(2.25, 3.35) * pen_factor * sample_pen, rng, wi))
                word_centers = []
            base_letter = polish.BASE.get(letter, letter)
            baseline_walk = max(-13.0 * baseline_gain, min(13.0 * baseline_gain, .78 * baseline_walk
                                + baseline_rng.uniform(-7.2, 7.2) * baseline_gain
                                + sample_amount * baseline_sample_rng.uniform(-2.1, 2.1) * baseline_gain))
            is_initial = li == 0 or plan == "monogram"
            size = (initial_factor if is_initial else 1.0) * rng.uniform(.91, 1.08)
            size *= 1 + sample_amount * motion.uniform(-.075, .085)
            glyph_w = scale_y * (.56 if base_letter not in "mw" else .72) * size * width_factor * letter_shape[base_letter][0] * sample_width
            if base_letter in "iljrt" and not is_initial:
                glyph_w *= .72
            glyph_h = scale_y * (1.24 if is_initial else 1.0)
            glyph = CAPITALS[base_letter] if is_initial else GLYPHS[base_letter]
            local = _smooth(glyph, steps=7)
            wobble_phase = rng.uniform(0, 2 * math.pi)
            base_shift = (1.5 * math.sin(x / 120 + baseline_wave_phase)
                          + rhythm * (x - 46) / 260 + sample_baseline + baseline_walk)
            hand_x = sample_amount * motion.uniform(-3.0, 3.0)
            hand_y = sample_amount * motion.uniform(-2.8, 2.8)
            hand_phase = motion.uniform(0, 2 * math.pi)
            loop_change = sample_amount * motion.uniform(-.105, .105)
            glyph_shear = sample_amount * motion.uniform(-2.2, 2.2)
            centers: list[tuple[float, float]] = []
            for i, (gx, gy) in enumerate(local):
                t = i / max(1, len(local) - 1)
                tremor = .13 * math.sin(t * 13 + wobble_phase)
                gx += letter_shape[base_letter][1] * math.sin(math.pi * gx)
                px = x + gx * glyph_w - gy * (slant + sample_slant) + tremor + hand_x + sample_amount * 1.9 * math.sin(2 * math.pi * t + hand_phase) - gy * glyph_shear
                py = baseline + base_shift + gy * glyph_h * (1 + loop_change) + .10 * math.sin(t * 11 + wobble_phase) + hand_y + sample_amount * 1.65 * math.sin(2 * math.pi * t + hand_phase * .7)
                centers.append((px, py))
            if word_centers:
                p0 = word_centers[-1]
                p1 = centers[0]
                if math.hypot(p1[0] - p0[0], p1[1] - p0[1]) < 27:
                    bridge = _smooth([p0, ((p0[0] + p1[0]) / 2, min(p0[1], p1[1]) - 2), p1], 6)
                    word_centers.extend(bridge[1:])
            word_centers.extend(centers)
            all_centers.extend(centers)
            for mark in polish.marks(letter, min(y for _, y in glyph) - .14, is_initial):
                mark_points = [(x + gx * glyph_w - gy * (slant + sample_slant) + hand_x - gy * glyph_shear,
                                baseline + base_shift + gy * glyph_h * (1 + loop_change) + hand_y)
                               for gx, gy in mark]
                path = "M" + " L".join(f"{px:.2f},{py:.2f}" for px, py in mark_points)
                clear_marks.append(f'<path d="{path}" fill="none" stroke="{ink}" '
                                   f'stroke-width="{max(1.6, 2.2 * pen_factor * sample_pen):.2f}" '
                                   'stroke-linecap="round" stroke-linejoin="round"/>')
            x += glyph_w * rng.uniform(spacing_factor - .025, spacing_factor + .025) * (1 + sample_amount * motion.uniform(-.065, .065))

            if base_letter in "ij" and not is_initial:
                dot_x = x - glyph_w * .52 + rng.uniform(-1.5, 1.5) + hand_x
                dot_y = baseline - glyph_h * .87 + rng.uniform(-2, 2) + sample_baseline + baseline_walk + hand_y
                ribbons.append(f"M{dot_x:.2f},{dot_y:.2f} a2.1,2.1 0 1,0 4.2,0 a2.1,2.1 0 1,0 -4.2,0")
            if base_letter == "t":
                cx = x - glyph_w * .51
                cross = _smooth([(cx - 8, baseline + baseline_walk - glyph_h * .59),
                                 (cx + 4, baseline + baseline_walk - glyph_h * .62),
                                 (cx + 16, baseline + baseline_walk - glyph_h * .58)])
                ribbons.append(_ribbon(cross, 1.7 * pen_factor * sample_pen, rng, wobble_phase))

    last_x, last_y = all_centers[-1]
    final_letter = polish.BASE.get(words[-1][-1], words[-1][-1])
    exit_turn = max(-10.0, min(10.0, (last_y - word_centers[-2][1]) * .25))
    if final_letter in "ijlt":
        tail_steps = ((12, -6), (29, -11), (43, -7))
    elif final_letter in "gjpqy":
        tail_steps = ((15, -3), (37, -14), (55, -12))
    elif final_letter in "aeo":
        tail_steps = ((16, -7), (39, -4), (64, 1))
    else:
        tail_steps = ((15, -13), (42, -9), (62, -15))
    tail_scale = (.85 if tail_mode == 1 else 1.20) if fast else (.55 if tail_mode == 1 else 1.0)
    style_reach = (1.0, .86, 1.07)[style] * tail_scale
    if not tail_mode:
        tail_steps = ()
    tail_bend = motion.uniform(.72, 1.28) if fast else 1.0
    finish_knots = [(last_x, last_y)] + [
        (last_x + dx * style_reach,
         last_y + dy * style_reach * tail_bend + exit_turn * (i + 1) / len(tail_steps))
        for i, (dx, dy) in enumerate(tail_steps)
    ]
    if sample_amount:
        tail_reach = 1 + 1.15 * (motion.uniform(.83, 1.18) - 1)
        tail_rise = 1 + 1.15 * (motion.uniform(.76, 1.22) - 1)
        finish_knots = [finish_knots[0]] + [
            (last_x + (px - last_x) * tail_reach + motion.uniform(-4.0, 4.0),
             last_y + (py - last_y) * tail_rise + motion.uniform(-4.5, 4.5))
            for px, py in finish_knots[1:]
        ]
    word_centers.extend(_smooth(finish_knots, 7)[1:])
    ribbons.append(_ribbon(word_centers, rng.uniform(2.25, 3.35) * pen_factor * sample_pen, rng, 2.1))
    last_x = finish_knots[-1][0]
    view_width = math.ceil(last_x + 90)
    paths = "\n  ".join([*(f'<path d="{p}"/>' for p in ribbons if p), *clear_marks])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_width} 170" '
        f'width="{view_width}" height="170" role="img" data-plan="{plan}" aria-label="Fictional handwritten signature">\n'
        f'  <title>Fictional signature for {escape(name)}</title>\n'
        f'  <g fill="{ink}">\n  {paths}\n  </g>\n</svg>\n'
    )
