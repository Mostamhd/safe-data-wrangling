import pandas as pd
from typing import Dict, Optional, Tuple
from pathlib import Path


class SenderMapper:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.sender_activity: Optional[pd.DataFrame] = None
        self.stats: Dict = {}

    def map_sender_activity(self) -> pd.DataFrame:
        if "sender" not in self.df.columns or "block_number" not in self.df.columns:
            raise ValueError("DataFrame must contain 'sender' and 'block_number' columns.")

        sender_block_counts = (
            self.df.groupby(["sender", "block_number"]).size().reset_index(name="event_count")
        )

        max_blocks = (
            sender_block_counts.sort_values("event_count", ascending=False)
            .drop_duplicates("sender")
            .sort_values("event_count", ascending=False)
        )

        max_blocks["rank_in_sender_activity"] = (
            max_blocks["event_count"].rank(method="min", ascending=False).astype(int)
        )

        self.sender_activity = max_blocks
        self._calculate_stats()
        return self.sender_activity

    def _calculate_stats(self) -> None:
        if self.sender_activity is None:
            raise ValueError("Sender activity not mapped. Call map_sender_activity() first.")

        self.stats = {
            "total_senders": self.sender_activity["sender"].nunique(),
            "avg_events_per_sender": self.sender_activity["event_count"].mean(),
            "median_events_per_sender": self.sender_activity["event_count"].median(),
            "max_events_in_block": self.sender_activity["event_count"].max(),
            "min_events_in_block": self.sender_activity["event_count"].min(),
        }

    def get_sender_summary(self) -> Dict:
        if self.sender_activity is None:
            raise ValueError("Sender activity not mapped. Call map_sender_activity() first.")

        summary = self.stats.copy()
        top_senders = (
            self.sender_activity.sort_values("rank_in_sender_activity")
            .head(10)[["sender", "event_count", "rank_in_sender_activity"]]
            .to_dict("records")
        )
        summary["top_senders"] = top_senders
        return summary

    def export_sender_activity(self, output_path: str = "outputs/sender_activity.csv") -> None:
        if self.sender_activity is None:
            raise ValueError("Sender activity not mapped. Call map_sender_activity() first.")

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        self.sender_activity.to_csv(output_path, index=False)


def map_sender_activity(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    mapper = SenderMapper(df)
    sender_activity = mapper.map_sender_activity()
    summary = mapper.get_sender_summary()
    return sender_activity, summary


if __name__ == "__main__":
    from csv_data_loader import load_contract_events

    df = load_contract_events()
    mapper = SenderMapper(df)
    sender_activity = mapper.map_sender_activity()
    summary = mapper.get_sender_summary()

    print("Sender Activity Mapping Results:")
    print(f"Total senders: {summary['total_senders']}")
    print(f"Avg events per sender: {summary['avg_events_per_sender']:.2f}")
    print(f"Median events per sender: {summary['median_events_per_sender']:.2f}")
    print(f"Max events in a block: {summary['max_events_in_block']}")
    print(f"Min events in a block: {summary['min_events_in_block']}")

    mapper.export_sender_activity()