"""
Script d execution dbt pour DuckDB
Execution: python scripts/run_dbt.py
"""

import os
import sys
import subprocess
from pathlib import Path

# Configuration des chemins
PROJECT_ROOT = Path(__file__).parent.parent
DBT_DIR = PROJECT_ROOT / "dbt"

def check_dbt_installation():
    """Verifie que dbt est installe"""
    try:
        subprocess.run(["dbt", "--version"], capture_output=True, check=True)
        print("[OK] dbt est installe")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[INFO] dbt non trouve. Installation via pip...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "dbt-duckdb"], check=True)
            print("[OK] dbt-duckdb installe avec succes")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[ERREUR] Impossible d installer dbt: {e}")
            return False

def check_parquet_files():
    """Verifie que les fichiers Parquet nettoyes existent"""
    clean_dir = PROJECT_ROOT / "data" / "parquet_clean"
    if not clean_dir.exists():
        print("[ERREUR] Dossier data/parquet_clean inexistant")
        print("        Lancez d abord: python scripts/clean_parquet.py")
        return False
    
    parquet_files = list(clean_dir.glob("*_clean.parquet"))
    if len(parquet_files) == 0:
        print("[ERREUR] Aucun fichier Parquet trouve dans data/parquet_clean/")
        print("        Lancez d abord: python scripts/clean_parquet.py")
        return False
    
    print(f"[OK] {len(parquet_files)} fichiers Parquet trouves")
    return True

def create_dbt_project_files():
    """Cree les fichiers dbt manquants"""
    
    # dbt_project.yml
    dbt_project_yml = DBT_DIR / "dbt_project.yml"
    if not dbt_project_yml.exists():
        dbt_project_yml.write_text("""
name: airline_performance
version: 1.0.0
config-version: 2

profile: airline_performance

model-paths: ["models"]
seed-paths: ["seeds"]
test-paths: ["tests"]
analysis-paths: ["analyses"]
macro-paths: ["macros"]

target-path: "target"
clean-targets:
    - "target"
    - "dbt_modules"

models:
  airline_performance:
    staging:
      +materialized: view
    gold:
      +materialized: table
""")
        print("[OK] dbt/dbt_project.yml cree")
    
    # profiles.yml
    profiles_yml = DBT_DIR / "profiles.yml"
    if not profiles_yml.exists():
        profiles_yml.write_text("""
airline_performance:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: ../data/airline_performance.duckdb
      extensions:
        - httpfs
        - parquet
""")
        print("[OK] dbt/profiles.yml cree")
    
    # models/staging/schema.yml
    schema_yml = DBT_DIR / "models" / "staging" / "schema.yml"
    schema_yml.parent.mkdir(parents=True, exist_ok=True)
    if not schema_yml.exists():
        schema_yml.write_text("""
version: 2

models:
  - name: stg_flights
    description: Union des 10 annees de vols
    columns:
      - name: year
        description: Annee du vol
      - name: iata_code
        description: Code IATA de la compagnie
      - name: arr_delay
        description: Retard a l arrivee en minutes
      - name: cancelled
        description: 1 si vol annule, 0 sinon
""")
        print("[OK] dbt/models/staging/schema.yml cree")
    
    # models/staging/stg_flights.sql
    stg_flights_sql = DBT_DIR / "models" / "staging" / "stg_flights.sql"
    if not stg_flights_sql.exists():
        stg_flights_sql.write_text("""
{{ config(materialized='view') }}

{% set years = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018] %}
{% set union_query = [] %}

{% for year in years %}
  {% set union_query = union_query.append("
    SELECT
      " ~ year ~ " AS year,
      MONTH,
      QUARTER,
      DAY_OF_MONTH,
      DAY_OF_WEEK,
      OP_UNIQUE_CARRIER AS iata_code,
      ORIGIN,
      DEST,
      CRS_DEP_TIME,
      DEP_TIME,
      DEP_DELAY,
      ARR_TIME,
      ARR_DELAY,
      ARR_DELAY_NEW,
      ARR_DEL15,
      CANCELLED,
      CANCELLATION_CODE,
      DIVERTED,
      CARRIER_DELAY,
      WEATHER_DELAY,
      NAS_DELAY,
      SECURITY_DELAY,
      LATE_AIRCRAFT_DELAY,
      DISTANCE
    FROM read_parquet('../data/parquet_clean/" ~ year ~ "_clean.parquet')
  ") %}
{% endfor %}

{{ union_query | join(' UNION ALL ') }}
""")
        print("[OK] dbt/models/staging/stg_flights.sql cree")
    
    # models/staging/dim_carrier.sql
    dim_carrier_sql = DBT_DIR / "models" / "staging" / "dim_carrier.sql"
    if not dim_carrier_sql.exists():
        dim_carrier_sql.write_text("""
{{ config(materialized='table') }}

SELECT DISTINCT
    iata_code,
    MIN(year) AS active_from,
    MAX(year) AS active_to,
    COUNT(*) AS total_years
FROM {{ ref('stg_flights') }}
GROUP BY iata_code
ORDER BY iata_code
""")
        print("[OK] dbt/models/staging/dim_carrier.sql cree")
    
    # models/gold/fact_flights.sql
    fact_flights_sql = DBT_DIR / "models" / "gold" / "fact_flights.sql"
    fact_flights_sql.parent.mkdir(parents=True, exist_ok=True)
    if not fact_flights_sql.exists():
        fact_flights_sql.write_text("""
{{ config(materialized='table') }}

SELECT
    {{ dbt_utils.generate_surrogate_key(['year', 'iata_code', 'ORIGIN', 'DEST', 'CRS_DEP_TIME']) }} AS flight_key,
    year,
    iata_code AS carrier_key,
    ORIGIN AS origin_key,
    DEST AS dest_key,
    ARR_DELAY_NEW AS arr_delay,
    DEP_DELAY AS dep_delay,
    ARR_DEL15,
    CANCELLED,
    CANCELLATION_CODE,
    DIVERTED,
    CARRIER_DELAY,
    WEATHER_DELAY,
    NAS_DELAY,
    SECURITY_DELAY,
    LATE_AIRCRAFT_DELAY,
    DISTANCE
FROM {{ ref('stg_flights') }}
""")
        print("[OK] dbt/models/gold/fact_flights.sql cree")
    
    # models/gold/mart_otp_annual.sql
    mart_otp_sql = DBT_DIR / "models" / "gold" / "mart_otp_annual.sql"
    if not mart_otp_sql.exists():
        mart_otp_sql.write_text("""
{{ config(materialized='table') }}

SELECT
    iata_code,
    year,
    COUNT(*) AS total_flights,
    SUM(CASE WHEN ARR_DEL15 = 0 AND CANCELLED = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS otp_pct,
    AVG(CASE WHEN ARR_DELAY_NEW > 0 THEN ARR_DELAY_NEW ELSE NULL END) AS avg_arr_delay_delayed_only,
    SUM(CASE WHEN CANCELLED = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS cancellation_rate,
    SUM(CARRIER_DELAY) AS total_carrier_delay,
    SUM(WEATHER_DELAY) AS total_weather_delay,
    SUM(NAS_DELAY) AS total_nas_delay,
    SUM(SECURITY_DELAY) AS total_security_delay,
    SUM(LATE_AIRCRAFT_DELAY) AS total_late_aircraft_delay
FROM {{ ref('stg_flights') }}
GROUP BY iata_code, year
ORDER BY iata_code, year
""")
        print("[OK] dbt/models/gold/mart_otp_annual.sql cree")
    
    # models/gold/mart_benchmarking.sql
    mart_benchmark_sql = DBT_DIR / "models" / "gold" / "mart_benchmarking.sql"
    if not mart_benchmark_sql.exists():
        mart_benchmark_sql.write_text("""
{{ config(materialized='table') }}

WITH otp_rank AS (
    SELECT iata_code, year, otp_pct,
           ROW_NUMBER() OVER (PARTITION BY year ORDER BY otp_pct DESC) AS otp_rank
    FROM {{ ref('mart_otp_annual') }}
),
delay_rank AS (
    SELECT iata_code, year, avg_arr_delay_delayed_only,
           ROW_NUMBER() OVER (PARTITION BY year ORDER BY avg_arr_delay_delayed_only ASC) AS delay_rank
    FROM {{ ref('mart_otp_annual') }}
),
cancel_rank AS (
    SELECT iata_code, year, cancellation_rate,
           ROW_NUMBER() OVER (PARTITION BY year ORDER BY cancellation_rate ASC) AS cancel_rank
    FROM {{ ref('mart_otp_annual') }}
)
SELECT
    o.iata_code,
    o.year,
    o.otp_pct,
    o.otp_rank,
    d.delay_rank,
    c.cancel_rank,
    (o.otp_rank * 0.5 + d.delay_rank * 0.3 + c.cancel_rank * 0.2) AS composite_score
FROM otp_rank o
LEFT JOIN delay_rank d ON o.iata_code = d.iata_code AND o.year = d.year
LEFT JOIN cancel_rank c ON o.iata_code = c.iata_code AND o.year = c.year
ORDER BY o.iata_code, o.year
""")
        print("[OK] dbt/models/gold/mart_benchmarking.sql cree")
    
    # models/gold/mart_delay_causes.sql
    mart_delays_sql = DBT_DIR / "models" / "gold" / "mart_delay_causes.sql"
    if not mart_delays_sql.exists():
        mart_delays_sql.write_text("""
{{ config(materialized='table') }}

SELECT
    iata_code,
    year,
    SUM(CARRIER_DELAY) AS total_carrier_delay,
    SUM(WEATHER_DELAY) AS total_weather_delay,
    SUM(NAS_DELAY) AS total_nas_delay,
    SUM(SECURITY_DELAY) AS total_security_delay,
    SUM(LATE_AIRCRAFT_DELAY) AS total_late_aircraft_delay,
    SUM(CARRIER_DELAY + WEATHER_DELAY + NAS_DELAY + SECURITY_DELAY + LATE_AIRCRAFT_DELAY) AS total_delay_minutes,
    SUM(CARRIER_DELAY) * 100.0 / NULLIF(SUM(CARRIER_DELAY + WEATHER_DELAY + NAS_DELAY + SECURITY_DELAY + LATE_AIRCRAFT_DELAY), 0) AS pct_carrier,
    SUM(WEATHER_DELAY) * 100.0 / NULLIF(SUM(CARRIER_DELAY + WEATHER_DELAY + NAS_DELAY + SECURITY_DELAY + LATE_AIRCRAFT_DELAY), 0) AS pct_weather,
    SUM(NAS_DELAY) * 100.0 / NULLIF(SUM(CARRIER_DELAY + WEATHER_DELAY + NAS_DELAY + SECURITY_DELAY + LATE_AIRCRAFT_DELAY), 0) AS pct_nas,
    SUM(SECURITY_DELAY) * 100.0 / NULLIF(SUM(CARRIER_DELAY + WEATHER_DELAY + NAS_DELAY + SECURITY_DELAY + LATE_AIRCRAFT_DELAY), 0) AS pct_security,
    SUM(LATE_AIRCRAFT_DELAY) * 100.0 / NULLIF(SUM(CARRIER_DELAY + WEATHER_DELAY + NAS_DELAY + SECURITY_DELAY + LATE_AIRCRAFT_DELAY), 0) AS pct_late_aircraft
FROM {{ ref('stg_flights') }}
GROUP BY iata_code, year
ORDER BY iata_code, year
""")
        print("[OK] dbt/models/gold/mart_delay_causes.sql cree")

def run_dbt():
    """Execute les commandes dbt"""
    os.chdir(DBT_DIR)
    
    print("\n[1/3] Nettoyage des anciennes cibles...")
    subprocess.run(["dbt", "clean"], capture_output=True)
    
    print("[2/3] Execution des models dbt...")
    result = subprocess.run(["dbt", "run"], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("[ERREUR] dbt run a echoue")
        print(result.stderr)
        return False
    
    print(result.stdout)
    
    print("[3/3] Generation de la documentation...")
    subprocess.run(["dbt", "docs", "generate"], capture_output=True)
    
    print("\n[SUCCES] Base de donnees creee: data/airline_performance.duckdb")
    return True

def main():
    print("=" * 60)
    print("EXECUTION DBT - PERFORMANCE AERIENNE")
    print("=" * 60)
    
    if not check_parquet_files():
        sys.exit(1)
    
    if not check_dbt_installation():
        sys.exit(1)
    
    create_dbt_project_files()
    
    if run_dbt():
        print("\n" + "=" * 60)
        print("SUCCES - Dashboard pret a etre lance")
        print("=" * 60)
        print("\nLancez maintenant:")
        print("  streamlit run dashboard/app.py")
    else:
        print("\n" + "=" * 60)
        print("ERREUR - Veuillez corriger les erreurs ci-dessus")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
