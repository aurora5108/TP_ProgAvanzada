# Guía de Evaluación - Dashboard AIS

Este repositorio contiene el trabajo práctico completo de programación avanzada: **Dashboard interactivo de eventos AIS**.

##  Instrucciones Rápidas de Evaluación

```bash
# 1. Clonar repositorio
git clone <URL_DEL_REPOSITORIO>
cd TP_ProgAvanzada

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar dashboard
jupyter notebook ais_dashboard_new.ipynb
```

## 📊 Dashboard Incluye

- **4 KPIs principales**: Total eventos, barcos únicos, duración y distancia promedio
- **4 visualizaciones**: Evolución temporal, ranking países, tipos de embarcación, scatter plot
- **Interactividad completa**: Hover, zoom, pan, exportación a HTML
- **Layout optimizado**: KPIs prominentes, gráficos bien distribuidos

## 🗄️ Base de Datos

- **Motor**: SQL Server (local)
- **Script**: `database_setup.py` para carga automática
- **Alternativa**: Dashboard funciona directamente con CSV

## 📁 Archivos Principales

- `ais_dashboard_new.ipynb` - **Dashboard principal**
- `database_setup.py` - Script de carga a BD
- `data/ais_disabling_events.csv` - Dataset (55,368 eventos)
- `README.md` - Documentación completa

---
