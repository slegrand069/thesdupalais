import streamlit as st
from models import add_tea, get_config_dict, update_tea, get_tea_by_id, get_config_values


def edit_screen():

    tea_id = st.session_state.get("edit_id")
    user_id = st.session_state.user.id

    tea = get_tea_by_id(tea_id, user_id) if tea_id else {}

    def val(key, default=""):
        return tea.get(key, default) if tea else default

    def to_list(v):
        return [x.strip() for x in v.split(",")] if v else []

    st.markdown(
        f"## {'✏️ Modifier un thé' if tea_id else '🍵 Nouveau thé'}"
    )

    # ---------------------------------------------------
    # DATA
    # ---------------------------------------------------

    COLORS = get_config_dict("color");

    BADGES = [
        x["value"]
        for x in get_config_values("badge")
    ]

    KEYWORDS = [
        x["value"]  
        for x in get_config_values("profilAromatique")
    ]

    MOMENTS = [
        x["value"]
        for x in get_config_values("moment")
    ]

    STATUS = [ 
        x["value"]
        for x in get_config_values("status")
    ]

    CONTAINERS = [
        x["value"]
        for x in get_config_values("contenant")
    ]

    # ---------------------------------------------------
    # FORM
    # ---------------------------------------------------

    with st.form("tea_form"):

        # =================================================
        # 🍵 IDENTITÉ
        # =================================================

        st.markdown(
            '<div class="form-card">',
            unsafe_allow_html=True
        )

        st.markdown("### 🍵 Identité")

        name = st.text_input(
            "Nom",
            val("name")
        )

        origin = st.text_input(
            "Origine",
            val("origin")
        )

        color_names = list(COLORS.keys())

        color = st.selectbox(
            "Couleur",
            color_names,
            index=color_names.index(val("color"))
            if val("color") in color_names
            else 0
        )
            
        selected_badges = st.multiselect(
            "🏅 Badges",
            BADGES,
            default=to_list(val("badges"))
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # =================================================
        # 👃 PROFIL SENSORIEL
        # =================================================

        st.markdown(
            '<div class="form-card">',
            unsafe_allow_html=True
        )

        st.markdown("### 👃 Profil sensoriel")

        description = st.text_area(
            "Description",
            val("description"),
            height=120
        )

        aromas = st.text_input(
            "Arômes",
            val("aromas")
        )

        selected_kw = st.multiselect(
            "🏷️ Profil aromatique",
            KEYWORDS,
            default=to_list(val("keywords"))
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # =================================================
        # ⭐ DÉGUSTATION
        # =================================================

        st.markdown(
            '<div class="form-card">',
            unsafe_allow_html=True
        )

        st.markdown("### ⭐ Dégustation")

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
            MOMENTS,
            index=MOMENTS.index(val("moment"))
            if val("moment") in MOMENTS
            else 0
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # =================================================
        # 📦 GESTION
        # =================================================

        st.markdown(
            '<div class="form-card">',
            unsafe_allow_html=True
        )

        st.markdown("### 📦 Gestion")

        container = st.selectbox(
            "Contenant",
            CONTAINERS,
            index=CONTAINERS.index(val("container"))
            if val("container") in CONTAINERS
            else 0
        )

        status = st.selectbox(
            "Statut",
            STATUS,
            index=STATUS.index(val("status"))
            if val("status") in STATUS
            else 0
        )

        technical = st.text_area(
            "⚙️ Notes techniques",
            val("technical"),
            height=100
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # =================================================
        # 📝 NOTES PERSO
        # =================================================

        st.markdown(
            '<div class="form-card">',
            unsafe_allow_html=True
        )

        st.markdown("### 📝 Notes personnelles")

        personal = st.text_area(
            "Notes perso",
            val("personal_notes"),
            height=140
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # =================================================
        # ACTIONS
        # =================================================

        st.markdown(
            '<div class="action-bar">',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        submitted = col1.form_submit_button(
            "💾 Enregistrer",
            use_container_width=True
        )

        cancel = col2.form_submit_button(
            "⬅️ Annuler",
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

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