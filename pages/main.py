from models import (
    get_teas,
    get_config_dict
)

from nlp import (
    score_tea,
    smart_filter,
    match_loose
)

import streamlit as st
import random

from tea_card_component import tea_card


def main_screen():

    user_id = st.session_state.user.id

    COLORS = get_config_dict("color")

    st.markdown("## 🍵 Mes thés")

    # =================================================
    # SEARCH
    # =================================================

    col1, col2 = st.columns([4,1])

    search = col1.text_input(
        "",
        placeholder="🔍 Rechercher"
    )

    if search.strip().lower() == "/admin":

        st.session_state.page = "admin"

        st.rerun()

    mode = col2.radio(
        "",
        ["🔎", "🧠"],
        horizontal=True
    )

    # =================================================
    # LOAD
    # =================================================

    teas = get_teas(user_id)

    # =================================================
    # SEARCH LOGIC
    # =================================================

    if search:

        if mode == "🔎":

            teas = [
                t
                for t in teas
                if match_loose(t, search)
            ]

        else:

            teas = smart_filter(
                teas,
                search
            )

    else:

        teas = sorted(
            teas,
            key=lambda t: score_tea(t, ""),
            reverse=True
        )

    # =================================================
    # ACTIONS
    # =================================================

    col1, col2 = st.columns(
        [1,1],
        gap="small"
    )

    if col1.button("➕ Ajouter"):

        st.session_state.edit_id = None
        st.session_state.page = "edit"

        st.rerun()

    if col2.button("🎲 Surprise"):

        if teas:

            top = teas[:5]

            t = random.choice(top)

            st.session_state.selected_tea = t["id"]
            st.session_state.page = "detail"

            st.rerun()

    # =================================================
    # NO RESULT
    # =================================================

    if not teas:

        st.info(
            f"Aucun thé trouvé pour : '{search}'"
        )

        return

    st.info(f"{len(teas)} thé(s) trouvés")

    safe_search = (
        search or ""
    ).replace(
        " ",
        "_"
    )

    # =================================================
    # CARDS
    # =================================================

    for t in teas:

        bg = COLORS.get(
            t["color"],
            {}
        ).get(
            "extra",
            "#FFFFFF"
        )

        badges = [

            b.strip()

            for b in (
                t.get("badges") or ""
            ).split(",")

            if b.strip()
        ]

        clicked = tea_card(

            tea={

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