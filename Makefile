# Makefile pour Windows (CMD/PowerShell)
# Installation: choco install make OU scoop install make

.PHONY: all help config install download convert clean run_dbt profiling notebook dashboard

MAKEFLAGS += --silent

all:
	@echo ============================================================
	@echo                    PIPELINE COMPLET
	@echo ============================================================
	$(MAKE) config
	$(MAKE) install
	$(MAKE) download
	$(MAKE) convert
	$(MAKE) clean
	$(MAKE) run_dbt
	$(MAKE) dashboard

help:
	@echo ============================================================
	@echo              COMMANDES MAKE POUR WINDOWS
	@echo ============================================================
	@echo.
	@echo Commandes disponibles:
	@echo   make help      : Afficher cette aide
	@echo   make all       : Executer tout le pipeline
	@echo   make config    : Verifier la configuration
	@echo   make install   : Installer les dependances Python
	@echo   make download  : Verifier les fichiers Kaggle
	@echo   make convert   : Convertir CSV en Parquet
	@echo   make clean     : Nettoyer les fichiers Parquet
	@echo   make run_dbt   : Executer les modeles dbt
	@echo   make profiling : Generer le rapport de profilage
	@echo   make notebook  : Executer les notebooks Jupyter
	@echo   make dashboard : Lancer le dashboard Streamlit
	@echo.
	@echo ------------------------------------------------------------
	@echo PREREQUIS:
	@echo   1. Python 3.10 ou 3.11 installe
	@echo   2. Fichier .env configure avec les bons chemins
	@echo   3. Fichiers CSV dans data/raw/ (2009.csv a 2018.csv)
	@echo ------------------------------------------------------------

config:
	@echo ============================================================
	@echo                    VERIFICATION CONFIGURATION
	@echo ============================================================
	@echo Verification du fichier .env...
	@if exist .env ( echo [OK] Fichier .env trouve ) else ( echo [ERREUR] Fichier .env manquant && exit 1 )
	@echo Creation des dossiers...
	@if not exist data\raw mkdir data\raw
	@if not exist data\parquet_raw mkdir data\parquet_raw
	@if not exist data\parquet_clean mkdir data\parquet_clean
	@if not exist data mkdir data
	@if not exist reports\profiling mkdir reports\profiling
	@if not exist notebooks\audit mkdir notebooks\audit
	@if not exist notebooks\analysis mkdir notebooks\analysis
	@if not exist dashboard\pages mkdir dashboard\pages
	@echo [OK] Configuration terminee
	@echo ============================================================
	@echo.

install:
	@echo ============================================================
	@echo              INSTALLATION DES DEPENDANCES PYTHON
	@echo ============================================================
	@echo Installation des paquets depuis requirements.txt...
	pip install -r requirements.txt
	@if %errorlevel% neq 0 ( echo [ERREUR] Echec de l installation && exit 1 )
	@echo [OK] Installation terminee
	@echo ============================================================
	@echo.

download:
	@echo ============================================================
	@echo              VERIFICATION DES FICHIERS KAGGLE
	@echo ============================================================
	python scripts/download_kaggle.py
	@if %errorlevel% neq 0 ( echo [ERREUR] Fichiers CSV manquants && exit 1 )
	@echo [OK] Verification terminee
	@echo ============================================================
	@echo.

convert:
	@echo ============================================================
	@echo              CONVERSION CSV VERS PARQUET
	@echo ============================================================
	python scripts/convert_to_parquet.py
	@if %errorlevel% neq 0 ( echo [ERREUR] Echec de la conversion && exit 1 )
	@echo [OK] Conversion terminee
	@echo ============================================================
	@echo.

clean:
	@echo ============================================================
	@echo              NETTOYAGE DES FICHIERS PARQUET
	@echo ============================================================
	python scripts/clean_parquet.py
	@if %errorlevel% neq 0 ( echo [ERREUR] Echec du nettoyage && exit 1 )
	@echo [OK] Nettoyage termine
	@echo ============================================================
	@echo.

run_dbt:
	@echo ============================================================
	@echo              EXECUTION DES MODELES DBT
	@echo ============================================================
	python scripts/run_dbt.py
	@if %errorlevel% neq 0 ( echo [ERREUR] Echec de l execution dbt && exit 1 )
	@echo [OK] Execution dbt terminee
	@echo ============================================================
	@echo.

profiling:
	@echo ============================================================
	@echo              PROFILAGE DE L ANNEE 2015
	@echo ============================================================
	python scripts/profiling_2015.py
	@if %errorlevel% neq 0 ( echo [ERREUR] Echec du profilage && exit 1 )
	@echo [OK] Profilage termine - rapport dans reports/profiling/
	@echo ============================================================
	@echo.

notebook:
	@echo ============================================================
	@echo              EXECUTION DES NOTEBOOKS JUPYTER
	@echo ============================================================
	jupyter nbconvert --to notebook --execute notebooks/audit/01_schema_audit.ipynb --output-dir notebooks/audit/
	jupyter nbconvert --to notebook --execute notebooks/analysis/AX1_benchmarking.ipynb --output-dir notebooks/analysis/
	jupyter nbconvert --to notebook --execute notebooks/analysis/AX2_delay_causes.ipynb --output-dir notebooks/analysis/
	@echo [OK] Execution des notebooks terminee
	@echo ============================================================
	@echo.

dashboard:
	@echo ============================================================
	@echo              LANCEMENT DU DASHBOARD STREAMLIT
	@echo ============================================================
	@echo Le dashboard va s ouvrir dans votre navigateur...
	@echo Appuyez sur Ctrl+C pour arreter
	@echo ============================================================
	streamlit run dashboard/app.py