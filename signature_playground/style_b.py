"""Procedural handwriting style B."""

from __future__ import annotations

import hashlib

import html

import math

import random

from . import polish

GLYPHS = {
    "a": (0.93, [(0, 0), (.09, -.37), (.28, -.58), (.55, -.53), (.66, -.25), (.48, .03), (.22, .03), (.17, -.27), (.35, -.56), (.68, -.59), (.69, -.12), (.93, 0)]),
    "b": (.96, [(0, 0), (.15, -.52), (.27, -1.15), (.14, -1.34), (.04, -1.16), (.35, -.54), (.38, -.05), (.55, -.51), (.79, -.56), (.91, -.25), (.72, .04), (.48, .03), (.96, 0)]),
    "c": (.84, [(0, 0), (.12, -.43), (.4, -.6), (.66, -.53), (.45, -.48), (.18, -.25), (.3, .01), (.61, .06), (.84, 0)]),
    "d": (1.03, [(0, 0), (.11, -.37), (.34, -.59), (.58, -.5), (.56, -.14), (.37, .04), (.18, -.14), (.31, -.49), (.57, -.57), (.72, -1.31), (.57, -1.37), (.53, -1.14), (.75, -.12), (1.03, 0)]),
    "e": (.82, [(0, 0), (.19, -.3), (.5, -.48), (.64, -.34), (.48, -.16), (.18, -.18), (.3, .04), (.62, .05), (.82, 0)]),
    "f": (.74, [(0, 0), (.2, -.48), (.41, -1.23), (.59, -1.38), (.7, -1.19), (.39, -.46), (.23, .42), (.38, .57), (.61, .36), (.74, 0)]),
    "g": (.95, [(0, 0), (.1, -.37), (.33, -.58), (.59, -.47), (.58, -.12), (.37, .05), (.17, -.12), (.3, -.45), (.62, -.55), (.72, .32), (.57, .65), (.36, .62), (.39, .39), (.95, 0)]),
    "h": (1.01, [(0, 0), (.15, -.56), (.29, -1.28), (.12, -1.37), (.08, -1.16), (.38, -.52), (.41, 0), (.55, -.38), (.78, -.55), (.88, -.42), (.76, -.05), (1.01, 0)]),
    "i": (.5, [(0, 0), (.16, -.3), (.27, -.52), (.34, -.35), (.29, -.06), (.5, 0)]),
    "j": (.57, [(0, 0), (.19, -.33), (.33, -.55), (.42, -.34), (.28, .38), (.12, .57), (-.04, .44), (.1, .17), (.57, 0)]),
    "k": (.99, [(0, 0), (.14, -.58), (.27, -1.27), (.1, -1.38), (.05, -1.16), (.34, -.5), (.39, 0), (.49, -.3), (.72, -.58), (.88, -.52), (.67, -.27), (.41, -.18), (.69, -.12), (.99, 0)]),
    "l": (.65, [(0, 0), (.17, -.59), (.31, -1.29), (.17, -1.39), (.09, -1.16), (.24, -.47), (.39, -.03), (.65, 0)]),
    "m": (1.45, [(0, 0), (.15, -.36), (.34, -.56), (.43, -.38), (.35, -.02), (.57, -.4), (.78, -.55), (.85, -.36), (.75, -.02), (.99, -.4), (1.22, -.55), (1.31, -.36), (1.2, -.04), (1.45, 0)]),
    "n": (1.01, [(0, 0), (.15, -.38), (.35, -.56), (.44, -.36), (.35, -.02), (.56, -.39), (.77, -.54), (.88, -.39), (.75, -.05), (1.01, 0)]),
    "o": (.89, [(0, 0), (.15, -.4), (.4, -.58), (.66, -.47), (.7, -.19), (.49, .04), (.23, -.05), (.21, -.35), (.48, -.56), (.76, -.39), (.89, -.28)]),
    "p": (.99, [(0, 0), (.12, -.37), (.3, -.58), (.4, -.38), (.32, .56), (.18, .68), (.2, .38), (.51, -.46), (.77, -.54), (.88, -.26), (.7, .02), (.49, -.03), (.99, 0)]),
    "q": (.96, [(0, 0), (.11, -.4), (.36, -.6), (.62, -.5), (.61, -.14), (.39, .04), (.19, -.1), (.31, -.46), (.63, -.55), (.75, .52), (.91, .6), (.84, .38), (.96, 0)]),
    "r": (.75, [(0, 0), (.14, -.36), (.32, -.53), (.39, -.34), (.35, -.14), (.48, -.48), (.65, -.56), (.74, -.42), (.6, -.23), (.75, 0)]),
    "s": (.77, [(0, 0), (.19, -.3), (.48, -.57), (.67, -.48), (.47, -.34), (.29, -.25), (.5, -.12), (.55, .03), (.29, .08), (.14, -.04), (.77, 0)]),
    "t": (.69, [(0, 0), (.2, -.49), (.39, -1.03), (.34, -.42), (.32, -.06), (.45, .03), (.69, 0)]),
    "u": (.98, [(0, 0), (.12, -.48), (.24, -.56), (.32, -.35), (.26, -.04), (.43, .03), (.63, -.17), (.77, -.55), (.82, -.35), (.77, -.05), (.98, 0)]),
    "v": (.92, [(0, 0), (.1, -.48), (.23, -.55), (.32, -.28), (.42, -.01), (.57, -.14), (.81, -.55), (.76, -.27), (.92, 0)]),
    "w": (1.27, [(0, 0), (.1, -.48), (.23, -.55), (.31, -.23), (.4, -.02), (.53, -.36), (.68, -.55), (.78, -.23), (.9, -.02), (1.06, -.3), (1.19, -.55), (1.14, -.22), (1.27, 0)]),
    "x": (.87, [(0, 0), (.19, -.5), (.31, -.56), (.48, -.29), (.74, 0), (.47, -.26), (.25, -.05), (.15, .03), (.46, -.28), (.77, -.58), (.87, 0)]),
    "y": (.96, [(0, 0), (.11, -.48), (.23, -.57), (.32, -.36), (.3, -.05), (.47, .04), (.65, -.21), (.8, -.55), (.67, .31), (.45, .64), (.28, .56), (.39, .35), (.96, 0)]),
    "z": (.85, [(0, 0), (.17, -.43), (.47, -.55), (.69, -.48), (.53, -.31), (.23, -.04), (.54, .03), (.85, 0)]),
}

PLANS = ("full", "surname", "initial_surname", "monogram", "personal_short", "gesture")

CAPITALS = {
    "a": (1.05, [(0, 0), (.16, -.62), (.48, -1.36), (.69, -.75), (.94, 0), (.75, -.45), (.29, -.43), (1.05, 0)]),
    "b": (1.04, [(0, 0), (.14, -.55), (.22, -1.31), (.51, -1.35), (.84, -1.15), (.70, -.89), (.27, -.68), (.68, -.68), (1.00, -.41), (.88, -.11), (.45, .04), (.18, 0), (1.04, 0)]),
    "c": (1.00, [(.99, -1.15), (.55, -1.38), (.13, -.94), (.12, -.32), (.51, .03), (1, -.12)]),
    "d": (1.05, [(0, 0), (.22, -1.32), (.58, -1.28), (.98, -.9), (.86, -.32), (.49, -.02), (0, 0), (1.05, 0)]),
    "e": (.96, [(.94, -1.3), (.25, -1.28), (.14, -.05), (.96, 0), (.18, -.55), (.76, -.61)]),
    "f": (.92, [(.02, 0), (.28, -1.3), (.9, -1.36), (.33, -.7), (.81, -.73), (.92, 0)]),
    "g": (1.06, [(1.02, -1.17), (.53, -1.37), (.12, -.91), (.16, -.27), (.55, .03), (.91, -.2), (.85, -.61), (.58, -.61), (1.06, 0)]),
    "h": (1.05, [(0, 0), (.22, -1.35), (.27, -.61), (.81, -.63), (.91, -1.34), (.76, 0), (1.05, 0)]),
    "i": (.59, [(0, -1.31), (.51, -1.34), (.29, -1.3), (.2, -.05), (.59, 0)]),
    "j": (.76, [(.18, -1.34), (.72, -1.37), (.55, -.21), (.3, .16), (0, .09), (.76, 0)]),
    "k": (1.03, [(.15, -1.35), (.14, -.93), (.13, -.47), (.12, 0)]),
    "l": (.83, [(0, -1.33), (.27, -1.36), (.18, -.04), (.83, 0)]),
    "m": (1.44, [(0, .02), (.24, -1.36), (.69, -.44), (1.13, -1.35), (1.44, 0)]),
    "n": (1.15, [(0, 0), (.22, -1.35), (.94, -.04), (.91, -1.35), (1.15, 0)]),
    "o": (1.05, [(.75, -1.34), (.22, -1.21), (0, -.62), (.24, -.03), (.8, -.06), (1.04, -.71), (.75, -1.34), (1.05, 0)]),
    "p": (1.02, [(0, 0), (.21, -1.33), (.65, -1.32), (.96, -1.04), (.73, -.68), (.24, -.64)]),
    "q": (1.09, [(.77, -1.3), (.22, -1.21), (0, -.59), (.27, -.02), (.86, -.1), (1.03, -.73), (.77, -1.3), (.61, -.25), (1.09, 0)]),
    "r": (1.06, [(0, 0), (.2, -1.34), (.65, -1.31), (.94, -1), (.71, -.67), (.25, -.62), (.58, -.59), (1.06, 0)]),
    "s": (.96, [(.92, -1.18), (.49, -1.36), (.16, -1.12), (.24, -.77), (.69, -.6), (.82, -.24), (.42, .03), (0, -.08), (.96, 0)]),
    "t": (.95, [(.48, -1.35), (.44, -.93), (.40, -.49), (.37, 0), (.95, 0)]),
    "u": (1.06, [(0, -1.35), (.14, -.31), (.44, 0), (.82, -.32), (.91, -1.35), (1.06, 0)]),
    "v": (1.03, [(0, -1.35), (.49, .01), (1.03, -1.35), (.73, -.37), (1.03, 0)]),
    "w": (1.35, [(0, -1.35), (.22, 0), (.58, -.91), (.78, 0), (1.35, -1.35), (1.06, -.36), (1.35, 0)]),
    "x": (1.03, [(0, -1.35), (.98, 0), (.52, -.68), (1.03, -1.35), (0, 0)]),
    "y": (1.01, [(0, -1.35), (.46, -.63), (.99, -1.35), (.46, -.63), (.5, 0), (1.01, 0)]),
    "z": (1.00, [(0, -1.35), (.98, -1.35), (.04, 0), (1, 0)]),
}

def _smooth(points: list[tuple[float, float]], per_segment: int = 7) -> list[tuple[float, float]]:
    """Sample a smooth curve through the pen control points."""
    if len(points) < 2:
        return points
    out = []
    for i in range(len(points) - 1):
        p0 = points[max(0, i - 1)]
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[min(len(points) - 1, i + 2)]
        for step in range(per_segment):
            t = step / per_segment
            t2, t3 = t * t, t * t * t
            x = .5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2*p0[0] - 5*p1[0] + 4*p2[0] - p3[0]) * t2 + (-p0[0] + 3*p1[0] - 3*p2[0] + p3[0]) * t3)
            y = .5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2*p0[1] - 5*p1[1] + 4*p2[1] - p3[1]) * t2 + (-p0[1] + 3*p1[1] - 3*p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(points[-1])
    return out

def _ink_path(points: list[tuple[float, float]], base_width: float, rng: random.Random) -> str:
    """Outline a stroke with thicker downstrokes and softly tapered endpoints."""
    curve = _smooth(points)
    if len(curve) < 2:
        return ""
    left, right = [], []
    phase = rng.random() * 6.28
    # Small, correlated hand tremor keeps long digital curves from looking
    # mechanically perfect. The envelope preserves the stroke endpoints.
    curve = [(x + .32 * math.sin(i * .47 + phase) * math.sin(math.pi * i / (len(curve) - 1)),
              y + .22 * math.sin(i * .41 + phase * .7) * math.sin(math.pi * i / (len(curve) - 1)))
             for i, (x, y) in enumerate(curve)]
    for i, (x, y) in enumerate(curve):
        x0, y0 = curve[max(0, i - 1)]
        x1, y1 = curve[min(len(curve) - 1, i + 1)]
        dx, dy = x1 - x0, y1 - y0
        length = math.hypot(dx, dy) or 1
        nx, ny = -dy / length, dx / length
        down = max(0, dy / length)
        taper = min(1, .22 + i / 8, .22 + (len(curve) - 1 - i) / 8)
        width = base_width * (0.65 + .78 * down) * (1 + .08 * math.sin(i * .16 + phase)) * taper
        left.append((x + nx * width / 2, y + ny * width / 2))
        right.append((x - nx * width / 2, y - ny * width / 2))
    outline = left + right[::-1]
    return "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in outline) + " Z"

def _letters(name: str, legibility: str) -> list[str]:
    # Normalize common Latin accents for the skeleton; preserve the source name
    # only in SVG metadata. Unsupported symbols become word breaks.
    plain = polish.letters(name)
    words = ["".join(c.lower() for c in part if polish.BASE.get(c.lower(), c.lower()) in GLYPHS)
             for part in plain.split()]
    words = [word for word in words if word]
    if legibility == "abbreviated":
        words = [word[:1] + (word[-1:] if len(word) > 3 else "") for word in words]
    elif legibility == "scribble":
        words = [word[:2] for word in words]
    return list(" ".join(words))

def _signature_plan(name: str, identity_seed: int, legibility: str,
                    requested: str | None = None) -> tuple[str, list[str]]:
    if legibility != "auto":
        return legibility, _letters(name, legibility)
    plain = polish.letters(name)
    words = ["".join(ch.lower() for ch in part if polish.BASE.get(ch.lower(), ch.lower()) in GLYPHS)
             for part in plain.split()]
    words = [word for word in words if word]
    if not words:
        return "full", []
    plan = requested or PLANS[identity_seed % len(PLANS)]
    if plan not in PLANS:
        raise ValueError(f"Unknown signature form: {plan}")
    if plan == "full":
        text = " ".join(words)
    elif plan == "surname":
        text = words[-1]
    elif plan == "initial_surname":
        text = (words[0][0] + " " + words[-1]) if len(words) > 1 else words[0]
    elif plan == "monogram":
        text = "".join(word[0] for word in words[:3])
    elif plan == "personal_short":
        text = words[0][:2] + (" " + words[-1][:3] if len(words) > 1 else words[0][2:4])
    else:
        text = "".join(word[0] for word in words[:2])
    return plan, list(text)

def _gesture(identity_rng: random.Random) -> tuple[list[list[tuple[float, float]]], list[list[tuple[float, float]]]]:
    """A name-stable calligraphic emblem, with an opening loop and long return."""
    radius = identity_rng.uniform(20, 30)
    span = identity_rng.uniform(160, 220)
    height = identity_rng.uniform(32, 48)
    baseline = 86
    main = [(3, baseline + 5), (-radius * .5, baseline - height * .55),
            (radius * .4, baseline - height * 1.55),
            (radius * 1.3, baseline - height * 1.05),
            (radius * .25, baseline - 4),
            (radius * 1.3, baseline - height * .9),
            (span * .38, baseline - height * .95),
            (span * .52, baseline - 3),
            (span * .64, baseline - height * .65),
            (span * .72, baseline + 4),
            (span, baseline - height * .42)]
    return [main], []

def generate(name: str, seed: int, legibility: str = "readable", sample: int = 0,
             plan_override: str | None = None, pen_scale: float = 1.0) -> str:
    # One writer identity belongs to the name. A separate stream supplies only
    # the small differences between consecutive signatures by that writer.
    identity_seed = int.from_bytes(
        hashlib.sha256(name.casefold().strip().encode("utf-8")).digest()[:8], "big")
    rng = random.Random(identity_seed)
    sample_seed = int.from_bytes(
        hashlib.sha256(f"{identity_seed}|{seed}|{sample}".encode("ascii")).digest()[:8], "big")
    sample_rng = random.Random(sample_seed)
    plan, chars = _signature_plan(name, identity_seed, legibility, plan_override)
    if not any(c != " " for c in chars):
        raise ValueError("Name needs at least one Latin letter (a-z).")
    tail_key = hashlib.sha256(f"{name.casefold().strip()}|tail-habit".encode()).digest()[0] / 255
    fast = plan in ("monogram", "personal_short", "gesture")
    tail_mode = (1 if tail_key < .32 else 2) if fast else (0 if tail_key < .32 else 1 if tail_key < .75 else 2)
    omission = 10 if fast else 32 if tail_mode == 1 else 20
    if sample and tail_mode and hashlib.sha256(
            f"{name.casefold().strip()}|{plan}|{sample}|tail".encode()).digest()[0] < omission:
        tail_mode = 0

    # Distinct writer profiles make the letter skeleton look different even
    # when two names contain similar letters. Fine tuning remains name-based.
    profile = identity_seed % 3
    sx, sy, writer_slant, writer_spacing, writer_pen = (
        (29.0, 44.0, .05, .84, 1.12),   # compact, upright, medium pressure
        (28.0, 63.0, .50, .90, .83),   # tall, strongly slanted, light
        (40.0, 47.0, .22, 1.06, 1.08), # broad, open, medium pressure
    )[profile]
    # These choices belong to the writer, so all samples retain one hand.
    traits = random.Random(hashlib.sha256(f"{name.casefold().strip()}|traits".encode()).digest())
    sx *= traits.uniform(.82, 1.18)
    sy *= traits.uniform(.80, 1.20)
    writer_slant += traits.uniform(-.14, .14)
    writer_spacing *= traits.uniform(.92, 1.16)
    writer_pen *= traits.uniform(.83, 1.09) * min(pen_scale, .92)
    writer_motion = traits.uniform(.68, 1.35)
    writer_flourish = traits.uniform(.70, 1.35)
    writer_lifts = traits.uniform(.04, .23)
    # One repeated signing changes tempo and arm reach, then individual
    # letters and joins react coherently to that tempo.
    hand_reach = 1 + (sample_rng.uniform(.86, 1.16) - 1) * writer_motion
    hand_height = 1 + (sample_rng.uniform(.82, 1.20) - 1) * writer_motion
    hand_slant = sample_rng.uniform(-.095, .095) * writer_motion
    rhythm_phase = sample_rng.uniform(-math.pi, math.pi)
    rhythm_strength = sample_rng.uniform(.045, .10) * writer_motion
    flourish_reach = sample_rng.uniform(.80, 1.28) * writer_flourish
    flourish_lift = sample_rng.uniform(.79, 1.25) * writer_flourish
    x_cursor = 0.0
    words: list[list[tuple[float, float]]] = []
    extras: list[list[tuple[float, float]]] = []
    clear_extras: set[int] = set()
    current: list[tuple[float, float]] = []
    word_index = 0
    letter_index = 0
    glyph_number = 0

    def quick_tail() -> None:
        nonlocal x_cursor
        if legibility != "scribble" or not current:
            return
        # A recognizable opening gives way to rapid rising and falling pen
        # gestures, as happens when a signer stops forming complete letters.
        px, py = current[-1]
        for _ in range(rng.randint(2, 4)):
            span = rng.uniform(13, 19)
            current.extend([(px + span * .42, py - rng.uniform(13, 24)),
                            (px + span, py + rng.uniform(-1.5, 3.5))])
            px, py = current[-1]
        x_cursor = max(x_cursor, px)

    for ch in chars:
        if ch == " ":
            if current:
                quick_tail()
                words.append(current)
                current = []
                word_index += 1
            if plan == "initial_surname" and word_index == 1:
                # A separate, imperfect dot belongs to the initial. In some
                # executions the pen dabs; in others it briefly drags.
                dot_x = x_cursor + sx * .21
                dot_y = 87 + sample_rng.uniform(-2.0, 2.0)
                dot_len = sample_rng.uniform(1.8, 5.5)
                extras.append([(dot_x, dot_y),
                               (dot_x + dot_len * .47, dot_y + sample_rng.uniform(-1.0, .8)),
                               (dot_x + dot_len, dot_y + sample_rng.uniform(-.7, 1.4))])
                # Leave room for the surname's capital entry loop so the dab
                # reads as punctuation rather than part of the next letter.
                x_cursor += sx * 1.20
            else:
                x_cursor += sx * (1.30 if plan == "full" else .60)
            letter_index = 0
            continue
        capital = letter_index == 0
        base_ch = polish.BASE.get(ch, ch)
        width, knots = CAPITALS[base_ch] if capital else GLYPHS[base_ch]
        pulse = math.sin(glyph_number * 1.42 + rhythm_phase)
        local_x = 1 + rhythm_strength * pulse + sample_rng.uniform(-.045, .045)
        local_y = 1 + rhythm_strength * math.sin(glyph_number * 1.12 + rhythm_phase) + sample_rng.uniform(-.04, .04)
        scale_x = rng.uniform(.94, 1.08) * hand_reach * local_x * (1.30 if plan == "monogram" else 1)
        scale_y = rng.uniform(.94, 1.05) * hand_height * local_y * (1.15 if plan == "monogram" else 1)
        base_y = 86 + word_index * 1.4 + 6.0 * writer_motion * math.sin(x_cursor / 112 + identity_seed * .2)
        base_y += sample_rng.uniform(-2.5, 2.5) * writer_motion + 4.8 * writer_motion * math.sin(glyph_number * 1.14 + rhythm_phase)
        slant = writer_slant + hand_slant + rng.uniform(-.025, .025)

        def place(px: float, py: float) -> tuple[float, float]:
            yy = py * sy * scale_y
            return (x_cursor + px * sx * scale_x - yy * slant,
                    base_y + yy + .35 * math.sin(px * 2.7 + x_cursor * .04))

        if capital and profile != 0:
            # Keep subsequent sample variation stable after removing the
            # detached mark that appeared before each capital.
            sample_rng.uniform(.80, 1.27)

        glyph_points = [place(px, py) for px, py in knots]
        if current:
            # Slightly arched connector stays in the same physical pen stroke.
            px, py = current[-1]
            qx, qy = glyph_points[0]
            lift = sample_rng.random() < writer_lifts
            if letter_index == 1 or lift:
                words.append(current)
                current = []
            else:
                current.extend([((px + qx) / 2, min(py, qy) - sample_rng.uniform(1.0, 7.0)), (qx, qy)])
        current.extend(glyph_points)

        if capital and base_ch == "t":
            extras.append([place(x, y) for x, y in [(.06, -1.29), (.48, -1.38), (.92, -1.29)]])
        if capital and base_ch == "k":
            extras.append([place(x, y) for x, y in [(.88, -1.35), (.64, -1.04), (.22, -.59), (.62, -.27), (.95, 0)]])
        for mark in polish.marks(ch, -1.48 if capital else -.78, capital):
            clear_extras.add(len(extras))
            extras.append([place(x, y) for x, y in mark])

        if base_ch in "ij" and not capital:
            clear_extras.add(len(extras))
            extras.append([place(.22, -.76), place(.29, -.83), place(.34, -.76)])
        if base_ch == "f" or (base_ch == "t" and not capital):
            clear_extras.add(len(extras))
            extras.append([place(.08, -.66), place(.4, -.7), place(.72, -.73)])
        x_cursor += width * sx * scale_x * writer_spacing * rng.uniform(.97, 1.03) * (.64 if plan == "monogram" else 1)
        letter_index += 1
        glyph_number += 1
    if current:
        quick_tail()
        words.append(current)

    if plan == "gesture":
        words, extras = _gesture(rng)
        x_cursor = max(x for stroke in words for x, _ in stroke)

    # The exit follows the final letter's shape and the writer's usual reach.
    last = words[-1]
    ex, ey = last[-1]
    final_letter = next(ch for ch in reversed(chars) if ch != " ")
    exit_turn = max(-8.0, min(8.0, (ey - last[-2][1]) * .25))
    if final_letter in "ijlt":
        tail_steps = ((10, -8), (26, -13), (38, -6))
    elif final_letter in "gjpqy":
        tail_steps = ((10, -2), (27, -11), (43, -13))
    elif final_letter in "aeo":
        tail_steps = ((14, -5), (34, -4), (50, 2))
    else:
        tail_steps = ((11, -10), (31, -2), (47, -6))
    if tail_mode:
        tail_scale = (.85 if tail_mode == 1 else 1.20) if fast else (.55 if tail_mode == 1 else 1.0)
        profile_reach = (.82, 1.12, 1.0)[profile]
        tail_bend = (random.Random(hashlib.sha256(
            f"{name.casefold().strip()}|{plan}|{sample}|tail-shape".encode()).digest()).uniform(.72, 1.28)
            if fast else 1.0)
        last.extend((ex + dx * flourish_reach * profile_reach * tail_scale,
                     ey + (dy * flourish_lift * tail_bend + exit_turn * (i + 1) / len(tail_steps)) * tail_scale)
                    for i, (dx, dy) in enumerate(tail_steps))
    if plan != "full" and profile != 0 and rng.random() < .015:
        underline = [(ex + 50, ey + 13), (ex + 8, ey + 25), (ex - x_cursor * .38, ey + 31), (ex - x_cursor * .74, ey + 25), (ex - x_cursor * .5, ey + 22)]
        extras.append(underline)

    # Small whole-hand changes plus tiny control-point shifts preserve the
    # writer's letter forms, spacing, flourish and pressure across samples.
    stretch_x = sample_rng.uniform(.975, 1.03)
    stretch_y = sample_rng.uniform(.945, 1.055)
    tilt = sample_rng.uniform(-.014, .014)
    def vary(stroke: list[tuple[float, float]]) -> list[tuple[float, float]]:
        # Smooth changes across a whole pen movement preserve the writer's
        # characteristic stroke instead of adding unrelated point noise.
        phase = sample_rng.uniform(-math.pi, math.pi)
        swing_x = sample_rng.uniform(.8, 2.5)
        swing_y = sample_rng.uniform(1.0, 3.0)
        n = max(1, len(stroke) - 1)
        return [(x * stretch_x + (y - 86) * tilt +
                 swing_x * math.sin(2 * math.pi * i / n + phase),
                 86 + (y - 86) * stretch_y +
                 swing_y * math.sin(2 * math.pi * i / n + phase * .7))
                for i, (x, y) in enumerate(stroke)]

    words = [vary(stroke) for stroke in words]
    extras = [vary(stroke) for stroke in extras]
    end_x, end_y = words[-1][-1]
    tail_x = sample_rng.uniform(4, 10)
    tail_y = sample_rng.uniform(-4, 5)
    if tail_mode:
        tail_scale = .55 if tail_mode == 1 else 1.0
        words[-1].append((end_x + tail_x * .55 * tail_scale, end_y + tail_y * .45 * tail_scale))
        words[-1].append((end_x + tail_x * tail_scale, end_y + tail_y * tail_scale))
    all_points = [pt for stroke in words + extras for pt in stroke]
    min_x = min(x for x, _ in all_points) - 12
    max_x = max(x for x, _ in all_points) + 12
    min_y = min(y for _, y in all_points) - 12
    max_y = max(y for _, y in all_points) + 12
    ink = rng.choice(["#202227", "#171e2a", "#25252b"])
    pressure = sample_rng.uniform(.90, 1.10)
    paths = [f'<path d="{_ink_path(stroke, 2.3 * writer_pen * pressure, sample_rng)}"/>' for stroke in words]
    for index, stroke in enumerate(extras):
        if index in clear_extras:
            path = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in stroke)
            paths.append(f'<path d="{path}" fill="none" stroke="{ink}" '
                         f'stroke-width="{max(1.5, 1.9 * writer_pen * pressure):.2f}" '
                         'stroke-linecap="round" stroke-linejoin="round"/>')
        else:
            paths.append(f'<path d="{_ink_path(stroke, (1.7 if len(stroke) > 4 else 2.0) * writer_pen * pressure, sample_rng)}"/>')
    title = html.escape(f"Fictional handwritten signature inspired by {name}", quote=True)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x:.1f} {min_y:.1f} {max_x-min_x:.1f} {max_y-min_y:.1f}" '
            f'width="{max_x-min_x:.0f}" height="{max_y-min_y:.0f}" role="img" data-plan="{plan}" aria-label="{title}">\n'
            f'<title>{title}</title>\n<g fill="{ink}">\n' + "\n".join(paths) + "\n</g>\n</svg>\n")
