"""
Insight Generator Agent

Takes SQL query results and generates natural language insights
with business context and actionable recommendations.
"""

import pandas as pd
import logging
from typing import Optional

from src.module_3_conversational.llm.llm_router import LLMRouter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a senior hotel analytics consultant. Given data results from a database query, provide:

1. A clear, concise answer to the original question
2. Key insights from the data (trends, anomalies, notable patterns)
3. Business context (what this means for the hotel)
4. One actionable recommendation

Keep your response under 200 words. Use specific numbers from the data.
Format currency as EUR. Use bullet points for clarity."""


class InsightGenerator:
    """Generates natural language insights from query results."""

    def __init__(self, router: LLMRouter = None):
        self.router = router or LLMRouter()

    def generate(self, question: str, data: pd.DataFrame, sql: str = "") -> dict:
        """Generate insight from query results."""
        # Prepare data summary for LLM
        data_summary = self._summarize_data(data)

        prompt = f"""Original question: "{question}"

SQL query used: {sql}

Data results:
{data_summary}

Provide a clear analytical response with insights and a recommendation."""

        result = self.router.query(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT,
            context="insight_generation",
            temperature=0.3,
        )

        return {
            "insight": result["response"],
            "source": result["source"],
        }

    def _summarize_data(self, data: pd.DataFrame, max_rows: int = 20) -> str:
        """Create a text summary of the dataframe for LLM context."""
        if data is None or data.empty:
            return "No data returned."

        summary_parts = []

        # Shape
        summary_parts.append(f"Shape: {data.shape[0]} rows x {data.shape[1]} columns")
        summary_parts.append(f"Columns: {', '.join(data.columns)}")

        # Show data (truncated)
        if len(data) <= max_rows:
            summary_parts.append(f"\nFull data:\n{data.to_string(index=False)}")
        else:
            summary_parts.append(f"\nFirst {max_rows} rows:\n{data.head(max_rows).to_string(index=False)}")
            summary_parts.append(f"... ({len(data) - max_rows} more rows)")

        # Numeric stats
        numeric_cols = data.select_dtypes(include="number").columns
        if len(numeric_cols) > 0:
            summary_parts.append(f"\nNumeric summary:")
            for col in numeric_cols[:5]:
                summary_parts.append(
                    f"  {col}: min={data[col].min():.2f}, max={data[col].max():.2f}, "
                    f"mean={data[col].mean():.2f}"
                )

        return "\n".join(summary_parts)

    def generate_summary(self, question: str) -> dict:
        """Generate a summary response without SQL data (for prediction/recommendation intents)."""
        prompt = f"""The user asked: "{question}"

As a hotel analytics expert, provide a thoughtful response based on general hotel industry knowledge and best practices.
Include specific, actionable advice. Keep it under 200 words."""

        result = self.router.query(
            prompt=prompt,
            system_prompt="You are a senior hotel analytics consultant with 15 years of experience in hospitality data science.",
            context="general_insight",
            temperature=0.4,
        )

        return {
            "insight": result["response"],
            "source": result["source"],
        }
