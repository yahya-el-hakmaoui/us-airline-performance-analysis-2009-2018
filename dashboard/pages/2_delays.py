# Page AX2 - Analyse des causes de retard

import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

DB_PATH = r"C:\Users\hp7\Desktop\Projet-Data-Visualization\us-airline-performance-analysis-2009-2018\data\airline_performance.duckdb"

def get_connection():
    try:
        conn = duckdb.connect(DB_PATH)
        return conn
    except Exception as e:
        st.error(f"Erreur de connexion: {e}")
        return None

def load_delay_causes_data(conn, year):
    df = conn.execute("""
        SELECT carrier_name, year, pct_carrier, pct_weather, pct_nas, 
               pct_security, pct_late_aircraft
        FROM mart_delay_causes
        WHERE year = ?
    """, [year]).fetchdf()
    df = df.rename(columns={'carrier_name': 'iata_code'})
    return df

def load_carrier_trend(conn, carrier, year_start=2009, year_end=2018):
    df = conn.execute("""
        SELECT year, pct_carrier, pct_weather, pct_nas, 
               pct_security, pct_late_aircraft
        FROM mart_delay_causes
        WHERE carrier_name = ? AND year BETWEEN ? AND ?
        ORDER BY year
    """, [carrier, year_start, year_end]).fetchdf()
    return df

def load_total_delays(conn):
    df = conn.execute("""
        SELECT 
            SUM(pct_carrier) as carrier_pct,
            SUM(pct_weather) as weather_pct,
            SUM(pct_nas) as nas_pct,
            SUM(pct_security) as security_pct,
            SUM(pct_late_aircraft) as late_aircraft_pct
        FROM mart_delay_causes
    """).fetchdf()
    return df

def display_stacked_bar(df, year):
    st.subheader(f"Decomposition des causes de retard - {year}")
    
    cause_columns = ['pct_carrier', 'pct_weather', 'pct_nas', 'pct_security', 'pct_late_aircraft']
    cause_labels = ['Carrier', 'Weather', 'NAS', 'Security', 'Late Aircraft']
    
    df_melted = df.melt(
        id_vars=['iata_code'], 
        value_vars=cause_columns,
        var_name='cause', 
        value_name='percentage'
    )
    
    df_melted['cause'] = df_melted['cause'].map({
        'pct_carrier': 'Carrier',
        'pct_weather': 'Weather', 
        'pct_nas': 'NAS',
        'pct_security': 'Security',
        'pct_late_aircraft': 'Late Aircraft'
    })
    
    fig = px.bar(
        df_melted,
        x="iata_code",
        y="percentage",
        color="cause",
        title=f"Causes de retard par compagnie - {year}",
        labels={"percentage": "Pourcentage (%)", "iata_code": "Compagnie", "cause": "Cause"},
        barmode="stack"
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

def display_carrier_trend(df, carrier):
    st.subheader(f"Evolution des causes - {carrier}")
    
    cause_columns = ['pct_carrier', 'pct_weather', 'pct_nas', 'pct_security', 'pct_late_aircraft']
    
    df_melted = df.melt(
        id_vars=['year'], 
        value_vars=cause_columns,
        var_name='cause', 
        value_name='percentage'
    )
    
    df_melted['cause'] = df_melted['cause'].map({
        'pct_carrier': 'Carrier',
        'pct_weather': 'Weather', 
        'pct_nas': 'NAS',
        'pct_security': 'Security',
        'pct_late_aircraft': 'Late Aircraft'
    })
    
    fig = px.line(
        df_melted,
        x="year",
        y="percentage",
        color="cause",
        title=f"Evolution des causes de retard - {carrier} (2009-2018)",
        labels={"percentage": "Pourcentage (%)", "year": "Annee", "cause": "Cause"},
        markers=True
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

def display_treemap(df_total):
    st.subheader("Repartition des retards par cause (2009-2018)")
    
    df_treemap = pd.DataFrame({
        'cause': ['Carrier', 'Weather', 'NAS', 'Security', 'Late Aircraft'],
        'percentage': [
            df_total['carrier_pct'].iloc[0],
            df_total['weather_pct'].iloc[0],
            df_total['nas_pct'].iloc[0],
            df_total['security_pct'].iloc[0],
            df_total['late_aircraft_pct'].iloc[0]
        ]
    })
    
    fig = px.treemap(
        df_treemap,
        path=['cause'],
        values='percentage',
        title="Repartition des causes de retard",
        labels={'percentage': 'Pourcentage (%)', 'cause': 'Cause'}
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.set_page_config(page_title="Analyse des Retards", layout="wide")
    st.title("Axe 2 - Analyse des Causes de Retard")
    st.markdown("---")
    
    conn = get_connection()
    if conn is None:
        st.stop()
    
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("Selectionner une annee", range(2009, 2019), index=9)
    with col2:
        carriers = conn.execute("SELECT carrier_name FROM mart_delay_causes GROUP BY carrier_name ORDER BY carrier_name").fetchdf()
        selected_carrier = st.selectbox("Selectionner une compagnie", carriers['carrier_name'].tolist())
    
    df_delays = load_delay_causes_data(conn, year)
    df_trend = load_carrier_trend(conn, selected_carrier)
    df_total = load_total_delays(conn)
    
    display_stacked_bar(df_delays, year)
    st.markdown("---")
    display_carrier_trend(df_trend, selected_carrier)
    st.markdown("---")
    display_treemap(df_total)
    
    conn.close()

if __name__ == "__main__":
    main()
