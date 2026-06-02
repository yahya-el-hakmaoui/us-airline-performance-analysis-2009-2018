.PHONY: all help config install download convert clean run_dbt profiling notebook dashboard

all: config install download convert #clean run_dbt dashboard

help:
	@echo "Utilisez python 3.10 ou 3.11"
	@echo 
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  help       : Affiche cette aide"
	@echo "  all        : Installation, téléchargement, conversion, nettoyage, dbt et dashboard"
	@echo "  install    : Installe les dépendances Python depuis requirements.txt"
	@echo "  download   : Verifier la presence des données (scripts/download_kaggle.py)"
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

config:
	@echo "============================================================"
	@echo "                      Configuration"
	@echo "============================================================"
	@echo "Assurez-vous que les chemins dans le fichier .env sont corrects :"
	@echo "   - DATA_RAW_PATH: chemin vers les fichiers CSV bruts"
	@echo "   - DATA_PARQUET_RAW_PATH: chemin vers les fichiers Parquet bruts"
	@echo "   - DATA_PARQUET_CLEAN_PATH: chemin vers les fichiers Parquet nettoyés"
	@echo "   - DUCKDB_PATH: chemin vers la base de données DuckDB"
	@echo 
	@echo "Utilisez python 3.10 ou 3.11"
	@echo "utiliser git bash ou WSL2 si vous utilisez Windows"
	@echo "============================================================"
	@echo "                  Configuration terminée"
	@echo "============================================================"
	@echo
	@sleep 5

install:
	@echo "============================================================"
	@echo "          Installation des dépendances Python"
	@echo "============================================================"
	@echo "Utilisez python 3.10 ou 3.11"
	@sleep 3
	pip install -r requirements.txt
	@echo "Installation terminée."
	@echo "============================================================"
	@echo "          Installation terminée avec succès!"
	@echo "============================================================"
	@echo
	@sleep 3

download:
	@echo "============================================================"
	@echo "             VÉRIFICATION DES DONNÉES KAGGLE"
	@echo "============================================================"
	python scripts/download_kaggle.py
	@echo "============================================================"
	@echo "       SUCCÈS - Tous les fichiers CSV sont présents!"
	@echo "============================================================"
	@echo
	@sleep 3

convert:
	@echo "============================================================"
	@echo "          Conversion des données CSV en Parquet"
	@echo "============================================================"
	python scripts/convert_to_parquet.py
	@echo "============================================================"
	@echo "          Conversion terminée avec succès!"
	@echo "============================================================"
	@echo
	@sleep 3

clean:
	@echo "============================================================"
	@echo "          Nettoyage des fichiers Parquet"
	@echo "============================================================"
	python scripts/clean_parquet.py
	@echo "============================================================"
	@echo "          Nettoyage terminé avec succès!"
	@echo "============================================================"
	@echo
	@sleep 3

run_dbt:
	@echo "============================================================"
	@echo "          Exécution des modèles dbt"
	@echo "============================================================"
	python scripts/run_dbt.py
	@echo "============================================================"
	@echo "          dbt terminé avec succès!"
	@echo "============================================================"
	@echo
	@sleep 3

profiling:
	@echo "============================================================"
	@echo "          Profiling des données 2015"
	@echo "============================================================"
	python scripts/profiling_2015.py
	@echo "============================================================"
	@echo "          Profiling terminé avec succès!"
	@echo "============================================================"
	@echo


notebook:
	@echo "============================================================"
	@echo "          Exécution des notebooks Jupyter"
	@echo "============================================================"
	jupyter nbconvert --to notebook --execute notebooks/audit/01_schema_audit.ipynb
	jupyter nbconvert --to notebook --execute notebooks/analysis/AX1_benchmarking.ipynb
	jupyter nbconvert --to notebook --execute notebooks/analysis/AX2_delay_causes.ipynb
	@echo "============================================================"
	@echo "          Notebooks exécutés avec succès!"
	@echo "============================================================"
	@echo

dashboard:
	@echo "============================================================"
	@echo "          Lancement du dashboard Streamlit"
	@echo "============================================================"
	streamlit run dashboard/app.py
	@echo "============================================================"
	@echo "          Dashboard lancé avec succès!"
	@echo "============================================================"
	@echo
	@sleep 3