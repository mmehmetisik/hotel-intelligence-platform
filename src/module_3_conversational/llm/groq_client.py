"""
Groq API Client Wrapper

Provides a unified interface to Groq LLM with:
- Retry logic with exponential backoff
- Token usage tracking
- Error handling
"""

import os
import time
import logging
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GroqClient:
    """Wrapper around Groq API with retry and tracking."""

    def __init__(
        self,
        model: str = "llama-3.3-70b-versatile",
        temperature: float = 0.1,
        max_tokens: int = 1024,
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = None
        self.total_tokens_used = 0
        self.total_calls = 0
        self._init_client()

    def _init_client(self):
        """Initialize Groq client."""
        try:
            from groq import Groq
            api_key = os.getenv("GROQ_API_KEY", "")
            if api_key:
                self.client = Groq(api_key=api_key)
                logger.info("Groq client initialized successfully")
            else:
                logger.warning("GROQ_API_KEY not found in environment")
        except ImportError:
            logger.warning("groq package not installed")

    @property
    def is_available(self) -> bool:
        return self.client is not None

    def chat(
        self,
        messages: list[dict],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Optional[str]:
        """Send chat completion request with retry logic."""
        if not self.is_available:
            return None

        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens

        for attempt in range(3):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temp,
                    max_tokens=tokens,
                )

                result = response.choices[0].message.content.strip()
                self.total_tokens_used += response.usage.total_tokens
                self.total_calls += 1

                return result

            except Exception as e:
                error_str = str(e).lower()
                if "rate_limit" in error_str or "429" in error_str:
                    wait = min(2 ** attempt * 2, 30)
                    logger.warning(f"Rate limit hit. Retrying in {wait}s... (attempt {attempt+1}/3)")
                    time.sleep(wait)
                else:
                    logger.error(f"Groq API error: {e}")
                    return None

        logger.error("All retry attempts exhausted")
        return None

    def simple_query(self, prompt: str, system_prompt: str = "") -> Optional[str]:
        """Simple single-turn query."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return self.chat(messages)

    def get_usage_stats(self) -> dict:
        return {
            "total_calls": self.total_calls,
            "total_tokens": self.total_tokens_used,
            "available": self.is_available,
        }
