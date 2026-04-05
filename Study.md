# Study Notes: Methods Used in 01_starter.ipynb

This file explains every method and pattern you used today, what it does, and which arguments you can change.

## 1) glob.glob("../data/raw/*.csv")
Purpose: Find all CSV files in the raw data folder.

Arguments you can change:
- Pattern string: "../data/raw/*.csv"
  - * means all file names.
  - You can change it to "../data/raw/Friday*.csv" to load only Friday files.
  - You can point to another folder if needed.

Notes:
- Returned value is a list of file paths.

## 2) pd.read_csv(i)
Purpose: Read one CSV file into a pandas DataFrame.

Important arguments you can change:
- filepath_or_buffer: the file path (i in your loop).
- sep=",": delimiter; change if your file uses ; or tab.
- encoding="utf-8": change if file encoding is different.
- low_memory=False: often useful for mixed-type columns.
- nrows=...: load only first N rows for fast testing.

## 3) df.shape
Purpose: Returns (number_of_rows, number_of_columns).

No arguments.

## 4) df.columns
Purpose: Returns all column names.

No arguments.

## 5) df[' Label'].value_counts()
Purpose: Count rows per label class.

Arguments you can change:
- dropna=True (default): if False, NaN labels are also counted.
- normalize=False (default): if True, returns proportions instead of counts.

Related line used by you:
- df[' Label'].value_counts(normalize=True) returns percentage distribution.

## 6) df[' Label'].unique()
Purpose: Show unique class labels present in that file.

No major arguments.

## 7) df[col].isnull().sum()
Purpose: Count missing values in one column.

No major arguments.

## 8) pd.to_numeric(df[col], errors='coerce')
Purpose: Convert a column to numeric type so numeric checks (like infinity detection) can be done safely.

This is your need more explanation line.

What errors='coerce' means:
- If a value cannot be converted to number (for example text like "abc"), pandas replaces it with NaN.
- This prevents conversion errors and lets the loop continue.
- After conversion, you can run numeric checks like np.isposinf(...) and np.isneginf(...).

Arguments you can change:
- errors='raise': throw an error on bad value.
- errors='ignore': keep original values (less useful for numeric checks).

## 9) np.isposinf(numeric_col).sum() and np.isneginf(numeric_col).sum()
Purpose: Count +inf and -inf values in numeric data.

No major arguments besides the input array/Series.

## 10) df.duplicated().sum()
Purpose: Count duplicate rows.

Arguments you can change:
- subset=[...]: check duplicates only on specific columns.
- keep='first'|'last'|False: define which duplicates are marked.

## 11) df.columns.str.strip()
Purpose: Remove leading/trailing spaces from each column name.

No important arguments in this usage.

## 12) df.columns.str.replace(' ', '_')
Purpose: Replace spaces with underscores in column names.

Arguments you can change:
- Old text ' ' and new text '_'.
- regex=False if you want plain text replacement explicitly.

## 13) df['Label'].str.replace('  ', '_') and df['Label'].str.replace(' ', '_')
Purpose: Standardize label strings to machine-friendly names.

Arguments you can change:
- Pattern and replacement text.
- regex=False to avoid regex interpretation where needed.

## 14) print(...)
Purpose: Display intermediate inspection results.

You can print:
- Shapes, column names, counts, unique labels, separators.

## Good Practice Improvements for Your Current Notebook
- Read each CSV once, then compute all checks in one pass to save time.
- Strip column names immediately after reading to avoid ' Label' vs 'Label' confusion.
- Save profiling results to CSV/Markdown (already done now).
- Consider parsing date/time columns in preprocessing for stronger train/val/test split.
