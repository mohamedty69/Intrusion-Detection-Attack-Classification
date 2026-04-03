# AI Project Workspace

Simple environment for working with datasets and Jupyter notebooks.

## Structure
- `data/raw/` : Original datasets
- `data/processed/` : Cleaned/transformed datasets
- `notebooks/` : Jupyter notebooks
- `src/` : Reusable Python scripts/modules
- `models/` : Saved model files

## Quick start (Windows PowerShell)
1. Create virtual environment:
   `py -m venv .venv`
2. Activate it:
   `.\.venv\Scripts\Activate.ps1`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Start Jupyter:
   `jupyter lab`

## Notes
- Put your dataset files in `data/raw/`.
- Keep experiments in notebooks, then move reusable code into `src/`.
