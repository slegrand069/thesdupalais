import streamlit as st

from models import (
    get_tea_by_id,
    delete_tea
)

from config import (
    get_color_hex
)


def detail_screen():

    tea_id = st.session_state.get("selected_tea")

    user_id = st.session_state.user.id

    tea = get_tea_by_id(
        tea_id,
        user_id
    )

    if not tea:

        st.error("Thé introuvable")

        return

    # =================================================
    # DATA
    # =================================================

    bg = get_color_hex(
        tea.get("color")
    )

    badges = [

        b.strip()

        for b in (
            tea.get("badges") or ""
        ).split(",")

        if b.strip()
    ]

    keywords = [

        k.strip()

        for k in (
            tea.get("keywords") or ""
        ).split(",")

        if k.strip()
    ]

    # =================================================
    # HERO
    # =================================================

    st.markdown(f"""
<div class="detail-hero" style="background:{bg};">
<div class="detail-title">
🍵 {tea.get("name", "")}</div>
<div class="detail-subtitle">
{tea.get("color", "")}•{tea.get("origin", "")}</div>
</div>
    """, unsafe_allow_html=True)

    # =================================================
    # BADGES
    # =================================================

    if badges:

        badges_html = "".join([

            f'<span class="badge">{b}</span>'

            for b in badges
        ])

        st.markdown(
            badges_html,
            unsafe_allow_html=True
        )

    # =================================================
    # DÉGUSTATION
    # =================================================

    with st.expander(
        "⭐ Dégustation",
        expanded=True
    ):

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "👃 Olfactif",
                tea.get("smell_rating", 0)
            )

            st.metric(
                "🍵 Gustatif",
                tea.get("taste_rating", 0)
            )

        with col2:

            st.metric(
                "🌡 Température",
                f"{tea.get('temperature', 0)}°C"
            )

            st.metric(
                "⏳ Durée",
                f"{tea.get('duration', 0)} min"
            )

        st.write(
            f"🌙 Moment idéal : "
            f"{tea.get('moment', '-')}"
        )

    # =================================================
    # PROFIL
    # =================================================

    with st.expander("👃 Profil sensoriel"):

        st.write(
            tea.get("description", "-")
        )

        st.write(
            f"**Arômes :** "
            f"{tea.get('aromas', '-')}"
        )

        if keywords:

            st.write("### 🏷️ Profil aromatique")

            kw_html = "".join([

                f'<span class="badge">{k}</span>'

                for k in keywords
            ])

            st.markdown(
                kw_html,
                unsafe_allow_html=True
            )

    # =================================================
    # NOTES
    # =================================================

    with st.expander("📝 Notes"):

        st.write(
            f"**Technique :**\n\n"
            f"{tea.get('technical', '-')}"
        )

        st.write(
            f"**Personnel :**\n\n"
            f"{tea.get('personal_notes', '-')}"
        )

    # =================================================
    # GESTION
    # =================================================

    with st.expander("📦 Gestion"):

        st.write(
            f"**Contenant :** "
            f"{tea.get('container', '-')}"
        )

        st.write(
            f"**Statut :** "
            f"{tea.get('status', '-')}"
        )

    # =================================================
    # ACTIONS
    # =================================================

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col1:

        if st.button(
            "✏️ Modifier",
            use_container_width=True
        ):

            st.session_state.edit_id = tea_id
            st.session_state.page = "edit"

            st.rerun()

    with col2:

        if st.button(
            "🗑️ Supprimer",
            use_container_width=True
        ):

            st.session_state.confirm_delete = True

    with col3:

        if st.button(
            "⬅️ Retour",
            use_container_width=True
        ):

            st.session_state.page = "main"

            st.rerun()

    if st.session_state.get("confirm_delete"):

        st.warning(
            f"⚠️ Supprimer définitivement "
            f"'{tea.get('name')}' ?"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "✅ Oui supprimer",
                use_container_width=True
            ):

                delete_tea(
                    tea_id,
                    user_id
                )

                st.session_state.confirm_delete = False

                st.session_state.page = "main"

                st.rerun()

        with col2:

            if st.button(
                "❌ Annuler",
                use_container_width=True
            ):

                st.session_state.confirm_delete = False

                st.rerun()