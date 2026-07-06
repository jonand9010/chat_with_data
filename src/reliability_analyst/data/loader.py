from __future__ import annotations

from pathlib import Path

import pandas as pd


class DataLoader:
    """Simple loader for local CSV or parquet data files."""

    def __init__(self, data_dir: str | Path | None = None) -> None:
        self.data_dir = Path(data_dir or "data")

    def load_csv(self, filename: str) -> pd.DataFrame:
        path = self.data_dir / filename
        return pd.read_csv(path)

    def load_parquet(self, filename: str) -> pd.DataFrame:
        path = self.data_dir / filename
        return pd.read_parquet(path)
