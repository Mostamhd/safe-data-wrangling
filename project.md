Home
exploration
Senior Data Analyst
Time
We respect your time and the challenge is defined in such a way that it does not take
more than 3-4 hours. We want to get a sense of your thought process and the way you
work. If there are things you don't have time to implement, feel free to describe the
intended approach to implementation.
Objective
This take-home assignment is designed to assess your skills with onchain tools, data
wrangling, data storytelling and analytical thinking. You will also showcase how you
approach product strategy.
Goal
The goal of this home-exploration is for you to gain some context around the tasks that
the data team at Safe faces and think about how you would approach some of these
tasks.
Task 1 : Revenue Analysis
The task at hand revolves around the monetised swaps within Safe{Wallet}.
You are given a materialised view which you can query on Dune:
dune.safe.result_testset
The materialised view has the following columns:
- block_date (the date of the transaction)
- block_time (the exact timestamp of the transaction)
- tx_hash (the transaction hash of the transaction)
- feature (the protocol used within Safe{Wallet} to facilitate the swap)
- trader (the Safe{Wallet} that executed the swap transaction)
- Is_stablecoin_pair (a flag where 1 means stablecoins were swapped and 0
means other erc20 assets were swapped)
- usd_value (the dollar value of the swap)
You are also given the following documentation that explains how we calculate the
revenue per swap:
- For Native Swaps:
https://safe.global/blog/introducing-tiered-fees-and-twap-orders-in-safe-walletnative-swaps
- For SafeApps:
Feature Fee Logic
CoW SafeApp 45% of 10bps on swap volume
1inch SafeApp 53% of 10bps on swap volume
KyberSwap 45% of 10bps on swap volume
You are expected to do the following:
1. Revenue Calculation (Dune)
- Write a Dune query to compute total revenue in USD across the dataset
- Your query should infer the fee per transaction based on the feature and swap
size using the documents above
2. Insights and Recommendations (Presentation)
- Using the data provided, share a short report/presentation that highlights:
- Swap usage or patterns
- Some examples but not limited to volume breakdown, distribution,
swap behaviour
- Fee efficiency analysis
- Some examples but not limited to which segments generate most
revenue, overpriced/underpriced tiers
- Strategic Recommendations
- Some examples but not limited to:
- What changes would you recommend to the current pricing?
- How does the current fee stack up against market standard?
Task 2 : Python Data Wrangling Challenge
The assignment is designed to assess your ability to analyze datasets using Python and
relational thinking. You’ll be working with a synthetic dataset of smart contract event logs,
inspired by some fictitious blockchain. The data has been pre-indexed into a CSV file.
Setup instructions
Use uv to create a Python virtual environment and install Pandas for data wrangling and
analysis.
Dataset
You will analyze the file: contract_events.csv
It contains ~20,000 records of smart contract events, each representing a
transaction-level emission from a contract. Clone the data set to your local working
directory (safehjc/wrangle-me). Check also the given README.
Column Description
event_id Unique identifier for the event
previous_event_id References another event, if applicable
tx_hash The transaction that emitted the event
contract_address The smart contract involved
sender The EOA initiating the transaction
block_number The block containing the transaction
block_timestamp When the block was mined
gas_used Synthetic gas usage estimate
status Confirmed, Pending, or Reorged
node_region Arbitrary metadata about location
tx_index Ordering index within the block (random)
Note: As with real-world data there might be inconsistencies, edge cases, or anomalies present. You are
encouraged to approach the dataset critically and mention anything unusual you find.
1. Orphan Event Detection
- Find all the orphan events in the dataset
2. Time Delta Per Contract
- For each contract_address, compute the number of seconds since the previous
event ordered by block_timestamp
3. Sender Mapping
- For each sender, find the block where they had the most events emitted, and rank
them by event frequency
Bonus Tasks (optional)
- Identify and explain inconsistencies or data quality issues you noticed
- Detect possible bot-like behavior
- Visualize interesting patterns (eg, frequency by event_type or contract_address)
- Trace multi-step event chains using previous_event_id
Note:
1. Please mention any assumptions that you consider
2. Please reach out if any statement/task is unclear
3. Feel free to request a Dune API Key if needed
Submission
- Please submit your Dune query, your code, visualizations, and analysis artefacts
with your comments via a GitHub repository
- Add a README file explaining how to setup and execute the code
- Provide documentation explaining your approach and any assumptions made
- The query/code should be clean, modular, and well-documented
Evaluation Criteria
- Correctness and efficiency of the solution
- Code readability and best practices
- Creative use of tools and technologies
- Ability to draw insights and tell a compelling story
- Strategic depth and creativity
Additional notes
Please note you will be expected to present your findings in the next interview stage. The
goal will be to dive into your process, thinking, and tradeoffs, not to critique the final
output.
During the technical interview, the focus will be more on how you would approach
different aspects of the data analyst role.
Good luck and have fun!
🚀