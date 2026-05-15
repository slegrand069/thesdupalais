import re

from datetime import datetime

from models import get_synonyms


# =====================================================
# MOMENT
# =====================================================

def get_current_moment():

    hour = datetime.now().hour

    if hour < 14:
        return "Matin"

    elif hour < 19:
        return "Après-midi"

    return "Soir"


# =====================================================
# NATIONALITÉS
# =====================================================

COUNTRY_MAP = {

    "chinois": "chine",
    "japonais": "japon",
    "indien": "inde",
    "taiwanais": "taiwan",
    "népalais": "népal",
    "sri lankais": "sri lanka",
    "africain": "afrique",
    "sud africain": "afrique",
    "vietnamien": "vietnam"
}


# =====================================================
# MOMENTS
# =====================================================

MOMENT_INTENTS = {

    "réveil": "matin",
    "énergie": "matin",
    "energisant": "matin",
    "fort": "matin",
    "réveiller": "matin",

    "détente": "soir",
    "relaxant": "soir",
    "zen": "soir",
    "calme": "soir",
    "dormir": "soir",
    "coucher": "soir",

    "apres-midi": "après-midi",
    "coup de pompe": "après-midi",
    "digestif": "après-midi",
    "digérer": "après-midi"
}


# =====================================================
# NLP HELPERS
# =====================================================

def expand_search(search):

    synonyms = get_synonyms()

    words = search.lower().split()

    expanded = []

    for w in words:

        expanded.append(w)

        if w in synonyms:

            expanded.extend(synonyms[w])

    # remove duplicates
    expanded = list(dict.fromkeys(expanded))

    return expanded


def extract_rating(search):

    search = search.lower()

    patterns = [

        r"(\d+)\s*etoiles?",
        r"(\d+)\s*stars?",
        r">\s*(\d+)",
        r"au moins\s*(\d+)",
        r"minimum\s*(\d+)"
    ]

    for p in patterns:

        m = re.search(p, search)

        if m:
            return int(m.group(1))

    return None


def extract_origin(search):

    search = search.lower()

    for nat, country in COUNTRY_MAP.items():

        if nat in search:
            return country

    return None


def extract_moment(search):

    search = search.lower()

    for word, moment in MOMENT_INTENTS.items():

        if word in search:
            return moment

    return None


# =====================================================
# MATCH
# =====================================================

def match_loose(t, search):

    if not search:
        return True

    words = search.lower().split()

    text = " ".join([

        str(t.get("name", "")),
        str(t.get("color", "")),
        str(t.get("origin", "")),
        str(t.get("keywords", "")),
        str(t.get("description", "")),
        str(t.get("personal_notes", "")),
        str(t.get("badges", ""))

    ]).lower()

    return any(w in text for w in words)


# =====================================================
# SCORE
# =====================================================

def score_tea(t, search):

    words = search.lower().split()

    score = 0

    def s(val, weight):

        if not val:
            return 0

        return sum(
            weight
            for w in words
            if w in val.lower()
        )

    # classic search

    score += s(t["name"], 5)
    score += s(t["color"], 4)
    score += s(t["origin"], 3)
    score += s(t["keywords"], 3)
    score += s(t["description"], 2)
    score += s(t["personal_notes"], 1)
    score += s(t.get("badges"), 4)

    # ratings

    score += t.get("taste_rating", 0) * 1.5
    score += t.get("smell_rating", 0) * 0.5

    # current moment

    current_moment = get_current_moment()

    if t.get("moment") == current_moment:

        score += 10

    elif t.get("moment") == "Toute la journée":

        score += 5

    return score


# =====================================================
# SMART FILTER
# =====================================================

def smart_filter(teas, search):

    if not search:
        return teas

    def match(t):

        score = 0

        words = expand_search(search)

        full_text = " ".join([

            str(t.get("name", "")),
            str(t.get("color", "")),
            str(t.get("origin", "")),
            str(t.get("keywords", "")),
            str(t.get("description", "")),
            str(t.get("personal_notes", "")),
            str(t.get("badges", ""))

        ]).lower()

        # -----------------------------------------
        # CLASSIC
        # -----------------------------------------

        for w in words:

            if w in str(t.get("name", "")).lower():
                score += 10

            if w in str(t.get("color", "")).lower():
                score += 8

            if w in str(t.get("origin", "")).lower():
                score += 8

            if w in str(t.get("badges", "")).lower():
                score += 7

            if w in str(t.get("keywords", "")).lower():
                score += 6

            if w in str(t.get("description", "")).lower():
                score += 4

            if w in str(t.get("personal_notes", "")).lower():
                score += 2

            # NLP GLOBAL
            if w in full_text:
                score += 3

        # -----------------------------------------
        # RATINGS
        # -----------------------------------------

        score += t.get("taste_rating", 0) * 2
        score += t.get("smell_rating", 0)

        # -----------------------------------------
        # MOMENT
        # -----------------------------------------

        current_moment = get_current_moment()

        if t.get("moment") == current_moment:

            score += 10

        elif t.get("moment") == "Toute la journée":

            score += 4

        # -----------------------------------------
        # NLP : MIN RATING
        # -----------------------------------------

        min_rating = extract_rating(search)

        if min_rating is not None:

            if t.get("taste_rating", 0) >= min_rating:
                score += 25

            else:
                score -= 25

        # -----------------------------------------
        # NLP : ORIGIN
        # -----------------------------------------

        origin = extract_origin(search)

        if origin:

            if origin in str(
                t.get("origin", "")
            ).lower():

                score += 25

        # -----------------------------------------
        # NLP : MOMENT
        # -----------------------------------------

        wanted_moment = extract_moment(search)

        if wanted_moment:

            if wanted_moment.lower() in str(
                t.get("moment", "")
            ).lower():

                score += 20

        return score

    scored = [

        (t, match(t))
        for t in teas
    ]

    # sort first
    scored.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # keep only relevant
    filtered = [

        t
        for t, s in scored
        if s > 0
    ]

    return filtered