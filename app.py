import streamlit as st

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

# ---------------- DATABASE ----------------
import sqlite3

def init_db(conn):
    c = conn.cursor()
    # Temporaire : on recrée la table à chaque lancement pour éviter les soucis de déploiement (ALTER TABLE pas supporté par SQLite)
     # 🔥 force reset
    c.execute("DROP TABLE IF EXISTS teas")
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS teas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        origin TEXT,
        color TEXT,
        description TEXT,
        aromas TEXT,
        smell_rating INTEGER DEFAULT 0,
        taste_rating INTEGER DEFAULT 0,
        temperature INTEGER DEFAULT 70,
        duration INTEGER DEFAULT 3, 
        container TEXT,
        keywords TEXT,
        technical TEXT,
        personal_notes TEXT,
        status TEXT DEFAULT 'Disponible',
        badges TEXT
    )
    """)
    conn.commit()


# connexion
conn = sqlite3.connect("teas.db")
c = conn.cursor()

# 🔥 IMPORTANT
init_db(conn)

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
    border-radius: 12px;
    margin-bottom: 8px;
    border: 1px solid rgba(0,0,0,0.05);
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

if "page" not in st.session_state:
    st.session_state.page = "main"

if "selected_tea" not in st.session_state:
    st.session_state.selected_tea = None

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

# ---------------- ROUTER ----------------
if st.session_state.page == "main":
    main_screen(conn, c)

elif st.session_state.page == "edit":
    edit_screen(conn, c)

elif st.session_state.page == "detail":
    detail_screen(conn, c)