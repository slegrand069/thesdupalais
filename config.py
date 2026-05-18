from models import (
    get_config_dict,
    get_config_values
)
from util import normalize_text, safe_split


# =====================================================
# GENERIC
# =====================================================

def get_values(config_type):

    return [
        x["value"]
        for x in get_config_values(config_type)
    ]


def get_dict(config_type):

    return get_config_dict(config_type)


# =====================================================
# COLORS
# =====================================================

def get_colors():

    return get_dict("color")


def get_color_names():

    return list(
        get_colors().keys()
    )


def get_color_hex(color):

    return get_colors().get(
        color,
        {}
    ).get(
        "extra",
        "#FFFFFF"
    )


# =====================================================
# KEYWORDS
# =====================================================

def get_keywords():

    return get_values("profilAromatique")


# =====================================================
# BADGES
# =====================================================

def get_badges():

    return get_values("badge")


# =====================================================
# MOMENTS
# =====================================================

def get_moments():

    return get_values("moment")


# =====================================================
# STATUS
# =====================================================

def get_status():

    return get_values("status")


# =====================================================
# CONTAINERS
# =====================================================

def get_containers():

    return get_values("contenant")

# =====================================================
# Nationalités
# =====================================================

def get_nationalities():

    rows = get_config_values("nationality")

    result = {}

    for r in rows:

        value = normalize_text(r["value"])

        extra = normalize_text(
            r.get("extra", "")
        )

        result[value] = safe_split(extra)

    return result

# =====================================================
# MOMENT INTENTS
# =====================================================

def get_moment_intents():

    rows = get_config_values("momentIntents")

    result = {}

    for r in rows:

        value = r["value"].lower()

        extra = r.get("extra", "")

        words = safe_split(extra)

        result[value] = words

    return result

# =====================================================
# SYNONYMS
# =====================================================

def get_synonyms():

    rows = get_config_values("synonyms")

    result = {}

    for r in rows:

        value = r["value"].lower()

        extra = r.get("extra", "")

        words = safe_split(extra)

        result[value] = words

    return result

# =====================================================
# CONCEPTS
# =====================================================

def get_concepts():

    rows = get_config_values("concept")

    result = {}

    for r in rows:

        value = r["value"].lower()

        extra = r.get("extra", "")

        result[value] = safe_split(extra)

    return result

# =====================================================
# FUZZY MATCHING
# =====================================================

def get_fuzzy_matchings():

    rows = get_config_values("fuzzyMatching")

    result = {}

    for r in rows:

        value = r["value"].lower()

        extra = r.get("extra", "")

        words = safe_split(extra)

        result[value] = words

    return result

