"""Identity-specific pen gesture for fictional SVG signatures."""
from __future__ import annotations

import hashlib
import html
import math
import random

from .style_a import CAPITALS, ascii_letters

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

def gesture_strokes(name: str, rng: random.Random, variation: random.Random,
                    tail_mode: int = 2):
    """Distort a name's initials into one fast, repeatable pen gesture."""
    words = ascii_letters(name).split()
    if not words:
        raise ValueError("Name needs at least one Latin letter")
    initials = [words[0][0].lower()]
    if len(words) > 1:
        initials.append(words[-1][0].lower())

    anchors = [(-.25, -.10)]
    cursor = 0.0
    for index, letter in enumerate(initials):
        width = (1.22 if index == 0 else .91) * rng.uniform(.94, 1.06)
        height = (1.02 if index == 0 else .75) * rng.uniform(.94, 1.06)
        width *= variation.uniform(.80, 1.20)
        height *= variation.uniform(.78, 1.22)
        skew = rng.uniform(.08, .24)
        letter_points = [(cursor + gx * width - gy * skew,
                          gy * height + variation.uniform(-.018, .018))
                         for gx, gy in CAPITALS[letter]]
        if index:
            anchors.append((cursor - .12, -.30))
        anchors.extend(letter_points)
        cursor += width + (.34 if index == 0 and len(initials) > 1 else 0)

    reach = rng.uniform(1.8, 2.4) * variation.uniform(.66, 1.34)
    lift = rng.uniform(.33, .54) * variation.uniform(.66, 1.34)
    last_initial = initials[-1]
    if last_initial in "ijlt":
        tail = [(cursor + .20, -.28), (cursor + reach * .52, -lift),
                (cursor + reach, -.38)]
    elif last_initial in "gjpqy":
        tail = [(cursor + .20, -.18), (cursor + reach * .35, .06),
                (cursor + reach * .70, -.25), (cursor + reach, -.43)]
    elif last_initial in "aeo":
        tail = [(cursor + .20, -.29), (cursor + reach * .33, -lift),
                (cursor + reach * .70, -.14), (cursor + reach, -.20)]
    elif last_initial in "csxz":
        tail = [(cursor + .20, -.24), (cursor + reach * .30, -.42),
                (cursor + reach * .67, -.15), (cursor + reach, -.37)]
    else:
        tail = [(cursor + .20, -.28), (cursor + reach * .32, -lift),
                (cursor + reach * .63, -.19), (cursor + reach, -.31)]
    anchors.extend(tail)
    anchors = [(x + variation.uniform(-.04, .04),
                y + variation.uniform(-.055, .055)) for x, y in anchors]
    if not tail_mode:
        del anchors[-len(tail):]
    elif tail_mode == 1:
        anchors[-len(tail):] = [(cursor + (x - cursor) * .75, y)
                                for x, y in anchors[-len(tail):]]
    tail_reach = reach * (0 if tail_mode == 0 else .75 if tail_mode == 1 else 1)
    return [catmull(anchors)], [], [], cursor + tail_reach + .3

def render_gesture(name: str, seed: int, sample: int = 0,
                   pen_scale: float = 1.0) -> str:
    if sample < 0:
        raise ValueError("sample must be non-negative")
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
    sample_key = hashlib.sha256(person_key + sample.to_bytes(8, "big")).digest()
    variation = random.Random(int.from_bytes(sample_key[:8], "big"))
    tail_key = hashlib.sha256(f"{name.casefold().strip()}|tail-habit".encode()).digest()[0] / 255
    tail_mode = 1 if tail_key < .32 else 2
    if sample and tail_mode and hashlib.sha256(
            f"{name.casefold().strip()}|gesture|{sample}|tail".encode()).digest()[0] < 10:
        tail_mode = 0
    plan = "gesture"
    words, dots, bars, length = gesture_strokes(name, rng, variation, tail_mode)
    canvas_w, canvas_h = 600, 300
    unit = min(75, (canvas_w-130)/max(length*width_scale, 1))
    start_x = (canvas_w - length*width_scale*unit)/2
    base_y = 182
    slant += variation.uniform(-.025, .025)
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
            elements.append(f'<path d="M{px-1.6:.2f},{py+1.1:.2f} Q{px:.2f},{py-1.6:.2f} {px+1.8:.2f},{py-.5:.2f}" fill="none" stroke="{ink}" stroke-width="1.5" stroke-linecap="round"/>')
    for left, right, y in bars:
        a = place((left, y))
        b = place((right, y-.07))
        elements.append(f'<path d="M{a[0]:.2f},{a[1]:.2f} Q{(a[0]+b[0])/2:.2f},{a[1]-4:.2f} {b[0]:.2f},{b[1]:.2f}" fill="none" stroke="{ink}" stroke-width="1.15" stroke-linecap="round"/>')
    # A finishing sweep is common in signatures, but omitted on some seeds.
    if flourish and length > 2:
        sweep = variation.uniform(.96, 1.04)
        x1 = start_x + unit*width_scale*max(0, length*.22)
        x2 = start_x + unit*width_scale*(length-.32)*sweep
        y = base_y + unit*variation.uniform(.73, .79)
        elements.append(f'<path d="M{x1:.2f},{y:.2f} C{x1+unit*length*.30:.2f},{y+unit*.16:.2f} {x2-unit*.6:.2f},{y-unit*.13:.2f} {x2:.2f},{y-unit*.34:.2f}" fill="none" stroke="{ink}" stroke-width="1.15" stroke-linecap="round" opacity=".9"/>')
    desc = html.escape(f"Synthetic handwritten signature for {name}; style gesture; seed {seed}; sample {sample}")
    name_words = ascii_letters(name).split()
    initials = name_words[0][0].upper()
    if len(name_words) > 1:
        initials += name_words[-1][0].upper()
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" viewBox="0 0 {canvas_w} {canvas_h}" data-plan="{plan}" data-initials="{initials}">\n<title>{desc}</title>\n<desc>Generated procedural artwork, not a record of a person\'s signature.</desc>\n' + "\n".join(elements) + "\n</svg>\n"
