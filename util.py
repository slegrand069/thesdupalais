import unicodedata, re

def normalize_text(text):

    if text is None:
        return ""

    if not isinstance(text, str):
        text = str(text)

    text = text.lower()

    # accents
    text = unicodedata.normalize(
        "NFD",
        text
    )

    text = "".join(
        c for c in text
        if unicodedata.category(c) != "Mn"
    )

    return text

def safe_split(text):

    text = text or ""

    return [

        normalize_text(x)

        for x in text.split(",")

        if x.strip()
    ]