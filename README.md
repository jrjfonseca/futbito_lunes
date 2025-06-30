# ⚽ Generador de Equipos Balanceados 5v5

Una aplicación web interactiva construida con Streamlit para generar equipos de fútbol balanceados basados en las habilidades de los jugadores.

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Python 3.8 o superior

### Pasos para ejecutar

1. **Clonar o descargar los archivos**
2. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación:**
   ```bash
   streamlit run app.py
   ```

4. **Abrir en el navegador:**
   - La aplicación se abrirá automáticamente en tu navegador
   - Si no, ve a: `http://localhost:8501`

## 📋 Cómo usar

### 1. Agregar Jugadores
- Usa la barra lateral para agregar jugadores
- Introduce el nombre y ajusta las métricas usando los sliders:
  - **Velocidad** (1-10): Rapidez del jugador
  - **Fuerza** (1-10): Potencia física
  - **Disparo** (1-10): Habilidad de tiro
  - **Regate** (1-10): Habilidad técnica
  - **Liderazgo** (1-10): Capacidad de liderazgo

### 2. Gestionar Jugadores
- Ver todos los jugadores en una tabla con sus métricas
- Editar jugadores existentes
- Eliminar jugadores
- Ver puntuación total de cada jugador

### 3. Generar Equipos
- Necesitas al menos **10 jugadores**
- Ajusta la **tolerancia** para permitir más variedad en los equipos
- Haz clic en "Generar Equipos" para crear equipos balanceados

### 4. Resultados
- Ve los equipos generados (Equipo A y Equipo B)
- Revisa los promedios de cada equipo por métrica
- Compara las diferencias entre equipos
- Genera nuevos equipos para obtener diferentes combinaciones

## 🎯 Características

- **Interface intuitiva**: Fácil de usar con sliders y botones
- **Equipos balanceados**: Algoritmo que minimiza las diferencias entre equipos
- **Variedad**: Sistema de tolerancia para generar diferentes combinaciones
- **Análisis completo**: Promedios y comparaciones detalladas
- **Gestión dinámica**: Agregar, editar y eliminar jugadores en tiempo real
- **Persistencia**: Los datos se mantienen durante la sesión

## 🔧 Tecnologías

- **Streamlit**: Framework para aplicaciones web
- **Pandas**: Manipulación de datos
- **Python**: Algoritmos de optimización

## 📈 Algoritmo

El algoritmo utiliza:
1. Generación de todas las combinaciones posibles de 5v5
2. Cálculo de diferencias en puntuación total
3. Selección de las mejores combinaciones (dentro de la tolerancia)
4. Selección aleatoria para variedad
5. Análisis detallado de métricas por equipo 