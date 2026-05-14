from modulefinder import test

from models import get_teas
import streamlit as st
import random
import re
from datetime import datetime
from tea_card_component import tea_card

def main_screen():

    user_id = st.session_state.user.id

    st.markdown("## 🍵 Mes thés")

    col1, col2 = st.columns([4,1])
    search = col1.text_input("", placeholder="🔍 Rechercher")
    if search.strip().lower() == "/admin":

        st.session_state.page = "admin"
        st.rerun()

    mode = col2.radio("", ["🔎", "🧠"], horizontal=True)

    teas = get_teas(user_id)

    if mode == "🧠":
        teas = sorted(
            teas,
            key=lambda t: score_tea(t, search or ""),
            reverse=True
        )

    # 🔎 LOGIQUE
    if search:
        if mode == "🔎":
            teas = [t for t in teas if match_loose(t, search)]
        else:
            expanded_search = expand_nlp_query(search)
            teas = smart_filter(teas, expanded_search)    

    # ACTIONS
    col1, col2 = st.columns([1,1], gap="small")

    if col1.button("➕ Ajouter"):
        st.session_state.edit_id = None
        st.session_state.page = "edit"
        st.rerun()

    if col2.button("🎲 Surprise"):
        if teas:
            scored = [(t, score_tea(t, "")) for t in teas]

            # tri
            scored.sort(key=lambda x: x[1], reverse=True)

            # top 5 pondéré
            top = [t for t, s in scored[:5]]

            t = random.choice(top)            
            st.session_state.selected_tea = t["id"]
            st.session_state.page = "detail"
            st.rerun()

    if not teas:
        st.info("Aucun thé trouvé. Essayez d'élargir votre recherche ou de changer de mode.")
        return
    else:        
        st.info(f"{len(teas)} thé(s) trouvés");

    safe_search = (search or "").replace(" ", "_")
    
    # CARDS
    for t in teas:

        bg = get_color(t["color"])

        badges = [b.strip() for b in (t.get("badges") or "").split(",") if b.strip()]
        
        clicked = tea_card(
                tea = {
                    "id": int(t["id"]),
                    "name": str(t["name"]),
                    "color": t["color"],
                    "origin": t["origin"],
                    "rating": t["taste_rating"],
                    "temp": t["temperature"],
                    "duration": t["duration"],
                    "moment": t["moment"],
                    "badges": badges,
                    "bg": bg
                },
            
            key=f"card_{t['id']}_{safe_search}_{mode}",
            height=None
        )
        
        if clicked:
           st.session_state.selected_tea = clicked
           st.session_state.page = "detail"
           st.rerun()          


def get_current_moment():
    hour = datetime.now().hour

    if hour < 14:
        return "Matin"
    elif hour < 19:
        return "Après-midi"
    else:
        return "Soir"
    
# 🔥 SCORE
def score_tea(t, search):

    words = search.lower().split()
    score = 0

    def s(val, weight):
        if not val:
            return 0
        return sum(weight for w in words if w in val.lower())

    # 🔎 recherche texte
    score += s(t["name"], 5)
    score += s(t["color"], 4)
    score += s(t["origin"], 3)
    score += s(t["keywords"], 3)
    score += s(t["description"], 2)
    score += s(t["personal_notes"], 1)
    score += s(t.get("badges"), 4)

    # ⭐ qualité
    score += t.get("taste_rating", 0) * 1.5
    score += t.get("smell_rating", 0) * 0.5

    # ⏰ moment intelligent
    current_moment = get_current_moment()

    if t.get("moment") == current_moment:
        score += 10  # 🔥 gros bonus
    elif t.get("moment") == "Toute la journée":
        score += 5

    return score

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

def smart_filter(teas, search):
    if not search:
        return teas

    words = search.lower().split()

    def match(t):

        score = 0

        # 🔤 mots de la recherche
        words = search.lower().split()

        # 📄 texte global
        full_text = " ".join([
            str(t.get("name", "")),
            str(t.get("color", "")),
            str(t.get("origin", "")),
            str(t.get("keywords", "")),
            str(t.get("description", "")),
            str(t.get("personal_notes", "")),
            str(t.get("badges", ""))
        ]).lower()

        # ---------------------------------------------------
        # 🔎 MATCH CLASSIQUE
        # ---------------------------------------------------

        for w in words:

            # nom
            if w in str(t.get("name", "")).lower():
                score += 10

            # couleur
            if w in str(t.get("color", "")).lower():
                score += 8

            # origine
            if w in str(t.get("origin", "")).lower():
                score += 8

            # badges
            if w in str(t.get("badges", "")).lower():
                score += 7

            # keywords
            if w in str(t.get("keywords", "")).lower():
                score += 6

            # description
            if w in str(t.get("description", "")).lower():
                score += 4

            # notes perso
            if w in str(t.get("personal_notes", "")).lower():
                score += 2

        # ---------------------------------------------------
        # ⭐ SCORE QUALITÉ
        # ---------------------------------------------------

        score += t.get("taste_rating", 0) * 2
        score += t.get("smell_rating", 0)

        # ---------------------------------------------------
        # 🌙 MOMENT ACTUEL
        # ---------------------------------------------------

        current_moment = get_current_moment()

        if t.get("moment") == current_moment:
            score += 10

        elif t.get("moment") == "Toute la journée":
            score += 4

        # ---------------------------------------------------
        # ⭐ NLP : NOTE MINIMUM
        # ---------------------------------------------------

        min_rating = extract_rating(search)

        if min_rating is not None:

            if t.get("taste_rating", 0) >= min_rating:
                score += 25
            else:
                score -= 25

        # ---------------------------------------------------
        # 🌍 NLP : ORIGINE / NATIONALITÉ
        # ---------------------------------------------------

        origin = extract_origin(search)

        if origin:

            if origin in str(t.get("origin", "")).lower():
                score += 25

        # ---------------------------------------------------
        # 🌙 NLP : MOMENT IMPLICITE
        # ---------------------------------------------------

        wanted_moment = extract_moment(search)

        if wanted_moment:

            if wanted_moment.lower() in str(t.get("moment", "")).lower():
                score += 20

        # ---------------------------------------------------
        # 🧠 NLP : CONCEPTS
        # ---------------------------------------------------

        expanded_search = expand_nlp_query(search)

        for w in expanded_search.split():

            if w in full_text:
                score += 5

        return score
    scored = [(t, match(t)) for t in teas]

    # 🔥 filtre : garder seulement pertinents
    filtered = [t for t, s in scored if s > 0]

    # tri
    filtered.sort(key=lambda t: match(t), reverse=True)

    return filtered

def get_color(color):
    return {
        "Vert": "#DFF5E1",
        "Noir": "#DADADA",
        "Blanc": "#FBFBFB",
        "Oolong": "#FFE8D6",
        "Pu'erh": "#E8DED3",
        "Pu'Erh": "#E8DED3",
        "Mixte": "#FFE3EC",
        "Infusion": "#E3F0FF"
    }.get(color, "#FFFFFF")

NLP_CONCEPTS = {

    # 🌙 relaxation
    "relaxant": [
        "soir",
        "doux",
        "infusion",
        "blanc",
        "fruité"
    ],

    # ⚡ énergie
    "énergisant": [
        "matin",
        "fort",
        "corsé",
        "noir", 
        "puissant", 
        "épicé"
    ],

    # 🍰 gourmand
    "gourmand": [
        "fruité",
        "doux",
        "sucré",
        "miel", 
        "doux"
    ],

    # 🍋 frais
    "rafraichissant": [
        "doux",
        "citron",
        "vert", 
        "fruité",
        "blanc",
        "jasmin",
        "fleurs",
        "agrumes"
    ],

    # 🫖 raffiné
    "raffiné": [
        "grand cru",
        "blanc",
        "chine",
        "Pu'erh",
        "Exception",
        "rare",
        "subtil"
    ]
}

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

def expand_nlp_query(search):

    search = search.lower()

    expanded = [search]

    for concept, related in NLP_CONCEPTS.items():

        if concept in search:

            expanded.extend(related)

    return " ".join(expanded)

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
    "apres-midi": "après-midi",
    "coup de pompe": "après-midi",
    "coucher": "soir",
    "digestif": "après-midi",
    "digérer": "après-midi"
}

def extract_moment(search):

    search = search.lower()

    for word, moment in MOMENT_INTENTS.items():

        if word in search:
            return moment

    return None