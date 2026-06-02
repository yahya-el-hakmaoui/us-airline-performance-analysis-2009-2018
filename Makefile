.PHONY: all help install download convert clean run_dbt profiling notebook dashboard

all: install download convert clean run_dbt dashboard

help:
	@echo "Utilisez python 3.10 ou 3.11"
	@echo 
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  help       : Affiche cette aide"
	@echo "  all        : Installation, téléchargement, conversion, nettoyage, dbt et dashboard"
	@echo "  install    : Installe les dépendances Python depuis requirements.txt"
	@echo "  download   : Télécharge les données (scripts/download_kaggle.py)"
	@echo "  convert    : Convertit les données csv en parquet (scripts/convert_to_parquet.py)"
	@echo "  clean      : Nettoie les fichiers parquet (scripts/clean_parquet.py)"
	@echo "  run_dbt    : Exécute les modèles dbt (scripts/run_dbt.py)"
	@echo "  profiling  : Lance le script de profiling (scripts/profiling_2015.py)"
	@echo "  notebook   : Exécute quelques notebooks (nbconvert --execute)"
	@echo "  dashboard  : Lance le dashboard Streamlit (dashboard/app.py)"
	@echo ""
	@echo "-------------------------------------------------------------------"
	@echo "WINDOWS UTILISATEURS : Utilisez 'make' avec l'un des shells suivants :"
	@echo "  1. Git Bash (recommandé) : inclus avec Git for Windows"
	@echo "  2. WSL2 (Windows Subsystem for Linux)"
	@echo "  3. PowerShell + 'make' via Chocolatey : 'choco install make'"
	@echo ""
	@echo "Alternative sans make (commandes manuelles) :"
	@echo "  pip install -r requirements.txt"
	@echo "  python scripts/download_kaggle.py"
	@echo "  python scripts/convert_to_parquet.py"
	@echo "  streamlit run dashboard/app.py"
	@echo "-------------------------------------------------------------------"

install:
	@echo "Installation des dépendances Python..."
	@echo "Utilisez python 3.10 ou 3.11"
	pip install -r requirements.txt
	@echo "Installation terminée."

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