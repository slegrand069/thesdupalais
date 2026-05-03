import streamlit as st
from models import add_tea, update_tea, get_tea_by_id

def edit_screen(conn=None, c=None):

    st.markdown("## ✏️ Édition")

    tea_id = st.session_state.get("edit_id")
    tea = get_tea_by_id(tea_id) if tea_id else None

    def val(key, default=""):
        return tea.get(key, default) if tea else default

    def to_list(v):
        return v.split(",") if v else []

    with st.form("form"):

        st.subheader("Infos")

        name = st.text_input("Nom", val("name"))
        origin = st.text_input("Origine", val("origin"))
        
        color = st.selectbox(
            "Couleur",
            ["Noir","Vert","Blanc","Oolong","Pu'erh","Mixte"]
        )

        st.subheader("🏅 Identité")

        BADGES = ["Grand Cru","Thé d'exception","Import"]
        selected_badges = []

        cols = st.columns(3)
        for i, b in enumerate(BADGES):
            with cols[i]:
                if st.checkbox(b, value=(b in to_list(val(15)))):
                    selected_badges.append(b)

        st.subheader("Profil")

        description = st.text_area("Description", val(4))
        aromas = st.text_input("Arômes", val(5))

        col1, col2 = st.columns(2)

        smell = col1.slider("Olfactif",0,10,int(val(6,5)))
        taste = col1.slider("Gustatif",0,10,int(val(7,5)))

        temp = col2.slider("Température",50,100,int(val(8,70)),step=5)
        duration = col2.slider("Durée",0,15,int(val(9,3)))

        container = st.selectbox(
            "Contenant",
            ["Boite","Sachet","Galette","Échantillon","Épuisé"]
        )

        st.subheader("🏷️ Profil aromatique")

        KEYWORDS = [
            "Floral","Fruité","Boisé","Épicé","Terreux",
            "Herbacé","Mielleux","Céréales","Doux",
            "Amer","Fumé","Végétal","Minéral","Sucré",
            "Léger","Corsé","Frais"
        ]

        selected_kw = []
        cols = st.columns(3)

        for i, kw in enumerate(KEYWORDS):
            with cols[i % 3]:
                if st.checkbox(kw, value=(kw in to_list(val(11)))):
                    selected_kw.append(kw)

        technical = st.text_area("Technique", val(12))
        personal = st.text_area("Notes perso", val(13))

        status = st.selectbox(
            "Statut",
            ["Disponible","Épuisé","En test","Favori"]
        )

        submitted = st.form_submit_button("💾 Enregistrer")

    if submitted:

        data = (
            name, origin, color, description, aromas,
            smell, taste, temp, duration, container,
            ",".join(selected_kw),
            technical, personal, status,
            ",".join(selected_badges)
        )

        if tea_id:
            update_tea(tea_id, data)
        else:
            add_tea(data)

        st.session_state.page = "main"
        st.session_state.edit_id = None
        st.rerun()