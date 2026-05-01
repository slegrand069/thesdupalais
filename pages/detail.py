import streamlit as st

def detail_screen(conn, c):

    tea_id = st.session_state.get("selected_tea")
    tea = c.execute("SELECT * FROM teas WHERE id=?", (tea_id,)).fetchone()

    if not tea:
        st.error("Thé introuvable")
        return

    st.markdown(f"## 🍵 {tea[1]}")
    st.markdown(f"<small>{tea[3]} • {tea[2]}</small>", unsafe_allow_html=True)

    # badges
    badges = (tea[15] or "").split(",")
    badge_html = "".join([f'<span class="badge">{b}</span>' for b in badges if b])
    st.markdown(badge_html, unsafe_allow_html=True)

    st.markdown("---")

    # notes
    st.markdown("### ⭐ Notes")
    st.markdown(f"Olfactif : {'⭐'*tea[6]}")
    st.markdown(f"Gustatif : {'⭐'*tea[7]}")

    # infusion
    st.markdown("### 🌡 Infusion")
    st.markdown(f"{tea[8]}°C • {tea[9]} min")

    # infos
    st.markdown("### 📦 Infos")
    st.markdown(f"Contenant : {tea[10]}")
    st.markdown(f"Statut : {tea[14]}")

    # contenu
    st.markdown("### 🏷️ Mots-clés")
    st.markdown(tea[11] or "-")

    st.markdown("### Description")
    st.markdown(tea[4] or "-")

    st.markdown("### Technique")
    st.markdown(tea[12] or "-")

    st.markdown("### Notes perso")
    st.markdown(tea[13] or "-")

    st.markdown("---")

    col1, col2 = st.columns(2)

    if col1.button("✏️ Modifier"):
        st.session_state.edit_id = tea_id
        st.session_state.page = "edit"
        st.rerun()

    if col2.button("⬅️ Retour"):
        st.session_state.page = "main"
        st.rerun()