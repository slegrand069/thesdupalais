import json

import streamlit as st

from streamlit_js_eval import streamlit_js_eval

from models import supabase

from config import get_themes

from ui import inject_css

from pages.main import main_screen
from pages.edit import edit_screen
from pages.detail import detail_screen
from pages.admin import admin_screen
from pages.theme_editor import theme_editor_screen


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Thés du Palais",
    page_icon="🍵",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =====================================================
# SESSION STATE INIT
# =====================================================

DEFAULT_SESSION = {

    "page": "main",

    "selected_tea": None,

    "edit_id": None,

    "theme": "Light"
}

for key, value in DEFAULT_SESSION.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =====================================================
# LOAD LOCAL STORAGE SESSION
# =====================================================

session_data = streamlit_js_eval(
    js_expressions="""
        localStorage.getItem(
            'supabase_session'
        )
    """,
    key="get_session"
)


# =====================================================
# RESTORE SESSION
# =====================================================

if (
    session_data
    and session_data != "null"
    and "user" not in st.session_state
):

    try:

        s = json.loads(session_data)

        supabase.auth.set_session(
            s["access_token"],
            s["refresh_token"]
        )

        user = supabase.auth.get_user()

        st.session_state.user = user.user

        st.session_state.session = s

    except Exception:

        # clear broken session
        streamlit_js_eval(
            js_expressions="""
                localStorage.removeItem(
                    'supabase_session'
                )
            """,
            key="clear_bad_session"
        )

        st.session_state.pop(
            "user",
            None
        )

        st.session_state.pop(
            "session",
            None
        )


# =====================================================
# LOGIN SCREEN
# =====================================================

def login_screen():

    st.title("🔐 Connexion")

    email = st.text_input("Email")

    password = st.text_input(
        "Mot de passe",
        type="password"
    )

    col1, col2 = st.columns(2)

    # =================================================
    # LOGIN
    # =================================================

    if col1.button(
        "🔓 Connexion",
        use_container_width=True
    ):

        try:

            res = supabase.auth.sign_in_with_password({

                "email": email,

                "password": password
            })

            if res and res.user:

                st.session_state.user = res.user

                st.session_state.session = {

                    "access_token":
                        res.session.access_token,

                    "refresh_token":
                        res.session.refresh_token
                }

                # save browser session
                streamlit_js_eval(
                    js_expressions=f"""
                        localStorage.setItem(
                            'supabase_session',

                            JSON.stringify({{
                                access_token:
                                    "{res.session.access_token}",

                                refresh_token:
                                    "{res.session.refresh_token}"
                            }})
                        )
                    """,
                    key="save_session"
                )

                st.rerun()

            else:

                st.error(
                    "Email ou mot de passe incorrect"
                )

        except Exception as e:

            st.error(
                f"Erreur connexion : {e}"
            )

    # =================================================
    # SIGNUP
    # =================================================

    if col2.button(
        "🆕 Créer un compte",
        use_container_width=True
    ):

        try:

            res = supabase.auth.sign_up({

                "email": email,

                "password": password
            })

            if res and res.user:

                st.success(
                    "Compte créé 🎉"
                )

            else:

                st.error(
                    "Erreur création compte"
                )

        except Exception as e:

            st.error(
                f"Erreur création : {e}"
            )


# =====================================================
# AUTH CHECK
# =====================================================

if "user" not in st.session_state:

    login_screen()

    st.stop()


# =====================================================
# LOAD THEMES
# =====================================================

themes = get_themes()

theme = themes.get(
    st.session_state.theme,
    themes.get("Light", {})
)
st.session_state.current_theme = theme


# =====================================================
# CSS
# =====================================================

inject_css(theme)


# =====================================================
# HEADER
# =====================================================

col1, col2 = st.columns([6,2])

with col1:

    st.title("🍵 Thés du Palais")

    st.markdown(f"""
    <div style="
        color:{theme.get('subtleText')};
        opacity:0.9;
        margin-top:-8px;
    ">
        Gérez votre collection de thés,
        notez-les et retrouvez-les facilement !
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "🚪 Déconnexion",
        use_container_width=True
    ):

        try:

            supabase.auth.sign_out()

        except:
            pass

        streamlit_js_eval(
            js_expressions="""
                localStorage.removeItem(
                    'supabase_session'
                )
            """,
            key="logout"
        )

        st.session_state.clear()

        st.rerun()


# =====================================================
# ROUTER
# =====================================================

page = st.session_state.page


if page == "main":

    main_screen()

elif page == "edit":

    edit_screen()

elif page == "detail":

    detail_screen()

elif page == "admin":

    admin_screen()

elif page == "theme_editor":

    theme_editor_screen()