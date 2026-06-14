# Page de comparaison entre compagnies

import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DB_PATH = r"C:\Users\hp7\Desktop\Projet-Data-Visualization\us-airline-performance-analysis-2009-2018\data\airline_performance.duckdb"

def get_connection():
    try:
        conn = duckdb.connect(DB_PATH)
        return conn
    except Exception as e:
        st.error(f"Erreur de connexion: {e}")
        return None

def load_comparison_data(conn, carrier1, carrier2):
    df1 = conn.execute("SELECT year, otp_percentage, cancellation_rate FROM mart_otp_annual WHERE carrier_name = ? ORDER BY year", [carrier1]).fetchdf()
    df1['carrier'] = carrier1
    df2 = conn.execute("SELECT year, otp_percentage, cancellation_rate FROM mart_otp_annual WHERE carrier_name = ? ORDER BY year", [carrier2]).fetchdf()
    df2['carrier'] = carrier2
    df = pd.concat([df1, df2], ignore_index=True)
    df = df.rename(columns={'otp_percentage': 'otp_pct'})
    return df

def load_delay_comparison(conn, carrier1, carrier2, year):
    df1 = conn.execute("SELECT pct_carrier, pct_weather, pct_nas, pct_security, pct_late_aircraft FROM mart_delay_causes WHERE carrier_name = ? AND year = ?", [carrier1, year]).fetchdf()
    df1['carrier'] = carrier1
    df2 = conn.execute("SELECT pct_carrier, pct_weather, pct_nas, pct_security, pct_late_aircraft FROM mart_delay_causes WHERE carrier_name = ? AND year = ?", [carrier2, year]).fetchdf()
    df2['carrier'] = carrier2
    return pd.concat([df1, df2], ignore_index=True)

def load_all_carriers(conn):
    df = conn.execute("SELECT carrier_name, AVG(otp_percentage) as avg_otp FROM mart_otp_annual GROUP BY carrier_name ORDER BY avg_otp DESC").fetchdf()
    df = df.rename(columns={'carrier_name': 'iata_code'})
    return df

def display_otp_comparison(df):
    st.subheader("Comparaison OTP sur 10 ans")
    fig = px.line(df, x="year", y="otp_pct", color="carrier", title="Evolution du taux de ponctualite", labels={"otp_pct": "OTP (%)", "year": "Annee", "carrier": "Compagnie"}, markers=True)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

def display_delay_comparison(df, year):
    st.subheader(f"Comparaison des causes de retard - {year}")
    cause_columns = ['pct_carrier', 'pct_weather', 'pct_nas', 'pct_security', 'pct_late_aircraft']
    df_melted = df.melt(id_vars=['carrier'], value_vars=cause_columns, var_name='cause', value_name='percentage')
    df_melted['cause'] = df_melted['cause'].map({'pct_carrier': 'Carrier', 'pct_weather': 'Weather', 'pct_nas': 'NAS', 'pct_security': 'Security', 'pct_late_aircraft': 'Late Aircraft'})
    fig = px.bar(df_melted, x="carrier", y="percentage", color="cause", title=f"Decomposition des retards - {year}", labels={"percentage": "Pourcentage (%)", "carrier": "Compagnie", "cause": "Cause"}, barmode="group")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

def display_ranking_table(df_all):
    st.subheader("Classement general des compagnies (moyenne 2009-2018)")
    df_all['rank'] = range(1, len(df_all) + 1)
    df_all = df_all[['rank', 'iata_code', 'avg_otp']]
    df_all.columns = ['Rang', 'Compagnie', 'OTP Moyen (%)']
    st.dataframe(df_all, use_container_width=True)

def main():
    st.set_page_config(page_title="Comparaison", layout="wide")
    st.title("Comparaison entre Compagnies")
    st.markdown("---")
    
    conn = get_connection()
    if conn is None:
        st.stop()
    
    carriers = conn.execute("SELECT carrier_name FROM mart_delay_causes GROUP BY carrier_name ORDER BY carrier_name").fetchdf()
    carrier_list = carriers['carrier_name'].tolist()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        carrier1 = st.selectbox("Premiere compagnie", carrier_list, index=0)
    with col2:
        carrier2 = st.selectbox("Deuxieme compagnie", carrier_list, index=1 if len(carrier_list) > 1 else 0)
    with col3:
        year = st.selectbox("Annee", range(2009, 2019), index=9)
    
    df_comparison = load_comparison_data(conn, carrier1, carrier2)
    df_delay_comp = load_delay_comparison(conn, carrier1, carrier2, year)
    df_all_carriers = load_all_carriers(conn)
    
    display_otp_comparison(df_comparison)
    st.markdown("---")
    display_delay_comparison(df_delay_comp, year)
    st.markdown("---")
    display_ranking_table(df_all_carriers)
    
    conn.close()

if __name__ == "__main__":
    main()
