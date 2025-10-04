"""
Dashboard AIS que lee datos desde SQL Server.
Este script demuestra la integración completa con base de datos.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pyodbc
import warnings
warnings.filterwarnings('ignore')

def connect_to_database():
    """Conecta a la base de datos SQL Server."""
    try:
        # Configuración de conexión
        server = 'localhost'
        database = 'ais_database'
        driver = '{ODBC Driver 17 for SQL Server}'
        
        connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        conn = pyodbc.connect(connection_string)
        
        print("✓ Conexión a SQL Server establecida")
        return conn
        
    except Exception as e:
        print(f"✗ Error de conexión: {e}")
        print("Asegúrate de que SQL Server esté ejecutándose y ejecuta database_setup.py")
        return None

def load_data_from_database():
    """Carga los datos desde la base de datos SQL Server."""
    
    conn = connect_to_database()
    if not conn:
        return None
    
    try:
        # Query para cargar todos los datos
        query = """
        SELECT gap_id, mmsi, vessel_class, flag, vessel_length_m, vessel_tonnage_gt,
               gap_start_timestamp, gap_start_lat, gap_start_lon, gap_start_distance_from_shore_m,
               gap_end_timestamp, gap_end_lat, gap_end_lon, gap_end_distance_from_shore_m, gap_hours
        FROM ais_disabling_events
        """
        
        df = pd.read_sql(query, conn)
        
        # Convertir timestamps a datetime
        df['gap_start_timestamp'] = pd.to_datetime(df['gap_start_timestamp'])
        df['gap_end_timestamp'] = pd.to_datetime(df['gap_end_timestamp'])
        
        # Extraer año y mes
        df['year'] = df['gap_start_timestamp'].dt.year
        df['month'] = df['gap_start_timestamp'].dt.month
        df['year_month'] = df['gap_start_timestamp'].dt.to_period('M')
        
        print(f"✓ Datos cargados desde SQL Server: {len(df)} registros")
        print(f"✓ Período: {df['gap_start_timestamp'].min()} a {df['gap_start_timestamp'].max()}")
        print(f"✓ Países únicos: {df['flag'].nunique()}")
        print(f"✓ Barcos únicos: {df['mmsi'].nunique()}")
        
        conn.close()
        return df
        
    except Exception as e:
        print(f"✗ Error al cargar datos: {e}")
        conn.close()
        return None

def create_dashboard(df):
    """Crea el dashboard interactivo con los datos de la base de datos."""
    
    # Calcular KPIs
    total_eventos = len(df)
    barcos_unicos = df['mmsi'].nunique()
    duracion_promedio = df['gap_hours'].mean()
    distancia_promedio = df['gap_start_distance_from_shore_m'].mean()
    
    print("=" * 60)
    print("📊 KPIs DEL DASHBOARD AIS (DESDE SQL SERVER)")
    print("=" * 60)
    print(f"🚢 Total de Eventos: {total_eventos:,}")
    print(f"⚓ Barcos Únicos: {barcos_unicos:,}")
    print(f"⏱️ Duración Promedio: {duracion_promedio:.2f} horas")
    print(f"🌊 Distancia Promedio: {distancia_promedio/1000:.2f} km")
    print("=" * 60)
    
    # Dashboard con KPIs integrados
    dashboard = make_subplots(
        rows=4, cols=2,
        specs=[[{"type":"indicator"}, {"type":"indicator"}],
               [{"type":"indicator"}, {"type":"indicator"}],
               [{"type":"xy"}, {"type":"xy"}],
               [{"type":"xy"}, {"type":"xy"}]],
        row_heights=[0.15, 0.15, 0.35, 0.35],
        subplot_titles=("Total Eventos", "Barcos Únicos", "Duración Promedio", "Distancia Promedio",
                       "Top 10 Países", "Top Banderas: Tipos de Embarcación", 
                       "Evolución Temporal", "Eventos por Mes vs Duración Promedio"),
        vertical_spacing=0.06,
        horizontal_spacing=0.1
    )
    
    # Agregar KPIs
    dashboard.add_trace(go.Indicator(
        mode="number",
        value=total_eventos,
        title={"text": ""},
        number={"valueformat": ",.0f"}
    ), row=1, col=1)
    
    dashboard.add_trace(go.Indicator(
        mode="number",
        value=barcos_unicos,
        title={"text": ""},
        number={"valueformat": ",.0f"}
    ), row=1, col=2)
    
    dashboard.add_trace(go.Indicator(
        mode="number",
        value=duracion_promedio,
        title={"text": ""},
        number={"valueformat": ".2f"}
    ), row=2, col=1)
    
    dashboard.add_trace(go.Indicator(
        mode="number",
        value=distancia_promedio/1000,
        title={"text": ""},
        number={"valueformat": ".2f"}
    ), row=2, col=2)
    
    # Gráfico 1: Top 10 países
    df_countries = df['flag'].value_counts().head(10).reset_index()
    df_countries.columns = ['flag', 'eventos']
    fig_bar = px.bar(df_countries, x="eventos", y="flag", orientation='h')
    for tr in fig_bar.data:
        dashboard.add_trace(tr, row=3, col=1)
    
    # Gráfico 2: Top banderas con tipos de embarcación
    df_cross = df.groupby(['flag', 'vessel_class']).size().reset_index(name='eventos')
    top_flags = df['flag'].value_counts().head(6).index
    top_vessels = df['vessel_class'].value_counts().head(6).index
    df_filtered = df_cross[
        (df_cross['flag'].isin(top_flags)) & 
        (df_cross['vessel_class'].isin(top_vessels))
    ]
    fig_cross = px.bar(df_filtered, x="flag", y="eventos", color="vessel_class",
                      color_discrete_sequence=px.colors.qualitative.Set3)
    for tr in fig_cross.data:
        dashboard.add_trace(tr, row=3, col=2)
    
    # Gráfico 3: Evolución temporal
    df_temporal = df.groupby('year', as_index=False).size()
    df_temporal.columns = ['year', 'eventos']
    fig_line = px.line(df_temporal, x="year", y="eventos", markers=True)
    fig_line.update_layout(
        xaxis=dict(
            tickmode='linear',
            tick0=2017,
            dtick=1,
            tickformat='d'
        )
    )
    for tr in fig_line.data:
        dashboard.add_trace(tr, row=4, col=1)
    
    # Gráfico 4: Eventos por mes vs duración promedio
    df_monthly_stats = df.groupby('month').agg({
        'mmsi': 'count',
        'gap_hours': 'mean'
    }).reset_index()
    df_monthly_stats.columns = ['month', 'eventos', 'duracion_promedio']
    meses_nombres = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun',
                    7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}
    df_monthly_stats['mes_nombre'] = df_monthly_stats['month'].map(meses_nombres)
    
    fig_scatter = px.scatter(
        df_monthly_stats, 
        x="eventos", 
        y="duracion_promedio",
        color="eventos",
        size="eventos",
        hover_data=['mes_nombre'],
        title="Eventos por Mes vs Duración Promedio",
        color_continuous_scale="Reds"
    )
    for tr in fig_scatter.data:
        dashboard.add_trace(tr, row=4, col=2)
    
    # Actualizar layout
    dashboard.update_layout(
        title="Dashboard AIS - Datos desde SQL Server",
        height=1200,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.45,
            xanchor="left",
            x=1.05
        ),
        margin=dict(l=50, r=120, t=80, b=40),
        coloraxis=dict(
            colorbar=dict(
                yanchor="bottom",
                y=0.08,
                xanchor="left",
                x=1.05,
                len=0.20,
                title="Eventos"
            )
        )
    )
    
    # Actualizar ejes
    dashboard.update_xaxes(title_text="Número de Eventos", row=3, col=1)
    dashboard.update_yaxes(title_text="País", row=3, col=1)
    
    dashboard.update_xaxes(title_text="Bandera (País)", row=3, col=2)
    dashboard.update_yaxes(title_text="Número de Eventos", row=3, col=2)
    
    dashboard.update_xaxes(title_text="Año", row=4, col=1, tickformat='d')
    dashboard.update_yaxes(title_text="Número de Eventos", row=4, col=1)
    
    dashboard.update_xaxes(title_text="Número de Eventos por Mes", row=4, col=2)
    dashboard.update_yaxes(title_text="Duración Promedio (horas)", row=4, col=2)
    
    return dashboard

def main():
    """Función principal."""
    print("=== Dashboard AIS - Integración con SQL Server ===")
    print("Cargando datos desde la base de datos...")
    
    # Cargar datos desde SQL Server
    df = load_data_from_database()
    if df is None:
        print("No se pudieron cargar los datos. Ejecuta database_setup.py primero.")
        return
    
    # Crear dashboard
    dashboard = create_dashboard(df)
    
    # Mostrar dashboard
    dashboard.show()
    
    # Exportar a HTML
    from pathlib import Path
    out = Path("dashboard_ais_sql.html")
    dashboard.write_html(str(out), include_plotlyjs="cdn", full_html=True)
    print(f"✓ Dashboard exportado a: {out.absolute()}")

if __name__ == "__main__":
    main()
