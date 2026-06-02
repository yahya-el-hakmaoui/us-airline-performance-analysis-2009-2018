# us-airline-performance-analysis-2009-2018
Benchmarking on-time performance and delay causes for US domestic airlines (2009-2018) — ~68M flights

**Summary:**
- **What:** A data pipeline and analysis repo that ingests annual CSV flight records (2009–2018), converts them to Parquet, and provides notebooks, profiling reports and a Streamlit dashboard (when available).
- **Source:** Kaggle dataset `yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018` (CSV files named `2009.csv`…`2018.csv`).

**Quick Start**
- **Install dependencies:** `pip install -r requirements.txt` — see [requirements.txt](requirements.txt#L1)
- **Configure paths:** copy [`.env.example`](.env.example#L1) → [`.env`](.env#L1) and set your local data paths.
- **Download / verify CSVs:** `make download` or `python scripts/download_kaggle.py`
- **Convert CSV → Parquet:** `make convert` or `python scripts/convert_to_parquet.py`
- **Run dashboard (if present):** `make dashboard` or `streamlit run dashboard/app.py`

**Files & Commands**
- **Makefile:** convenient targets — see [Makefile](Makefile#L1). Common targets:
  - **install:** installs Python deps from [requirements.txt](requirements.txt#L1)
  - **download:** runs [scripts/download_kaggle.py](scripts/download_kaggle.py#L1)
  - **convert:** runs [scripts/convert_to_parquet.py](scripts/convert_to_parquet.py#L1)
  - **clean:** runs [scripts/clean_parquet.py](scripts/clean_parquet.py#L1) (file may be empty)
  - **run_dbt:** runs [scripts/run_dbt.py](scripts/run_dbt.py#L1) (file may be empty)
  - **notebook:** executes selected notebooks (nbconvert)

**Environment / Paths**
- The pipeline reads paths from [`.env`](.env#L1). Important variables:
  - **DATA_RAW_PATH:** folder with raw CSVs (e.g. `data/csv_raw`) — see [`.env`](.env#L1)
  - **DATA_PARQUET_RAW_PATH:** output folder for Parquet (e.g. `data/parquet_raw`)
  - **DATA_PARQUET_CLEAN_PATH:** folder for cleaned Parquet
  - **DUCKDB_PATH:** path to the DuckDB file used by dbt/analysis

**Scripts (overview)**
- `scripts/download_kaggle.py`: verifies presence of `2009.csv`…`2018.csv`, prints instructions to download from Kaggle if missing. Uses `DATA_RAW_PATH` from `.env`. See [scripts/download_kaggle.py](scripts/download_kaggle.py#L1).
- `scripts/convert_to_parquet.py`: converts CSV files found in `DATA_RAW_PATH` into Parquet files under `DATA_PARQUET_RAW_PATH` using Polars and pyarrow. Supports `--dry-run`, `--overwrite`, and `--chunksize`. See [scripts/convert_to_parquet.py](scripts/convert_to_parquet.py#L1).
- `scripts/clean_parquet.py`: placeholder for parquet cleaning (file currently empty). See [scripts/clean_parquet.py](scripts/clean_parquet.py#L1).
- `scripts/run_dbt.py`: placeholder to run dbt models (file currently empty). See [scripts/run_dbt.py](scripts/run_dbt.py#L1).

**Notebooks & Reports**
- Jupyter notebooks live in `notebooks/` and include auditing and analysis flows. The Makefile `notebook` target runs a subset via `nbconvert`.
- Profiling reports are written to `reports/profiling` (paths configured via `.env`).

**Notes & Troubleshooting**
- The repo expects Python 3.10 or 3.11 (Makefile hint). Use a virtualenv (recommended `.venv`).
- If `scripts/convert_to_parquet.py` errors about missing packages, install `polars`, `pyarrow`, etc. from [requirements.txt](requirements.txt#L1).
- The dashboard entrypoint referenced in the Makefile is `dashboard/app.py`; the `dashboard/` directory may be incomplete in this workspace (check `dashboard/pages/`).
- `scripts/clean_parquet.py` and `scripts/run_dbt.py` are present but empty — implement or ignore depending on your workflow.

**Recommended Workflow (example)**
1. Create and activate virtualenv:

	python -m venv .venv
	source .venv/bin/activate

2. Install dependencies:

	pip install -r requirements.txt

3. Populate `.env` (copy `.env.example` and update paths).

4. Verify/download CSVs:

	make download

5. Convert to Parquet:

	make convert

6. (Optional) Run notebooks, profiling, dbt or dashboard via Makefile targets.

**Where to look next**
- Data paths / env: [`.env`](.env#L1)
- Conversion logic: [scripts/convert_to_parquet.py](scripts/convert_to_parquet.py#L1)
- CSV verification: [scripts/download_kaggle.py](scripts/download_kaggle.py#L1)

If you'd like, I can:
- run the conversion dry-run to list planned Parquet files,
- implement `clean_parquet.py` or `run_dbt.py` stubs,
- or draft a simple `dashboard/app.py` to make the dashboard runnable.
