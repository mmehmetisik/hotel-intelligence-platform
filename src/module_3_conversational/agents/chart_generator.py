"""
Chart Generator Agent

Automatically generates appropriate Plotly charts based on
the data structure and question context.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChartGenerator:
    """Generates appropriate charts from query results."""

    def detect_chart_type(self, data: pd.DataFrame, question: str = "") -> str:
        """Detect the most appropriate chart type."""
        q = question.lower()
        n_rows = len(data)
        n_cols = len(data.columns)
        numeric_cols = data.select_dtypes(include="number").columns
        string_cols = data.select_dtypes(include="object").columns

        # Keyword-based detection
        if any(w in q for w in ["trend", "over time", "monthly", "weekly", "daily"]):
            return "line"
        if any(w in q for w in ["distribution", "histogram", "spread"]):
            return "histogram"
        if any(w in q for w in ["compare", "vs", "versus", "between"]):
            return "bar"
        if any(w in q for w in ["breakdown", "percentage", "share", "proportion"]):
            if n_rows <= 8:
                return "pie"
            return "bar"
        if any(w in q for w in ["top", "best", "worst", "ranking"]):
            return "bar_horizontal"
        if any(w in q for w in ["correlation", "relationship", "scatter"]):
            return "scatter"

        # Data-structure based detection
        if n_rows == 1 and len(numeric_cols) <= 3:
            return "metric"
        if n_rows <= 6 and len(string_cols) >= 1 and len(numeric_cols) >= 1:
            return "pie"
        if len(numeric_cols) >= 1 and len(string_cols) >= 1:
            return "bar"
        if len(numeric_cols) >= 2:
            return "scatter"

        return "table"

    def generate(self, data: pd.DataFrame, question: str = "", chart_type: str = None) -> dict:
        """Generate a chart from data."""
        if data is None or data.empty:
            return {"chart": None, "type": "none", "message": "No data to visualize"}

        if chart_type is None:
            chart_type = self.detect_chart_type(data, question)

        try:
            fig = self._create_chart(data, chart_type, question)
            return {"chart": fig, "type": chart_type}
        except Exception as e:
            logger.error(f"Chart generation error: {e}")
            return {"chart": None, "type": "error", "message": str(e)}

    def _create_chart(self, data: pd.DataFrame, chart_type: str, question: str) -> go.Figure:
        """Create a Plotly figure."""
        numeric_cols = data.select_dtypes(include="number").columns.tolist()
        string_cols = data.select_dtypes(include="object").columns.tolist()

        # Default axes
        x_col = string_cols[0] if string_cols else data.columns[0]
        y_col = numeric_cols[0] if numeric_cols else data.columns[-1]

        if chart_type == "bar":
            fig = px.bar(data, x=x_col, y=y_col, title=question or "Results",
                         color_discrete_sequence=["#2E86AB"])

        elif chart_type == "bar_horizontal":
            fig = px.bar(data, y=x_col, x=y_col, orientation="h",
                         title=question or "Results",
                         color_discrete_sequence=["#2E86AB"])

        elif chart_type == "line":
            fig = px.line(data, x=x_col, y=y_col, title=question or "Trend",
                          markers=True, color_discrete_sequence=["#2E86AB"])

        elif chart_type == "pie":
            fig = px.pie(data, names=x_col, values=y_col, title=question or "Distribution",
                         color_discrete_sequence=px.colors.qualitative.Set2)

        elif chart_type == "histogram":
            fig = px.histogram(data, x=y_col, title=question or "Distribution",
                               color_discrete_sequence=["#2E86AB"])

        elif chart_type == "scatter":
            y2 = numeric_cols[1] if len(numeric_cols) > 1 else y_col
            fig = px.scatter(data, x=y_col, y=y2, title=question or "Scatter",
                             color_discrete_sequence=["#2E86AB"])

        elif chart_type == "metric":
            # Single value display
            value = data[y_col].iloc[0] if y_col in data.columns else data.iloc[0, 0]
            fig = go.Figure(go.Indicator(
                mode="number",
                value=float(value),
                title={"text": question or y_col},
            ))
        else:
            # Default: table as figure
            fig = go.Figure(data=[go.Table(
                header=dict(values=list(data.columns), fill_color="#2E86AB", font=dict(color="white")),
                cells=dict(values=[data[col] for col in data.columns], fill_color="#F5F5F5"),
            )])

        # Styling
        fig.update_layout(
            template="plotly_white",
            font=dict(family="Arial", size=12),
            margin=dict(l=40, r=40, t=60, b=40),
            height=400,
        )

        return fig
