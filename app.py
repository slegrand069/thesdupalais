import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import json
from pages.main import main_screen
from pages.edit import edit_screen
from pages.detail import detail_screen  
from models import supabase

# Supabase THD3w!nt3Res26!

# 🔥 DOIT ÊTRE EN TOUT PREMIER
st.set_page_config(
    page_title="Thés du Palais",
    page_icon="🍵",
    layout="centered",
    initial_sidebar_state="collapsed"
)
session_data = streamlit_js_eval(
    js_expressions="localStorage.getItem('supabase_session')",
    key="get_session"
)

# ---------------- LOGIN ----------------
def login_screen():

    st.title("🔐 Connexion")

    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    col1, col2= st.columns(2, gap="small")
    col3, _ = st.columns([1,4], gap="small")

    # 🔓 LOGIN
    if col1.button("🔓 Connexion"):
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if res and res.user:
            st.session_state.user = res.user
            st.session_state.session = res.session
            
            # 🔥 stocker dans navigateur
            streamlit_js_eval(js_expressions=f"""
                localStorage.setItem("supabase_session", JSON.stringify({{
                access_token: "{res.session.access_token}",
                refresh_token: "{res.session.refresh_token}"
                }}))
            """)
            st.rerun()
        else:
            st.error("Email ou mot de passe incorrect")

    # 🆕 SIGNUP
    if col2.button("🆕 Créer un compte"):
        res = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        if res and res.user:
            st.success("Compte créé 🎉")
        else:
            st.error("Erreur création compte")

    # 🚪 LOGOUT
    if col3.button("🚪 Déconnexion"):
        supabase.auth.sign_out()
        streamlit_js_eval(js_expressions="localStorage.removeItem('supabase_session')")
        st.session_state.clear()
        st.rerun()

if session_data and session_data != "null" and "session" not in st.session_state:
    try:
        s = json.loads(session_data)

        supabase.auth.set_session(
            s["access_token"],
            s["refresh_token"]
        )

        user = supabase.auth.get_user()

        st.session_state.user = user.user
        st.session_state.session = s

    except Exception as e:
        st.write("Session restore error:", e)

if "user" not in st.session_state:
    login_screen()
    st.stop()

        
# ---------------- DATABASE ----------------

url = "https://ptcsqnskkybxmnsdsdxg.supabase.co"
# anon public
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB0Y3NxbnNra3lieG1uc2RzZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc2Nzc4MzYsImV4cCI6MjA5MzI1MzgzNn0.jcwmddYOVL2DNNPCUEjb3c3l3RWUTLTzagtLDqbTpvw"

# ---------------- APP ----------------

st.title("🍵 Thés du Palais")
st.write("Gérez votre collection de thés, notez-les et retrouvez-les facilement !")
col1, col2 = st.columns([6,1])

with col2:
    if st.button("🚪", help="Déconnexion"):
        supabase.auth.sign_out()
        streamlit_js_eval(js_expressions="localStorage.removeItem('supabase_session')")
        st.session_state.clear()
        st.rerun()

st.markdown("""
<style>

/* GLOBAL */
html, body, [class*="css"] {
    font-size: 14px;
}

/* TITRES */
h1 {
    font-size: 24px !important;
}
h2 {
    font-size: 20px !important;
}
h3 {
    font-size: 16px !important;
}

/* CARDS */
.card {
    padding: 12px;
    border-radius: 14px;
    margin-bottom: 10px;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
            
/* BOUTONS */

/* Boutons normaux */
.stButton > button {
    text-align: left !important;
    padding: 16px;
    border-radius: 16px;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    background-color: #E8F5E9; /* ou dynamique si besoin */
    font-size: 14px;
    line-height: 1.6;
}
            
            /* INPUTS */
.stTextInput>div>div>input {
    font-size: 13px;
}

/* SLIDERS */
.stSlider {
    padding-top: 0px;
}

/* BADGES */
.badge {
    background: #f0f0f0;
    padding: 3px 8px;
    border-radius: 8px;
    font-size: 11px;
    margin-right: 4px;
}

/* FORM SECTIONS */
.form-card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    margin-bottom: 16px;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* TITRES */
.section-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 12px;
}

/* TEXT AREA */
textarea {
    border-radius: 12px !important;
}

/* INPUTS */
.stTextInput input {
    border-radius: 12px !important;
}

/* SELECT */
.stSelectbox div[data-baseweb="select"] {
    border-radius: 12px !important;
}

/* SLIDERS */
.stSlider {
    padding-top: 10px;
}

/* ACTION BAR */
.action-bar {
    position: sticky;
    bottom: 0;
    background: rgba(255,255,255,0.9);
    backdrop-filter: blur(10px);
    padding-top: 12px;
    padding-bottom: 8px;
}

</style>
""", unsafe_allow_html=True)

if "user" not in st.session_state:
    login_screen()
    st.stop()

user_id = st.session_state.user.id

if "page" not in st.session_state:
    st.session_state.page = "main"

if "selected_tea" not in st.session_state:
    st.session_state.selected_tea = None

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

# ---------------- ROUTER ----------------
if st.session_state.page == "main":
    main_screen()

elif st.session_state.page == "edit":
    edit_screen()

elif st.session_state.page == "detail":
    detail_screen()


