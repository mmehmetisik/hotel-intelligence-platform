"""
Page 6: Analytics Chatbot

Features:
- Natural language to SQL
- Real-time Groq LLM integration
- Auto-generated charts
- Business insight generation
- Split layout: chat left, visualization right
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app.theme import apply_theme, COLORS
from app.i18n import t
from app.components import (
    section_header, info_box, apply_plotly_theme,
    sidebar_info, get_current_lang,
)

st.set_page_config(page_title="Analytics Chatbot", page_icon="💬", layout="wide")
apply_theme()
lang = get_current_lang()

st.markdown(f"# {t('chat_title', lang)}")
st.caption(t("chat_desc", lang))

# ─── Initialize Chatbot ───
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "chatbot" not in st.session_state:
    st.session_state.chatbot = None
if "last_chart" not in st.session_state:
    st.session_state.last_chart = None
if "last_data" not in st.session_state:
    st.session_state.last_data = None
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# Try to init chatbot
if st.session_state.chatbot is None:
    try:
        from src.module_3_conversational.chatbot import HotelAnalyticsChatbot
        st.session_state.chatbot = HotelAnalyticsChatbot()
        chatbot_ready = True
    except Exception as e:
        chatbot_ready = False
        chatbot_error = str(e)
else:
    chatbot_ready = True

# ─── Sidebar: Examples & Status ───
st.sidebar.markdown(f"### {t('chat_examples', lang)}")
example_questions = [
    "How many bookings were canceled?",
    "What is the average daily rate by hotel type?",
    "Top 5 countries by number of bookings",
    "Show cancellation rate trend by month",
    "Which market segment has highest revenue?",
    "Compare city hotel vs resort hotel",
    "What is the average lead time for canceled bookings?",
    "Show customer segment distribution",
]

for q in example_questions:
    if st.sidebar.button(q, key=f"ex_{hash(q)}", use_container_width=True):
        st.session_state.chat_messages.append({"role": "user", "content": q})
        st.session_state.pending_question = q

# ─── Split Layout ───
chat_col, viz_col = st.columns([1, 1])

with chat_col:
    st.markdown(f"""
    <div style="background: {COLORS['surface']}; border: 1px solid {COLORS['border']};
         border-radius: 12px; padding: 8px 16px; margin-bottom: 16px;">
        <span style="color: {COLORS['success']};">●</span>
        <span style="color: {COLORS['text_secondary']}; font-size: 0.85rem;">
            {t('chatbot_ready', lang) if chatbot_ready else t('chatbot_offline', lang)}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Chat history
    chat_container = st.container(height=500)
    with chat_container:
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input(t("chat_placeholder", lang))

    # Handle sidebar button click
    if "pending_question" in st.session_state and st.session_state.pending_question:
        user_input = st.session_state.pending_question
        st.session_state.pending_question = None

    if user_input:
        # Only add to messages if not already added by sidebar button
        if not st.session_state.chat_messages or st.session_state.chat_messages[-1].get("content") != user_input:
            st.session_state.chat_messages.append({"role": "user", "content": user_input})

        if chatbot_ready:
            with st.spinner(t("analyzing", lang)):
                try:
                    response = st.session_state.chatbot.ask(user_input)

                    answer = response.answer
                    if response.sql:
                        answer += f"\n\n```sql\n{response.sql}\n```"

                    st.session_state.chat_messages.append({"role": "assistant", "content": answer})

                    if response.chart:
                        st.session_state.last_chart = response.chart
                    if response.data is not None:
                        st.session_state.last_data = response.data

                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)[:200]}"
                    st.session_state.chat_messages.append({"role": "assistant", "content": error_msg})
        else:
            # Fallback demo response
            demo_response = t("demo_mode_msg", lang)
            st.session_state.chat_messages.append({"role": "assistant", "content": demo_response})

        st.rerun()

with viz_col:
    st.markdown(f"#### {t('visualization', lang)}")

    if st.session_state.last_chart is not None:
        try:
            fig = st.session_state.last_chart
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.info(t("chart_placeholder_msg", lang))

    elif st.session_state.last_data is not None:
        st.dataframe(st.session_state.last_data, use_container_width=True)
    else:
        st.markdown(f"""
        <div class="premium-card" style="text-align: center; min-height: 300px;
             display: flex; align-items: center; justify-content: center; flex-direction: column;">
            <div style="font-size: 3rem; margin-bottom: 16px;">📊</div>
            <div style="color: {COLORS['text_secondary']};">
                {t('viz_placeholder_msg', lang)}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Data table below chart
    if st.session_state.last_data is not None:
        with st.expander(t("view_raw_data", lang)):
            st.dataframe(st.session_state.last_data, use_container_width=True)

# ─── Architecture Info ───
with st.expander(t("how_it_works", lang)):
    st.markdown(f"""
    <div style="color: {COLORS['text_secondary']};">
        <b>{t('pipeline_architecture', lang)}</b><br><br>
        1. <b>{t('intent_detection', lang)}</b> — {t('intent_detail', lang)}<br>
        2. <b>{t('sql_generation', lang)}</b> — {t('sql_gen_detail', lang)}<br>
        3. <b>{t('execution', lang)}</b> — {t('execution_detail', lang)}<br>
        4. <b>{t('insight_generation', lang)}</b> — {t('insight_detail', lang)}<br>
        5. <b>{t('auto_viz', lang)}</b> — {t('auto_viz_detail', lang)}<br><br>
        <b>{t('llm_routing', lang)}</b> {t('llm_routing_detail', lang)}
    </div>
    """, unsafe_allow_html=True)

# Clear chat button
if st.button(f"🗑️ {t('clear_chat', lang)}", use_container_width=True):
    st.session_state.chat_messages = []
    st.session_state.last_chart = None
    st.session_state.last_data = None
    st.rerun()

sidebar_info()
