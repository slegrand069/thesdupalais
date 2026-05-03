import streamlit as st
# Supabase THD3w!nt3Res26!
# 🔥 DOIT ÊTRE EN TOUT PREMIER
st.set_page_config(
    page_title="Thés du Palais",
    page_icon="🍵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

from pages.main import main_screen
from pages.edit import edit_screen
from pages.detail import detail_screen  
from models import supabase

if "session" in st.session_state and st.session_state.session:
    try:
        supabase.auth.set_session(
            st.session_state.session.access_token,
            st.session_state.session.refresh_token
        )
    except:
        pass

# ---------------- LOGIN ----------------
def login_screen():

    st.title("🔐 Connexion")

    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    col1, col2, col3 = st.columns(3)

    # 🔓 LOGIN
    if col1.button("🔓 Connexion"):
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if res and res.user:
            st.session_state.user = res.user
            st.session_state.session = res.session
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
        st.session_state.clear()
        st.rerun()
        
# ---------------- DATABASE ----------------

url = "https://ptcsqnskkybxmnsdsdxg.supabase.co"
# anon public
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB0Y3NxbnNra3lieG1uc2RzZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc2Nzc4MzYsImV4cCI6MjA5MzI1MzgzNn0.jcwmddYOVL2DNNPCUEjb3c3l3RWUTLTzagtLDqbTpvw"

# ---------------- APP ----------------

st.title("🍵 Thés du Palais")

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
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 13px;
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


