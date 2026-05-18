import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import json
from pages.admin import admin_screen
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

col1, col2 = st.columns([6,2], gap="small")
with col1:
    st.title("🍵 Thés du Palais")
    st.write("Gérez votre collection de thés, notez-les et retrouvez-les facilement !")

with col2:
    if st.button("🚪Déconnexion", help="Déconnexion"):
        supabase.auth.sign_out()
        streamlit_js_eval(js_expressions="localStorage.removeItem('supabase_session')")
        st.session_state.clear()
        st.rerun()
st.markdown("""
<style>
div.stButton > button {
    border-radius: 14px;
    font-size: 14px;
    padding: 16px;
    use_container_width: true;
    border: 1px solid rgba(0,0,0,0.05);
            margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)            

st.markdown("""
<style>

/* ======================================================
   GLOBAL
====================================================== */

html, body, [class*="css"] {
    font-size: 14px;
}

/* ======================================================
   APP BACKGROUND
====================================================== */

.stApp {
    background: linear-gradient(
        90deg,
        #66A066 0%,
        #B0E0D0 50%,
        #66A066 100%
    );

    background-attachment: fixed;
}

/* ======================================================
   STREAMLIT CLEANUP
====================================================== */

/* Header blanc du haut */
header[data-testid="stHeader"] {
    display: none;
}

/* Toolbar dev */
div[data-testid="stToolbar"] {
    display: none;
}

/* Menu hamburger */
#MainMenu {
    display: none;
}

/* Footer */
footer {
    display: none;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    display: none;
}

/* Bouton collapse sidebar */
[data-testid="collapsedControl"] {
    display: none;
}

/* Réduit espace top */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
}
            
[data-testid="stDecoration"] {
    display: none;
}

[data-testid="stAppViewContainer"] > .main {
    padding-top: 0rem;
}

/* ======================================================
   IMPROVE DETAILS STYLE
====================================================== */
                        
details {
    background: rgba(255,255,255,0.18);
    backdrop-filter: blur(4px);

    border-radius: 16px;

    padding: 2px 8px;

    margin-bottom: 0.5rem !important;
}

summary {
    font-weight: 600;
}

div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stExpander"]) {
    margin-bottom: 0.4rem !important;
}

div[data-testid="stExpander"] {
    margin-bottom: 0rem !important;
}
            
details[open] {
    background: rgba(255,255,255,0.28);
}
            
.detail-hero {

    padding: 22px;

    border-radius: 22px;

    margin-bottom: 12px;

    box-shadow:
        0 6px 18px rgba(0,0,0,0.08);
}

.detail-title {

    font-size: 28px;

    font-weight: 700;

    margin-bottom: 8px;
}

.detail-subtitle {

    opacity: 0.8;

    font-size: 15px;
}

/* ======================================================
   TITRES
====================================================== */

h1 {
    font-size: 24px !important;
}

h2 {
    font-size: 20px !important;
}

h3 {
    font-size: 16px !important;
}

/* ======================================================
   CARDS
====================================================== */

.card {
    padding: 12px;
    border-radius: 14px;
    margin-bottom: 10px;

    border: 1px solid rgba(0,0,0,0.05);

    box-shadow:
        0 4px 12px rgba(0,0,0,0.08);
}

/* ======================================================
   SECTION TITLES
====================================================== */

.section-title {
    font-size: 18px;
    font-weight: 600;

    margin-bottom: 10px;
}

/* ======================================================
   BUTTONS
====================================================== */

.stButton > button {

    text-align: left !important;

    padding: 12px 16px;

    border-radius: 14px;

    border: 1px solid rgba(0,0,0,0.05);

    box-shadow:
        0 4px 12px rgba(0,0,0,0.08);

    background-color: #E8F5E9;

    font-size: 14px;

    line-height: 1.4;

    transition: all 0.15s ease;
}

.stButton > button:hover {

    transform: translateY(-1px);

    box-shadow:
        0 6px 16px rgba(0,0,0,0.12);
}

/* ======================================================
   INPUTS
====================================================== */

.stTextInput input {
    border-radius: 12px !important;
    font-size: 13px;
}

textarea {
    border-radius: 12px !important;
}
            
input[type="color"] {
    cursor: pointer;
}

/* ======================================================
   SELECTBOX
====================================================== */

.stSelectbox div[data-baseweb="select"] {
    border-radius: 12px !important;
}

/* ======================================================
   SLIDERS
====================================================== */

.stSlider {
    padding-top: 4px;
}

/* ======================================================
   BADGES
====================================================== */

.badge {

    background: #f0f0f0;

    padding: 3px 8px;

    border-radius: 8px;

    font-size: 11px;

    margin-right: 4px;
}

/* ======================================================
   ACTION BAR
====================================================== */

.action-bar {

    margin-top: 8px;

    padding-top: 6px;

    padding-bottom: 2px;
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

elif st.session_state.page == "admin":
    admin_screen()
