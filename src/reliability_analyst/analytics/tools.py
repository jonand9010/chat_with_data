from __future__ import annotations

from typing import Any

import pandas as pd


class AnalyticsToolError(ValueError):
    """Raised when a requested analytics action is invalid."""


def summarize_engine(df: pd.DataFrame, engine_id: int) -> dict[str, Any]:
    """Return a basic summary for a single engine."""
    if "engine_id" not in df.columns:
        raise AnalyticsToolError("DataFrame must contain an 'engine_id' column")

    engine_df = df[df["engine_id"] == engine_id]
    if engine_df.empty:
        raise AnalyticsToolError(f"No data found for engine {engine_id}")

    return {
        "type": "text",
        "title": f"Engine {engine_id} summary",
        "data": {
            "engine_id": int(engine_id),
            "cycles": int(len(engine_df)),
            "start_rul": float(engine_df["rul"].iloc[0]),
            "end_rul": float(engine_df["rul"].iloc[-1]),
        },
        "metadata": {"source": "summarize_engine"},
    }


def rank_degrading_engines(df: pd.DataFrame, sensor: str, top_n: int = 5) -> dict[str, Any]:
    """Rank engines by the average value of a sensor."""
    if sensor not in df.columns:
        raise AnalyticsToolError(f"Sensor '{sensor}' not found")

    ranking = (
        df.groupby("engine_id", as_index=False)[sensor]
        .mean()
        .sort_values(sensor, ascending=False)
        .head(top_n)
    )

    return {
        "type": "table",
        "title": f"Top {top_n} engines by {sensor}",
        "data": ranking.to_dict(orient="records"),
        "metadata": {"sensor": sensor, "top_n": top_n},
    }
