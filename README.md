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
- **Contents**:
  - **Swap Patterns**: Volume breakdown, user behavior.
  - **Fee Efficiency**: Revenue segments, pricing analysis.
  - **Recommendations**: Pricing adjustments, competitive benchmarking.

---

### 2. Python Data Wrangling
#### Setup
```bash
git clone https://github.com/your-repo/safe.git
cd safe
uv venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install pandas
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

---

## Evaluation Criteria
1. **Correctness**: Accurate revenue calculation and event analysis.
2. **Code Quality**: Modular, documented, and PEP-8 compliant.
3. **Insights**: Actionable recommendations from data.
4. **Presentation**: Clear storytelling with visuals.

---

## Notes
- **Dataset**: Assumes `contract_events.csv` is pre-cleaned.
- **Edge Cases**: Handled in code (e.g., empty DataFrames).
- **Time Budget**: ~3-4 hours (per task guidelines).

---

## Next Steps
1. Run scripts as described above.
2. Review the [presentation](https://docs.google.com/presentation/d/19VjhlASEtby82zHfXq9_lV0R1k5wMIHSSyx9xbDxwuc/edit?usp=sharing) for strategic insights.
3. For queries, contact [your-email@example.com](mailto:your-email@example.com).