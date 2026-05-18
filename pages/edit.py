import streamlit as st
from models import (
    add_tea, 
    update_tea, 
    get_tea_by_id 
)

from config import (
    get_color_names,
    get_keywords,
    get_badges,
    get_moments,
    get_status,
    get_containers
)

def edit_screen():

    tea_id = st.session_state.get("edit_id")
    user_id = st.session_state.user.id

    tea = get_tea_by_id(tea_id, user_id) if tea_id else {}

    def val(key, default=""):
        return tea.get(key, default) if tea else default

    def to_list(v):
        if not v:
            return []
        return [
            x.strip()
            for x in v.split(",")
            if x.strip()
        ]

    st.markdown(
        f"## {'✏️ Modifier un thé' if tea_id else '🍵 Nouveau thé'}"
    )

    # ---------------------------------------------------
    # FORM
    # ---------------------------------------------------

    with st.form("tea_form"):

        # =================================================
        # 🍵 IDENTITÉ
        # =================================================

        with st.expander("🍵 Identité", expanded=True):
            name = st.text_input(
                "Nom",
                val("name")
            )

            origin = st.text_input(
                "Origine",
                val("origin")
            )

            color_names = get_color_names()

            color = st.selectbox(
                "Couleur",
                color_names,
                index=color_names.index(val("color"))
                if val("color") in color_names
                else 0
            )
                
            selected_badges = st.multiselect(
                "🏅 Badges",
                get_badges(),
                default=to_list(val("badges"))
            )

        # =================================================
        # 👃 PROFIL SENSORIEL
        # =================================================

        with st.expander("👃 Profil sensoriel", expanded=True):

            description = st.text_area(
                "Description",
                val("description"),
                height=120
            )

            aromas = st.text_input(
                "Arômes",
                val("aromas")
            )

            keywords_options = [
                x.strip()
                for x in get_keywords()
            ]
    
            default_keywords = [
                k
                for k in to_list(val("keywords"))
                if k in keywords_options
            ]

            selected_kw = st.multiselect(
                "🏷️ Profil aromatique",
                keywords_options,
                default=default_keywords
            )

        # =================================================
        # ⭐ DÉGUSTATION
        # =================================================

        with st.expander("⭐ Dégustation", expanded=True):
            col1, col2 = st.columns(2)

            with col1:

                smell = st.slider(
                    "👃 Olfactif",
                    0,
                    10,
                    int(val("smell_rating", 5))
                )

                taste = st.slider(
                    "🍵 Gustatif",
                    0,
                    10,
                    int(val("taste_rating", 5))
                )

            with col2:

                temp = st.slider(
                    "🌡 Température",
                    50,
                    100,
                    int(val("temperature", 75)),
                    step=5
                )

                duration = st.slider(
                    "⏳ Durée",
                    0,
                    10,
                    int(val("duration", 3))
                )

            moment = st.selectbox(
                "🌙 Moment idéal",
                get_moments(),
                index=get_moments().index(val("moment"))
                if val("moment") in get_moments()
                else 0
            )

        # =================================================
        # 📦 GESTION
        # =================================================

        with st.expander("📦 Gestion", expanded=True):

            container = st.selectbox(
                "Contenant",
                get_containers(),
                index=get_containers().index(val("container"))
                if val("container") in get_containers()
                else 0
            )

            status = st.selectbox(
                "Statut",
                get_status(),
                index=get_status().index(val("status"))
                if val("status") in get_status()
                else 0
            )

            technical = st.text_area(
                "⚙️ Notes techniques",
                val("technical"),
                height=100
            )

        # =================================================
        # 📝 NOTES PERSO
        # =================================================

        with st.expander("📝 Notes personnelles", expanded=True):
            personal = st.text_area(
            "Notes perso",
            val("personal_notes"),
            height=140
        )

        # =================================================
        # ACTIONS
        # =================================================


        col1, col2, col3 = st.columns([1,2,1])

        with col1:

            submitted = st.form_submit_button(
                "💾 Enregistrer",
                use_container_width=True
            )

        with col3:

            cancel = st.form_submit_button(
                "⬅️ Annuler",
                use_container_width=True
            )

    # ---------------------------------------------------
    # LOGIC
    # ---------------------------------------------------

    if cancel:
        st.session_state.page = "main"
        st.rerun()

    if submitted:

        data = (
            name,
            origin,
            color,
            description,
            aromas,
            smell,
            taste,
            temp,
            duration,
            container,
            ",".join(selected_kw),
            technical,
            personal,
            status,
            ",".join(selected_badges),
            moment
        )

        if tea_id:
            update_tea(
                tea_id,
                data,
                user_id
            )
        else:
            add_tea(
                data,
                user_id
            )

        st.session_state.page = "main"
        st.session_state.edit_id = None

        st.rerun()