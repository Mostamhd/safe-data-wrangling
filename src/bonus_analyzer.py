import pandas as pd
from typing import Dict, List, Optional
from pathlib import Path
from csv_data_loader import load_contract_events


class BonusAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.bot_behavior: Optional[pd.DataFrame] = None
        self.data_issues: Optional[pd.DataFrame] = None

    def detect_bot_behavior(self) -> pd.DataFrame:
        if "sender" not in self.df.columns or "block_timestamp" not in self.df.columns:
            raise ValueError("DataFrame must contain 'sender' and 'block_timestamp'.")

        sender_stats = (
            self.df.groupby("sender")
            .agg(
                event_count=("event_id", "size"),
                avg_time_between_events=("block_timestamp", lambda x: x.diff().dt.total_seconds().mean()),
            )
            .reset_index()
        )

        sender_stats["is_bot_like"] = (
            (sender_stats["event_count"] > 100) & (sender_stats["avg_time_between_events"] < 10)
        )

        self.bot_behavior = sender_stats.sort_values("event_count", ascending=False)
        return self.bot_behavior

    def detect_data_issues(self) -> pd.DataFrame:
        issues = []

        missing = self.df.isnull().sum()
        for col, count in missing.items():
            if count > 0:
                issues.append({"column": col, "issue_type": "missing", "count": count})

        if "status" in self.df.columns and "previous_event_id" in self.df.columns:
            invalid_status = self.df[
                (self.df["status"] == "Reorged") & (self.df["previous_event_id"].notna())
            ]
            if len(invalid_status) > 0:
                issues.append(
                    {"column": "status", "issue_type": "invalid_reorged_chain", "count": len(invalid_status)}
                )

        self.data_issues = pd.DataFrame(issues)
        return self.data_issues

    def export_results(self, output_path: str = "outputs/bonus_analysis.csv") -> None:
        if self.bot_behavior is None or self.data_issues is None:
            raise ValueError("Run detection methods first.")

        combined = pd.concat(
            [
                self.bot_behavior.assign(analysis_type="bot_behavior"),
                self.data_issues.assign(analysis_type="data_issue"),
            ]
        )

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        combined.to_csv(output_path, index=False)


def analyze_bonus(df: pd.DataFrame) -> Dict:
    analyzer = BonusAnalyzer(df)
    bot_behavior = analyzer.detect_bot_behavior()
    data_issues = analyzer.detect_data_issues()

    return {
        "bot_behavior_stats": bot_behavior.describe().to_dict(),
        "data_issues": data_issues.to_dict("records"),
    }


if __name__ == "__main__":

    df = load_contract_events()
    analyzer = BonusAnalyzer(df)
    bot_behavior = analyzer.detect_bot_behavior()
    data_issues = analyzer.detect_data_issues()

    print("Bot-like Behavior (Top 10):")
    print(bot_behavior.head(10).to_string(index=False))

    print("\nData Quality Issues:")
    print(data_issues.to_string(index=False))

    analyzer.export_results()