# Study Notes: Current Workflow in 01_starter.ipynb

This note matches the current code in `notebooks/01_starter.ipynb` and the outputs you generated.

## 1) Load all raw CSV files once

Code pattern:
- `data_dir = gb.glob("../data/raw/*.csv")`
- Loop through `data_dir`
- `datasets[Path(file_path).name] = pd.read_csv(file_path)`

Why this is good:
- You read each file one time and keep it in memory.
- Later checks (labels, missing values, duplicates) reuse `datasets` without reloading from disk.

What you can tune:
- File pattern: `../data/raw/*.csv` (example: only Friday files).
- `pd.read_csv(...)` options such as `low_memory=False`, `nrows=...`, or `encoding=...`.

## 2) Inspect labels per dataset

Code pattern:
- `df[' Label'].value_counts()`
- `df[' Label'].value_counts(normalize=True)`
- `df[' Label'].unique()`

Purpose:
- Check class counts and class ratio per file.
- Detect imbalance early before training.

Note:
- The label column starts as `' Label'` (with a leading space) in these raw files.

## 3) Check missing values and infinity values

Code pattern:
- `df[col].isnull().sum()`
- `numeric_col = pd.to_numeric(df[col], errors='coerce')`
- `np.isposinf(numeric_col).sum()`
- `np.isneginf(numeric_col).sum()`

Meaning of `errors='coerce'`:
- If a value cannot be converted to numeric, pandas sets it to `NaN`.
- This avoids conversion crashes and lets the loop continue for all columns.
- It makes infinity checks safe on mixed-type columns.

## 4) Check duplicate rows

Code pattern:
- `df.duplicated().sum()`

Purpose:
- Measure potential repeated flows/records that can bias modeling if not handled.

## 5) Standardize column names and label text

Code pattern:
- `df.columns = df.columns.str.strip()`
- `df.columns = df.columns.str.replace(' ', '_')`
- `df['Label'] = df['Label'].str.replace(' – ', '_')`
- `df['Label'] = df['Label'].str.replace(' ', '_')`

Purpose:
- Make names model-friendly (no spaces, consistent separators).
- Normalize label strings for cleaner downstream encoding.

Important detail:
- The replacement ` ' – ' ` handles labels that use a dash-like separator between words.

## 6) Generated profiling artifacts

Your notebook workflow produced summary artifacts:
- `data_profile_report.md`
- `dataset_metadata_summary.csv`

These files summarize, per dataset:
- Row count
- Missing values
- Infinity values
- Duplicate rows
- Benign vs attack label composition

## 7) Key project takeaway from current profile

- The combined dataset is strongly imbalanced toward `BENIGN` traffic.
- There are many duplicates and some infinity values across files.
- Day/time-aware splitting is preferred over random row split to reduce leakage risk.

## 8) Suggested next coding step

Create a preprocessing script in `src/` that:
- Applies the same renaming/cleaning rules consistently.
- Handles missing and infinity values with explicit policy.
- Writes cleaned outputs to `data/processed/` for model training.

## DAY_2 Learning Notes

### 1. Handling Extreme and Missing Values
- **pd.to_numeric(..., errors='coerce')**: Attempts conversion to numeric form; bad conversions bypass errors and become NaN.
- **df.replace(np.inf, np.nan)**: Crucial for machine learning as most models algorithms (like scikit-learn classifiers) will instantly break if handed an infinitely large number.

### 2. Selecting Column Types and Median Imputation
- **df.select_dtypes(include=np.number).columns**: Automatically grabs all numerical features by excluding categorical or object ones.
- **Median Imputation (.fillna(df.median()))**: Missing data replaced by the median. Median is resistant/robust to major outliers comparing to Mean values which was key in these security datasets with gigantic extremes.

### 3. Binary Classification Labeling
- Constructed an isAttack target column by taking everything that isn't 'BENIGN'. 
- .astype(int) quickly casts boolean maps (True/False) to Machine learning digestible integer states (1/0).

### 4. Consolidating and Exporting Data
- **pd.concat(datasets.values())**: Safely stacks a dictionary or list of dataframes on top of one another into a solid DataFrame block.
- Stored the cleaned result in data/processed/combined_dataset.csv for next step splits and Machine Learning pipelines.

