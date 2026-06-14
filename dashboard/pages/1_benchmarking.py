# Page AX1 - Benchmarking OTP

import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "airline_performance.duckdb"

def get_connection():
    try:
        conn = duckdb.connect(str(DB_PATH))
        return conn
    except Exception as e:
        st.error(f"Erreur de connexion: {e}")
        return None

def load_benchmarking_data(conn, year):
    df = conn.execute("""
        SELECT carrier_name, year, otp_percentage, cancellation_rate, avg_arr_delay
        FROM mart_otp_annual
        WHERE year = ?
        ORDER BY otp_percentage DESC
    """, [year]).fetchdf()
    df = df.rename(columns={'carrier_name': 'iata_code', 'otp_percentage': 'otp_pct'})
    return df

def load_ranking_history(conn):
    df = conn.execute("""
        SELECT carrier_name, year, otp_percentage
        FROM mart_otp_annual
        ORDER BY carrier_name, year
    """).fetchdf()
    return df

def display_lollipop_chart(df, year):
    st.subheader(f"Classement OTP {year}")
    
    fig = px.bar(
        df,
        x="iata_code",
        y="otp_pct",
        title=f"Taux de ponctualite par compagnie - {year}",
        labels={"otp_pct": "OTP (%)", "iata_code": "Compagnie"},
        color="otp_pct",
        color_continuous_scale="Viridis"
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df[['iata_code', 'otp_pct']], use_container_width=True)

def display_bump_chart(df):
    st.subheader("Evolution du Classement OTP (2009-2018)")
    
    df_pivot = df.pivot(index='year', columns='carrier_name', values='otp_percentage')
    
    for col in df_pivot.columns:
        df_pivot[f'rank_{col}'] = df_pivot[col].rank(ascending=False, method='min')
    
    df_rank = pd.DataFrame()
    for col in df_pivot.columns:
        if col.startswith('rank_'):
            carrier = col.replace('rank_', '')
            temp = df_pivot[[col]].copy()
            temp.columns = ['rank']
            temp['carrier'] = carrier
            temp['year'] = temp.index
            df_rank = pd.concat([df_rank, temp])
    
    fig = px.line(
        df_rank,
        x="year",
        y="rank",
        color="carrier",
        title="Evolution des rangs OTP sur la decennie",
        labels={"rank": "Classement (1=meilleur)", "year": "Annee", "carrier": "Compagnie"},
        markers=True
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.set_page_config(page_title="Benchmarking OTP", layout="wide")
    st.title("Axe 1 - Benchmarking OTP et Classement")
    st.markdown("---")
    
    conn = get_connection()
    if conn is None:
        st.stop()
    
    year = st.selectbox("Selectionner une annee", range(2009, 2019), index=9)
    df_benchmark = load_benchmarking_data(conn, year)
    df_ranking = load_ranking_history(conn)
    
    display_lollipop_chart(df_benchmark, year)
    st.markdown("---")
    display_bump_chart(df_ranking)
    
    conn.close()

if __name__ == "__main__":
    main()
