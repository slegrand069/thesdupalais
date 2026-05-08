from models import get_teas
import streamlit as st
import random
import textwrap
from datetime import datetime
from tea_card_component import tea_card

def main_screen():

    user_id = st.session_state.user.id

    st.markdown("## 🍵 Mes thés")

    col1, col2 = st.columns([4,1])
    search = col1.text_input("", placeholder="🔍 Rechercher")
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
            teas = sorted(
                teas,
                key=lambda t: score_tea(t, search or ""),
                reverse=True
            )

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
        st.info("Aucun thé")
        return

    # CARDS
    for t in teas:

        bg = get_color(t["color"])

        badges = [b.strip() for b in (t.get("badges") or "").split(",") if b.strip()]

        clicked = tea_card(
            tea={
            "id": t["id"],
            "name": t["name"],
            "color": t["color"],
            "origin": t["origin"],
            "rating": t["taste_rating"],
            "temp": t["temperature"],
            "duration": t["duration"],
            "moment": t["moment"],
            "badges": badges,
            "bg": get_color(t["color"])
            },
        key=f"card_{t['id']}"
        )

        if clicked:
            st.session_state.selected_tea = clicked
            st.session_state.page = "detail"
            st.rerun()          
            
        st.markdown("---")


def get_current_moment():
    hour = datetime.now().hour

    if hour < 12:
        return "Matin"
    elif hour < 18:
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
    score += t.get("taste_rating", 0) * 0.5
    score += t.get("smell_rating", 0) * 0.3

    # ⏰ moment intelligent
    current_moment = get_current_moment()

    if t.get("moment") == current_moment:
        score += 5  # 🔥 gros bonus
    elif t.get("moment") == "Toute la journée":
        score += 2

    return score

def match_loose(t, search):
    text = " ".join(map(str, [t[1],t[2],t[3],t[4],t[11],t[13]])).lower()
    return any(w in text for w in search.lower().split())


def get_color(color):
    return {
        "Vert": "#DFF5E1",
        "Noir": "#DADADA",
        "Blanc": "#FBFBFB",
        "Oolong": "#FFE8D6",
        "Pu'erh": "#E8DED3",
        "Mixte": "#FFE3EC",
        "Infusion": "#E3F0FF"
    }.get(color, "#FFFFFF")