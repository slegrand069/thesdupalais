import streamlit as st
from models import add_tea, update_tea, get_tea_by_id

def edit_screen():

    st.markdown("## ✏️ Édition")

    tea_id = st.session_state.get("edit_id")
    user_id = st.session_state.user.id

    tea = get_tea_by_id(tea_id, user_id) if tea_id else {}

    def val(key, default=""):
        return tea.get(key, default) if tea else default

    def to_list(v):
        return v.split(",") if v else []

    with st.form("form"):

        # ---------------- INFOS ----------------
        st.subheader("Infos")

        name = st.text_input("Nom", val("name"))
        origin = st.text_input("Origine", val("origin"))

        colors = ["Noir","Vert","Blanc","Oolong","Pu'erh","Mixte"]
        color = st.selectbox(
            "Couleur",
            colors,
            index=colors.index(val("color")) if val("color") in colors else 0
        )

        # ---------------- BADGES ----------------
        st.subheader("🏅 Identité")

        BADGES = ["Grand Cru","Thé d'exception","Import"]
        selected_badges = []

        cols = st.columns(3)
        existing_badges = to_list(val("badges"))

        for i, b in enumerate(BADGES):
            with cols[i % 3]:
                if st.checkbox(b, value=(b in existing_badges)):
                    selected_badges.append(b)

        # ---------------- DESCRIPTION ----------------
        st.subheader("Profil")

        description = st.text_area("Description", val("description"))
        aromas = st.text_input("Arômes", val("aromas"))

        col1, col2 = st.columns(2)

        smell = col1.slider("Olfactif", 0, 10, int(val("smell_rating", 5)))
        taste = col1.slider("Gustatif", 0, 10, int(val("taste_rating", 5)))

        temp = col2.slider("Température", 50, 100, int(val("temperature", 70)), step=5)
        duration = col2.slider("Durée", 0, 10, int(val("duration", 3)))
 
        container = st.selectbox(
            "Contenant",
            ["Boite","Sachet","Galette","Échantillon","Épuisé"],
            index=0
        )

        # ---------------- MOMENT ----------------
        moment_options = ["Matin", "Après-midi", "Soir", "Toute la journée"]

        moment = st.selectbox(
            "Moment idéal",
            moment_options,
            index=moment_options.index(val("moment")) if val("moment") in moment_options else 0
        )

        # ---------------- KEYWORDS ----------------
        st.subheader("🏷️ Profil aromatique")

        KEYWORDS = [
            "Floral","Fruité","Boisé","Épicé","Terreux",
            "Herbacé","Mielleux","Céréales","Doux",
            "Amer","Fumé","Végétal","Minéral","Sucré",
            "Léger","Corsé","Frais"
        ]

        selected_kw = []
        existing_kw = to_list(val("keywords"))

        cols = st.columns(2)  # 🔥 mobile fix

        for i, kw in enumerate(KEYWORDS):
            with cols[i % 2]:
                if st.checkbox(kw, value=(kw in existing_kw)):
                    selected_kw.append(kw)

        # ---------------- NOTES ----------------
        technical = st.text_area("Technique", val("technical"))
        personal = st.text_area("Notes perso", val("personal_notes"))

        status_options = ["Disponible","Épuisé","En test","Favori"]

        status = st.selectbox(
            "Statut",
            status_options,
            index=status_options.index(val("status")) if val("status") in status_options else 0
        )

        # ---------------- ACTIONS ----------------
        col1, col2 = st.columns(2)

        submitted = col1.form_submit_button("💾 Enregistrer")
        cancel = col2.form_submit_button("⬅️ Annuler")

    # ---------------- LOGIC ----------------

    if cancel:
        st.session_state.page = "main"
        st.rerun()

    if submitted:

        data = (
            name, origin, color, description, aromas,
            smell, taste, temp, duration, container,
            ",".join(selected_kw),
            technical, personal, status,
            ",".join(selected_badges),
            moment  # 🔥 NEW
        )

        if tea_id:
            update_tea(tea_id, data, user_id)
        else:
            add_tea(data, user_id)

        st.session_state.page = "main"
        st.session_state.edit_id = None
        st.rerun()