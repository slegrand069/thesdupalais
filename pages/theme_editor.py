import json
import traceback
import streamlit as st

from config import get_themes
from models import (
    update_config_extra,
    get_config_row
)


def theme_editor_screen():

    st.markdown("## 🎨 Theme Editor")

    themes = get_themes()

    theme_names = list(
        themes.keys()
    )

    selected_theme = st.selectbox(
        "🎨 Thème à éditer",
        theme_names,
        index=theme_names.index(
            st.session_state.theme
        )
        if st.session_state.theme in theme_names
        else 0
    )

    theme = themes[selected_theme]

    theme_name = selected_theme

    row = get_config_row(
        "theme",
        theme_name
    )

    try:

        theme = json.loads(
            row["extra"]
    )

    except Exception as e:

        st.error(
            f"Erreur chargement thème : {e}"
        )

        st.code(traceback.format_exc())
        return


    # =================================================
    # GLOBAL
    # =================================================

    with st.expander(
        "🌍 Global UI",
        expanded=True
    ):

        col1, col2 = st.columns(2)

        with col1:

            bgBorder = st.color_picker(
                "🌑 Background Border",
                theme.get(
                    "bgBorder",
                    "#66A066"
                )
            )

            bgCenter = st.color_picker(
                "🌕 Background Center",
                theme.get(
                    "bgCenter",
                    "#B0E0D0"
                )
            )

            card = st.color_picker(
                "🪟 Cards",
                theme.get(
                    "card",
                    "#FFFFFF"
                )
            )

            input_bg = st.color_picker(
                "⌨️ Inputs",
                theme.get(
                    "input",
                    "#FFFFFF"
                )
            )

        with col2:

            text = st.color_picker(
                "📝 Main Text",
                theme.get(
                    "text",
                    "#222222"
                )
            )

            subtleText = st.color_picker(
                "💬 Secondary Text",
                theme.get(
                    "subtleText",
                    "#444444"
                )
            )

            button = st.color_picker(
                "🔘 Buttons",
                theme.get(
                    "button",
                    "#E8F5E9"
                )
            )

            border = st.color_picker(
                "📦 Borders",
                theme.get(
                    "border",
                    "#DDDDDD"
                )
            )

        cardOpacity = st.slider(
            "🫧 Card Opacity",
            0.1,
            1.0,
            float(
                theme.get(
                    "cardOpacity",
                    0.92
                )
            ),
            step=0.01
        )

    # =================================================
    # TEA COLORS
    # =================================================

    tea_colors = theme.get("teaCardColors", 
        {
        "green": "#E8F5E9",
        "oolong": "#FFF3E0",
        "black": "#EFEBE9",
        "white": "#E3F2FD",
        "mixed": "#F3E5F5",
        "mate": "#E0F7FA",
        "infusion": "#FCE4EC",
        "pu-erh": "#FBE9E7",
        "default": "#E8F5E9"
        }
    )

    with st.expander(
        "🍵 Tea Cards",
        expanded=True
    ):

        for key in tea_colors:

            tea_colors[key] = st.color_picker(
                key.capitalize(),
                tea_colors[key]
            )

    # =================================================
    # PREVIEW
    # =================================================

    st.markdown("### 👀 Preview")

    st.markdown(f"""
<div style="
background:{card};
color:{text};
padding:20px;
border-radius:18px;
border:1px solid rgba(0,0,0,0.08);
margin-top:10px;
">
<h3>🍵 Sencha Impérial</h3>
<p>
Thé vert japonais délicat
</p>
<button style="
background:{button};
border:none;
padding:10px 14px;
border-radius:10px;
">
Exemple bouton
</button>
<input
placeholder="Recherche..."
style="
background:{input_bg};
color:{text};
border:1px solid {border};
border-radius:10px;
padding:10px;
width:100%;
margin-top:12px;
"/>
</div>
    """, unsafe_allow_html=True)

    # =================================================
    # SAVE
    # =================================================

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    if col3.button(
        "💾 Sauvegarder",
        use_container_width=True
    ):

        theme_data = {
            "bgBorder": bgBorder,
            "bgCenter": bgCenter,
            "card": card,
            "cardOpacity": cardOpacity,

            "button": button,

            "text": text,
            "subtleText": subtleText,

            "input": input_bg,

            "border": border,
            
            "teaCardColors": tea_colors
        }

        update_config_extra(
            row["id"],
            json.dumps(theme_data)
        )

        st.success("Thème sauvegardé")

    if col2.button(
    "↩️ Annuler",
    use_container_width=True
    ):
        st.rerun()

    if col1.button("⬅️ Retour",
    use_container_width=True
    ):
        st.session_state.page = "main"
        st.rerun()

