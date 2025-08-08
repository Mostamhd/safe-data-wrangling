import pandas as pd
import numpy as np
from typing import Optional, Tuple
from pathlib import Path


class CsvDataLoader:
    def __init__(self, file_path: str = "data/contract_events.csv"):
        self.file_path = Path(file_path)
        self.df: Optional[pd.DataFrame] = None

    def load_data(self) -> pd.DataFrame:
        try:
            self.df = pd.read_csv(
                self.file_path,
                dtype={
                    "tx_hash": "string",
                    "event_id": "string",
                    "event_type": "string",
                    "contract_address": "string",
                    "sender": "string",
                    "previous_event_id": "string",
                    "status": "string",
                    "node_region": "string",
                    "block_number": "Int64",
                    "gas_used": "Int64",
                    "tx_index": "Int64",
                },
                parse_dates=["block_timestamp"],
            )

            self.df.columns = self.df.columns.str.strip()
            

            return self.df

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")
        except pd.errors.EmptyDataError:
            raise pd.errors.EmptyDataError(f"Empty CSV file: {self.file_path}")
        except Exception as e:
            raise e

def load_contract_events(file_path: str = "data/contract_events.csv") -> pd.DataFrame:
    loader = CsvDataLoader(file_path)
    return loader.load_data()
