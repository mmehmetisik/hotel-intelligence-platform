"""
Hotel Analytics Chatbot — Main Orchestrator

Orchestrates the full conversational pipeline:
User Question → Intent Detection → SQL/Prediction → Data → Insight → Chart → Response
"""

import pandas as pd
import logging
from dataclasses import dataclass, field
from typing import Optional

from src.module_3_conversational.llm.llm_router import LLMRouter
from src.module_3_conversational.agents.intent_detector import IntentDetector
from src.module_3_conversational.agents.sql_generator import SQLGenerator
from src.module_3_conversational.agents.insight_generator import InsightGenerator
from src.module_3_conversational.agents.chart_generator import ChartGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ChatResponse:
    """Structured response from the chatbot."""
    question: str
    intent: str
    answer: str
    sql: Optional[str] = None
    data: Optional[pd.DataFrame] = None
    chart: Optional[object] = None
    chart_type: Optional[str] = None
    source: str = "unknown"
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)


class HotelAnalyticsChatbot:
    """Main chatbot orchestrator."""

    def __init__(self):
        self.router = LLMRouter()
        self.intent_detector = IntentDetector(self.router)
        self.sql_generator = SQLGenerator(self.router)
        self.insight_generator = InsightGenerator(self.router)
        self.chart_generator = ChartGenerator()
        self.conversation_history = []

        logger.info("Hotel Analytics Chatbot initialized")
        logger.info(f"  Groq API: {'Available' if self.router.groq.is_available else 'Unavailable'}")

    def ask(self, question: str) -> ChatResponse:
        """Process a user question and return a structured response."""
        logger.info(f"\nUser: {question}")

        # Step 1: Detect intent
        intent_result = self.intent_detector.detect(question)
        intent = intent_result["intent"]
        logger.info(f"  Intent: {intent} (source: {intent_result['source']})")

        # Step 2: Route based on intent
        if intent == "sql_query":
            response = self._handle_sql_query(question)
        elif intent == "prediction":
            response = self._handle_prediction(question)
        elif intent == "recommendation":
            response = self._handle_recommendation(question)
        elif intent == "summary":
            response = self._handle_summary(question)
        else:
            response = self._handle_general(question)

        response.intent = intent

        # Save to history
        self.conversation_history.append({
            "question": question,
            "intent": intent,
            "answer_preview": response.answer[:100] if response.answer else "",
        })

        return response

    def _handle_sql_query(self, question: str) -> ChatResponse:
        """Handle questions that require database queries."""
        # Generate and execute SQL
        query_result = self.sql_generator.query(question)

        if not query_result["success"]:
            return ChatResponse(
                question=question, intent="sql_query",
                answer=f"I couldn't retrieve the data. Error: {query_result.get('error', 'Unknown')}",
                sql=query_result.get("sql"),
                error=query_result.get("error"),
            )

        data = query_result["data"]
        sql = query_result["sql"]

        # Generate insight
        insight_result = self.insight_generator.generate(question, data, sql)

        # Generate chart
        chart_result = self.chart_generator.generate(data, question)

        return ChatResponse(
            question=question, intent="sql_query",
            answer=insight_result["insight"],
            sql=sql,
            data=data,
            chart=chart_result.get("chart"),
            chart_type=chart_result.get("type"),
            source=insight_result["source"],
            metadata={"row_count": len(data), "columns": data.columns.tolist()},
        )

    def _handle_prediction(self, question: str) -> ChatResponse:
        """Handle prediction/forecast questions."""
        insight = self.insight_generator.generate_summary(question)
        return ChatResponse(
            question=question, intent="prediction",
            answer=insight["insight"],
            source=insight["source"],
        )

    def _handle_recommendation(self, question: str) -> ChatResponse:
        """Handle recommendation questions."""
        insight = self.insight_generator.generate_summary(question)
        return ChatResponse(
            question=question, intent="recommendation",
            answer=insight["insight"],
            source=insight["source"],
        )

    def _handle_summary(self, question: str) -> ChatResponse:
        """Handle summary/overview questions."""
        # Try to get some data for context
        query_result = self.sql_generator.query(
            "Show total bookings, cancellation rate, average revenue, and average rating"
        )

        if query_result["success"]:
            insight = self.insight_generator.generate(question, query_result["data"], query_result["sql"])
        else:
            insight = self.insight_generator.generate_summary(question)

        return ChatResponse(
            question=question, intent="summary",
            answer=insight["insight"],
            data=query_result.get("data") if query_result["success"] else None,
            source=insight["source"],
        )

    def _handle_general(self, question: str) -> ChatResponse:
        """Handle general/explanation questions."""
        insight = self.insight_generator.generate_summary(question)
        return ChatResponse(
            question=question, intent="explanation",
            answer=insight["insight"],
            source=insight["source"],
        )

    def get_status(self) -> dict:
        """Get chatbot status."""
        return {
            **self.router.get_status(),
            "conversation_length": len(self.conversation_history),
        }
