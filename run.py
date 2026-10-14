"""Edit the settings below, then run this file with Python 3.10+."""

from __future__ import annotations

import hashlib
import html
import re
import unicodedata
import webbrowser
from pathlib import Path

from signature_playground import PLANS, render, writer_style


# EDIT THESE SETTINGS
NAMES = ["Anna Nowak", "Tomasz Kowalski"]
SAMPLES_PER_FORM = 10
FORMS = [
    "full", "surname", "initial_surname",
    "monogram", "personal_short", "gesture",
]  # Remove a form name if you want fewer forms.
VARIANT = 0  # Change this number for another repeatable set.
OPEN_GALLERY = True

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
FORM_LABELS = {
    "full": "Full name",
    "surname": "Surname",
    "initial_surname": "Initial + surname",
    "monogram": "Monogram",
    "personal_short": "Personal shorthand",
    "gesture": "Gesture mark",
}


def folder_name(name: str) -> str:
    plain = unicodedata.normalize("NFKD", name.replace("ł", "l").replace("Ł", "L"))
    plain = "".join(char for char in plain if not unicodedata.combining(char))
    readable = re.sub(r"[^a-z0-9]+", "_", plain.lower()).strip("_")[:40] or "name"
    short_hash = hashlib.sha256(name.encode("utf-8")).hexdigest()[:6]
    return f"{readable}_{short_hash}"


def make_gallery(groups: list[tuple[str, list[tuple[str, list[Path]]]]]) -> Path:
    parts = [
        '<!doctype html><html lang="en"><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<title>Signature playground</title>',
        '<style>body{font:16px system-ui,sans-serif;color:#172536;background:#f4f5f7;',
        'margin:24px auto;max-width:1200px;padding:0 16px}h1,h2,h3{font-weight:500}',
        'h2{margin-top:36px}.grid{display:grid;grid-template-columns:',
        'repeat(auto-fit,minmax(280px,1fr));gap:12px}figure{margin:0;background:white;',
        'padding:10px}img{display:block;width:100%;height:145px;object-fit:contain}',
        'figcaption{color:#5b6675;font-size:13px;margin-top:4px}</style>',
        '<h1>Signature playground</h1>',
    ]
    for name, forms in groups:
        parts.append(f"<h2>{html.escape(name)} · style {writer_style(name)}</h2>")
        for form, paths in forms:
            parts.append(f"<h3>{FORM_LABELS[form]}</h3><div class=\"grid\">")
            for number, path in enumerate(paths, start=1):
                url = html.escape(path.relative_to(OUTPUT_DIR).as_posix(), quote=True)
                parts.append(f'<figure><img src="{url}" alt="{FORM_LABELS[form]} sample {number}">'
                             f'<figcaption>{number:02d}</figcaption></figure>')
            parts.append("</div>")
    parts.append("</html>")
    gallery = OUTPUT_DIR / "index.html"
    gallery.write_text("\n".join(parts), encoding="utf-8")
    return gallery


def main() -> None:
    if not NAMES or any(not isinstance(name, str) or not name.strip() for name in NAMES):
        raise ValueError("NAMES must contain at least one non-empty name")
    if not 1 <= SAMPLES_PER_FORM <= 100:
        raise ValueError("SAMPLES_PER_FORM must be between 1 and 100")
    if not FORMS or any(form not in PLANS for form in FORMS):
        raise ValueError("FORMS must contain names from generator.PLANS")

    OUTPUT_DIR.mkdir(exist_ok=True)
    groups = []
    total = 0
    for name in NAMES:
        person_dir = OUTPUT_DIR / folder_name(name)
        forms = []
        for form in FORMS:
            form_dir = person_dir / form
            form_dir.mkdir(parents=True, exist_ok=True)
            paths = []
            for sample in range(SAMPLES_PER_FORM):
                path = form_dir / f"signature_{sample + 1:02d}.svg"
                path.write_text(render(name, sample, VARIANT, form), encoding="utf-8")
                paths.append(path)
                total += 1
            forms.append((form, paths))
        groups.append((name, forms))

    gallery = make_gallery(groups)
    print(f"Saved {total} SVG files. Gallery: {gallery}")
    if OPEN_GALLERY:
        webbrowser.open(gallery.as_uri())


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        raise SystemExit(f"Check settings in run.py: {error}")
