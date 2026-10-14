"""Procedural handwriting style A."""

from __future__ import annotations

import hashlib

import html

import math

import random

import unicodedata

from . import polish

GLYPHS = {
    "a": [(0,-.34),(.12,-.72),(.42,-.98),(.70,-.80),(.70,-.37),(.48,-.08),(.17,-.12),(.04,-.42),(.27,-.87),(.68,-.85),(.77,-.52),(.80,-.13),(1,-.33)],
    "b": [(0,-.36),(.18,-.70),(.29,-1.37),(.43,-1.70),(.55,-1.35),(.45,-.78),(.28,-.17),(.49,-.79),(.76,-.91),(.90,-.59),(.79,-.19),(.49,-.11),(.87,-.12),(1,-.34)],
    "c": [(0,-.37),(.22,-.77),(.56,-.91),(.83,-.70),(.61,-.83),(.28,-.68),(.23,-.28),(.52,-.10),(.83,-.17),(1,-.35)],
    "d": [(0,-.35),(.14,-.75),(.44,-.97),(.69,-.79),(.67,-.37),(.43,-.09),(.15,-.15),(.04,-.48),(.29,-.87),(.66,-.84),(.80,-1.23),(.91,-1.69),(.99,-1.36),(.89,-.25),(1,-.34)],
    "e": [(0,-.38),(.25,-.52),(.53,-.74),(.76,-.67),(.60,-.45),(.27,-.43),(.30,-.18),(.58,-.08),(.83,-.17),(1,-.35)],
    "f": [(0,-.35),(.19,-.74),(.32,-1.40),(.55,-1.72),(.68,-1.42),(.44,-.77),(.34,.34),(.49,.69),(.70,.43),(.86,-.12),(1,-.35)],
    "g": [(0,-.34),(.17,-.75),(.47,-.96),(.73,-.77),(.70,-.33),(.43,-.10),(.17,-.16),(.06,-.49),(.31,-.87),(.73,-.85),(.70,.27),(.49,.61),(.29,.47),(.55,.12),(1,-.34)],
    "h": [(0,-.35),(.17,-.72),(.30,-1.38),(.44,-1.65),(.56,-1.30),(.43,-.67),(.35,-.17),(.54,-.77),(.75,-.90),(.88,-.69),(.82,-.17),(1,-.35)],
    "i": [(0,-.38),(.18,-.74),(.33,-.85),(.44,-.69),(.40,-.24),(.57,-.12),(.78,-.20),(1,-.36)],
    "j": [(0,-.38),(.24,-.77),(.48,-.86),(.60,-.67),(.52,.30),(.35,.63),(.13,.46),(.43,.09),(1,-.36)],
    "k": [(0,-.36),(.16,-.76),(.30,-1.40),(.44,-1.65),(.56,-1.35),(.43,-.62),(.35,-.13),(.52,-.61),(.87,-.91),(.59,-.49),(.88,-.13),(1,-.35)],
    "l": [(0,-.37),(.16,-.77),(.32,-1.43),(.49,-1.67),(.61,-1.42),(.49,-.72),(.41,-.19),(.61,-.10),(.80,-.20),(1,-.37)],
    "m": [(0,-.37),(.18,-.74),(.36,-.86),(.48,-.70),(.41,-.16),(.57,-.75),(.75,-.87),(.85,-.67),(.79,-.16),(.96,-.75),(1.13,-.88),(1.26,-.66),(1.20,-.19),(1.40,-.35)],
    "n": [(0,-.37),(.18,-.75),(.36,-.85),(.49,-.65),(.41,-.15),(.59,-.74),(.78,-.87),(.92,-.65),(.85,-.17),(1,-.35)],
    "o": [(0,-.35),(.17,-.77),(.49,-.94),(.77,-.76),(.75,-.36),(.50,-.10),(.19,-.16),(.08,-.47),(.31,-.87),(.69,-.84),(.78,-.43),(1,-.35)],
    "p": [(0,-.37),(.17,-.77),(.38,-.88),(.49,-.60),(.38,.41),(.49,.57),(.60,.31),(.49,-.36),(.66,-.82),(.87,-.86),(.98,-.56),(.83,-.17),(.58,-.15),(1,-.35)],
    "q": [(0,-.36),(.18,-.77),(.47,-.95),(.74,-.76),(.72,-.35),(.46,-.10),(.18,-.18),(.07,-.48),(.31,-.87),(.72,-.83),(.80,.35),(.98,.43),(1.08,.10),(1,-.35)],
    "r": [(0,-.35),(.18,-.75),(.36,-.85),(.49,-.58),(.41,-.18),(.58,-.67),(.75,-.83),(.91,-.67),(.75,-.50),(.83,-.17),(1,-.35)],
    "s": [(0,-.36),(.28,-.74),(.59,-.87),(.79,-.68),(.62,-.53),(.30,-.42),(.28,-.18),(.56,-.10),(.82,-.22),(1,-.35)],
    "t": [(0,-.37),(.18,-.77),(.35,-1.32),(.52,-1.48),(.60,-1.25),(.50,-.68),(.45,-.20),(.61,-.12),(.83,-.20),(1,-.36)],
    "u": [(0,-.37),(.17,-.75),(.30,-.83),(.41,-.66),(.32,-.23),(.49,-.13),(.70,-.71),(.86,-.84),(.93,-.65),(.85,-.17),(1,-.35)],
    "v": [(0,-.37),(.16,-.73),(.30,-.79),(.43,-.26),(.54,-.10),(.69,-.47),(.82,-.79),(.90,-.58),(1,-.35)],
    "w": [(0,-.36),(.15,-.73),(.28,-.79),(.40,-.22),(.52,-.12),(.66,-.72),(.78,-.80),(.89,-.22),(1.01,-.11),(1.16,-.74),(1.28,-.77),(1.40,-.35)],
    "x": [(0,-.36),(.18,-.72),(.34,-.82),(.57,-.22),(.76,-.13),(1,-.35)],
    "y": [(0,-.36),(.18,-.76),(.35,-.83),(.44,-.62),(.36,-.19),(.55,-.11),(.75,-.73),(.91,-.84),(.82,.29),(.62,.61),(.36,.47),(.60,.10),(1,-.35)],
    "z": [(0,-.37),(.23,-.77),(.54,-.88),(.80,-.77),(.57,-.48),(.29,-.18),(.62,-.14),(.85,-.22),(1,-.35)],
}

CAPITALS = {
    "a": [(0,-.3),(.17,-.85),(.48,-1.61),(.63,-1.34),(.83,-.18),(.71,-.76),(.30,-.74),(.75,-.72),(1,-.34)],
    "b": [(0,-.3),(.24,-.64),(.31,-1.52),(.53,-1.63),(.78,-1.44),(.70,-1.12),(.35,-.99),(.77,-.93),(.89,-.56),(.67,-.18),(.33,-.16),(1,-.34)],
    "c": [(0,-.3),(.22,-.91),(.56,-1.56),(.89,-1.43),(.61,-1.48),(.31,-1.11),(.27,-.47),(.59,-.16),(.89,-.24),(1,-.34)],
    "d": [(0,-.3),(.24,-.69),(.33,-1.51),(.57,-1.62),(.87,-1.35),(.90,-.58),(.62,-.17),(.32,-.20),(.80,-.27),(1,-.34)],
    "e": [(0,-.3),(.26,-.70),(.77,-.79),(.48,-.74),(.33,-1.28),(.67,-1.58),(.87,-1.39),(.46,-.98),(.31,-.38),(.65,-.15),(1,-.34)],
    "f": [(0,-.3),(.22,-.72),(.31,-1.50),(.79,-1.57),(.41,-1.45),(.38,-.83),(.75,-.90),(.38,-.82),(.38,-.15)],
    "g": [(0,-.3),(.18,-.97),(.53,-1.56),(.87,-1.39),(.62,-1.48),(.32,-1.13),(.28,-.47),(.55,-.16),(.79,-.24),(.79,-.80),(.80,-.13),(1,-.34)],
    "h": [(0,-.3),(.26,-.73),(.30,-1.57),(.35,-.84),(.75,-.86),(.77,-1.55),(.78,-.23),(.85,-.36),(1,-.34)],
    "i": [(0,-.3),(.20,-.74),(.31,-1.54),(.69,-1.53),(.51,-1.48),(.48,-.22),(.29,-.19),(.71,-.18),(1,-.34)],
    "j": [(0,-.3),(.19,-.73),(.43,-1.53),(.81,-1.52),(.62,-1.48),(.60,-.12),(.39,.19),(.19,.07),(.48,-.22),(1,-.34)],
    "k": [(0,-.3),(.25,-.70),(.32,-1.55),(.35,-.15),(.42,-.75),(.83,-1.52),(.51,-.87),(.83,-.17),(1,-.34)],
    "l": [(0,-.3),(.24,-.73),(.36,-1.56),(.39,-.19),(.82,-.17),(1,-.34)],
    "m": [(0,-.3),(.20,-1.51),(.33,-1.18),(.50,-.66),(.69,-1.18),(.82,-1.51),(.91,-.18),(1,-.34)],
    "n": [(0,-.3),(.25,-1.51),(.31,-.18),(.36,-.61),(.77,-1.46),(.85,-.17),(1,-.34)],
    "o": [(0,-.3),(.16,-.81),(.44,-1.53),(.71,-1.55),(.88,-1.09),(.77,-.40),(.49,-.15),(.25,-.29),(.23,-.98),(.54,-1.48),(1,-.34)],
    "p": [(0,-.3),(.24,-.72),(.31,-1.52),(.54,-1.57),(.85,-1.34),(.82,-.95),(.37,-.87),(.37,-.19),(1,-.34)],
    "q": [(0,-.3),(.17,-.87),(.46,-1.53),(.77,-1.45),(.88,-.89),(.70,-.31),(.43,-.17),(.24,-.36),(.28,-1.07),(.56,-1.49),(.72,-.24),(.92,.02),(1,-.34)],
    "r": [(0,-.3),(.25,-.70),(.33,-1.53),(.60,-1.55),(.84,-1.31),(.72,-.91),(.37,-.82),(.56,-.83),(.85,-.17),(1,-.34)],
    "s": [(0,-.3),(.22,-.76),(.77,-1.51),(.54,-1.50),(.29,-1.23),(.66,-.81),(.81,-.46),(.56,-.17),(.25,-.26),(1,-.34)],
    "t": [(0,-.3),(.19,-.76),(.31,-1.48),(.83,-1.51),(.52,-1.44),(.51,-.18),(.54,-.73),(.80,-.75),(1,-.34)],
    "u": [(0,-.3),(.22,-1.49),(.30,-.56),(.52,-.18),(.76,-.57),(.82,-1.48),(.87,-.18),(1,-.34)],
    "v": [(0,-.3),(.22,-1.48),(.46,-.18),(.59,-.27),(.84,-1.49),(1,-.34)],
    "w": [(0,-.3),(.18,-1.49),(.34,-.20),(.49,-.87),(.65,-.20),(.85,-1.49),(1,-.34)],
    "x": [(0,-.3),(.22,-1.47),(.78,-.17),(.51,-.82),(.82,-1.49),(.29,-.18),(1,-.34)],
    "y": [(0,-.3),(.20,-1.47),(.51,-.86),(.80,-1.48),(.51,-.85),(.52,-.18),(1,-.34)],
    "z": [(0,-.3),(.23,-1.48),(.83,-1.49),(.39,-.18),(.84,-.17),(1,-.34)],
}

ACCENT_MAP = str.maketrans({"ł": "l", "Ł": "L", "ß": "ss", "æ": "ae", "Æ": "Ae", "ø": "o", "Ø": "O"})

def ascii_letters(name: str) -> str:
    plain = unicodedata.normalize("NFKD", name.translate(ACCENT_MAP))
    plain = "".join(c for c in plain if not unicodedata.combining(c))
    return "".join(c if c.isalpha() and c.lower() in GLYPHS else " " for c in plain)


def signature_letters(name: str) -> str:
    return "".join(c if c.lower() in GLYPHS or c.lower() in polish.BASE else " "
                   for c in polish.letters(name))

def catmull(points: list[tuple[float, float]], steps: int = 7) -> list[tuple[float, float]]:
    """Interpolate pen points without sharp corners."""
    if len(points) < 2:
        return points
    out = []
    for i in range(len(points) - 1):
        p0 = points[max(i - 1, 0)]
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[min(i + 2, len(points) - 1)]
        for j in range(steps):
            t = j / steps
            t2, t3 = t*t, t*t*t
            x = .5 * (2*p1[0] + (-p0[0]+p2[0])*t + (2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2 + (-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
            y = .5 * (2*p1[1] + (-p0[1]+p2[1])*t + (2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2 + (-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
            out.append((x, y))
    out.append(points[-1])
    return out

def path_d(points: list[tuple[float, float]]) -> str:
    return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in points)

def ink_ribbon(points: list[tuple[float, float]], phase: float, base_width: float = 2.2) -> str:
    """A single filled outline: smooth nib pressure and tapered pen lifts."""
    left, right = [], []
    count = len(points)
    for i, (x, y) in enumerate(points):
        before = points[max(0, i-1)]
        after = points[min(count-1, i+1)]
        dx, dy = after[0]-before[0], after[1]-before[1]
        distance = math.hypot(dx, dy) or 1.0
        nx, ny = -dy/distance, dx/distance
        down = max(0.0, dy/distance)
        taper = min(1.0, .20+i/9, .20+(count-1-i)/12)
        pressure = (.62 + .80*down) * (1 + .07*math.sin(i*.16+phase))
        radius = base_width*pressure*taper/2
        left.append((x+nx*radius, y+ny*radius))
        right.append((x-nx*radius, y-ny*radius))
    return path_d(left+right[::-1]) + " Z"

PLANS = ("full", "surname", "initial_surname", "monogram", "personal_short", "gesture")

def signature_plan(name: str, requested: str | None = None) -> tuple[str, str]:
    """Choose the person's signature idea from the name, independently of sample/seed."""
    words = signature_letters(name).split()
    if not words:
        raise ValueError("--name musi zawierać przynajmniej jedną literę A-Z")
    digest = hashlib.sha256(name.casefold().strip().encode("utf-8")).digest()
    plan = requested or PLANS[int.from_bytes(digest[:4], "big") % len(PLANS)]
    if plan not in PLANS:
        raise ValueError(f"Unknown signature form: {plan}")
    if plan == "full":
        text = " ".join(words)
    elif plan == "surname":
        text = words[-1]
    elif plan == "initial_surname":
        text = words[0][0] + " " + words[-1] if len(words) > 1 else words[0]
    elif plan == "monogram":
        text = "".join(word[0] for word in words) if len(words) > 1 else words[0][:2]
    elif plan == "personal_short":
        text = words[0][:3] + " " + words[-1][:3] if len(words) > 1 else words[0][:4]
    else:
        text = ""
    return plan, text

def gesture_strokes(rng: random.Random, variation: random.Random):
    """One repeatable, letter-free pen gesture, with small execution changes."""
    rise = rng.uniform(1.25, 1.85) * variation.uniform(.71, 1.29)
    loop = rng.uniform(.58, .95) * variation.uniform(.60, 1.40)
    middle = rng.uniform(2.0, 2.8) * variation.uniform(.73, 1.27)
    end = rng.uniform(4.2, 5.0) * variation.uniform(.71, 1.33)
    anchors = [(-.3, -.18), (0, -.52), (.26, -rise), (.60, -rise*.93),
               (.72, -.45), (.22, -.17), (.32, -.88), (loop, -1.03),
               (1.18, -.26), (1.54, -.12), (middle, -.72),
               (middle+.43, -.20), (middle+.91, -.54),
               (end-.45, -.18), (end, -.35), (end-.65, .24),
               (end-1.9, .30), (end-2.55, .12)]
    anchors = [(x + variation.uniform(-.118, .118),
                y + variation.uniform(-.198, .198)) for x, y in anchors]
    return [catmull(anchors)], [], [], end + .3

def strokes(name: str, rng: random.Random, style: str,
            variation: random.Random | None = None, energy: float = 1.0,
            tail_mode: int = 2):
    words = signature_letters(name).split()
    if not words:
        raise ValueError("--name musi zawierać przynajmniej jedną literę A-Z")
    if style == "quick":
        if len(words) > 1:
            words = [words[0][0], words[-1][:min(4, len(words[-1]))]]
        else:
            words = [words[0][:min(4, len(words[0]))]]
    all_words = []
    dots = []
    bars = []
    accents = []
    xcursor = 0.0
    baseline_walk = 0.0
    for word_index, word in enumerate(words):
        anchors = []
        for index, char in enumerate(word):
            capital = index == 0 or style == "monogram"
            base_char = polish.BASE.get(char.lower(), char.lower())
            glyph = CAPITALS[base_char] if capital else GLYPHS[base_char]
            width = 1.0 if capital and base_char == "f" else glyph[-1][0]
            xstretch = rng.uniform(1 - .12 * energy, 1 + .13 * energy)
            ystretch = rng.uniform(1 - .07 * energy, 1 + .10 * energy) * (1.12 if style == "monogram" else 1)
            if variation is not None:
                xstretch *= variation.uniform(.88, 1.12)
                ystretch *= variation.uniform(.91, 1.09)
            baseline_walk = max(-.20 * energy, min(.20 * energy, .70 * baseline_walk
                                + rng.uniform(-.13 * energy, .13 * energy)
                                + (variation.uniform(-.035 * energy, .035 * energy) if variation is not None else 0)))
            letter_lift = baseline_walk + .11 * energy * math.sin(index * .85 + word_index * 1.8)
            # Tall first letter, slight wobble, and independent character rhythm.
            for gx, gy in glyph:
                xx = xcursor + gx*xstretch
                yy = gy*ystretch + letter_lift + rng.uniform(-.025, .025)
                if variation is not None:
                    yy += variation.uniform(-.045, .045)
                anchors.append((xx, yy))
            for mark in polish.marks(char, min(y for _, y in glyph) - .14, capital):
                accents.append([(xcursor + gx*xstretch, gy*ystretch + letter_lift)
                                for gx, gy in mark])
            if base_char in "ij" and not capital:
                dots.append((xcursor + .46*xstretch, -1.22*ystretch + letter_lift, "letter"))
            if base_char in "tf":
                bars.append((xcursor + .10*xstretch, xcursor + .72*xstretch, -.83*ystretch + letter_lift))
            if base_char == "x":
                bars.append((xcursor + .19*xstretch, xcursor + .78*xstretch, -.73*ystretch + letter_lift))
            rhythm = variation.uniform(.92, 1.09) if variation is not None else 1
            xcursor += width*xstretch*rng.uniform(.86, 1.04)*rhythm
            if index == 0 and base_char == "f" and len(word) > 1:
                all_words.append(catmull(anchors))
                anchors = []
        if style in ("quick", "personal_short", "monogram") and word_index == len(words) - 1:
            # The final glyph determines the direction of the shorthand exit.
            x, y = anchors[-1]
            tail = variation.uniform(.85, 1.18) if variation is not None else 1
            if tail_mode:
                tail *= 1.30 if tail_mode == 1 else 1.65
                bend = variation.uniform(.75, 1.25) if variation is not None else 1.0
                exit_turn = max(-.12, min(.12, (y - anchors[-2][1]) * .25))
                if word[-1].lower() in "ijlt":
                    tail_steps = ((.20, -.08), (.58, -.22), (1.22, -.10))
                elif word[-1].lower() in "gjpqy":
                    tail_steps = ((.24, .03), (.74, -.20), (1.62, -.28))
                elif word[-1].lower() in "aeo":
                    tail_steps = ((.30, -.11), (.93, -.08), (2.02, .02))
                else:
                    tail_steps = ((.24, -.21), (.85, -.04), (1.77, -.17))
                anchors.extend((x + dx * tail, y + (dy * bend + exit_turn * (i + 1)) * tail)
                               for i, (dx, dy) in enumerate(tail_steps))
                xcursor += tail_steps[-1][0] * tail
        all_words.append(catmull(anchors))
        if style == "initial_surname" and word_index == 0 and len(words) > 1:
            # A pen tap after the initial remains in the word gap. Its exact
            # position changes a little with each execution of this signature.
            dx = variation.uniform(-.035, .035) if variation is not None else 0
            dy = variation.uniform(-.040, .040) if variation is not None else 0
            dots.append((xcursor + .02 + dx, -.055 + dy, "period"))
        xcursor += 0 if style == "monogram" else rng.uniform(.42, .73)
    return all_words, dots, bars, xcursor, accents

def render(name: str, seed: int, style: str = "readable", sample: int = 0,
           pen_scale: float = 1.0, plan_override: str | None = None) -> str:
    if sample < 0:
        raise ValueError("sample musi być liczbą nieujemną")
    if style not in ("readable", "quick", "auto", "gesture"):
        raise ValueError("style musi być readable, quick, auto albo gesture")
    # The person's name and seed define one stable hand; sample changes only
    # small execution details, never the hand's main proportions or gestures.
    identity = f"{name.casefold().strip()}\0{seed}".encode("utf-8")
    person_key = hashlib.sha256(identity).digest()
    rng = random.Random(int.from_bytes(person_key[:8], "big"))
    profile = random.Random(int.from_bytes(person_key[8:16], "big"))
    width_scale = profile.uniform(.78, 1.23)
    height_scale = profile.uniform(.80, 1.22)
    slant = profile.uniform(-.10, .42)
    line_slope = profile.uniform(-.022, .030)
    pen_width = profile.uniform(1.55, 3.05)
    flourish = profile.random() < .015
    energy = profile.uniform(.65, 1.35)
    sample_key = hashlib.sha256(person_key + sample.to_bytes(8, "big")).digest()
    variation = random.Random(int.from_bytes(sample_key[:8], "big"))
    if style == "auto":
        plan, planned_text = signature_plan(name, plan_override)
    else:
        plan = "gesture" if style == "gesture" else "full" if style == "readable" else "personal_short"
    tail_key = hashlib.sha256(f"{name.casefold().strip()}|tail-habit".encode()).digest()[0] / 255
    fast = plan in ("monogram", "personal_short", "gesture")
    tail_mode = (1 if tail_key < .32 else 2) if fast else (0 if tail_key < .32 else 1 if tail_key < .75 else 2)
    omission = 10 if fast else 32 if tail_mode == 1 else 20
    if sample and tail_mode and hashlib.sha256(
            f"{name.casefold().strip()}|{plan}|{sample}|tail".encode()).digest()[0] < omission:
        tail_mode = 0
    width_scale *= variation.uniform(.86, 1.14)
    height_scale *= variation.uniform(.84, 1.16)
    if style == "gesture":
        words, dots, bars, length = gesture_strokes(rng, variation)
        accents = []
    elif style == "auto":
        if plan == "gesture":
            words, dots, bars, length = gesture_strokes(rng, variation)
            accents = []
        else:
            words, dots, bars, length, accents = strokes(planned_text, rng, plan, variation, energy, tail_mode)
    else:
        words, dots, bars, length, accents = strokes(name, rng, style, variation, energy, tail_mode)
    canvas_w, canvas_h = (600, 300) if plan == "gesture" else (1000, 300)
    unit = min(75, (canvas_w-130)/max(length*width_scale, 1)) if plan == "gesture" else min(46, 870/max(length*width_scale, 1))
    start_x = (canvas_w - length*width_scale*unit)/2
    base_y = 182
    slant += variation.uniform(-.075, .075)
    wobble_phase = rng.uniform(0, 6.28)
    baseline_shift = variation.uniform(-1.5, 1.5)
    motion_phase = variation.uniform(0, 6.28)
    motion_amount = variation.uniform(.012, .025)

    def place(pt):
        x, y = pt
        wave = .035*math.sin(x*.70 + wobble_phase) + line_slope*x
        wave += motion_amount*math.sin(x*.85 + motion_phase)
        return (start_x + unit*(width_scale*x - slant*height_scale*y),
                base_y + baseline_shift + unit*(height_scale*y + wave))

    elements = []
    ink = rng.choice(("#15202a", "#172536", "#1a2430", "#20212a"))
    for word_index, word in enumerate(words):
        pts = [place(p) for p in word]
        if word_index == 0:
            # A light opening gesture enters the first letter from below.
            a = pts[0]
            lead = catmull([(a[0]-unit*.55, a[1]+unit*.25),
                            (a[0]-unit*.39, a[1]+unit*.02),
                            (a[0]-unit*.15, a[1]-unit*.05), a], 6)
            elements.append(f'<path d="{ink_ribbon(lead, rng.random()*6.28, 1.4)}" fill="{ink}"/>')
        elements.append(f'<path d="{ink_ribbon(pts, rng.random()*6.28, pen_width * pen_scale * variation.uniform(.94, 1.06))}" fill="{ink}"/>')
    for x, y, kind in dots:
        px, py = place((x, y))
        if kind == "period":
            elements.append(f'<path data-mark="initial-period" d="M{px-1.7:.2f},{py+1.0:.2f} Q{px:.2f},{py-1.5:.2f} {px+2.0:.2f},{py-.2:.2f}" fill="none" stroke="{ink}" stroke-width="2.4" stroke-linecap="round"/>')
        else:
            elements.append(f'<path d="M{px-1.6:.2f},{py+1.1:.2f} Q{px:.2f},{py-1.6:.2f} {px+1.8:.2f},{py-.5:.2f}" fill="none" stroke="{ink}" stroke-width="2.0" stroke-linecap="round"/>')
    for left, right, y in bars:
        a = place((left, y))
        b = place((right, y-.07))
        elements.append(f'<path d="M{a[0]:.2f},{a[1]:.2f} Q{(a[0]+b[0])/2:.2f},{a[1]-4:.2f} {b[0]:.2f},{b[1]:.2f}" fill="none" stroke="{ink}" stroke-width="1.7" stroke-linecap="round"/>')
    for mark in accents:
        mark_points = [place(p) for p in mark]
        mark_width = max(1.65, min(2.2, pen_width * pen_scale * .9))
        elements.append(f'<path d="{path_d(mark_points)}" fill="none" stroke="{ink}" '
                        f'stroke-width="{mark_width:.2f}" stroke-linecap="round" stroke-linejoin="round"/>')
    # A finishing sweep is common in signatures, but omitted on some seeds.
    if flourish and length > 2:
        sweep = variation.uniform(.96, 1.04)
        x1 = start_x + unit*width_scale*max(0, length*.22)
        x2 = start_x + unit*width_scale*(length-.32)*sweep
        y = base_y + unit*variation.uniform(.73, .79)
        elements.append(f'<path d="M{x1:.2f},{y:.2f} C{x1+unit*length*.30:.2f},{y+unit*.16:.2f} {x2-unit*.6:.2f},{y-unit*.13:.2f} {x2:.2f},{y-unit*.34:.2f}" fill="none" stroke="{ink}" stroke-width="1.15" stroke-linecap="round" opacity=".9"/>')
    desc = html.escape(f"Synthetic handwritten signature for {name}; style {style}; seed {seed}; sample {sample}")
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" viewBox="0 0 {canvas_w} {canvas_h}" data-plan="{plan}">\n<title>{desc}</title>\n<desc>Generated procedural artwork, not a record of a person\'s signature.</desc>\n' + "\n".join(elements) + "\n</svg>\n"
