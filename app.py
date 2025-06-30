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

# CSS personalizado optimizado para móviles
st.markdown("""
<style>
    /* Ocultar sidebar completamente */
    .css-1d391kg {
        display: none;
    }
    
    /* Ocultar header de streamlit para más espacio */
    .css-18e3th9 {
        padding-top: 0rem;
    }
    
    /* Contenedor principal optimizado para móvil */
    .main .block-container {
        padding-top: 0.5rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
        margin: 0 auto;
    }
    
    /* Títulos compactos para móvil */
    h1 {
        text-align: center;
        font-size: 2rem;
        margin-bottom: 0.3rem;
        margin-top: 0rem;
    }
    
    h2 {
        text-align: center;
        font-size: 1.3rem;
        margin: 0.5rem 0;
        color: #1f77b4;
    }
    
    h3 {
        text-align: center;
        font-size: 1.1rem;
        margin: 0.3rem 0;
    }
    
    /* Botones optimizados para táctil móvil */
    .stButton > button {
        width: 100%;
        height: 3.5rem;
        font-size: 1rem;
        font-weight: bold;
        border-radius: 8px;
        margin: 0.2rem 0;
    }
    
    /* Progress bar compacta */
    .stProgress .st-bo {
        height: 1.5rem;
    }
    
    /* Selectbox compacto */
    .stSelectbox {
        font-size: 1rem;
    }
    
    /* Sliders más compactos */
    .stSlider {
        margin: 0.2rem 0;
    }
    
    /* Dataframe compacto y centrado */
    .stDataFrame {
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    
    /* Text input compacto */
    .stTextInput {
        margin: 0.3rem 0;
    }
    
    /* Expander más compacto */
    .streamlit-expanderHeader {
        font-size: 1rem;
    }
    
    /* Reducir espaciado entre elementos */
    .element-container {
        margin: 0.3rem 0;
    }
    
    /* Mensajes de success/error más compactos */
    .stAlert {
        margin: 0.3rem 0;
        padding: 0.5rem;
    }
    
    /* Columnas más compactas en móvil */
    @media (max-width: 768px) {
        .row-widget {
            margin: 0.2rem 0;
        }
        
        h1 {
            font-size: 1.8rem;
        }
        
        h2 {
            font-size: 1.2rem;
        }
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

# TÍTULO PRINCIPAL COMPACTO
st.title("⚽ Generador de Equipos")
st.markdown("<p style='text-align: center; color: #666; font-size: 0.9rem; margin-top: -1rem;'>🤖 <i>Algoritmo de equipos balanceados</i></p>", unsafe_allow_html=True)

# PASO 1: AGREGAR JUGADORES
st.markdown("<h2 style='text-align: center;'>👥 PASO 1: Agrega Jugadores</h2>", unsafe_allow_html=True)

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
        st.write("**O agrega jugadores predefinidos uno por uno:**")
        
        # Crear botones para cada jugador disponible
        cols = st.columns(min(5, len(available_players)))
        for i, player in enumerate(available_players):
            with cols[i % 5]:
                if st.button(f"➕ {player}", key=f"add_{player}", use_container_width=True):
                    st.session_state.players[player] = DEFAULT_PLAYERS[player].copy()
                    st.success(f"¡{player} agregado!")
                    st.rerun()

# Crear jugador personalizado - Compacto para móvil
st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

with st.expander("✨ Crear Jugador Personalizado", expanded=False):
    new_player_name = st.text_input("Nombre del nuevo jugador:", key="new_player_name")
    
    st.write("**Configura las habilidades (1-10):**")
    col_new1, col_new2 = st.columns(2)
    
    with col_new1:
        new_speed = st.slider("🏃 Velocidad", 1, 10, 5, key="new_speed")
        new_shooting = st.slider("⚽ Disparo", 1, 10, 5, key="new_shooting")
        new_leadership = st.slider("👑 Liderazgo", 1, 10, 5, key="new_leadership")
    
    with col_new2:
        new_strength = st.slider("💪 Fuerza", 1, 10, 5, key="new_strength")
        new_dribble = st.slider("🎯 Regate", 1, 10, 5, key="new_dribble")
    
    if st.button("🌟 CREAR JUGADOR", type="primary", use_container_width=True):
        if new_player_name and new_player_name not in st.session_state.players:
            st.session_state.players[new_player_name] = {
                'speed': new_speed,
                'strength': new_strength,
                'shooting': new_shooting,
                'dribble': new_dribble,
                'liderazgo': new_leadership
            }
            st.success(f"¡{new_player_name} creado exitosamente!")
            st.balloons()
            st.rerun()
        elif new_player_name in st.session_state.players:
            st.error(f"Ya existe un jugador llamado {new_player_name}")
        else:
            st.error("Por favor ingresa un nombre para el jugador")

# PASO 2: VER JUGADORES (aparece solo si hay jugadores)
if st.session_state.players:
    st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)
    
    # Centrar el título del paso 2
    st.markdown("<h2 style='text-align: center;'>📋 PASO 2: Gestiona Tus Jugadores</h2>", unsafe_allow_html=True)
    
    # Mostrar tabla de jugadores - Compacta para móvil
    df_players = pd.DataFrame.from_dict(st.session_state.players, orient='index')
    df_players.index.name = 'Jugador'
    df_players['Total'] = df_players.sum(axis=1)
    
    # Renombrar columnas para móvil (más cortas)
    df_display = df_players.copy()
    df_display.columns = ['🏃V', '💪F', '⚽D', '🎯R', '👑L', '📊T']
    
    st.dataframe(df_display, use_container_width=True, height=200)
    
    # Gestión de jugadores - Compacto para móvil
    with st.expander("✏️ Editar Jugador", expanded=False):
        if st.session_state.players:
            player_to_edit = st.selectbox(
                "Selecciona jugador:",
                ["Selecciona..."] + list(st.session_state.players.keys()),
                key="edit_selector"
            )
            
            if player_to_edit != "Selecciona...":
                current_stats = st.session_state.players[player_to_edit]
                
                st.markdown(f"**🎯 Editando: {player_to_edit}**")
                
                # Sliders compactos para editar
                edit_speed = st.slider("🏃 Velocidad", 1, 10, current_stats['speed'], key=f"edit_speed_{player_to_edit}")
                edit_strength = st.slider("💪 Fuerza", 1, 10, current_stats['strength'], key=f"edit_strength_{player_to_edit}")
                edit_shooting = st.slider("⚽ Disparo", 1, 10, current_stats['shooting'], key=f"edit_shooting_{player_to_edit}")
                edit_dribble = st.slider("🎯 Regate", 1, 10, current_stats['dribble'], key=f"edit_dribble_{player_to_edit}")
                edit_leadership = st.slider("👑 Liderazgo", 1, 10, current_stats['liderazgo'], key=f"edit_leadership_{player_to_edit}")
                
                if st.button(f"💾 ACTUALIZAR {player_to_edit.upper()}", type="primary", use_container_width=True):
                    st.session_state.players[player_to_edit] = {
                        'speed': edit_speed,
                        'strength': edit_strength,
                        'shooting': edit_shooting,
                        'dribble': edit_dribble,
                        'liderazgo': edit_leadership
                    }
                    st.success(f"¡{player_to_edit} actualizado!")
                    st.rerun()
    
    with st.expander("🗑️ Eliminar Jugadores", expanded=False):
        st.markdown("**Haz clic para eliminar:**")
        
        # Crear botones de eliminar compactos
        players_list = list(st.session_state.players.keys())
        
        # Dividir en grupos de 3 para móvil
        cols = st.columns(3)
        for i, player in enumerate(players_list):
            with cols[i % 3]:
                if st.button(f"❌ {player}", key=f"remove_{player}", use_container_width=True):
                    del st.session_state.players[player]
                    st.success(f"{player} eliminado")
                    st.rerun()

# PASO 3: GENERAR EQUIPOS (aparece solo con 10+ jugadores)
if len(st.session_state.players) >= 10:
    st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)
    
    # Centrar el título del paso 3
    st.markdown("<h2 style='text-align: center;'>🎲 PASO 3: Generar Equipos</h2>", unsafe_allow_html=True)
    
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

# SECCIÓN DE GUÍA (aparece cuando faltan jugadores para el paso 3)
if len(st.session_state.players) > 0 and len(st.session_state.players) < 10:
    st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)
    remaining = 10 - len(st.session_state.players)
    
    # Mensaje de progreso compacto
    st.markdown(f"<h3 style='text-align: center; color: #ff6600;'>⏳ Faltan {remaining} jugadores</h3>", unsafe_allow_html=True)
    
    # Botón de completar automático prominente
    if st.button(f"🚀 COMPLETAR CON {remaining} PREDEFINIDOS", type="primary", use_container_width=True, key="auto_complete"):
        available = [name for name in DEFAULT_PLAYERS.keys() if name not in st.session_state.players]
        needed = min(remaining, len(available))
        for i in range(needed):
            player_name = available[i]
            st.session_state.players[player_name] = DEFAULT_PLAYERS[player_name].copy()
        st.success(f"¡{needed} jugadores agregados! 🎉")
        st.balloons()
        st.rerun()

# PASO 4: RESULTADOS (aparece solo después de generar equipos)
if 'team_results' in st.session_state:
    st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)
    
    # Centrar el título de resultados
    st.markdown("<h2 style='text-align: center;'>🏆 TUS EQUIPOS</h2>", unsafe_allow_html=True)
    
    results = st.session_state.team_results
    
    st.success(f"✅ Diferencia: {results['actual_diff']} puntos")
    
    # Mostrar equipos uno debajo del otro para móvil
    
    # EQUIPO A
    st.markdown("### 🔵 EQUIPO A")
    st.info(f"**Total: {results['team_a_total']} pts | Promedio: {results['team_a_total']/5:.1f}**")
    
    # Mostrar jugadores del equipo A en formato compacto
    for name in results['team_a']:
        metrics = st.session_state.players[name]
        st.markdown(f"⚽ **{name}** → V:{metrics['speed']} F:{metrics['strength']} D:{metrics['shooting']} R:{metrics['dribble']} L:{metrics['liderazgo']}")
    
    st.markdown("---")
    
    # EQUIPO B
    st.markdown("### 🔴 EQUIPO B")
    st.info(f"**Total: {results['team_b_total']} pts | Promedio: {results['team_b_total']/5:.1f}**")
    
    # Mostrar jugadores del equipo B en formato compacto
    for name in results['team_b']:
        metrics = st.session_state.players[name]
        st.markdown(f"⚽ **{name}** → V:{metrics['speed']} F:{metrics['strength']} D:{metrics['shooting']} R:{metrics['dribble']} L:{metrics['liderazgo']}")
    
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

# Instrucciones compactas para móvil
with st.expander("❓ Ayuda", expanded=False):
    st.markdown("""
    **🚀 Uso rápido:**
    1. Cargar Todos → Generar Equipos → ¡Listo!
    
    **🎯 El algoritmo:**
    - Calcula todas las combinaciones posibles
    - Encuentra los equipos más equilibrados
    
    **👥 Jugadores:** David, Dan, Diego, Morales, Buco, Joao, Nestor, Nico, Ribery, Sergio
    """)

# Ocultar el sidebar completamente
st.sidebar.write("")

# Espacio final para móviles
st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True) 