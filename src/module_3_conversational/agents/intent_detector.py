"""
Intent Detector Agent

Classifies user questions into intents to determine the right
processing pipeline (SQL query, prediction, or summary).
"""

import logging
from src.module_3_conversational.llm.llm_router import LLMRouter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INTENT_CATEGORIES = {
    "sql_query": "Question that can be answered by querying the database (counts, averages, trends, comparisons, top-N)",
    "prediction": "Question asking for a future prediction or forecast (predict, forecast, will, likely)",
    "recommendation": "Question asking for advice or recommendations (should, suggest, improve, recommend)",
    "summary": "Question asking for an overview or executive summary",
    "explanation": "Question asking to explain a concept, metric, or methodology",
}

SYSTEM_PROMPT = """You are an intent classifier for a hotel analytics chatbot.

Classify the user's question into exactly ONE of these intents:
- sql_query: Can be answered by querying a database (metrics, counts, trends, comparisons, lists)
- prediction: Asks about the future or predictions (forecast, predict, risk, likely)
- recommendation: Asks for advice or suggestions (should, improve, recommend, suggest)
- summary: Asks for an overview or executive summary
- explanation: Asks to explain a concept or methodology

Respond with ONLY the intent name, nothing else."""


class IntentDetector:
    """Detects user intent from natural language questions."""

    def __init__(self, router: LLMRouter = None):
        self.router = router or LLMRouter()

    def detect(self, question: str) -> dict:
        """Detect intent of a user question."""
        result = self.router.query(
            prompt=f'Classify this question: "{question}"',
            system_prompt=SYSTEM_PROMPT,
            context="intent_detection",
        )

        intent = result["response"].strip().lower().replace(" ", "_")

        # Validate
        if intent not in INTENT_CATEGORIES:
            intent = self._rule_based_fallback(question)

        return {
            "intent": intent,
            "description": INTENT_CATEGORIES.get(intent, ""),
            "source": result["source"],
        }

    def _rule_based_fallback(self, question: str) -> str:
        """Rule-based fallback for intent detection."""
        q = question.lower()

        prediction_words = ["predict", "forecast", "will", "likely", "risk", "expect", "future"]
        recommendation_words = ["should", "suggest", "recommend", "improve", "advice", "strategy"]
        summary_words = ["summary", "overview", "executive", "kpi", "dashboard", "highlight"]
        explanation_words = ["explain", "what is", "how does", "why", "define", "meaning"]

        if any(w in q for w in prediction_words):
            return "prediction"
        if any(w in q for w in recommendation_words):
            return "recommendation"
        if any(w in q for w in summary_words):
            return "summary"
        if any(w in q for w in explanation_words):
            return "explanation"

        return "sql_query"
