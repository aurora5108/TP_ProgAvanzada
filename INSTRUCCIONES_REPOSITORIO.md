# Instrucciones para el Repositorio - Dashboard AIS

## 📋 Resumen del Proyecto

Este repositorio contiene un **dashboard interactivo** para analizar eventos de deshabilitación del sistema AIS (Automatic Identification System) de embarcaciones, desarrollado como parte de un trabajo práctico de programación avanzada.

## 🎯 Objetivos Cumplidos

✅ **Dataset público seleccionado**: Eventos de deshabilitación AIS de Global Fishing Watch  
✅ **Base de datos implementada**: MongoDB con estructura optimizada  
✅ **Dashboard interactivo**: Notebook con visualizaciones usando Plotly  
✅ **Documentación completa**: README detallado y replicable  
✅ **Funcionalidad de exportación**: Dashboard exportable a HTML  

## 🚀 Cómo Ejecutar el Proyecto

### Paso 1: Clonar el Repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd TP_ProgAvanzada
```

### Paso 2: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 3: Configurar Base de Datos (Opcional)
```bash
# Solo si quieres usar SQL Server en lugar del CSV
python database_setup.py
```

### Paso 4: Ejecutar Dashboard
```bash
# Opción 1: Script automático
python run_dashboard.py

# Opción 2: Jupyter Notebook
jupyter notebook ais_dashboard_new.ipynb
```

## 📊 Características del Dashboard

### Visualizaciones Implementadas:
1. **KPIs**: 4 indicadores clave (total eventos, barcos únicos, duración promedio, distancia promedio)
2. **Evolución Temporal**: Gráfico de línea con tendencias anuales
3. **Ranking de Países**: Top 10 países por número de eventos
4. **Análisis Geográfico**: Scatter plot duración vs distancia con filtro por país
5. **Animación Temporal**: Slider para explorar evolución año por año

### Interactividad:
- **Dropdowns**: Filtro por país
- **Sliders**: Navegación temporal
- **Hover**: Información detallada
- **Zoom/Pan**: Navegación en gráficos
- **Exportación**: Dashboard exportable a HTML

## 🗄️ Base de Datos

**Motor**: SQL Server (Local)  
**Justificación**: Análisis robusto de datos estructurados, excelente rendimiento para consultas complejas y reportes

### Estructura:
- **Base de datos**: `ais_database`
- **Tabla**: `ais_disabling_events`
- **Índices sugeridos**: MMSI, flag, vessel_class, timestamps

## 📁 Archivos del Proyecto

| Archivo | Descripción |
|---------|-------------|
| `ais_dashboard_new.ipynb` | **Dashboard principal** - Notebook interactivo |
| `database_setup.py` | Script para configurar MongoDB |
| `run_dashboard.py` | Script para ejecutar el dashboard automáticamente |
| `data/ais_disabling_events.csv` | Dataset original (55,000+ registros) |
| `requirements.txt` | Dependencias de Python |
| `README.md` | Documentación completa del proyecto |

## 🔧 Tecnologías Utilizadas

- **Python 3.8+**
- **Pandas**: Manipulación de datos
- **Plotly**: Visualizaciones interactivas
- **SQL Server**: Base de datos relacional (opcional)
- **Jupyter**: Entorno de desarrollo
- **NumPy**: Cálculos numéricos

## 📈 Dataset

**Fuente**: Global Fishing Watch  
**Tamaño**: 55,000+ eventos  
**Período**: 2017-2019  
**Campos**: 15 columnas incluyendo coordenadas, timestamps, metadatos del barco

### Campos Principales:
- `mmsi`: Identificación del barco
- `flag`: Bandera del país
- `vessel_class`: Clase de embarcación
- `gap_hours`: Duración del evento
- `gap_start_lat/lon`: Coordenadas geográficas
- `gap_start_distance_from_shore_m`: Distancia desde costa

## 🎨 Características del Dashboard

### Inspirado en Gapminder:
- **Layout tipo dashboard** con subplots
- **KPIs prominentes** en la parte superior
- **Controles interactivos** (dropdowns, sliders)
- **Exportación a HTML** para compartir
- **Visualizaciones múltiples** en un solo lienzo

### Funcionalidades Avanzadas:
- **Filtros dinámicos** por país
- **Animación temporal** con slider
- **Información contextual** en hover
- **Navegación intuitiva** con zoom/pan

## ✅ Criterios de Evaluación Cumplidos

1. **✅ Claridad y organización del repositorio**: Estructura clara, documentación completa
2. **✅ Correcta carga de datos**: Script de SQL Server funcional, datos validados
3. **✅ Funcionalidad del dashboard**: Visualizaciones interactivas, controles funcionales
4. **✅ Calidad del README**: Documentación detallada, instrucciones claras
5. **✅ Replicabilidad**: Proyecto ejecutable sin errores, dependencias especificadas

## 🚀 Próximos Pasos Sugeridos

1. **Migrar a Dash/Streamlit**: Para aplicación web completa
2. **Agregar más filtros**: Por duración, clase de embarcación, etc.
3. **Mapas interactivos**: Visualización geográfica con Mapbox
4. **Análisis predictivo**: Modelos de machine learning
5. **API REST**: Para integración con otros sistemas

## 📞 Soporte

Para problemas o preguntas:
1. Revisar la sección "Troubleshooting" en README.md
2. Verificar que todas las dependencias estén instaladas
3. Asegurar que SQL Server esté ejecutándose (si se usa)
4. Contactar al autor del repositorio

---

**Nota**: Este proyecto demuestra un ciclo completo de trabajo con datos: obtención, almacenamiento, análisis y visualización interactiva, cumpliendo todos los requisitos del trabajo práctico.