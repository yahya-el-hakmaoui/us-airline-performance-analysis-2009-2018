# Page A propos - Methodologie et sources

import streamlit as st

def main():
    st.set_page_config(page_title="A propos", layout="wide")
    
    st.title("A propos du projet")
    st.markdown("---")
    
    st.header("Contexte")
    st.write("""
    Ce projet analyse la performance operationnelle des compagnies aeriennes americaines 
    sur la periode 2009-2018. Les donnees proviennent du Bureau of Transportation Statistics (BTS) 
    et couvrent environ 68 millions de vols domestiques.
    """)
    
    st.header("Perimetre d'analyse")
    st.write("""
    **Axe 1: Benchmarking OTP et Classement**
    - Analyse du taux de ponctualite (OTP)
    - Classement des compagnies sur 10 ans
    - Score composite combinant OTP, annulations et retards
    
    **Axe 2: Causes de retard**
    - Decomposition des 5 causes officielles BTS
    - Evolution temporelle par compagnie
    - Identification des signatures operationnelles
    """)
    
    st.header("Architecture technique")
    st.write("""
    - Langage: Python 3.10
    - Moteur OLAP: DuckDB
    - Transformation: dbt (models SQL)
    - Visualisation: Streamlit + Plotly
    - Orchestration: Makefile
    """)
    
    st.header("Pipeline de donnees")
    st.write("""
    1. Telechargement des CSV depuis Kaggle
    2. Conversion CSV vers Parquet
    3. Nettoyage et verification des donnees
    4. Modelisation dbt (couche Gold)
    5. Dashboard interactif
    """)
    
    st.header("Definitions")
    
    st.subheader("OTP (On-Time Performance)")
    st.write("""
    Proportion de vols arrivant avec moins de 15 minutes de retard.
    C'est le KPI officiel du Department of Transportation.
    """)
    
    st.subheader("Causes de retard")
    st.write("""
    - Carrier Delay: Retard imputable a la compagnie (maintenance, equipage, nettoyage)
    - Weather Delay: Conditions meteorologiques extremes
    - NAS Delay: Systeme national de gestion du trafic aerien
    - Security Delay: Retards lies a la securite aeroportuaire
    - Late Aircraft Delay: Retard propage d'un vol precedent
    """)
    
    st.header("Sources")
    st.write("""
    - Dataset: Airline Delay and Cancellation Data (2009-2018)
    - Source: Kaggle / Bureau of Transportation Statistics (BTS/DOT)
    - Lien: https://www.kaggle.com/datasets/yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018
    """)
    
    st.header("Equipe")
    st.write("""
    - Personne 1: Infrastructure, audit, conversion Parquet
    - Personne 2: Profiling et nettoyage des donnees
    - Personne 3: Modelisation dbt et tables Gold
    - Personne 4: Documentation et notebooks EDA
    - Personne 5: Dashboard Streamlit et rapport final
    """)
    
    st.header("Limites")
    st.write("""
    - Donnees auto-declarees par les compagnies
    - Evolution des codes IATA post-fusions
    - Absence de donnees sur les causes externes (greves, evenements)
    - Exclusion des vols < 0.5% de part de marche
    """)
    
    st.markdown("---")
    st.caption("Projet Data Visualisation - Performance des Compagnies Aeriennes Americaines 2009-2018")

if __name__ == "__main__":
    main()
