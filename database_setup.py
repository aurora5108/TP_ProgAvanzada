"""
Script para configurar la base de datos SQL Server y cargar los datos del dataset AIS.
Este script crea las tablas y carga los datos del archivo CSV.
"""

import pandas as pd
import pyodbc
import os
from pathlib import Path

def setup_database():
    """Configura la conexión a SQL Server y crea la base de datos."""
    
    # Configuración de conexión (ajustar según tu instalación)
    server = 'localhost'  # o tu servidor SQL Server
    database = 'ais_database'
    driver = '{ODBC Driver 17 for SQL Server}'  # Ajustar según tu versión
    
    try:
        # Conexión a SQL Server
        connection_string = f'DRIVER={driver};SERVER={server};DATABASE=master;Trusted_Connection=yes;'
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # Crear base de datos si no existe
        cursor.execute(f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{database}') CREATE DATABASE {database}")
        conn.commit()
        print(f"Base de datos '{database}' creada o verificada")
        
        conn.close()
        
        # Conectar a la base de datos específica
        connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        return conn, cursor
        
    except Exception as e:
        print(f"Error de conexión: {e}")
        print("Asegúrate de que SQL Server esté ejecutándose y la conexión sea correcta")
        return None, None

def create_table(cursor):
    """Crea la tabla para los eventos AIS."""
    
    create_table_sql = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ais_disabling_events' AND xtype='U')
    CREATE TABLE ais_disabling_events (
        gap_id NVARCHAR(50),
        mmsi BIGINT,
        vessel_class NVARCHAR(50),
        flag NVARCHAR(10),
        vessel_length_m FLOAT,
        vessel_tonnage_gt FLOAT,
        gap_start_timestamp DATETIME,
        gap_start_lat FLOAT,
        gap_start_lon FLOAT,
        gap_start_distance_from_shore_m FLOAT,
        gap_end_timestamp DATETIME,
        gap_end_lat FLOAT,
        gap_end_lon FLOAT,
        gap_end_distance_from_shore_m FLOAT,
        gap_hours FLOAT
    )
    """
    
    cursor.execute(create_table_sql)
    print("Tabla 'ais_disabling_events' creada o verificada")

def load_data_to_database(csv_file_path, cursor, conn):
    """Carga los datos del CSV a SQL Server."""
    
    print(f"Cargando datos desde: {csv_file_path}")
    
    # Leer el archivo CSV
    df = pd.read_csv(csv_file_path)
    
    print(f"Datos cargados: {len(df)} registros")
    print(f"Columnas: {list(df.columns)}")
    
    # Limpiar la tabla existente
    cursor.execute("DELETE FROM ais_disabling_events")
    
    # Insertar los datos
    for index, row in df.iterrows():
        insert_sql = """
        INSERT INTO ais_disabling_events 
        (gap_id, mmsi, vessel_class, flag, vessel_length_m, vessel_tonnage_gt,
         gap_start_timestamp, gap_start_lat, gap_start_lon, gap_start_distance_from_shore_m,
         gap_end_timestamp, gap_end_lat, gap_end_lon, gap_end_distance_from_shore_m, gap_hours)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        cursor.execute(insert_sql, 
                      row['gap_id'], row['mmsi'], row['vessel_class'], row['flag'],
                      row['vessel_length_m'], row['vessel_tonnage_gt'],
                      row['gap_start_timestamp'], row['gap_start_lat'], row['gap_start_lon'],
                      row['gap_start_distance_from_shore_m'],
                      row['gap_end_timestamp'], row['gap_end_lat'], row['gap_end_lon'],
                      row['gap_end_distance_from_shore_m'], row['gap_hours'])
    
    conn.commit()
    print(f"Datos insertados exitosamente: {len(df)} registros")

def create_indexes(cursor):
    """Crea índices para mejorar el rendimiento de las consultas."""
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_mmsi ON ais_disabling_events(mmsi)",
        "CREATE INDEX IF NOT EXISTS idx_flag ON ais_disabling_events(flag)",
        "CREATE INDEX IF NOT EXISTS idx_vessel_class ON ais_disabling_events(vessel_class)",
        "CREATE INDEX IF NOT EXISTS idx_gap_start_timestamp ON ais_disabling_events(gap_start_timestamp)",
        "CREATE INDEX IF NOT EXISTS idx_gap_end_timestamp ON ais_disabling_events(gap_end_timestamp)"
    ]
    
    for index_sql in indexes:
        try:
            cursor.execute(index_sql)
        except:
            pass  # Índice ya existe o error menor
    
    print("Índices creados exitosamente")

def verify_data(cursor):
    """Verifica que los datos se cargaron correctamente."""
    
    # Contar registros
    cursor.execute("SELECT COUNT(*) FROM ais_disabling_events")
    total_records = cursor.fetchone()[0]
    print(f"Total de registros en la base de datos: {total_records}")
    
    # Estadísticas básicas
    print("\n=== Estadísticas de la base de datos ===")
    
    # Top 5 banderas
    cursor.execute("""
        SELECT TOP 5 flag, COUNT(*) as eventos 
        FROM ais_disabling_events 
        GROUP BY flag 
        ORDER BY eventos DESC
    """)
    
    print("\nTop 5 banderas por número de eventos:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} eventos")
    
    # Clases de embarcación
    cursor.execute("""
        SELECT vessel_class, COUNT(*) as eventos 
        FROM ais_disabling_events 
        GROUP BY vessel_class 
        ORDER BY eventos DESC
    """)
    
    print("\nEventos por clase de embarcación:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} eventos")

def main():
    """Función principal para configurar la base de datos."""
    
    try:
        # Configurar base de datos
        conn, cursor = setup_database()
        if not conn:
            return
        
        print("Conexión a SQL Server establecida")
        
        # Ruta al archivo CSV
        csv_path = "data/ais_disabling_events.csv"
        
        if not os.path.exists(csv_path):
            print(f"Error: No se encontró el archivo {csv_path}")
            return
        
        # Crear tabla
        create_table(cursor)
        
        # Cargar datos
        load_data_to_database(csv_path, cursor, conn)
        
        # Crear índices
        create_indexes(cursor)
        
        # Verificar la carga
        verify_data(cursor)
        
        print("\nBase de datos configurada exitosamente!")
        print("Ahora puedes ejecutar el dashboard que leerá desde SQL Server")
        
        conn.close()
        
    except Exception as e:
        print(f"Error al configurar la base de datos: {e}")
        print("Asegúrate de que SQL Server esté ejecutándose y pyodbc esté instalado")

if __name__ == "__main__":
    main()
