# Prompt Log — IIMT3688 HW5

This file records the full AI-assisted development process for the Streamlit dashboard assignment.

---

## Session 1 — Project Setup & File Generation

**Date:** 2026-04-15  
**Tool:** Claude Code (claude-sonnet-4-6) via VSCode extension

---

### Turn 1

**User prompt:**
> Objective: Create a simple Streamlit dashboard that provides a user interface for interacting with an AI agent.
> [full assignment spec pasted]
> In the next prompt I will give you my deepseek api key which you can put in the .env file

**Assistant response:**
> Understood. I'll wait for your DeepSeek API key in the next message, then I'll build all the required files:
> - app.py — Streamlit dashboard
> - agent.py — Local agent module using DeepSeek
> - requirements.txt — Dependencies
> - .env — API key (with .gitignore entry)
> - README.md — Documentation
> - prompt-log.md — AI-assisted development log
>
> Go ahead and share the key when ready.

---

### Turn 2

**User prompt:**
> [assignment spec repeated]
> sorry here you go
> API KEY

**Assistant actions:**
1. Checked the project directory — confirmed it was empty (only `.git` present).
2. Created `agent.py` with:
   - `load_dotenv()` to pull the API key from `.env`
   - `get_client()` returning an `openai.OpenAI` instance pointed at `https://api.deepseek.com`
   - `run_agent(query, model, temperature, max_tokens, history)` that assembles a message list (system prompt + conversation history + new user query) and calls `client.chat.completions.create`
   - `ValueError` raised if `DEEPSEEK_API_KEY` is not set
3. Created `app.py` (~130 lines) with:
   - `st.set_page_config` for title, icon, wide layout
   - Session-state initialisation for `history` and `last_response`
   - Sidebar: model selectbox, temperature slider, max-tokens slider, clear-conversation button
   - Main area: title, description, `st.form` with text area and submit button
   - Input validation (whitespace-only check with `st.warning`)
   - `st.spinner` wrapping the `run_agent` call
   - `st.success` / `st.error` feedback
   - Conversation rendered with `st.chat_message` bubbles
4. Created `requirements.txt` with `streamlit`, `openai`, `python-dotenv`.
5. Created `.env` with the provided API key.
6. Created `.gitignore` excluding `.env`, `__pycache__`, `.venv`, `.DS_Store`.
7. Created `README.md` with system overview, run instructions, features, and design decisions.
8. Created this `prompt-log.md`.

**Key design decisions made by the assistant:**
- Use the `openai` SDK (not `requests`) because DeepSeek exposes an OpenAI-compatible API — fewer dependencies, cleaner code.
- Store conversation history in `st.session_state` so the agent maintains context across turns without any database.
- Use `st.form` so the text area clears automatically after submission, preventing duplicate sends.
- Keep `agent.py` UI-agnostic so it can be tested or reused independently of Streamlit.
- Noted that the API key was shared in plain text in the chat and advised the user to regenerate it after submission.

---

## Notes on AI Assistance

All six deliverable files were generated in a single assistant turn after the assignment brief and API key were provided. The assistant:

- Interpreted the rubric requirements (layout 30%, input 30%, agent integration 30%, UX 10%) and mapped them to specific Streamlit components and patterns.
- Proactively added `.gitignore` and session-state conversation history, which were not explicitly required but are standard best practices.
- Flagged the credential-exposure risk of sharing the API key in chat.

No manual edits were required beyond what the assistant produced.
