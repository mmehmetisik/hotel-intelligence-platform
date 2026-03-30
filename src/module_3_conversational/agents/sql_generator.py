"""
SQL Generator Agent

Converts natural language questions to SQL queries using LLM.
Schema-aware prompting ensures valid queries against our database.
"""

import sqlite3
import pandas as pd
import logging
from typing import Optional

from src.module_3_conversational.llm.llm_router import LLMRouter
from src.module_3_conversational.database.init_db import get_connection, get_schema_description

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a SQL expert for a hotel analytics database (SQLite).

{schema}

RULES:
1. Write valid SQLite SQL only
2. Use proper table and column names from the schema above
3. Always use single quotes for string literals
4. Use strftime() for date operations in SQLite
5. Limit results to 50 rows unless the user asks for more
6. Use aliases for readability
7. Return ONLY the SQL query, no explanation, no markdown code blocks
8. For percentage calculations, multiply by 100.0
9. Round numeric results to 2 decimal places
10. Handle NULLs appropriately"""


class SQLGenerator:
    """Generates SQL from natural language questions."""

    def __init__(self, router: LLMRouter = None):
        self.router = router or LLMRouter()
        self.schema = get_schema_description()

    def generate_sql(self, question: str) -> dict:
        """Generate SQL query from natural language question."""
        prompt = f'Convert this question to a SQL query:\n\n"{question}"'
        system = SYSTEM_PROMPT.format(schema=self.schema)

        result = self.router.query(
            prompt=prompt,
            system_prompt=system,
            context="sql_generation",
            temperature=0.0,
        )

        sql = self._clean_sql(result["response"])

        return {
            "sql": sql,
            "source": result["source"],
            "valid": self._validate_sql(sql),
        }

    def _clean_sql(self, response: str) -> str:
        """Clean LLM response to extract pure SQL."""
        sql = response.strip()

        # Remove markdown code blocks
        if sql.startswith("```"):
            lines = sql.split("\n")
            sql = "\n".join(
                line for line in lines
                if not line.startswith("```")
            ).strip()

        # Remove leading 'sql' label
        if sql.lower().startswith("sql\n"):
            sql = sql[4:].strip()
        if sql.lower().startswith("sql "):
            sql = sql[4:].strip()

        # Ensure it ends with semicolon
        if sql and not sql.rstrip().endswith(";"):
            sql = sql.rstrip() + ";"

        return sql

    def _validate_sql(self, sql: str) -> bool:
        """Basic SQL validation."""
        if not sql or len(sql) < 10:
            return False

        sql_upper = sql.upper().strip()

        # Must start with SELECT
        if not sql_upper.startswith("SELECT"):
            return False

        # Must not contain dangerous operations
        dangerous = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "CREATE", "TRUNCATE"]
        for word in dangerous:
            if word in sql_upper.split():
                return False

        return True

    def execute_sql(self, sql: str) -> dict:
        """Execute SQL and return results."""
        if not self._validate_sql(sql):
            return {"success": False, "error": "Invalid or unsafe SQL query", "data": None}

        try:
            conn = get_connection()
            df = pd.read_sql_query(sql.rstrip(";"), conn)
            conn.close()

            return {
                "success": True,
                "data": df,
                "row_count": len(df),
                "columns": df.columns.tolist(),
            }
        except Exception as e:
            logger.error(f"SQL execution error: {e}")
            return {"success": False, "error": str(e), "data": None}

    def query(self, question: str) -> dict:
        """Full pipeline: question → SQL → execute → results."""
        # Generate SQL
        sql_result = self.generate_sql(question)

        if not sql_result["valid"]:
            return {
                "success": False,
                "sql": sql_result["sql"],
                "error": "Generated SQL was invalid",
                "data": None,
            }

        # Execute
        exec_result = self.execute_sql(sql_result["sql"])

        return {
            "success": exec_result["success"],
            "sql": sql_result["sql"],
            "data": exec_result.get("data"),
            "row_count": exec_result.get("row_count", 0),
            "columns": exec_result.get("columns", []),
            "error": exec_result.get("error"),
            "source": sql_result["source"],
        }
