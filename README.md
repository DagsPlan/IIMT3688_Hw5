# DeepSeek AI Assistant — IIMT3688 HW5

## System Overview

**Problem:** Provide a simple, browser-based UI for querying a large-language-model agent without writing any frontend code.

**Workflow:**
1. User types a question in the Streamlit text area and clicks **Send**.
2. `app.py` validates the input, then calls `agent.run_agent()` with the query, model settings, and conversation history.
3. `agent.py` builds a message list (system prompt + history + new query) and sends it to the DeepSeek API via the OpenAI-compatible client.
4. The reply is appended to session-state history and rendered in a chat-message layout.

**Key components:**

| File | Role |
|---|---|
| `app.py` | Streamlit UI — layout, input, display |
| `agent.py` | Agent logic — API client, prompt assembly, error handling |
| `.env` | Secret storage (never committed) |
| `requirements.txt` | Python dependencies |

---

## How to Run

```bash
# 1. Clone and enter the repo
git clone <repo-url>
cd IIMT3688_Hw5

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API key to .env (already present if running locally)
#    DEEPSEEK_API_KEY=sk-...

# 4. Launch the app
streamlit run app.py
```

The app opens at `http://localhost:8501` in your browser.

---

## Features Implemented

- **Dashboard layout** — page title, sidebar config panel, wide main area
- **Sidebar controls** — model selector (deepseek-chat / deepseek-reasoner), temperature slider (0–1.5), max-tokens slider (128–4096), clear-conversation button
- **Input handling** — text area, submit button inside a form, whitespace-only validation with user warning
- **Agent integration** — full conversation history passed on every call; spinner during API call; success/error feedback via `st.success` / `st.error`
- **Chat history** — rendered with `st.chat_message` bubbles, persisted in `st.session_state` for the session lifetime
- **Secrets management** — API key loaded from `.env` via `python-dotenv`; `.env` excluded from git via `.gitignore`

---

## Design Decisions

- **OpenAI SDK against DeepSeek** — DeepSeek exposes an OpenAI-compatible REST API, so using the `openai` package avoids an extra dependency and keeps `agent.py` straightforward.
- **Session-state history** — storing the full conversation in `st.session_state` lets the agent maintain context across multiple turns without a database.
- **Form-based input** — `st.form` clears the text area after submission, preventing accidental duplicate sends.
- **Separation of concerns** — `agent.py` is UI-agnostic; `app.py` only handles display logic. This makes the agent reusable from scripts or tests.
