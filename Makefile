.PHONY: all help download convert clean run_dbt profiling notebook dashboard

all: download convert clean run_dbt dashboard

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  help       : Affiche cette aide"
	@echo "  all        : Télécharge, convertit, nettoie, exécute dbt et lance le dashboard"
	@echo "  download   : Télécharge les données (scripts/download_kaggle.py)"
	@echo "  convert    : Convertit les données csv en parquet (scripts/convert_to_parquet.py)"
	@echo "  clean      : Nettoie les fichiers parquet (scripts/clean_parquet.py)"
	@echo "  run_dbt    : Exécute les modèles dbt (scripts/run_dbt.py)"
	@echo "  profiling  : Lance le script de profiling (scripts/profiling_2015.py)"
	@echo "  notebook   : Exécute quelques notebooks (nbconvert --execute)"
	@echo "  dashboard  : Lance le dashboard Streamlit (dashboard/app.py)"

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