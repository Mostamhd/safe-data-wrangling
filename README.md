# Safe{Wallet} Data Analysis Challenge

This repository contains solutions for two tasks:
1. **Revenue Analysis** (Dune SQL + Presentation)
2. **Python Data Wrangling** (Orphan Events, Time Deltas, Sender Mapping)

---

## Submission Guide

### 1. Revenue Analysis (Dune SQL + Presentation)
#### Dune Query
- **File**: [`sql/dune_safe_revenues_analysis.sql`](./sql/dune_safe_revenues_analysis.sql)
- **Objective**: Calculate total revenue from monetized swaps in Safe{Wallet}, segmented by feature and stablecoin pairs.
- **Key Logic**:
  - Categorizes swaps (`native_swaps`, `cow_safeapp`, etc.).
  - Applies tiered fee logic based on [Safe{Wallet} documentation](https://safe.global/blog/introducing-tiered-fees-and-twap-orders-in-safe-wallet-native-swaps).
  - Outputs revenue, volume, and average fee percentage by feature and pair.

#### Presentation
- **Link**: [Google Slides](https://docs.google.com/presentation/d/19VjhlASEtby82zHfXq9_lV0R1k5wMIHSSyx9xbDxwuc/edit?usp=sharing)


### 2. Python Data Wrangling
#### Setup
1. Ensure you have [`uv`](https://github.com/your-uv-repo) installed.
2. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/Mostamhd/safe-data-wrangling
   cd safe-data-wrangling
   ```
3. Sync dependencies and activate the virtual environment:
   ```bash
   uv sync
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

#### Tasks
| Task | Script | Output | Key Assumptions |
|------|--------|--------|-----------------|
| Orphan Events | [`src/orphan_detector.py`](./src/orphan_detector.py) | `outputs/task1_orphan_events.csv` | `event_id` is unique; `previous_event_id` is nullable. |
| Time Deltas | [`src/time_delta_calculator.py`](./src/time_delta_calculator.py) | `outputs/time_deltas.csv` | `block_timestamp` is parseable; events are chronological. |
| Sender Mapping | [`src/sender_mapper.py`](./src/sender_mapper.py) | `outputs/sender_activity.csv` | `sender` and `block_number` are non-null. |

#### Bonus (Optional)
- **Bot Detection**: High-frequency senders (`bonus_analyzer.py`).
- **Data Quality**: Missing values, invalid `Reorged` statuses.


## Notes
- **Dataset**: Assumes `contract_events.csv` is pre-cleaned.
- **Edge Cases**: Handled in code (e.g., empty DataFrames).
- **Time Budget**: ~3-4 hours (per task guidelines).

