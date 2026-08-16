"""
utils/llm_router.py

Provides a single public function, get_match_score(resume_text, job_text), that
routes LLM calls to the appropriate backend:

  1. Groq  – used when GROQ_API_KEY is present in the environment.
  2. Ollama – used as a fallback when:
       - GROQ_API_KEY is not set, OR
       - the Groq API call fails or times out.

The scoring prompt and the integer score returned (0-100) are identical
regardless of which backend handles the request, so downstream CSV output
format stays unchanged.
"""

import os
import re
import logging

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Shared prompt builder
# ---------------------------------------------------------------------------

def _build_prompt(resume_text: str, job_text: str) -> str:
    """Return the scoring prompt used by both Groq and Ollama backends."""
    return f"""You are a strict AI evaluator.

Given a job and a resume, respond with a SINGLE number from 0 to 100 that represents the match score.

DO NOT respond with explanation, just the number.

Job: {job_text[:200]}

Resume: {resume_text[:200]}

Score:"""


def _parse_score(text: str) -> int:
    """Extract the first integer 0-100 from the model response, or return 0."""
    if not text:
        return 0
    match = re.search(r"\b(\d{1,3})\b", text)
    if match:
        score = int(match.group(1))
        if 0 <= score <= 100:
            return score
    return 0


# ---------------------------------------------------------------------------
# Groq backend
# ---------------------------------------------------------------------------

def _call_groq(prompt: str) -> str | None:
    """
    Send *prompt* to the Groq API and return the raw text response.

    Returns None on any error so the caller can fall back to Ollama.
    """
    try:
        from groq import Groq  # imported lazily so Ollama-only usage doesn't require groq

        groq_model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        client = Groq(api_key=os.environ["GROQ_API_KEY"])

        logger.info("Sending prompt to Groq (%s)…", groq_model)
        print(f"\n⚡ Sending prompt to Groq ({groq_model})...")

        completion = client.chat.completions.create(
            model=groq_model,
            messages=[{"role": "user", "content": prompt}],
            timeout=30,
        )
        return completion.choices[0].message.content.strip()

    except KeyError:
        # GROQ_API_KEY missing from environment – should not reach here normally
        logger.warning("GROQ_API_KEY not found in environment; falling back to Ollama.")
        return None
    except Exception as exc:
        logger.warning("Groq API call failed (%s); falling back to Ollama.", exc)
        print(f"⚠️  Groq request failed ({exc}); falling back to Ollama.")
        return None


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def get_match_score(resume_text: str, job_text: str) -> int:
    """
    Return an integer match score (0-100) for the given resume / job pair.

    Routing logic:
      - If GROQ_API_KEY is set  → try Groq first; fall back to Ollama on failure.
      - If GROQ_API_KEY is unset → go directly to Ollama.
    """
    prompt = _build_prompt(resume_text, job_text)
    raw_response: str | None = None
    backend_used: str = "ollama"

    if os.getenv("GROQ_API_KEY"):
        raw_response = _call_groq(prompt)
        if raw_response is not None:
            backend_used = "groq"

    if raw_response is None:
        # Ollama path (primary when no key, fallback when Groq fails)
        from utils.ollama_utils import query_ollama  # noqa: PLC0415

        raw_response = query_ollama(prompt)
        backend_used = "ollama"

    print(f"\n🧠 {backend_used.capitalize()} response:\n{raw_response}\n")

    if raw_response and (
        "sorry" in raw_response.lower() or "not able" in raw_response.lower()
    ):
        print("⚠️  Skipping irrelevant response.")
        return 0

    score = _parse_score(raw_response)
    print(f"🎯 Parsed Score: {score}")
    return score
