"""
Premium Dark Theme — Strawberry-Inspired

Custom CSS that transforms Streamlit into a premium dashboard.
Color palette inspired by hospitality warmth with professional dark tones.
"""


# ─────────────────── Color Palette ───────────────────

COLORS = {
    "primary": "#FF4B4B",       # Strawberry red-orange
    "primary_light": "#FF6B6B",
    "primary_dark": "#CC3C3C",
    "secondary": "#1B1F3B",     # Deep navy
    "accent": "#FF8C42",        # Warm orange
    "background": "#0E1117",    # Dark background
    "surface": "#1E2130",       # Card surfaces
    "surface_hover": "#262A3E",
    "border": "#2D3250",
    "success": "#00D26A",       # Green positive
    "warning": "#FFB800",       # Amber warning
    "danger": "#FF4B4B",
    "info": "#4DA8FF",
    "text": "#FAFAFA",          # White text
    "text_secondary": "#9CA3AF",
    "text_muted": "#6B7280",
}


# ─────────────────── Main CSS ───────────────────

CUSTOM_CSS = f"""
<style>
    /* ═══ Global ═══ */
    .stApp {{
        background-color: {COLORS['background']};
        color: {COLORS['text']};
    }}

    /* ═══ Sidebar ═══ */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['secondary']} 0%, #12152B 100%);
        border-right: 1px solid {COLORS['border']};
    }}
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li {{
        color: {COLORS['text_secondary']};
    }}

    /* ═══ Headers ═══ */
    h1, h2, h3 {{
        color: {COLORS['text']} !important;
        font-weight: 700 !important;
    }}
    h1 {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['accent']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.2rem !important;
    }}

    /* ═══ Metric Cards ═══ */
    div[data-testid="stMetric"] {{
        background: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 16px 20px;
        transition: all 0.3s ease;
    }}
    div[data-testid="stMetric"]:hover {{
        border-color: {COLORS['primary']};
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 75, 75, 0.15);
    }}
    div[data-testid="stMetric"] label {{
        color: {COLORS['text_secondary']} !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
        color: {COLORS['text']} !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }}
    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] svg {{
        display: inline;
    }}

    /* ═══ Buttons ═══ */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.3);
    }}

    /* ═══ Tabs ═══ */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: {COLORS['surface']};
        border-radius: 10px;
        padding: 4px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        color: {COLORS['text_secondary']};
        font-weight: 500;
    }}
    .stTabs [aria-selected="true"] {{
        background: {COLORS['primary']} !important;
        color: white !important;
    }}

    /* ═══ DataFrames & Tables ═══ */
    .stDataFrame {{
        border: 1px solid {COLORS['border']};
        border-radius: 10px;
        overflow: hidden;
    }}

    /* ═══ Selectbox, Input ═══ */
    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        background-color: {COLORS['surface']} !important;
        color: {COLORS['text']} !important;
        border-color: {COLORS['border']} !important;
        border-radius: 8px !important;
    }}

    /* ═══ Expander ═══ */
    .streamlit-expanderHeader {{
        background-color: {COLORS['surface']};
        border-radius: 8px;
        color: {COLORS['text']} !important;
    }}

    /* ═══ Plotly Charts ═══ */
    .js-plotly-plot .plotly .modebar {{
        background: transparent !important;
    }}

    /* ═══ Chat Messages ═══ */
    .stChatMessage {{
        background: {COLORS['surface']} !important;
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
    }}

    /* ═══ Custom Card Component ═══ */
    .premium-card {{
        background: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 14px;
        padding: 24px;
        transition: all 0.3s ease;
    }}
    .premium-card:hover {{
        border-color: {COLORS['primary']};
        box-shadow: 0 8px 30px rgba(255, 75, 75, 0.12);
    }}

    /* ═══ Module Card ═══ */
    .module-card {{
        background: linear-gradient(145deg, {COLORS['surface']} 0%, {COLORS['secondary']} 100%);
        border: 1px solid {COLORS['border']};
        border-radius: 16px;
        padding: 28px;
        text-align: center;
        transition: all 0.4s ease;
        cursor: pointer;
    }}
    .module-card:hover {{
        border-color: {COLORS['primary']};
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(255, 75, 75, 0.2);
    }}
    .module-card h3 {{
        margin-top: 12px;
        font-size: 1.1rem !important;
    }}
    .module-card p {{
        color: {COLORS['text_secondary']};
        font-size: 0.9rem;
    }}
    .module-icon {{
        font-size: 2.5rem;
        margin-bottom: 8px;
    }}

    /* ═══ Hero Section ═══ */
    .hero-section {{
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, {COLORS['secondary']} 0%, {COLORS['background']} 50%, {COLORS['secondary']} 100%);
        border-radius: 20px;
        border: 1px solid {COLORS['border']};
        margin-bottom: 30px;
    }}
    .hero-title {{
        font-size: 3rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['accent']} 50%, {COLORS['primary_light']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
    }}
    .hero-subtitle {{
        color: {COLORS['text_secondary']};
        font-size: 1.2rem;
        max-width: 700px;
        margin: 0 auto;
    }}

    /* ═══ KPI Row ═══ */
    .kpi-value {{
        font-size: 2.2rem;
        font-weight: 800;
        color: {COLORS['primary']};
    }}
    .kpi-label {{
        font-size: 0.85rem;
        color: {COLORS['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* ═══ Status Badge ═══ */
    .badge-healthy {{
        background: rgba(0, 210, 106, 0.15);
        color: {COLORS['success']};
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }}
    .badge-warning {{
        background: rgba(255, 184, 0, 0.15);
        color: {COLORS['warning']};
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }}
    .badge-critical {{
        background: rgba(255, 75, 75, 0.15);
        color: {COLORS['danger']};
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }}

    /* ═══ Tech Stack Pills ═══ */
    .tech-pill {{
        display: inline-block;
        background: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 20px;
        padding: 6px 14px;
        margin: 4px;
        font-size: 0.85rem;
        color: {COLORS['text_secondary']};
        transition: all 0.2s ease;
    }}
    .tech-pill:hover {{
        border-color: {COLORS['primary']};
        color: {COLORS['primary']};
    }}

    /* ═══ Hide Streamlit Branding ═══ */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
</style>
"""


def apply_theme():
    """Apply the premium theme to the Streamlit app."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
