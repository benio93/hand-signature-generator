"""Keep Polish letters in the drawing and place their handwritten marks."""

import unicodedata


BASE = dict(zip("ąćęłńóśźż", "acelnoszz"))


def letters(text: str) -> str:
    result = []
    for char in text:
        if char.lower() in BASE:
            result.append(char)
        else:
            result.extend(c for c in unicodedata.normalize("NFKD", char)
                          if not unicodedata.combining(c))
    return "".join(result)


def marks(char: str, top: float, capital: bool = False) -> list[list[tuple[float, float]]]:
    lower = char.lower()
    if lower in "ćńóśź":
        return [[(.37, top), (.56, top - .20)]]
    if lower == "ż":
        return [[(.46, top - .04), (.50, top - .08), (.54, top - .04)]]
    if lower == "ł":
        y = -.71 if capital else -.57
        return [[(.04, y + .07), (.32, y), (.56, y - .07)]]
    if lower in "ąę":
        return [[(.68, -.08), (.79, .13), (.72, .25), (.58, .22)]]
    return []
