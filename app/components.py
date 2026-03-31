"""
Reusable UI Components

Premium components for the Streamlit dashboard:
- Module cards with hover effects
- KPI metric cards
- Hero section
- Tech stack pills
- Status badges
"""

import streamlit as st
from app.theme import COLORS


def hero_section(title: str, subtitle: str):
    """Render the hero section with gradient title."""
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-title">{title}</div>
        <div class="hero-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def module_card(icon: str, title: str, description: str, page_key: str = ""):
    """Render a module card with hover effect."""
    st.markdown(f"""
    <div class="module-card">
        <div class="module-icon">{icon}</div>
        <h3>{title}</h3>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)


def kpi_card(label: str, value: str, delta: str = "", color: str = ""):
    """Render a custom KPI card."""
    col_style = f"color: {color};" if color else f"color: {COLORS['primary']};"
    delta_html = ""
    if delta:
        delta_color = COLORS['success'] if not delta.startswith("-") else COLORS['danger']
        delta_html = f'<div style="color: {delta_color}; font-size: 0.9rem; margin-top: 4px;">{delta}</div>'

    st.markdown(f"""
    <div class="premium-card" style="text-align: center;">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="{col_style}">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str, subtitle: str = "", icon: str = ""):
    """Render a section header with optional icon."""
    icon_html = f"{icon} " if icon else ""
    st.markdown(f"### {icon_html}{title}")
    if subtitle:
        st.caption(subtitle)


def status_badge(status: str):
    """Render a status badge (healthy/warning/critical)."""
    badge_class = f"badge-{status}" if status in ("healthy", "warning", "critical") else "badge-healthy"
    label = status.capitalize()
    return f'<span class="{badge_class}">{label}</span>'


def tech_stack_pills(techs: list):
    """Render tech stack as pills."""
    pills_html = "".join(f'<span class="tech-pill">{tech}</span>' for tech in techs)
    st.markdown(f'<div style="text-align: center; margin: 20px 0;">{pills_html}</div>', unsafe_allow_html=True)


def info_box(text: str, box_type: str = "info"):
    """Render a styled info/warning/success box."""
    colors = {
        "info": (COLORS['info'], "rgba(77, 168, 255, 0.1)"),
        "warning": (COLORS['warning'], "rgba(255, 184, 0, 0.1)"),
        "success": (COLORS['success'], "rgba(0, 210, 106, 0.1)"),
        "error": (COLORS['danger'], "rgba(255, 75, 75, 0.1)"),
    }
    text_color, bg_color = colors.get(box_type, colors["info"])
    st.markdown(f"""
    <div style="background: {bg_color}; border-left: 4px solid {text_color};
         padding: 14px 18px; border-radius: 0 8px 8px 0; margin: 10px 0;
         color: {text_color}; font-size: 0.95rem;">
        {text}
    </div>
    """, unsafe_allow_html=True)


def plotly_theme() -> dict:
    """Get Plotly chart theme matching the app."""
    return {
        "template": "plotly_dark",
        "paper_bgcolor": COLORS["surface"],
        "plot_bgcolor": COLORS["surface"],
        "font": {"color": COLORS["text"], "family": "Inter, sans-serif"},
        "colorway": [
            COLORS["primary"], COLORS["accent"], COLORS["info"],
            COLORS["success"], COLORS["warning"], "#A78BFA",
            "#EC4899", "#14B8A6", "#F97316", "#8B5CF6",
        ],
        "margin": dict(l=40, r=20, t=50, b=40),
    }


def apply_plotly_theme(fig):
    """Apply premium theme to a Plotly figure."""
    theme = plotly_theme()
    fig.update_layout(
        template=theme["template"],
        paper_bgcolor=theme["paper_bgcolor"],
        plot_bgcolor=theme["plot_bgcolor"],
        font=theme["font"],
        colorway=theme["colorway"],
        margin=theme["margin"],
    )
    fig.update_xaxes(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"])
    fig.update_yaxes(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"])
    return fig


def sidebar_language_selector():
    """Language selector for sidebar. Returns current language."""
    from app.i18n import LANG_OPTIONS, t
    lang_label = t("language", get_current_lang())
    selected = st.sidebar.selectbox(
        f"🌍 {lang_label}",
        list(LANG_OPTIONS.keys()),
        index=0,
        key="lang_selector",
    )
    lang = LANG_OPTIONS[selected]
    st.session_state["lang"] = lang
    return lang


def get_current_lang() -> str:
    """Get current language from session state."""
    return st.session_state.get("lang", "en")


def sidebar_info():
    """Render sidebar footer info."""
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"""
        <div style="text-align: center; color: {COLORS['text_muted']}; font-size: 0.75rem; line-height: 1.8;">
            Built by <b>Mehmet ISIK</b><br>
            Kaggle Grandmaster<br>
            <a href="https://mehmetisik.dev" style="color: {COLORS['primary']};">Website</a> ·
            <a href="https://www.linkedin.com/in/mehmetisik4601" style="color: {COLORS['primary']};">LinkedIn</a> ·
            <a href="https://www.kaggle.com/mehmetisik" style="color: {COLORS['primary']};">Kaggle</a><br>
            <a href="https://medium.com/@mmehmetisiken" style="color: {COLORS['primary']};">Medium</a> ·
            <a href="https://github.com/mmehmetisik/hotel-intelligence-platform" style="color: {COLORS['primary']};">GitHub Repo</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
