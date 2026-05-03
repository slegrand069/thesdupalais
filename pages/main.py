from models import get_teas
import streamlit as st
import random
import textwrap

def main_screen():

    st.markdown("## 🍵 Mes thés")

    col1, col2 = st.columns([3,1])
    search = col1.text_input("🔍 Rechercher")
    mode = col2.radio("", ["🔎", "🧠"], horizontal=True)

    teas = get_teas()

    # 🔎 LOGIQUE
    if search:
        if mode == "🔎":
            teas = [t for t in teas if match_loose(t, search)]
        else:
            teas = sorted(teas, key=lambda t: score_tea(t, search), reverse=True)

    # ACTIONS
    col1, col2 = st.columns(2)

    if col1.button("➕ Ajouter"):
        st.session_state.edit_id = None
        st.session_state.page = "edit"
        st.rerun()

    if col2.button("🎲 Surprise"):
        if teas:
            t = random.choice(teas)
            st.session_state.selected_tea = t["id"]
            st.session_state.page = "detail"
            st.rerun()

    if not teas:
        st.info("Aucun thé")
        return

    # CARDS
    for t in teas:

        bg = get_color(t["color"])

        badges = (t.get("badges") or "").split(",")
        badge_html = "".join([f'<span class="badge">{b}</span>' for b in badges if b])

        html = textwrap.dedent(f"""
<div class="card" style="background-color:{bg}">
<b>🍵 {t["name"]}</b><br>
<small>{t["color"]} • {t["origin"]}</small>
<div style="margin-top:6px;">{badge_html}</div>
<div style="display:flex; gap:8px; margin-top:8px; font-size:12px;">
<span>⭐ {t["taste_rating"]}</span>
<span>🌡 {t["temperature"]}°C</span>
<span>⏳ {t["duration"]} min</span>
</div>
</div>
""")

        st.markdown(html, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        if col1.button("Voir", key=f"v{t['id']}"):
            st.session_state.selected_tea = t["id"]
            st.session_state.page = "detail"
            st.rerun()

        if col2.button("✏️", key=f"e{t['id']}"):
            st.session_state.edit_id = t["id"]
            st.session_state.page = "edit"
            st.rerun()

        st.markdown("---")

# 🔥 SCORE
def score_tea(t, search):
    words = search.lower().split()

    def s(val, w):
        return sum(w for word in words if val and word in val.lower())

    return (
        s(t[1],5)+s(t[3],4)+s(t[2],3)+
        s(t[11],3)+s(t[4],2)+s(t[13],1)+s(t[15],4)
    )


def match_loose(t, search):
    text = " ".join(map(str, [t[1],t[2],t[3],t[4],t[11],t[13]])).lower()
    return any(w in text for w in search.lower().split())


def get_color(color):
    return {
        "Vert": "#E8F5E9",
        "Noir": "#F5F5F5",
        "Blanc": "#FAFAFA",
        "Oolong": "#FFF3E0",
        "Pu'erh": "#EFEBE9",
        "Mixte": "#FCE4EC",
        "Infusion": "#E3F2FD"
    }.get(color, "#FFFFFF")