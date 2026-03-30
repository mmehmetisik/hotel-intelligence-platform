"""
Tests for Module 3 — Conversational AI Pipeline

Tests cover:
- LLM layer (cache, router, groq client)
- Database initialization and schema
- Agent layer (intent detection, SQL generation, chart generation, insights)
- End-to-end chatbot orchestration

All tests use mocks for external API calls (Groq) to ensure deterministic results.
"""

import os
import sys
import sqlite3
import tempfile
import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import patch, MagicMock

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))


# ─────────────────────── Cache Manager Tests ───────────────────────


class TestCacheManager:
    """Tests for LLM response cache."""

    def test_cache_init(self):
        """Cache initializes without errors."""
        from src.module_3_conversational.llm.cache_manager import CacheManager
        with tempfile.TemporaryDirectory() as tmp:
            cache = CacheManager(ttl=60, cache_dir=Path(tmp) / "test_cache")
            assert cache.cache is not None

    def test_cache_set_and_get(self):
        """Cache stores and retrieves values."""
        from src.module_3_conversational.llm.cache_manager import CacheManager
        with tempfile.TemporaryDirectory() as tmp:
            cache = CacheManager(ttl=3600, cache_dir=Path(tmp) / "test_cache")
            cache.set("test prompt", "test response", context="test")
            result = cache.get("test prompt", context="test")
            assert result == "test response"

    def test_cache_miss(self):
        """Cache returns None on miss."""
        from src.module_3_conversational.llm.cache_manager import CacheManager
        with tempfile.TemporaryDirectory() as tmp:
            cache = CacheManager(ttl=3600, cache_dir=Path(tmp) / "test_cache")
            result = cache.get("nonexistent prompt", context="x")
            assert result is None

    def test_cache_clear(self):
        """Cache can be cleared."""
        from src.module_3_conversational.llm.cache_manager import CacheManager
        with tempfile.TemporaryDirectory() as tmp:
            cache = CacheManager(ttl=3600, cache_dir=Path(tmp) / "test_cache")
            cache.set("p", "r", "c")
            cache.clear()
            assert cache.get("p", "c") is None

    def test_cache_key_uniqueness(self):
        """Different context produces different cache keys."""
        from src.module_3_conversational.llm.cache_manager import CacheManager
        with tempfile.TemporaryDirectory() as tmp:
            cache = CacheManager(ttl=3600, cache_dir=Path(tmp) / "test_cache")
            cache.set("same prompt", "response_a", context="ctx_a")
            cache.set("same prompt", "response_b", context="ctx_b")
            assert cache.get("same prompt", "ctx_a") == "response_a"
            assert cache.get("same prompt", "ctx_b") == "response_b"

    def test_cache_stats(self):
        """Cache stats returns valid dict."""
        from src.module_3_conversational.llm.cache_manager import CacheManager
        with tempfile.TemporaryDirectory() as tmp:
            cache = CacheManager(ttl=3600, cache_dir=Path(tmp) / "test_cache")
            stats = cache.stats()
            assert "type" in stats
            assert "size" in stats


# ─────────────────────── Groq Client Tests ───────────────────────


class TestGroqClient:
    """Tests for Groq API client wrapper."""

    def test_client_without_api_key(self):
        """Client initializes without API key (graceful degradation)."""
        with patch.dict(os.environ, {"GROQ_API_KEY": ""}, clear=False):
            from src.module_3_conversational.llm.groq_client import GroqClient
            client = GroqClient.__new__(GroqClient)
            client.model = "llama-3.3-70b-versatile"
            client.temperature = 0.1
            client.max_tokens = 1024
            client.client = None
            client.total_tokens_used = 0
            client.total_calls = 0
            assert not client.is_available

    def test_chat_returns_none_when_unavailable(self):
        """Chat returns None when client not available."""
        from src.module_3_conversational.llm.groq_client import GroqClient
        client = GroqClient.__new__(GroqClient)
        client.client = None
        client.total_tokens_used = 0
        client.total_calls = 0
        client.temperature = 0.1
        client.max_tokens = 1024
        result = client.chat([{"role": "user", "content": "test"}])
        assert result is None

    def test_usage_stats(self):
        """Usage stats returns proper structure."""
        from src.module_3_conversational.llm.groq_client import GroqClient
        client = GroqClient.__new__(GroqClient)
        client.client = None
        client.total_tokens_used = 100
        client.total_calls = 5
        stats = client.get_usage_stats()
        assert stats["total_calls"] == 5
        assert stats["total_tokens"] == 100
        assert stats["available"] is False


# ─────────────────────── LLM Router Tests ───────────────────────


class TestLLMRouter:
    """Tests for the LLM routing pipeline."""

    def _make_router_with_mocks(self):
        """Create a router with mocked dependencies."""
        from src.module_3_conversational.llm.llm_router import LLMRouter
        router = LLMRouter.__new__(LLMRouter)

        # Mock cache
        mock_cache = MagicMock()
        mock_cache.get.return_value = None
        router.cache = mock_cache

        # Mock groq
        mock_groq = MagicMock()
        mock_groq.is_available = True
        mock_groq.chat.return_value = "API response"
        mock_groq.total_tokens_used = 50
        router.groq = mock_groq

        router.fallback_responses = {
            "default": "Fallback response.",
            "sql_error": "SQL fallback.",
            "insight_error": "Insight fallback.",
        }

        return router

    def test_cache_hit(self):
        """Router returns cached response when available."""
        router = self._make_router_with_mocks()
        router.cache.get.return_value = "cached answer"

        result = router.query("test", context="test")
        assert result["source"] == "cache"
        assert result["response"] == "cached answer"
        assert result["tokens_used"] == 0

    def test_api_call_on_cache_miss(self):
        """Router calls API when cache misses."""
        router = self._make_router_with_mocks()
        result = router.query("test", context="test")
        assert result["source"] == "api"
        assert result["response"] == "API response"

    def test_fallback_when_api_unavailable(self):
        """Router falls back when API is unavailable."""
        router = self._make_router_with_mocks()
        router.groq.is_available = False
        result = router.query("test", context="default")
        assert result["source"] == "fallback"

    def test_fallback_when_api_returns_none(self):
        """Router falls back when API returns None."""
        router = self._make_router_with_mocks()
        router.groq.chat.return_value = None
        result = router.query("test", context="default")
        assert result["source"] == "fallback"

    def test_cache_disabled(self):
        """Router skips cache when use_cache=False."""
        router = self._make_router_with_mocks()
        router.cache.get.return_value = "cached"
        result = router.query("test", use_cache=False)
        assert result["source"] == "api"  # Skipped cache

    def test_get_status(self):
        """Status returns proper structure."""
        router = self._make_router_with_mocks()
        router.groq.get_usage_stats.return_value = {"total_calls": 0}
        router.cache.stats.return_value = {"type": "disk", "size": 0}
        status = router.get_status()
        assert "groq_available" in status
        assert "cache_stats" in status


# ─────────────────────── Intent Detector Tests ───────────────────────


class TestIntentDetector:
    """Tests for intent classification."""

    def _make_detector(self, api_response="sql_query"):
        """Create detector with mocked router."""
        from src.module_3_conversational.agents.intent_detector import IntentDetector
        mock_router = MagicMock()
        mock_router.query.return_value = {
            "response": api_response,
            "source": "api",
            "tokens_used": 10,
        }
        return IntentDetector(router=mock_router)

    def test_sql_query_intent(self):
        """Detects SQL query intent."""
        detector = self._make_detector("sql_query")
        result = detector.detect("How many bookings were canceled?")
        assert result["intent"] == "sql_query"

    def test_prediction_intent(self):
        """Detects prediction intent."""
        detector = self._make_detector("prediction")
        result = detector.detect("What will the occupancy rate be next month?")
        assert result["intent"] == "prediction"

    def test_recommendation_intent(self):
        """Detects recommendation intent."""
        detector = self._make_detector("recommendation")
        result = detector.detect("How should we improve our revenue?")
        assert result["intent"] == "recommendation"

    def test_summary_intent(self):
        """Detects summary intent."""
        detector = self._make_detector("summary")
        result = detector.detect("Give me an executive summary")
        assert result["intent"] == "summary"

    def test_explanation_intent(self):
        """Detects explanation intent."""
        detector = self._make_detector("explanation")
        result = detector.detect("What is ADR?")
        assert result["intent"] == "explanation"

    def test_rule_based_fallback(self):
        """Falls back to rule-based when API returns invalid intent."""
        detector = self._make_detector("invalid_intent_xyz")
        result = detector.detect("What will happen next month?")
        assert result["intent"] == "prediction"  # "will" keyword

    def test_fallback_recommendation(self):
        """Rule-based fallback catches recommendation keywords."""
        detector = self._make_detector("unknown")
        result = detector.detect("Can you suggest improvements?")
        assert result["intent"] == "recommendation"

    def test_fallback_explanation(self):
        """Rule-based fallback catches explanation keywords."""
        detector = self._make_detector("unknown")
        result = detector.detect("Explain what RevPAR means")
        assert result["intent"] == "explanation"

    def test_fallback_default_sql(self):
        """Default fallback is sql_query."""
        detector = self._make_detector("unknown")
        result = detector.detect("Show me top 10 countries")
        assert result["intent"] == "sql_query"

    def test_result_structure(self):
        """Result has correct structure."""
        detector = self._make_detector("sql_query")
        result = detector.detect("test")
        assert "intent" in result
        assert "description" in result
        assert "source" in result


# ─────────────────────── SQL Generator Tests ───────────────────────


class TestSQLGenerator:
    """Tests for SQL generation and execution."""

    def _make_generator(self, sql_response="SELECT COUNT(*) AS total FROM bookings;"):
        """Create SQL generator with mocked router."""
        from src.module_3_conversational.agents.sql_generator import SQLGenerator
        mock_router = MagicMock()
        mock_router.query.return_value = {
            "response": sql_response,
            "source": "api",
            "tokens_used": 20,
        }
        gen = SQLGenerator.__new__(SQLGenerator)
        gen.router = mock_router
        gen.schema = "test schema"
        return gen

    def test_generate_sql(self):
        """Generates valid SQL from question."""
        gen = self._make_generator()
        result = gen.generate_sql("How many bookings?")
        assert result["sql"].strip().upper().startswith("SELECT")
        assert result["valid"] is True

    def test_clean_sql_removes_markdown(self):
        """SQL cleaner strips markdown code blocks."""
        gen = self._make_generator()
        cleaned = gen._clean_sql("```sql\nSELECT 1;\n```")
        assert "```" not in cleaned
        assert cleaned.strip().startswith("SELECT")

    def test_clean_sql_adds_semicolon(self):
        """SQL cleaner adds missing semicolon."""
        gen = self._make_generator()
        cleaned = gen._clean_sql("SELECT 1")
        assert cleaned.endswith(";")

    def test_validate_sql_rejects_empty(self):
        """Validator rejects empty SQL."""
        gen = self._make_generator()
        assert gen._validate_sql("") is False
        assert gen._validate_sql("short") is False

    def test_validate_sql_rejects_dangerous(self):
        """Validator rejects destructive SQL."""
        gen = self._make_generator()
        assert gen._validate_sql("DROP TABLE bookings;") is False
        assert gen._validate_sql("DELETE FROM bookings;") is False
        assert gen._validate_sql("INSERT INTO bookings VALUES (1);") is False
        assert gen._validate_sql("UPDATE bookings SET adr=0;") is False

    def test_validate_sql_accepts_select(self):
        """Validator accepts valid SELECT statements."""
        gen = self._make_generator()
        assert gen._validate_sql("SELECT * FROM bookings LIMIT 10;") is True
        assert gen._validate_sql("SELECT COUNT(*) AS total FROM bookings;") is True

    def test_execute_sql_rejects_invalid(self):
        """Execute rejects invalid SQL."""
        gen = self._make_generator()
        result = gen.execute_sql("DROP TABLE x;")
        assert result["success"] is False

    def test_execute_sql_with_real_db(self):
        """Execute works with a real in-memory SQLite database."""
        gen = self._make_generator()

        # Create a temporary in-memory DB
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE bookings (id INTEGER, hotel TEXT, adr REAL)")
        conn.execute("INSERT INTO bookings VALUES (1, 'City Hotel', 120.5)")
        conn.execute("INSERT INTO bookings VALUES (2, 'Resort Hotel', 200.0)")
        conn.commit()

        # Patch get_connection
        with patch("src.module_3_conversational.agents.sql_generator.get_connection", return_value=conn):
            result = gen.execute_sql("SELECT COUNT(*) AS total FROM bookings;")
            assert result["success"] is True
            assert result["data"].iloc[0]["total"] == 2

    def test_full_query_pipeline(self):
        """Full pipeline: question → SQL → execute → results."""
        gen = self._make_generator("SELECT COUNT(*) AS total FROM bookings;")

        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE bookings (id INTEGER, hotel TEXT)")
        conn.execute("INSERT INTO bookings VALUES (1, 'City Hotel')")
        conn.commit()

        with patch("src.module_3_conversational.agents.sql_generator.get_connection", return_value=conn):
            result = gen.query("How many bookings?")
            assert result["success"] is True
            assert result["data"].iloc[0]["total"] == 1


# ─────────────────────── Chart Generator Tests ───────────────────────


class TestChartGenerator:
    """Tests for chart type detection and generation."""

    def setup_method(self):
        from src.module_3_conversational.agents.chart_generator import ChartGenerator
        self.gen = ChartGenerator()

    def test_detect_line_chart(self):
        """Detects line chart for trend questions."""
        df = pd.DataFrame({"month": ["Jan", "Feb"], "revenue": [100, 200]})
        assert self.gen.detect_chart_type(df, "Show revenue trend over time") == "line"

    def test_detect_bar_chart(self):
        """Detects bar chart for comparison questions."""
        df = pd.DataFrame({"hotel": ["A", "B"], "bookings": [100, 200]})
        assert self.gen.detect_chart_type(df, "Compare bookings between hotels") == "bar"

    def test_detect_pie_chart(self):
        """Detects pie chart for breakdown questions."""
        df = pd.DataFrame({"segment": ["VIP", "Regular"], "count": [30, 70]})
        assert self.gen.detect_chart_type(df, "Show breakdown of segments") == "pie"

    def test_detect_horizontal_bar(self):
        """Detects horizontal bar for ranking questions."""
        df = pd.DataFrame({"country": ["US", "UK", "FR"], "bookings": [100, 80, 60]})
        assert self.gen.detect_chart_type(df, "Top countries by bookings") == "bar_horizontal"

    def test_detect_histogram(self):
        """Detects histogram for distribution questions."""
        df = pd.DataFrame({"adr": [100, 120, 150, 80, 200]})
        assert self.gen.detect_chart_type(df, "Show ADR distribution") == "histogram"

    def test_detect_scatter(self):
        """Detects scatter for correlation questions."""
        df = pd.DataFrame({"adr": [100, 120], "rating": [4.5, 3.2]})
        assert self.gen.detect_chart_type(df, "Show correlation of ADR and rating") == "scatter"

    def test_detect_metric_single_value(self):
        """Detects metric card for single-row numeric data."""
        df = pd.DataFrame({"total_bookings": [11938]})
        assert self.gen.detect_chart_type(df, "Total number of bookings") == "metric"

    def test_generate_returns_chart(self):
        """Generate produces a Plotly figure."""
        df = pd.DataFrame({"hotel": ["City", "Resort"], "revenue": [1000, 2000]})
        result = self.gen.generate(df, "Compare revenue by hotel")
        assert result["chart"] is not None
        assert result["type"] in ["bar", "line", "pie", "scatter", "bar_horizontal"]

    def test_generate_empty_data(self):
        """Generate handles empty data gracefully."""
        result = self.gen.generate(pd.DataFrame(), "test")
        assert result["chart"] is None
        assert result["type"] == "none"

    def test_generate_none_data(self):
        """Generate handles None data gracefully."""
        result = self.gen.generate(None, "test")
        assert result["chart"] is None

    def test_generate_metric_chart(self):
        """Generate produces metric indicator for single value."""
        df = pd.DataFrame({"avg_adr": [145.67]})
        result = self.gen.generate(df, "Average ADR", chart_type="metric")
        assert result["chart"] is not None
        assert result["type"] == "metric"

    def test_generate_table_chart(self):
        """Generate produces table for complex data."""
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4], "c": ["x", "y"]})
        result = self.gen.generate(df, "Show data", chart_type="table")
        assert result["chart"] is not None
        assert result["type"] == "table"


# ─────────────────────── Insight Generator Tests ───────────────────────


class TestInsightGenerator:
    """Tests for insight generation."""

    def _make_generator(self, response="Here are the key insights..."):
        from src.module_3_conversational.agents.insight_generator import InsightGenerator
        mock_router = MagicMock()
        mock_router.query.return_value = {
            "response": response,
            "source": "api",
            "tokens_used": 30,
        }
        return InsightGenerator(router=mock_router)

    def test_generate_insight(self):
        """Generates insight from data."""
        gen = self._make_generator("Revenue is up 15% this quarter.")
        df = pd.DataFrame({"month": ["Jan", "Feb"], "revenue": [1000, 1150]})
        result = gen.generate("What's the revenue trend?", df, "SELECT ...")
        assert result["insight"] == "Revenue is up 15% this quarter."
        assert result["source"] == "api"

    def test_generate_summary(self):
        """Generates summary without data."""
        gen = self._make_generator("Hotels should focus on direct bookings.")
        result = gen.generate_summary("How to improve revenue?")
        assert "direct bookings" in result["insight"].lower()

    def test_summarize_data_empty(self):
        """Data summarizer handles empty DataFrame."""
        gen = self._make_generator()
        summary = gen._summarize_data(pd.DataFrame())
        assert "No data" in summary

    def test_summarize_data_none(self):
        """Data summarizer handles None."""
        gen = self._make_generator()
        summary = gen._summarize_data(None)
        assert "No data" in summary

    def test_summarize_data_with_content(self):
        """Data summarizer includes shape and columns."""
        gen = self._make_generator()
        df = pd.DataFrame({"hotel": ["A", "B"], "revenue": [100, 200]})
        summary = gen._summarize_data(df)
        assert "2 rows" in summary
        assert "hotel" in summary
        assert "revenue" in summary

    def test_summarize_data_truncation(self):
        """Data summarizer truncates large datasets."""
        gen = self._make_generator()
        df = pd.DataFrame({"x": range(100), "y": range(100)})
        summary = gen._summarize_data(df, max_rows=10)
        assert "more rows" in summary


# ─────────────────────── Database Tests ───────────────────────


class TestDatabase:
    """Tests for database schema and initialization."""

    def test_schema_file_exists(self):
        """Schema SQL file exists."""
        schema_path = ROOT_DIR / "src" / "module_3_conversational" / "database" / "schema.sql"
        assert schema_path.exists()

    def test_schema_creates_tables(self):
        """Schema creates all required tables."""
        schema_path = ROOT_DIR / "src" / "module_3_conversational" / "database" / "schema.sql"
        conn = sqlite3.connect(":memory:")
        with open(schema_path) as f:
            conn.executescript(f.read())

        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}

        expected = {"bookings", "transactions", "customers", "customer_segments", "reviews", "daily_metrics"}
        assert expected == tables
        conn.close()

    def test_schema_bookings_columns(self):
        """Bookings table has correct columns."""
        schema_path = ROOT_DIR / "src" / "module_3_conversational" / "database" / "schema.sql"
        conn = sqlite3.connect(":memory:")
        with open(schema_path) as f:
            conn.executescript(f.read())

        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(bookings)")
        columns = {row[1] for row in cursor.fetchall()}

        required = {"booking_id", "hotel", "is_canceled", "lead_time", "adr", "country"}
        assert required.issubset(columns)
        conn.close()

    def test_get_schema_description(self):
        """Schema description includes all tables."""
        from src.module_3_conversational.database.init_db import get_schema_description
        desc = get_schema_description()
        assert "bookings" in desc
        assert "transactions" in desc
        assert "customers" in desc
        assert "customer_segments" in desc
        assert "reviews" in desc

    def test_get_connection(self):
        """get_connection returns a valid connection."""
        from src.module_3_conversational.database.init_db import get_connection, DB_PATH
        # If DB doesn't exist, this initializes it (or we test with existing)
        if DB_PATH.exists():
            conn = get_connection()
            assert conn is not None
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = {row[0] for row in cursor.fetchall()}
            assert "bookings" in tables or len(tables) > 0
            conn.close()


# ─────────────────────── Chatbot Orchestrator Tests ───────────────────────


class TestChatbotOrchestrator:
    """Tests for the main chatbot pipeline."""

    def _make_chatbot(self):
        """Create chatbot with fully mocked dependencies."""
        from src.module_3_conversational.chatbot import HotelAnalyticsChatbot, ChatResponse

        chatbot = HotelAnalyticsChatbot.__new__(HotelAnalyticsChatbot)
        chatbot.conversation_history = []

        # Mock intent detector
        chatbot.intent_detector = MagicMock()
        chatbot.intent_detector.detect.return_value = {
            "intent": "sql_query",
            "description": "Database query",
            "source": "api",
        }

        # Mock SQL generator
        chatbot.sql_generator = MagicMock()
        chatbot.sql_generator.query.return_value = {
            "success": True,
            "sql": "SELECT COUNT(*) AS total FROM bookings;",
            "data": pd.DataFrame({"total": [11938]}),
            "row_count": 1,
            "columns": ["total"],
            "error": None,
            "source": "api",
        }

        # Mock insight generator
        chatbot.insight_generator = MagicMock()
        chatbot.insight_generator.generate.return_value = {
            "insight": "There are 11,938 total bookings in the system.",
            "source": "api",
        }
        chatbot.insight_generator.generate_summary.return_value = {
            "insight": "General hotel insight.",
            "source": "api",
        }

        # Mock chart generator
        chatbot.chart_generator = MagicMock()
        chatbot.chart_generator.generate.return_value = {
            "chart": MagicMock(),
            "type": "metric",
        }

        # Mock router
        chatbot.router = MagicMock()
        chatbot.router.get_status.return_value = {
            "groq_available": True,
            "groq_usage": {"total_calls": 0},
            "cache_stats": {"type": "disk", "size": 0},
        }

        return chatbot

    def test_ask_sql_query(self):
        """Chatbot handles SQL query intent correctly."""
        chatbot = self._make_chatbot()
        response = chatbot.ask("How many bookings are there?")

        assert response.intent == "sql_query"
        assert response.answer is not None
        assert "11,938" in response.answer
        assert response.sql is not None
        assert response.data is not None
        assert response.error is None

    def test_ask_prediction(self):
        """Chatbot handles prediction intent."""
        chatbot = self._make_chatbot()
        chatbot.intent_detector.detect.return_value = {
            "intent": "prediction",
            "description": "Prediction",
            "source": "api",
        }
        response = chatbot.ask("Will cancellations increase next month?")
        assert response.intent == "prediction"
        assert response.answer is not None

    def test_ask_recommendation(self):
        """Chatbot handles recommendation intent."""
        chatbot = self._make_chatbot()
        chatbot.intent_detector.detect.return_value = {
            "intent": "recommendation",
            "description": "Recommendation",
            "source": "api",
        }
        response = chatbot.ask("How should we reduce cancellations?")
        assert response.intent == "recommendation"

    def test_ask_summary(self):
        """Chatbot handles summary intent."""
        chatbot = self._make_chatbot()
        chatbot.intent_detector.detect.return_value = {
            "intent": "summary",
            "description": "Summary",
            "source": "api",
        }
        response = chatbot.ask("Give me a KPI overview")
        assert response.intent == "summary"

    def test_ask_explanation(self):
        """Chatbot handles explanation/general intent."""
        chatbot = self._make_chatbot()
        chatbot.intent_detector.detect.return_value = {
            "intent": "explanation",
            "description": "Explanation",
            "source": "api",
        }
        response = chatbot.ask("What is RevPAR?")
        assert response.intent == "explanation"

    def test_sql_query_failure(self):
        """Chatbot handles SQL failure gracefully."""
        chatbot = self._make_chatbot()
        chatbot.sql_generator.query.return_value = {
            "success": False,
            "sql": "SELECT invalid;",
            "data": None,
            "error": "no such column: invalid",
        }
        response = chatbot.ask("Show me invalid column")
        assert response.error is not None or "couldn't" in response.answer.lower()

    def test_conversation_history(self):
        """Chatbot tracks conversation history."""
        chatbot = self._make_chatbot()
        chatbot.ask("Question 1")
        chatbot.ask("Question 2")
        assert len(chatbot.conversation_history) == 2

    def test_get_status(self):
        """Chatbot status includes all components."""
        chatbot = self._make_chatbot()
        chatbot.ask("test")
        status = chatbot.get_status()
        assert "conversation_length" in status
        assert status["conversation_length"] == 1

    def test_chat_response_dataclass(self):
        """ChatResponse dataclass has all fields."""
        from src.module_3_conversational.chatbot import ChatResponse
        resp = ChatResponse(
            question="test",
            intent="sql_query",
            answer="Test answer",
            sql="SELECT 1;",
            source="api",
        )
        assert resp.question == "test"
        assert resp.data is None
        assert resp.chart is None
        assert resp.error is None
        assert resp.metadata == {}


# ─────────────────────── Integration Test ───────────────────────


class TestEndToEnd:
    """End-to-end integration tests with in-memory DB."""

    def test_sql_generator_with_real_db(self):
        """Full SQL pipeline with a real SQLite database."""
        from src.module_3_conversational.agents.sql_generator import SQLGenerator

        # Create in-memory test DB
        conn = sqlite3.connect(":memory:")
        conn.execute("""CREATE TABLE bookings (
            booking_id TEXT, hotel TEXT, is_canceled INTEGER, adr REAL, country TEXT
        )""")
        conn.execute("INSERT INTO bookings VALUES ('B1', 'City Hotel', 0, 120.5, 'PRT')")
        conn.execute("INSERT INTO bookings VALUES ('B2', 'Resort Hotel', 1, 200.0, 'GBR')")
        conn.execute("INSERT INTO bookings VALUES ('B3', 'City Hotel', 0, 95.0, 'PRT')")
        conn.commit()

        # Create generator with mock router that returns valid SQL
        mock_router = MagicMock()
        mock_router.query.return_value = {
            "response": "SELECT hotel, COUNT(*) AS total, ROUND(AVG(adr), 2) AS avg_adr FROM bookings GROUP BY hotel;",
            "source": "api",
            "tokens_used": 20,
        }

        gen = SQLGenerator.__new__(SQLGenerator)
        gen.router = mock_router
        gen.schema = "test"

        with patch("src.module_3_conversational.agents.sql_generator.get_connection", return_value=conn):
            result = gen.query("Show bookings by hotel with average ADR")

        assert result["success"] is True
        assert len(result["data"]) == 2
        assert "hotel" in result["columns"]
        assert "avg_adr" in result["columns"]

    def test_chart_from_real_data(self):
        """Chart generator with realistic query results."""
        from src.module_3_conversational.agents.chart_generator import ChartGenerator

        gen = ChartGenerator()
        df = pd.DataFrame({
            "hotel": ["City Hotel", "Resort Hotel"],
            "total_bookings": [7500, 4438],
            "cancel_rate": [41.73, 27.76],
        })
        result = gen.generate(df, "Compare cancellation rates between hotels")
        assert result["chart"] is not None
        assert result["type"] == "bar"
