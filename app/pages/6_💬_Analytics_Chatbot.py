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
st.caption("Ask questions about your hotel data in natural language")

# ─── Initialize Chatbot ───
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "chatbot" not in st.session_state:
    st.session_state.chatbot = None
if "last_chart" not in st.session_state:
    st.session_state.last_chart = None
if "last_data" not in st.session_state:
    st.session_state.last_data = None

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

# ─── Split Layout ───
chat_col, viz_col = st.columns([1, 1])

with chat_col:
    st.markdown(f"""
    <div style="background: {COLORS['surface']}; border: 1px solid {COLORS['border']};
         border-radius: 12px; padding: 8px 16px; margin-bottom: 16px;">
        <span style="color: {COLORS['success']};">●</span>
        <span style="color: {COLORS['text_secondary']}; font-size: 0.85rem;">
            {'Chatbot Ready — Groq LLM Connected' if chatbot_ready else 'Chatbot Offline'}
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

    if user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})

        if chatbot_ready:
            with st.spinner("Analyzing..."):
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
            demo_response = (
                "I'm currently running in demo mode (Groq API not connected). "
                "In production, I would:\n"
                "1. Detect your intent (SQL query, prediction, recommendation)\n"
                "2. Generate a SQL query from your question\n"
                "3. Execute it against the hotel database\n"
                "4. Generate business insights from the results\n"
                "5. Create an auto-visualization"
            )
            st.session_state.chat_messages.append({"role": "assistant", "content": demo_response})

        st.rerun()

with viz_col:
    st.markdown(f"#### Visualization")

    if st.session_state.last_chart is not None:
        try:
            fig = st.session_state.last_chart
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.info("Chart will appear here when you ask a data question.")

    elif st.session_state.last_data is not None:
        st.dataframe(st.session_state.last_data, use_container_width=True)
    else:
        st.markdown(f"""
        <div class="premium-card" style="text-align: center; min-height: 300px;
             display: flex; align-items: center; justify-content: center; flex-direction: column;">
            <div style="font-size: 3rem; margin-bottom: 16px;">📊</div>
            <div style="color: {COLORS['text_secondary']};">
                Charts and data tables will appear here<br>when you ask a question
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Data table below chart
    if st.session_state.last_data is not None:
        with st.expander("View Raw Data"):
            st.dataframe(st.session_state.last_data, use_container_width=True)

# ─── Architecture Info ───
with st.expander("How it works"):
    st.markdown(f"""
    <div style="color: {COLORS['text_secondary']};">
        <b>Pipeline Architecture:</b><br><br>
        1. <b>Intent Detection</b> — LLM classifies question into: sql_query, prediction, recommendation, summary, explanation<br>
        2. <b>SQL Generation</b> — Schema-aware NL-to-SQL with safety validation (no DROP/DELETE)<br>
        3. <b>Execution</b> — Query runs against SQLite analytics database (119K+ records)<br>
        4. <b>Insight Generation</b> — LLM generates natural language business insights from results<br>
        5. <b>Auto-Visualization</b> — Detects optimal chart type (bar, line, pie, scatter, metric)<br><br>
        <b>LLM Routing:</b> Cache (diskcache) → Groq API (LLaMA 3.3 70B) → Fallback
    </div>
    """, unsafe_allow_html=True)

# Clear chat button
if st.button("🗑️ Clear Chat", use_container_width=True):
    st.session_state.chat_messages = []
    st.session_state.last_chart = None
    st.session_state.last_data = None
    st.rerun()

sidebar_info()
