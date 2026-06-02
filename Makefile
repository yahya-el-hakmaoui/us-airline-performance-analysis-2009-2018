.PHONY: all download convert clean run_dbt profiling notebook dashboard

all: download convert clean run_dbt dashboard

download:
	python scripts/download_kaggle.py

convert:
	python scripts/convert_to_parquet.py

clean:
	python scripts/clean_parquet.py

run_dbt:
	python scripts/run_dbt.py

profiling:
	python scripts/profiling_2015.py

notebook:
	jupyter nbconvert --to notebook --execute notebooks/audit/01_schema_audit.ipynb
	jupyter nbconvert --to notebook --execute notebooks/analysis/AX1_benchmarking.ipynb
	jupyter nbconvert --to notebook --execute notebooks/analysis/AX2_delay_causes.ipynb

dashboard:
	streamlit run dashboard/app.py