import pandas as pd
import numpy as np
from typing import Tuple, Dict, Optional
from pathlib import Path
from csv_data_loader import load_contract_events


class OrphanEventDetector:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.orphan_events: Optional[pd.DataFrame] = None
        self.stats: Dict = {}

    def find_orphan_events(self) -> pd.DataFrame:
        existing_event_ids = set(self.df["event_id"].dropna())
        events_with_previous = self.df[self.df["previous_event_id"].notna()].copy()

        if events_with_previous.empty:
            self.orphan_events = pd.DataFrame(
                columns=[
                    "event_id",
                    "previous_event_id",
                    "contract_address",
                    "event_type",
                    "block_number",
                ]
            )
            return self.orphan_events

        orphan_mask = ~events_with_previous["previous_event_id"].isin(existing_event_ids)
        self.orphan_events = events_with_previous[orphan_mask].copy()

        required_columns = [
            "event_id",
            "previous_event_id",
            "contract_address",
            "event_type",
            "block_number",
        ]
        self.orphan_events = self.orphan_events[required_columns]

        self._calculate_orphan_events_stats(events_with_previous)
        return self.orphan_events

    def _calculate_orphan_events_stats(self, events_with_previous: pd.DataFrame) -> None:
        total_events = len(self.df)
        events_with_prev = len(events_with_previous)
        orphan_count = len(self.orphan_events)

        self.stats = {
            "total_events": total_events,
            "events_with_previous_id": events_with_prev,
            "orphan_events": orphan_count,
            "orphan_percentage": (orphan_count / events_with_prev * 100) if events_with_prev > 0 else 0,
            "orphan_vs_total_percentage": (orphan_count / total_events * 100) if total_events > 0 else 0,
        }

    def get_orphan_summary(self) -> Dict:
        if self.orphan_events is None:
            raise ValueError("Orphan detection not run. Call find_orphan_events() first.")

        summary = self.stats.copy()

        if not self.orphan_events.empty:
            summary["top_contracts_with_orphans"] = (
                self.orphan_events.groupby("contract_address")
                .size()
                .sort_values(ascending=False)
                .head(10)
                .to_dict()
            )

            summary["orphan_events_by_type"] = (
                self.orphan_events.groupby("event_type").size().sort_values(ascending=False).to_dict()
            )

            if "block_timestamp" in self.df.columns:
                summary["orphan_time_range"] = {
                    "earliest": self.df["block_timestamp"].min(),
                    "latest": self.df["block_timestamp"].max(),
                }

        return summary

    def get_task1_output(self) -> pd.DataFrame:
        if self.orphan_events is None:
            raise ValueError("Orphan detection not run. Call find_orphan_events() first.")
        return self.orphan_events

    def export_task1_output(self, output_path: str = "outputs/task1_orphan_events.csv") -> None:
        if self.orphan_events is None:
            raise ValueError("Orphan detection not run. Call find_orphan_events() first.")

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        self.orphan_events.to_csv(output_path, index=False)


def find_orphan_events(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    detector = OrphanEventDetector(df)
    orphan_events = detector.find_orphan_events()
    summary = detector.get_orphan_summary()
    return orphan_events, summary


if __name__ == "__main__":
    df = load_contract_events()
    detector = OrphanEventDetector(df)
    orphan_events = detector.find_orphan_events()

    print("Task 1 - Orphan Event Detection Results:")
    print(orphan_events.to_string(index=False))

    detector.export_task1_output()