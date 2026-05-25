
def hex_to_rgba(hex_color, opacity):

    hex_color = hex_color.lstrip("#")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return f"rgba({r},{g},{b},{opacity})"


def inject_css(theme):

    import streamlit as st

    bg_border = theme.get(
        "bgBorder",
        "#66A066"
    )

    bg_center = theme.get(
        "bgCenter",
        "#B0E0D0"
    )

    text = theme.get(
        "text",
        "#222222"
    )

    button = theme.get(
        "button",
        "#E8F5E9"
    )

    card = theme.get(
        "card",
        "#FFFFFF"
    )

    opacity = theme.get(
        "cardOpacity",
        0.92
    )

    card_rgba = hex_to_rgba(
        card,
        opacity
    )

    input_bg = theme.get(
    "input",
    "#FFFFFF"
    )

    subtle_text = theme.get(
    "subtleText",
    text
    )

    st.markdown(f"""
    <style>

    /* =====================================================
       GLOBAL
    ===================================================== */

    html, body, [class*="css"] {{

        font-size: 14px;
    }}

    /* =====================================================
       BACKGROUND
    ===================================================== */

    .stApp {{

        background: linear-gradient(
            90deg,
            {bg_border} 0%,
            {bg_center} 50%,
            {bg_border} 100%
        );

        background-attachment: fixed;
    }}

    /* =====================================================
       STREAMLIT CLEANUP
    ===================================================== */

    header[data-testid="stHeader"] {{
        display: none;
    }}

    div[data-testid="stToolbar"] {{
        display: none;
    }}

    #MainMenu {{
        display: none;
    }}

    footer {{
        display: none;
    }}

    section[data-testid="stSidebar"] {{
        display: none;
    }}

    [data-testid="collapsedControl"] {{
        display: none;
    }}

    [data-testid="stDecoration"] {{
        display: none;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        padding-top: 0rem;
    }}

    .block-container {{

        padding-top: 1rem;
        padding-bottom: 1rem;
    }}

    /* =====================================================
       TITLES
    ===================================================== */

    h1, h2, h3 {{

        color: {text} !important;
    }}

    /* =====================================================
       BUTTONS
    ===================================================== */

    .stButton > button {{

        text-align: left !important;

        padding: 12px 16px;

        border-radius: 14px;

        border: 1px solid rgba(0,0,0,0.05);

        background-color: {button};

        color: {text};

        box-shadow:
            0 4px 12px rgba(0,0,0,0.08);

        transition: all 0.15s ease;
    }}

    .stButton > button:hover {{

        transform: translateY(-1px);

        box-shadow:
            0 6px 16px rgba(0,0,0,0.12);
    }}

    /* =====================================================
    INPUTS
    ===================================================== */

    .stTextInput input {{
        background: {input_bg} !important;

        color: {text} !important;

        border-radius: 12px !important;

        border: 1px solid rgba(255,255,255,0.08);
    }}

    textarea {{

        background: {input_bg} !important;

        color: {text} !important;

        border-radius: 12px !important;
    }}

    /* SELECTBOX */

    .stSelectbox div[data-baseweb="select"] {{

        background: {input_bg} !important;

        color: {text} !important;

        border-radius: 12px !important;
    }}

    /* dropdown internal */

    [data-baseweb="select"] * {{

        color: {text} !important;
    }}

    input::placeholder {{

    color: {subtle_text} !important;

    opacity: 0.7;
    }}

    /* =====================================================
       SELECT
    ===================================================== */

    .stSelectbox div[data-baseweb="select"] {{

        border-radius: 12px !important;
    }}

    /* =====================================================
       DETAILS / EXPANDERS
    ===================================================== */

    details {{

        background: {card_rgba};

        color: {text};

        border-radius: 16px;

        padding: 2px 8px;

        margin-bottom: 0.4rem !important;

        backdrop-filter: blur(4px);
    }}

    details[open] {{

        background: {card_rgba};
    }}

    details * {{

        color: {subtle_text};
    }}

    summary {{

        color: {subtle_text} !important;

        font-weight: 600;
    }}

    /* streamlit expander label */

    summary * {{

        color: {subtle_text} !important;
    }}

    div[data-testid="stExpander"] {{

        margin-bottom: 0rem !important;
    }}

    /* =====================================================
       FORMS
    ===================================================== */

    .form-card {{

        background: {card_rgba};

        color: {text};

        padding: 18px;

        border-radius: 18px;

        margin-bottom: 10px;

        border: 1px solid rgba(0,0,0,0.05);

        box-shadow:
            0 4px 12px rgba(0,0,0,0.05);
    }}

    /* =====================================================
       DETAIL
    ===================================================== */

    .detail-hero {{

        background: {card_rgba};

        color: {text};

        padding: 22px;

        border-radius: 22px;

        margin-bottom: 12px;

        box-shadow:
            0 6px 18px rgba(0,0,0,0.08);
    }}

    .detail-title {{

        font-size: 28px;

        font-weight: 700;

        margin-bottom: 8px;

        color: {text};
    }}

    .detail-subtitle {{

        font-size: 15px;

        opacity: 0.85;

        color: {text};
    }}

    /* =====================================================
       BADGES
    ===================================================== */

    .badge {{

        background: {button};

        color: {text};

        padding: 3px 8px;

        border-radius: 8px;

        font-size: 11px;

        margin-right: 4px;
    }}

    /* =====================================================
       ACTION BAR
    ===================================================== */

    .action-bar {{

        margin-top: 8px;

        padding-top: 6px;

        padding-bottom: 2px;
    }}

    </style>
    """, unsafe_allow_html=True)