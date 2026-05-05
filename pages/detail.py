from models import get_tea_by_id
from models import delete_tea
import streamlit as st

def detail_screen():

    user_id = st.session_state.user.id

    tea_id = st.session_state.get("selected_tea")
    tea = get_tea_by_id(tea_id, user_id) if tea_id else None

    if not tea:
        st.error("Thé introuvable")
        return

    st.markdown(f"## 🍵 {tea['name']}")
    st.markdown(f"{tea['color']} • {tea['origin']}")

    badges = (tea.get("badges") or "").split(",")
    for b in badges:
        if b:
            st.markdown(f"🏅 {b}")

    st.markdown("---")

    st.markdown("### ⭐ Notes")
    st.markdown(f"Olfactif : {'⭐'*tea['smell_rating']}")
    st.markdown(f"Gustatif : {'⭐'*tea['taste_rating']}")

    st.markdown("### 🌡 Infusion")
    st.markdown(f"{tea['temperature']}°C • {tea['duration']} min")

    st.markdown("### 🌇 Meilleur moment")
    st.markdown(f"{tea['moment']}")

    st.markdown("### 📦 Infos")
    st.markdown(f"Contenant : {tea['container']}")
    st.markdown(f"Statut : {tea['status']}")

    st.markdown("### 🏷️ Mots-clés")
    st.markdown(tea['keywords'] or "-")

    st.markdown("### Description")
    st.markdown(tea['description'] or "-")

    st.markdown("### Technique")
    st.markdown(tea['technical'] or "-")

    st.markdown("### Notes perso")
    st.markdown(tea['personal_notes'] or "-")

    col1, col2 = st.columns(2)

    if col1.button("✏️ Modifier"):
        st.session_state.edit_id = tea_id
        st.session_state.page = "edit"
        st.rerun()

    if col2.button("⬅️ Retour"):
        st.session_state.page = "main"
        st.rerun()