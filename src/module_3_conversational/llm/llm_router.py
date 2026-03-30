"""
LLM Router

Routes LLM requests through: Cache → Groq API → Fallback
Provides a single interface for all LLM operations in the chatbot.
"""

import logging
from typing import Optional

from src.module_3_conversational.llm.groq_client import GroqClient
from src.module_3_conversational.llm.cache_manager import CacheManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMRouter:
    """Routes LLM requests through cache → API → fallback."""

    def __init__(self):
        self.groq = GroqClient()
        self.cache = CacheManager(ttl=3600)
        self.fallback_responses = {
            "default": "I'm unable to process this request right now. Please try again later.",
            "sql_error": "I couldn't generate a valid SQL query for your question. Could you rephrase it?",
            "insight_error": "I have the data but couldn't generate insights at this time.",
        }

    def query(
        self,
        prompt: str,
        system_prompt: str = "",
        context: str = "",
        use_cache: bool = True,
        temperature: Optional[float] = None,
    ) -> dict:
        """
        Send a query through the routing pipeline.

        Returns:
            dict with keys: response, source (cache/api/fallback), tokens_used
        """
        # Layer 1: Cache
        if use_cache:
            cached = self.cache.get(prompt, context)
            if cached:
                return {"response": cached, "source": "cache", "tokens_used": 0}

        # Layer 2: Groq API
        if self.groq.is_available:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = self.groq.chat(messages, temperature=temperature)
            if response:
                if use_cache:
                    self.cache.set(prompt, response, context)
                return {
                    "response": response,
                    "source": "api",
                    "tokens_used": self.groq.total_tokens_used,
                }

        # Layer 3: Fallback
        fallback = self.fallback_responses.get(context, self.fallback_responses["default"])
        return {"response": fallback, "source": "fallback", "tokens_used": 0}

    def get_status(self) -> dict:
        return {
            "groq_available": self.groq.is_available,
            "groq_usage": self.groq.get_usage_stats(),
            "cache_stats": self.cache.stats(),
        }
