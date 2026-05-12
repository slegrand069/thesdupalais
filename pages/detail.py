import streamlit as st
import textwrap
from models import get_tea_by_id


def detail_screen():

    tea_id = st.session_state.get("selected_tea")
    user_id = st.session_state.user.id

    tea = get_tea_by_id(tea_id, user_id)

    if not tea:
        st.error("Thé introuvable")
        return

    # ---------------------------------------------------
    # HELPERS
    # ---------------------------------------------------

    def to_list(v):
        return [x.strip() for x in v.split(",")] if v else []

    def get_color(color):

        return {
            "Vert": "#DFF5E1",
            "Noir": "#E5E5E5",
            "Blanc": "#FAFAFA",
            "Oolong": "#FFE8D6",
            "Pu'erh": "#E8DED3",
            "Mixte": "#FFE3EC",
            "Infusion": "#E3F0FF"
        }.get(color, "#FFFFFF")

    bg = get_color(tea.get("color"))

    badges = to_list(tea.get("badges"))
    keywords = to_list(tea.get("keywords"))

    # ---------------------------------------------------
    # CSS
    # ---------------------------------------------------

    st.markdown(f"""
    <style>

    .detail-header {{
        background: {bg};
        padding: 22px;
        border-radius: 22px;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.05);
    }}

    .detail-title {{
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 4px;
    }}

    .detail-subtitle {{
        font-size: 14px;
        color: #555;
    }}

    .badge {{
        display: inline-block;
        padding: 4px 10px;
        border-radius: 10px;
        background: rgba(255,255,255,0.75);
        margin-right: 6px;
        margin-top: 8px;
        font-size: 12px;
        border: 1px solid rgba(0,0,0,0.05);
    }}

    .info-card {{
        background: white;
        padding: 18px;
        border-radius: 18px;
        margin-bottom: 16px;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}

    .info-title {{
        font-size: 17px;
        font-weight: 600;
        margin-bottom: 10px;
    }}

    .metric {{
        font-size: 14px;
        margin-bottom: 6px;
    }}

    .keyword {{
        display: inline-block;
        padding: 5px 10px;
        border-radius: 12px;
        background: #F5F5F5;
        margin-right: 6px;
        margin-bottom: 6px;
        font-size: 12px;
    }}

    .action-bar {{
        position: sticky;
        bottom: 0;
        background: rgba(255,255,255,0.92);
        backdrop-filter: blur(10px);
        padding-top: 10px;
        padding-bottom: 6px;
        z-index: 999;
    }}

    </style>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------
    # HEADER
    # ---------------------------------------------------

    badges_html = "".join(
        [f'<span class="badge">{b}</span>' for b in badges]
    )

    st.markdown(textwrap.dedent(f"""
<div class="detail-header">
<div class="detail-title">
🍵 {tea.get("name", "-")}
</div>
<div class="detail-subtitle">
{tea.get("color", "-")} • {tea.get("origin", "-")}
</div>
<div>
{badges_html}
</div>
</div>
    """), unsafe_allow_html=True
    )

    # ---------------------------------------------------
    # MÉTRIQUES
    # ---------------------------------------------------

    st.markdown(
        '<div class="info-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="info-title">⭐ Dégustation</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="metric">
            👃 <b>Olfactif :</b> {tea.get("smell_rating", "-")}/10
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="metric">
            🍵 <b>Gustatif :</b> {tea.get("taste_rating", "-")}/10
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric">
            🌡 <b>Température :</b> {tea.get("temperature", "-")}°C
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="metric">
            ⏳ <b>Durée :</b> {tea.get("duration", "-")} min
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="metric">
        🌙 <b>Moment :</b> {tea.get("moment", "-")}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # DESCRIPTION
    # ---------------------------------------------------

    st.markdown(
        '<div class="info-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="info-title">👃 Profil sensoriel</div>',
        unsafe_allow_html=True
    )

    st.write(tea.get("description", "-"))

    if tea.get("aromas"):

        st.markdown("#### 🌸 Arômes")

        st.write(tea.get("aromas"))

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # KEYWORDS
    # ---------------------------------------------------

    if keywords:

        keywords_html = "".join(
            [f'<span class="keyword">{k}</span>' for k in keywords]
        )

        st.markdown(
            '<div class="info-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="info-title">🏷️ Profil aromatique</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            keywords_html,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # TECHNIQUE
    # ---------------------------------------------------

    if tea.get("technical"):

        st.markdown(
            '<div class="info-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="info-title">⚙️ Notes techniques</div>',
            unsafe_allow_html=True
        )

        st.write(tea.get("technical"))

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # NOTES PERSO
    # ---------------------------------------------------

    if tea.get("personal_notes"):

        st.markdown(
            '<div class="info-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="info-title">📝 Notes personnelles</div>',
            unsafe_allow_html=True
        )

        st.write(tea.get("personal_notes"))

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # GESTION
    # ---------------------------------------------------

    st.markdown(
        '<div class="info-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="info-title">📦 Gestion</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="metric">
        📦 <b>Contenant :</b> {tea.get("container", "-")}
        </div>

        <div class="metric">
        📌 <b>Statut :</b> {tea.get("status", "-")}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # ACTIONS
    # ---------------------------------------------------

    st.markdown(
        '<div class="action-bar">',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    if col1.button(
        "✏️ Modifier",
        use_container_width=True
    ):

        st.session_state.edit_id = tea_id
        st.session_state.page = "edit"

        st.rerun()

    if col2.button(
        "⬅️ Retour",
        use_container_width=True
    ):

        st.session_state.page = "main"

        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)