import re

from datetime import datetime

from config import (
    get_fuzzy_matchings,
    get_synonyms, 
    get_nationalities, 
    get_moment_intents,
    get_concepts
)
from util import normalize_text

SEARCH_WEIGHTS = {

    "name": 12,
    "color": 8,
    "origin": 8,
    "badge": 7,
    "keyword": 6,
    "description": 4,
    "notes": 2,

    "global": 1,

    "taste_rating": 1,
    "smell_rating": 0.5,

    "moment_match": 10,
    "all_day": 4, 

    "origin_bonus": 25,
    "moment_bonus": 20,
    "rating_bonus": 25,
}

# =====================================================
# MOMENT
# =====================================================

def get_current_moment():

    hour = datetime.now().hour

    if hour < 2:
        return "Soir"

    elif hour < 13:
        return "Matin"

    elif hour < 18:
        return "Après-midi"

    return "Soir"


# =====================================================
# NLP HELPERS
# =====================================================

def expand_search(search):

    words = normalize_text(search).split()

    words = apply_fuzzy(words)

    words = apply_synonyms(words)

    words = apply_concepts(words)

    # remove duplicates
    words = list(
        dict.fromkeys(words)
    )

    return words

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

    search = normalize_text(search)

    nationalities = get_nationalities()
    for nat, country in nationalities.items():
        nat = normalize_text(nat)
        if nat in search:
            return normalize_text(country)

    return None


def extract_moment(search):

    search = normalize_text(search)

    moment_intents = get_moment_intents()
    for word, moment in moment_intents.items():
        word = normalize_text(word)
        if word in search:
            return normalize_text(moment)

    return None


# =====================================================
# MATCH
# =====================================================

def match_loose(t, search):

    if not search:
        return True

    words = normalize_text(search).split()

    text = build_search_text(t)
    return any(w in text for w in words)


# =====================================================
# SCORE
# =====================================================

def score_tea(t, search):

    words = normalize_text(search).split()

    score = 0

    def s(val, weight):

        if not val:
            return 0

        return sum(
            weight
            for w in words
                if w in normalize_text(val)
            )

    # classic search

    score += s(t["name"], SEARCH_WEIGHTS["name"])
    score += s(t["color"], SEARCH_WEIGHTS["color"])
    score += s(t["origin"], SEARCH_WEIGHTS["origin"])
    score += s(t["keywords"], SEARCH_WEIGHTS["keyword"])
    score += s(t["description"], SEARCH_WEIGHTS["description"])
    score += s(t["personal_notes"], SEARCH_WEIGHTS["notes"])
    score += s(t.get("badges"), SEARCH_WEIGHTS["badge"])

    # ratings

    score += t.get("taste_rating", 0) * SEARCH_WEIGHTS["taste_rating"]
    score += t.get("smell_rating", 0) * SEARCH_WEIGHTS["smell_rating"]

    # current moment

    current_moment = get_current_moment()

    if t.get("moment") == current_moment:

        score += SEARCH_WEIGHTS["moment_match"]

    elif t.get("moment") == "Toute la journée":

        score += SEARCH_WEIGHTS["all_day"]

    return score


# =====================================================
# SMART FILTER
# =====================================================

def smart_filter(teas, search):

    if not search:
        return teas
    search = normalize_text(search)
    
    min_rating = extract_rating(search)
    origin = extract_origin(search)
    wanted_moment = extract_moment(search)
    words = expand_search(search)
    
    def match(t):

        score = 0

        full_text = build_search_text(t)

        # -----------------------------------------
        # CLASSIC
        # -----------------------------------------

        for w in words:

            if w in normalize_text(str(t.get("name", ""))):
                score += SEARCH_WEIGHTS["name"]

            if w in normalize_text(str(t.get("color", ""))):
                score += SEARCH_WEIGHTS["color"]

            if w in normalize_text(str(t.get("origin", ""))):
                score += SEARCH_WEIGHTS["origin"]

            if w in normalize_text(str(t.get("badges", ""))):
                score += SEARCH_WEIGHTS["badge"]

            if w in normalize_text(str(t.get("keywords", ""))):
                score += SEARCH_WEIGHTS["keyword"]

            if w in normalize_text(str(t.get("description", ""))):
                score += SEARCH_WEIGHTS["description"]

            if w in normalize_text(str(t.get("personal_notes", ""))):
                score += SEARCH_WEIGHTS["notes"]

            # NLP GLOBAL
            if w in full_text:
                score += SEARCH_WEIGHTS["global"]

        # -----------------------------------------
        # RATINGS
        # -----------------------------------------

        score += t.get("taste_rating", 0) * SEARCH_WEIGHTS["taste_rating"]
        score += t.get("smell_rating", 0) * SEARCH_WEIGHTS["smell_rating"]

        # -----------------------------------------
        # MOMENT
        # -----------------------------------------

        current_moment = get_current_moment()

        if t.get("moment") == current_moment:

            score += SEARCH_WEIGHTS["moment_match"]

        elif t.get("moment") == "Toute la journée":

            score += SEARCH_WEIGHTS["all_day"]

        # -----------------------------------------
        # NLP : MIN RATING
        # -----------------------------------------

        if min_rating is not None:

            if t.get("taste_rating", 0) >= min_rating:
                score += SEARCH_WEIGHTS["rating_bonus"]

            else:
                score -= SEARCH_WEIGHTS["rating_bonus"]

        # -----------------------------------------
        # NLP : ORIGIN
        # -----------------------------------------

        if origin:

            if origin in normalize_text(str(
                t.get("origin", ""))
            ):

                score += SEARCH_WEIGHTS["origin_bonus"]

        # -----------------------------------------
        # NLP : MOMENT
        # -----------------------------------------

        if wanted_moment:

            if wanted_moment.lower() in normalize_text(str(
                t.get("moment", "")
            )):

                score += SEARCH_WEIGHTS["moment_bonus"] 

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
        if s > 5
    ]

    return filtered

def apply_fuzzy(words):

    fuzzy = get_fuzzy_matchings()

    result = []
    words = normalize_text(" ".join(words)).split()

    for w in words:

        result.append(w)

        if w in fuzzy:

            result.append(fuzzy[w])

    return result

def apply_synonyms(words):

    synonyms = get_synonyms()

    result = []
    words = normalize_text(" ".join(words)).split()
    
    for w in words:

        result.append(w)

        if w in synonyms:

            result.extend(
                synonyms[w]
            )

    return result

def apply_concepts(words):

    concepts = get_concepts()

    result = []
    words = normalize_text(" ".join(words)).split()

    for w in words:

        result.append(w)

        if w in concepts:

            result.extend(
                concepts[w]
            )

    return result

def build_search_text(t):

    return normalize_text(

        " ".join([

        str(t.get("name", "")),
        str(t.get("color", "")),
        str(t.get("origin", "")),
        str(t.get("keywords", "")),
        str(t.get("description", "")),
        str(t.get("personal_notes", "")),
        str(t.get("badges", "")),
        str(t.get("aromas", "")),
        str(t.get("technical", "")),
        str(t.get("moment", "")),
        str(t.get("status", ""))

        ])
    )