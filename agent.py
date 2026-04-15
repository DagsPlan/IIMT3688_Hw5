"""
agent.py — Local AI agent module using DeepSeek via OpenAI-compatible API.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

SYSTEM_PROMPT = """You are a helpful AI assistant. Answer questions clearly and concisely.
If asked to summarize, do so in bullet points. If asked to explain code, walk through it step by step."""


def get_client() -> OpenAI:
    """Return an OpenAI client pointed at the DeepSeek API."""
    if not DEEPSEEK_API_KEY:
        raise ValueError(
            "DEEPSEEK_API_KEY is not set. "
            "Please add it to your .env file."
        )
    return OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)


def run_agent(
    query: str,
    model: str = "deepseek-chat",
    temperature: float = 0.7,
    max_tokens: int = 1024,
    history: list[dict] | None = None,
) -> str:
    """
    Send a query to the DeepSeek agent and return the response text.

    Args:
        query:       The user's input text.
        model:       DeepSeek model to use.
        temperature: Sampling temperature (0.0 – 1.5).
        max_tokens:  Maximum tokens in the response.
        history:     Optional prior conversation turns
                     (list of {"role": ..., "content": ...} dicts).

    Returns:
        The assistant's reply as a plain string.

    Raises:
        ValueError: If the API key is missing.
        Exception:  For any API-level errors.
    """
    client = get_client()

    messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content
