# Dashboard Interactivo de Eventos AIS

Este proyecto implementa un dashboard interactivo para analizar eventos de deshabilitación del sistema AIS (Automatic Identification System) de embarcaciones. El dashboard permite explorar patrones geográficos, temporales y por tipo de embarcación usando visualizaciones interactivas con Plotly.

## 📊 Dataset Seleccionado

**Dataset**: AIS Disabling Events  
**Fuente**: Global Fishing Watch  
**Descripción**: Contiene información sobre eventos donde los barcos han deshabilitado temporalmente su sistema AIS, incluyendo coordenadas geográficas, timestamps, duración del evento, y metadatos del barco.

### Campos del Dataset:
- `gap_id`: Identificador único del evento
- `mmsi`: Identificación única del barco
- `vessel_class`: Clase de embarcación
- `flag`: Bandera del país
- `vessel_length_m`: Longitud del barco en metros
- `vessel_tonnage_gt`: Tonelaje del barco
- `gap_start_timestamp`: Timestamp de inicio del evento
- `gap_start_lat/lon`: Coordenadas de inicio
- `gap_start_distance_from_shore_m`: Distancia desde la costa al inicio
- `gap_end_timestamp`: Timestamp de fin del evento
- `gap_end_lat/lon`: Coordenadas de fin
- `gap_end_distance_from_shore_m`: Distancia desde la costa al fin
- `gap_hours`: Duración del evento en horas

## 🗄️ Base de Datos

**Motor**: SQL Server 
**Justificación**: SQL Server Management Studio permite un análisis robusto de datos estructurados con excelente rendimiento para consultas complejas y reportes.

### Estructura:
- **Base de datos**: `ais_database`
- **Tabla**: `ais_disabling_events`
- **Índices sugeridos**: MMSI, flag, vessel_class, gap_start_timestamp, gap_end_timestamp

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- SQL Server Management Studio
- Jupyter Notebook

### 1. Configurar SQL Server (Opcional)

El dashboard funciona directamente con el archivo CSV, pero si deseas usar SQL Server:

```sql
-- Crear base de datos
CREATE DATABASE ais_database;

-- Crear tabla (estructura sugerida)
CREATE TABLE ais_disabling_events (
    gap_id VARCHAR(50),
    mmsi BIGINT,
    vessel_class VARCHAR(50),
    flag VARCHAR(10),
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
);
```

### 2. Clonar el Repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd TP_ProgAvanzada
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar la Base de Datos
```bash
# Cargar datos a SQL Server (requerido para el ciclo completo)
python database_setup.py
```

**Nota**: Este paso es obligatorio para cumplir con los requisitos del trabajo práctico.

## 📈 Ejecutar el Dashboard

### Opción 1: Dashboard con SQL Server (Recomendado)
```bash
python ais_dashboard_sql.py
```

### Opción 2: Dashboard con CSV (Jupyter Notebook)
```bash
jupyter notebook ais_dashboard_new.ipynb
```

### Opción 3: JupyterLab
```bash
jupyter lab ais_dashboard_new.ipynb
```

## 🎛️ Funcionalidades del Dashboard

### Dashboard Interactivo con Plotly
El dashboard incluye visualizaciones interactivas similares al ejemplo de Gapminder:

### Visualizaciones Principales

1. **KPIs (Indicadores Clave)**
   - Total de eventos
   - Barcos únicos involucrados
   - Duración promedio de eventos
   - Distancia promedio desde costa

2. **Evolución Temporal**
   - Gráfico de línea mostrando tendencias anuales
   - Identificación de patrones temporales

3. **Top 10 Países por Eventos**
   - Ranking horizontal de países
   - Visualización clara de los países más activos

4. **Eventos por Mes vs Duración Promedio**
   - Scatter plot interactivo por mes
   - Análisis de correlación entre volumen y duración
   - Hover con información del mes

5. **Dashboard Principal**
   - Layout combinado con KPIs y gráficos
   - Controles interactivos integrados

### Controles Interactivos
- **Hover Information**: Detalles al pasar el mouse sobre puntos y barras
- **Zoom y Pan**: Navegación en gráficos
- **Exportación**: Dashboard exportable a HTML

### Estadísticas Resumen
- Total de eventos mostrados
- Número de barcos únicos
- Número de países únicos
- Duración promedio y máxima
- Distancia promedio desde costa
- Top 5 barcos con más eventos

## 📁 Estructura del Proyecto

```
TP_ProgAvanzada/
├── data/
│   └── ais_disabling_events.csv      # Dataset original
├── ais_dashboard_new.ipynb           # Dashboard interactivo principal
├── database_setup.py                 # Script de configuración de BD
├── run_dashboard.py                  # Script para ejecutar dashboard
├── requirements.txt                  # Dependencias de Python
└── README.md                         # Este archivo
```

## 🔧 Troubleshooting

### Error de Conexión a SQL Server
```bash
# Verificar que SQL Server esté ejecutándose
# Windows - Servicios
services.msc
# Buscar "SQL Server" y verificar que esté "En ejecución"

# O usar SQL Server Configuration Manager
# Iniciar SQL Server (MSSQLSERVER)
```

### Error de Dependencias
```bash
# Reinstalar dependencias
pip install --upgrade -r requirements.txt
```

### Error de Permisos en Windows
- Ejecutar PowerShell como Administrador
- Verificar políticas de ejecución: `Set-ExecutionPolicy RemoteSigned`

## 📊 Insights del Dataset

### Hallazgos Principales:
1. **Concentración Geográfica**: Los eventos se concentran en ciertas rutas marítimas
2. **Patrones Temporales**: Variaciones estacionales en la actividad
3. **Tipos de Embarcaciones**: Diferentes comportamientos por clase de barco
4. **Duración de Eventos**: Mayoría de eventos cortos, algunos muy largos

### Casos de Uso:
- **Monitoreo Marítimo**: Identificar zonas de alta actividad
- **Análisis de Cumplimiento**: Detectar posibles violaciones
- **Investigación**: Patrones de comportamiento de flotas
- **Regulación**: Información para políticas marítimas

## 🤝 Contribuciones

Este proyecto es parte de un trabajo académico. Para contribuciones:
1. Fork el repositorio
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Crear un Pull Request

## 📄 Licencia

Este proyecto es para fines educativos. El dataset original pertenece a Global Fishing Watch.

## 📞 Contacto

Para preguntas sobre este proyecto, contactar al autor del repositorio.

---

**Nota**: El dashboard funciona directamente con el archivo CSV. SQL Server es opcional para análisis más avanzados. El script `database_setup.py` puede ejecutarse si deseas cargar los datos a SQL Server.
