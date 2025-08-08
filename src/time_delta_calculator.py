import pandas as pd
from typing import Dict, Optional, Tuple
from pathlib import Path


class TimeDeltaCalculator:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.time_deltas: Optional[pd.DataFrame] = None
        self.stats: Dict = {}

    def calculate_time_deltas(self) -> pd.DataFrame:
        if "block_timestamp" not in self.df.columns or "contract_address" not in self.df.columns:
            raise ValueError("DataFrame must contain 'block_timestamp' and 'contract_address' columns.")

        self.df["block_timestamp"] = pd.to_datetime(self.df["block_timestamp"])
        sorted_df = self.df.sort_values(["contract_address", "block_timestamp"])

        sorted_df["seconds_since_last_event"] = (
            sorted_df.groupby("contract_address")["block_timestamp"].diff().dt.total_seconds()
        )

        self.time_deltas = sorted_df
        self._calculate_stats()
        return self.time_deltas

    def _calculate_stats(self) -> None:
        if self.time_deltas is None:
            raise ValueError("Time deltas not calculated. Call calculate_time_deltas() first.")

        self.stats = {
            "total_contracts": self.time_deltas["contract_address"].nunique(),
            "total_events_with_deltas": len(self.time_deltas[self.time_deltas["seconds_since_last_event"].notna()]),
            "avg_time_delta_seconds": self.time_deltas["seconds_since_last_event"].mean(),
            "median_time_delta_seconds": self.time_deltas["seconds_since_last_event"].median(),
            "min_time_delta_seconds": self.time_deltas["seconds_since_last_event"].min(),
            "max_time_delta_seconds": self.time_deltas["seconds_since_last_event"].max(),
        }

    def get_time_delta_summary(self) -> Dict:
        if self.time_deltas is None:
            raise ValueError("Time deltas not calculated. Call calculate_time_deltas() first.")

        summary = self.stats.copy()
        if "contract_address" in self.time_deltas.columns:
            contract_activity = (
                self.time_deltas.groupby("contract_address")
                .size()
                .sort_values(ascending=False)
                .head(10)
                .to_dict()
            )
            summary["top_contracts_by_activity"] = contract_activity
        return summary

    def export_time_deltas(self, output_path: str = "outputs/time_deltas.csv") -> None:
        if self.time_deltas is None:
            raise ValueError("Time deltas not calculated. Call calculate_time_deltas() first.")

        required_columns = [
            "event_id",
            "contract_address",
            "event_type",
            "block_timestamp",
            "seconds_since_last_event",
        ]
        output_df = self.time_deltas[required_columns]

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        output_df.to_csv(output_path, index=False)


def calculate_time_deltas(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    calculator = TimeDeltaCalculator(df)
    time_deltas = calculator.calculate_time_deltas()
    summary = calculator.get_time_delta_summary()
    return time_deltas, summary


if __name__ == "__main__":
    from csv_data_loader import load_contract_events

    df = load_contract_events()
    calculator = TimeDeltaCalculator(df)
    time_deltas = calculator.calculate_time_deltas()
    summary = calculator.get_time_delta_summary()

    print("Time Delta Calculation Results:")
    print(f"Total contracts: {summary['total_contracts']}")
    print(f"Events with time deltas: {summary['total_events_with_deltas']}")
    print(f"Avg time delta (seconds): {summary['avg_time_delta_seconds']:.2f}")
    print(f"Median time delta (seconds): {summary['median_time_delta_seconds']:.2f}")
    print(f"Min time delta (seconds): {summary['min_time_delta_seconds']:.2f}")
    print(f"Max time delta (seconds): {summary['max_time_delta_seconds']:.2f}")

    calculator.export_time_deltas()