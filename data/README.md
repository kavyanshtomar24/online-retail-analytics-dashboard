# Data files

The full raw and cleaned datasets are stored as gzip-compressed CSV files so the repository stays comfortably below GitHub's large-file limits while preserving the complete data.

## Files

- `raw/online_retail_II.csv.gz` — full raw Online Retail II dataset.
- `cleaned/online_retail_II_cleaned.csv.gz` — full cleaned dataset used for analysis and dashboarding.
- `samples/raw_sample_1000_rows.csv` — small preview of the raw data.
- `samples/cleaned_sample_1000_rows.csv` — small preview of the cleaned data.

Pandas reads `.csv.gz` directly:

```python
import pandas as pd

df = pd.read_csv("data/cleaned/online_retail_II_cleaned.csv.gz")
```
