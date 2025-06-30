import streamlit as st
import pandas as pd
import itertools
import random

st.set_page_config(
    page_title="Generador de Equipos Balanceados", 
    page_icon="⚽", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado para interfaz simple
st.markdown("""
<style>
    /* Ocultar sidebar completamente */
    .css-1d391kg {
        display: none;
    }
    
    /* Botones más grandes y llamativos */
    .stButton > button {
        width: 100%;
        height: 4rem;
        font-size: 1.3rem;
        font-weight: bold;
        border-radius: 10px;
    }
    
    /* Contenedor principal más centrado */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Títulos más grandes */
    h1 {
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        text-align: center;
        font-size: 2rem;
        margin: 1rem 0;
    }
    
    /* Progress bar más visible */
    .stProgress .st-bo {
        height: 2rem;
    }
    
    /* Selectbox más grande */
    .stSelectbox {
        font-size: 1.2rem;
    }
    
    /* Dataframe más legible */
    .stDataFrame {
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Base de datos de jugadores predefinida
DEFAULT_PLAYERS = {
    "David": {"speed": 7, "strength": 6, "shooting": 7, "dribble": 7, "liderazgo": 6},
    "Dan": {"speed": 4, "strength": 8, "shooting": 6, "dribble": 5, "liderazgo": 3},
    "Diego": {"speed": 7, "strength": 7, "shooting": 5, "dribble": 5, "liderazgo": 5},
    "Morales": {"speed": 6, "strength": 6, "shooting": 6, "dribble": 7, "liderazgo": 6},
    "Buco": {"speed": 5, "strength": 6, "shooting": 6, "dribble": 5, "liderazgo": 9},
    "Joao": {"speed": 5, "strength": 6, "shooting": 6, "dribble": 5, "liderazgo": 4},
    "Nestor": {"speed": 5, "strength": 5, "shooting": 5, "dribble": 5, "liderazgo": 5},
    "Nico": {"speed": 6, "strength": 6, "shooting": 8, "dribble": 6, "liderazgo": 4},
    "Ribery": {"speed": 8, "strength": 6, "shooting": 8, "dribble": 8, "liderazgo": 7},
    "Sergio": {"speed": 7, "strength": 7, "shooting": 6, "dribble": 7, "liderazgo": 5}
}

# Initialize session state
if 'players' not in st.session_state:
    st.session_state.players = {}

# TÍTULO PRINCIPAL
st.title("⚽ Generador de Equipos")
st.markdown("### 🤖 *Cuando el humano falla, vente al verdadero algoritmo.*")

# PASO 1: AGREGAR JUGADORES
st.header("👥 PASO 1: Agrega Jugadores")

# Botones principales de carga
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🚀 CARGAR TODOS LOS JUGADORES", type="primary", use_container_width=True):
        st.session_state.players = DEFAULT_PLAYERS.copy()
        st.success("¡10 jugadores cargados!")
        st.rerun()

with col2:
    if st.button("🗑️ LIMPIAR TODO", type="secondary", use_container_width=True):
        st.session_state.players = {}
        if 'team_results' in st.session_state:
            del st.session_state.team_results
        st.rerun()

with col3:
    # Botón de completar automático si faltan jugadores
    if len(st.session_state.players) > 0 and len(st.session_state.players) < 10:
        remaining = 10 - len(st.session_state.players)
        if st.button(f"➕ COMPLETAR ({remaining} más)", use_container_width=True):
            available = [name for name in DEFAULT_PLAYERS.keys() if name not in st.session_state.players]
            needed = min(remaining, len(available))
            for i in range(needed):
                player_name = available[i]
                st.session_state.players[player_name] = DEFAULT_PLAYERS[player_name].copy()
            st.success(f"¡{needed} jugadores agregados!")
            st.rerun()

# Contador de progreso prominente
if st.session_state.players:
    progress = len(st.session_state.players) / 10
    st.progress(progress)
    
    if len(st.session_state.players) >= 10:
        st.success(f"🎯 ¡{len(st.session_state.players)} jugadores listos! Puedes generar equipos.")
    else:
        remaining = 10 - len(st.session_state.players)
        st.warning(f"⏰ Tienes {len(st.session_state.players)} jugadores. Faltan {remaining} para generar equipos.")
else:
    st.progress(0)
    st.info("📝 Comienza agregando jugadores")

# Agregar jugadores individuales (simple)
if len(st.session_state.players) < 10:
    available_players = [name for name in DEFAULT_PLAYERS.keys() if name not in st.session_state.players]
    
    if available_players:
        st.write("**O agrega jugadores uno por uno:**")
        
        # Crear botones para cada jugador disponible
        cols = st.columns(min(5, len(available_players)))
        for i, player in enumerate(available_players):
            with cols[i % 5]:
                if st.button(f"➕ {player}", key=f"add_{player}", use_container_width=True):
                    st.session_state.players[player] = DEFAULT_PLAYERS[player].copy()
                    st.success(f"¡{player} agregado!")
                    st.rerun()

# PASO 2: VER JUGADORES (si hay alguno)
if st.session_state.players:
    st.markdown("---")
    st.header("📋 PASO 2: Tus Jugadores")
    
    # Mostrar tabla de jugadores
    df_players = pd.DataFrame.from_dict(st.session_state.players, orient='index')
    df_players.index.name = 'Jugador'
    df_players['Total'] = df_players.sum(axis=1)
    
    # Renombrar columnas para mejor visualización
    df_display = df_players.copy()
    df_display.columns = ['🏃 Velocidad', '💪 Fuerza', '⚽ Disparo', '🎯 Regate', '👑 Liderazgo', '📊 Total']
    
    st.dataframe(df_display, use_container_width=True)
    
    # Opción simple para eliminar jugadores
    st.write("**¿Quieres quitar algún jugador?**")
    cols_remove = st.columns(min(5, len(st.session_state.players)))
    for i, player in enumerate(st.session_state.players.keys()):
        with cols_remove[i % 5]:
            if st.button(f"❌ {player}", key=f"remove_{player}", use_container_width=True):
                del st.session_state.players[player]
                st.success(f"{player} eliminado")
                st.rerun()

# PASO 3: GENERAR EQUIPOS
if len(st.session_state.players) >= 10:
    st.markdown("---")
    st.header("🎲 PASO 3: Generar Equipos")
    
    # Botón súper prominente para generar equipos
    if st.button("🎲 GENERAR EQUIPOS BALANCEADOS", type="primary", use_container_width=True, key="generate_main"):
        # Algoritmo de generación de equipos
        def team_score(team, players_data):
            return sum(sum(players_data[name].values()) for name in team)
        
        def compute_team_averages(team, df):
            team_data = df.loc[team]
            return team_data.mean()
        
        players = list(st.session_state.players.keys())
        df = pd.DataFrame.from_dict(st.session_state.players, orient='index')
        
        best_diff = float('inf')
        best_splits = []
        
        # Encontrar la mejor combinación
        for combo in itertools.combinations(players, 5):
            team_a = list(combo)
            team_b = [p for p in players if p not in team_a]
            diff = abs(team_score(team_a, st.session_state.players) - team_score(team_b, st.session_state.players))
            if diff < best_diff:
                best_diff = diff
        
        # Recoger todas las combinaciones con diferencia mínima o muy cercana
        tolerance = 1
        for combo in itertools.combinations(players, 5):
            team_a = list(combo)
            team_b = [p for p in players if p not in team_a]
            diff = abs(team_score(team_a, st.session_state.players) - team_score(team_b, st.session_state.players))
            if diff <= best_diff + tolerance:
                best_splits.append((team_a, team_b, diff))
        
        # Seleccionar aleatoriamente una de las mejores
        team_a, team_b, actual_diff = random.choice(best_splits)
        
        # Calcular promedios
        team_a_avg = compute_team_averages(team_a, df)
        team_b_avg = compute_team_averages(team_b, df)
        team_a_total = team_score(team_a, st.session_state.players)
        team_b_total = team_score(team_b, st.session_state.players)
        
        # Guardar resultados
        st.session_state.team_results = {
            'team_a': team_a,
            'team_b': team_b,
            'team_a_avg': team_a_avg,
            'team_b_avg': team_b_avg,
            'team_a_total': team_a_total,
            'team_b_total': team_b_total,
            'actual_diff': actual_diff
        }
        
        st.success("¡Equipos generados! 🎉")
        st.balloons()

# MOSTRAR RESULTADOS
if 'team_results' in st.session_state:
    st.markdown("---")
    st.header("🏆 TUS EQUIPOS BALANCEADOS")
    
    results = st.session_state.team_results
    
    st.success(f"✅ Diferencia de puntos entre equipos: {results['actual_diff']}")
    
    # Mostrar equipos lado a lado
    col_team1, col_team2 = st.columns(2)
    
    with col_team1:
        st.subheader("🔵 EQUIPO A")
        st.info(f"**Total: {results['team_a_total']} puntos**")
        
        for name in results['team_a']:
            metrics = st.session_state.players[name]
            st.write(f"⚽ **{name}**")
            st.write(f"V:{metrics['speed']} F:{metrics['strength']} D:{metrics['shooting']} R:{metrics['dribble']} L:{metrics['liderazgo']}")
        
        st.write("**📊 Promedios:**")
        st.write(f"🏃 Velocidad: {results['team_a_avg']['speed']:.1f}")
        st.write(f"💪 Fuerza: {results['team_a_avg']['strength']:.1f}")
        st.write(f"⚽ Disparo: {results['team_a_avg']['shooting']:.1f}")
        st.write(f"🎯 Regate: {results['team_a_avg']['dribble']:.1f}")
        st.write(f"👑 Liderazgo: {results['team_a_avg']['liderazgo']:.1f}")
    
    with col_team2:
        st.subheader("🔴 EQUIPO B")
        st.info(f"**Total: {results['team_b_total']} puntos**")
        
        for name in results['team_b']:
            metrics = st.session_state.players[name]
            st.write(f"⚽ **{name}**")
            st.write(f"V:{metrics['speed']} F:{metrics['strength']} D:{metrics['shooting']} R:{metrics['dribble']} L:{metrics['liderazgo']}")
        
        st.write("**📊 Promedios:**")
        st.write(f"🏃 Velocidad: {results['team_b_avg']['speed']:.1f}")
        st.write(f"💪 Fuerza: {results['team_b_avg']['strength']:.1f}")
        st.write(f"⚽ Disparo: {results['team_b_avg']['shooting']:.1f}")
        st.write(f"🎯 Regate: {results['team_b_avg']['dribble']:.1f}")
        st.write(f"👑 Liderazgo: {results['team_b_avg']['liderazgo']:.1f}")
    
    # Botón para generar nuevos equipos
    if st.button("🔄 GENERAR OTROS EQUIPOS", use_container_width=True):
        # Reutilizar el mismo algoritmo
        def team_score(team, players_data):
            return sum(sum(players_data[name].values()) for name in team)
        
        def compute_team_averages(team, df):
            team_data = df.loc[team]
            return team_data.mean()
        
        players = list(st.session_state.players.keys())
        df = pd.DataFrame.from_dict(st.session_state.players, orient='index')
        
        best_diff = float('inf')
        best_splits = []
        
        for combo in itertools.combinations(players, 5):
            team_a = list(combo)
            team_b = [p for p in players if p not in team_a]
            diff = abs(team_score(team_a, st.session_state.players) - team_score(team_b, st.session_state.players))
            if diff < best_diff:
                best_diff = diff
        
        tolerance = 1
        for combo in itertools.combinations(players, 5):
            team_a = list(combo)
            team_b = [p for p in players if p not in team_a]
            diff = abs(team_score(team_a, st.session_state.players) - team_score(team_b, st.session_state.players))
            if diff <= best_diff + tolerance:
                best_splits.append((team_a, team_b, diff))
        
        team_a, team_b, actual_diff = random.choice(best_splits)
        team_a_avg = compute_team_averages(team_a, df)
        team_b_avg = compute_team_averages(team_b, df)
        team_a_total = team_score(team_a, st.session_state.players)
        team_b_total = team_score(team_b, st.session_state.players)
        
        st.session_state.team_results = {
            'team_a': team_a,
            'team_b': team_b,
            'team_a_avg': team_a_avg,
            'team_b_avg': team_b_avg,
            'team_a_total': team_a_total,
            'team_b_total': team_b_total,
            'actual_diff': actual_diff
        }
        
        st.rerun()

# Instrucciones simples al final
with st.expander("❓ ¿Cómo funciona?"):
    st.markdown("""
    ### Es súper fácil:
    
    1. **🚀 Cargar Todos** - Agrega automáticamente 10 jugadores predefinidos
    2. **🎲 Generar Equipos** - Crea equipos balanceados automáticamente  
    3. **🏆 ¡Listo!** - Ve tus equipos y empieza a jugar
    
    ### ¿Qué hace el algoritmo?
    - Calcula **todas las combinaciones posibles** de equipos
    - Encuentra la división más **equilibrada** 
    - Te da equipos con diferencias **mínimas** de habilidades
    
    ### Jugadores incluidos:
    David, Dan, Diego, Morales, Buco, Joao, Nestor, Nico, Ribery, Sergio
    """)

# Ocultar el sidebar con contenido mínimo
st.sidebar.write("App simplificada")
st.sidebar.write("Todo está en la pantalla principal 👆") 