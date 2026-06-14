"""
Dashboard Principal - Performance des Compagnies Aeriennes
"""

import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

DB_PATH = r"C:\Users\hp7\Desktop\Projet-Data-Visualization\us-airline-performance-analysis-2009-2018\data\airline_performance.duckdb"

CONNECTION = None

def get_connection():
    global CONNECTION
    if CONNECTION is None:
        try:
            import os
            if not os.path.exists(DB_PATH):
                st.error(f"Base non trouvee: {DB_PATH}")
                return None
            CONNECTION = duckdb.connect(DB_PATH)
            st.success("Connexion reussie")
        except Exception as e:
            st.error(f"Erreur: {e}")
            CONNECTION = None
    return CONNECTION

def load_carriers(conn):
    df = conn.execute("SELECT carrier_name FROM mart_otp_annual GROUP BY carrier_name ORDER BY carrier_name").fetchdf()
    return df['carrier_name'].tolist()

def load_otp_data(conn, carrier_list=None, year_start=2009, year_end=2018):
    query = """
        SELECT carrier_name, year, otp_percentage, cancellation_rate, avg_arr_delay
        FROM mart_otp_annual
        WHERE year BETWEEN ? AND ?
    """
    params = [year_start, year_end]
    
    if carrier_list:
        placeholders = ','.join(['?'] * len(carrier_list))
        query += f" AND carrier_name IN ({placeholders})"
        params.extend(carrier_list)
    
    query += " ORDER BY carrier_name, year"
    
    df = conn.execute(query, params).fetchdf()
    df = df.rename(columns={'carrier_name': 'iata_code', 'otp_percentage': 'otp_pct'})
    return df

def load_total_flights(conn):
    try:
        df = conn.execute("SELECT COUNT(*) as total FROM stg_flights").fetchdf()
        return df['total'].iloc[0]
    except:
        try:
            df = conn.execute("SELECT SUM(total_flights) as total FROM mart_otp_annual").fetchdf()
            return df['total'].iloc[0] if df['total'].iloc[0] else 0
        except:
            return 0

def setup_page():
    st.set_page_config(page_title="Performance Aerienne USA", page_icon=":airplane:", layout="wide")

def create_sidebar(conn):
    with st.sidebar:
        st.title("Filtres")
        
        carriers = load_carriers(conn)
        
        selected_carriers = st.multiselect(
            "Compagnies",
            options=carriers,
            default=carriers[:5] if len(carriers) >= 5 else carriers
        )
        
        year_range = st.slider(
            "Periode",
            min_value=2009,
            max_value=2018,
            value=(2009, 2018)
        )
        
        st.markdown("---")
        st.caption("Source: BTS/DOT 2009-2018")
        
        return selected_carriers, year_range

def display_kpi_cards(df_otp, total_flights):
    col1, col2, col3, col4 = st.columns(4)
    
    avg_otp = df_otp['otp_pct'].mean()
    col1.metric("OTP Moyen", f"{avg_otp:.1f}%")
    
    df_2018 = df_otp[df_otp['year'] == 2018]
    if not df_2018.empty:
        best_carrier = df_2018.loc[df_2018['otp_pct'].idxmax(), 'iata_code']
        best_otp = df_2018['otp_pct'].max()
        col2.metric("Meilleur OTP 2018", f"{best_carrier} ({best_otp:.1f}%)")
    
    avg_cancel = df_otp['cancellation_rate'].mean()
    col3.metric("Taux Annulation", f"{avg_cancel:.2f}%")
    
    if total_flights > 0:
        col4.metric("Total Vols", f"{total_flights/1e6:.1f}M")
    else:
        col4.metric("Total Vols", "Calcul en cours")

def display_otp_trend(df_otp):
    st.subheader("Evolution de la Ponctualite")
    
    fig = px.line(
        df_otp,
        x="year",
        y="otp_pct",
        color="iata_code",
        title="Taux de ponctualite par compagnie (2009-2018)",
        labels={"otp_pct": "OTP (%)", "year": "Annee", "iata_code": "Compagnie"},
        markers=True
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

def display_data_table(df_otp):
    with st.expander("Donnees detaillees"):
        st.dataframe(df_otp, use_container_width=True)

def main():
    setup_page()
    
    st.title("Observatoire de la Performance Operationnelle")
    st.markdown("### Compagnies Aeriennes Americaines | 2009-2018")
    st.markdown("---")
    
    conn = get_connection()
    if conn is None:
        st.stop()
    
    selected_carriers, year_range = create_sidebar(conn)
    
    df_otp = load_otp_data(conn, selected_carriers, year_range[0], year_range[1])
    total_flights = load_total_flights(conn)
    
    if df_otp.empty:
        st.warning("Aucune donnee pour les filtres selectionnes.")
        st.stop()
    
    display_kpi_cards(df_otp, total_flights)
    st.markdown("---")
    display_otp_trend(df_otp)
    display_data_table(df_otp)

if __name__ == "__main__":
    main()
