"""
app.py — Streamlit dashboard for interacting with the DeepSeek AI agent.

Run with:
    streamlit run app.py
"""

import streamlit as st
from agent import run_agent

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DeepSeek AI Assistant",
    page_icon="🤖",
    layout="wide",
)

# ── Session state initialisation ──────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []          # list of {role, content} dicts
if "last_response" not in st.session_state:
    st.session_state.last_response = None

# ── Sidebar — configuration ───────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Configuration")
    st.markdown("---")

    model = st.selectbox(
        "Model",
        options=["deepseek-chat", "deepseek-reasoner"],
        index=0,
        help="deepseek-chat is faster; deepseek-reasoner uses chain-of-thought.",
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.5,
        value=0.7,
        step=0.05,
        help="Higher values make responses more creative; lower values more deterministic.",
    )

    max_tokens = st.slider(
        "Max response tokens",
        min_value=128,
        max_value=4096,
        value=1024,
        step=128,
        help="Maximum length of the agent's reply.",
    )

    st.markdown("---")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.history = []
        st.session_state.last_response = None
        st.success("Conversation cleared.")

    st.markdown("---")
    st.caption("IIMT3688 · HW5 · DeepSeek Agent")

# ── Main area ─────────────────────────────────────────────────────────────────
st.title("🤖 DeepSeek AI Assistant")
st.markdown(
    "Ask anything — the agent remembers your conversation within this session. "
    "Adjust model settings in the sidebar."
)
st.markdown("---")

# Input form
with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_area(
        "Your message",
        placeholder="e.g. Explain what a REST API is in simple terms…",
        height=120,
    )
    submitted = st.form_submit_button("Send ➤", use_container_width=True)

# Validation + agent call
if submitted:
    cleaned = user_input.strip()
    if not cleaned:
        st.warning("Please enter a message before submitting.")
    else:
        with st.spinner("Agent is thinking…"):
            try:
                reply = run_agent(
                    query=cleaned,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    history=st.session_state.history,
                )
                # Persist turn in history
                st.session_state.history.append({"role": "user", "content": cleaned})
                st.session_state.history.append({"role": "assistant", "content": reply})
                st.session_state.last_response = reply
                st.success("Response received!")
            except ValueError as e:
                st.error(f"Configuration error: {e}")
            except Exception as e:
                st.error(f"Agent error: {e}")

# ── Conversation display ───────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("### Conversation")
    for turn in st.session_state.history:
        if turn["role"] == "user":
            with st.chat_message("user"):
                st.markdown(turn["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(turn["content"])
else:
    st.info("No conversation yet — type a message above and hit **Send**.")
