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

# CSS ultra-compacto para móvil - sin scroll excesivo
st.markdown("""
<style>
    /* Ocultar elementos de Streamlit */
    .css-1d391kg, .css-18e3th9, header, .stDecoration {
        display: none !important;
    }
    
    /* Contenedor ultra-compacto */
    .main .block-container {
        padding: 0.2rem 0.5rem;
        max-width: 100%;
        margin: 0;
    }
    
    /* Títulos ultra-compactos */
    h1 {
        text-align: center;
        font-size: 1.5rem;
        margin: 0.2rem 0;
        line-height: 1.2;
    }
    
    h2 {
        text-align: center;
        font-size: 1rem;
        margin: 0.2rem 0;
        color: #1f77b4;
        line-height: 1.1;
    }
    
    h3 {
        text-align: center;
        font-size: 0.9rem;
        margin: 0.1rem 0;
        line-height: 1.1;
    }
    
    /* Botones ultra-compactos pero táctiles */
    .stButton > button {
        width: 100%;
        height: 2.5rem;
        font-size: 0.9rem;
        font-weight: bold;
        border-radius: 6px;
        margin: 0.1rem 0;
        padding: 0.3rem;
    }
    
    /* Progress bar ultra-delgada */
    .stProgress .st-bo {
        height: 0.8rem;
    }
    
    /* Elementos de formulario compactos */
    .stSelectbox, .stTextInput, .stSlider {
        margin: 0.1rem 0;
        font-size: 0.8rem;
    }
    
    /* Dataframe ultra-compacto */
    .stDataFrame {
        font-size: 0.7rem;
        margin: 0.2rem 0;
    }
    
    /* Expanders compactos */
    .streamlit-expanderHeader {
        font-size: 0.9rem;
        padding: 0.3rem !important;
    }
    
    .streamlit-expanderContent {
        padding: 0.3rem !important;
    }
    
    /* Eliminar espacios entre elementos */
    .element-container {
        margin: 0.1rem 0;
    }
    
    /* Alertas compactas */
    .stAlert {
        margin: 0.1rem 0;
        padding: 0.3rem;
        font-size: 0.8rem;
    }
    
    /* Texto más pequeño en general */
    p, div, span {
        font-size: 0.8rem;
        line-height: 1.2;
    }
    
    /* Quitar separadores gruesos */
    hr {
        margin: 0.2rem 0;
        border: 0.5px solid #eee;
    }
    
    /* Tabs compactos si los uso */
    .stTabs {
        margin: 0;
    }
    
    /* Mobile específico */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.1rem 0.3rem;
        }
        
        h1 {
            font-size: 1.3rem;
        }
        
        h2 {
            font-size: 0.9rem;
        }
        
        .stButton > button {
            height: 2.2rem;
            font-size: 0.8rem;
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

# TÍTULO ULTRA-COMPACTO
st.title("⚽ Equipos")

# TABS PARA EVITAR SCROLL
tab1, tab2, tab3 = st.tabs(["👥 Jugadores", "⚙️ Gestionar", "🎲 Equipos"])

with tab1:
    # Contador de progreso compacto
    if st.session_state.players:
        progress = len(st.session_state.players) / 10
        st.progress(progress)
        st.markdown(f"**{len(st.session_state.players)}/10 jugadores** {'✅' if len(st.session_state.players) >= 10 else '⏳'}")
    else:
        st.progress(0)
        st.markdown("**0/10 jugadores** 📝")

    # Botones principales compactos
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 CARGAR TODOS", type="primary", use_container_width=True):
            st.session_state.players = DEFAULT_PLAYERS.copy()
            st.success("¡10 jugadores cargados!")
            st.rerun()
    with col2:
        if st.button("🗑️ LIMPIAR", type="secondary", use_container_width=True):
            st.session_state.players = {}
            if 'team_results' in st.session_state:
                del st.session_state.team_results
            st.rerun()

    # Completar automático si faltan
    if 0 < len(st.session_state.players) < 10:
        remaining = 10 - len(st.session_state.players)
        if st.button(f"➕ COMPLETAR ({remaining} más)", use_container_width=True):
            available = [name for name in DEFAULT_PLAYERS.keys() if name not in st.session_state.players]
            needed = min(remaining, len(available))
            for i in range(needed):
                player_name = available[i]
                st.session_state.players[player_name] = DEFAULT_PLAYERS[player_name].copy()
            st.success(f"¡{needed} jugadores agregados!")
            st.rerun()

    # Agregar jugadores individuales compacto
    if len(st.session_state.players) < 10:
        available_players = [name for name in DEFAULT_PLAYERS.keys() if name not in st.session_state.players]
        
        if available_players:
            st.markdown("**Agregar uno por uno:**")
            
            # Grid compacto de botones
            cols = st.columns(3)
            for i, player in enumerate(available_players):
                with cols[i % 3]:
                    if st.button(f"➕ {player}", key=f"add_{player}", use_container_width=True):
                        st.session_state.players[player] = DEFAULT_PLAYERS[player].copy()
                        st.success(f"¡{player} agregado!")
                        st.rerun()

    # Crear jugador personalizado
    with st.expander("✨ Crear Personalizado", expanded=False):
        new_player_name = st.text_input("Nombre:", key="new_player_name")
        
        # Sliders en una sola columna para ahorrar espacio
        new_speed = st.slider("🏃 Velocidad", 1, 10, 5, key="new_speed")
        new_strength = st.slider("💪 Fuerza", 1, 10, 5, key="new_strength")
        new_shooting = st.slider("⚽ Disparo", 1, 10, 5, key="new_shooting")
        new_dribble = st.slider("🎯 Regate", 1, 10, 5, key="new_dribble")
        new_leadership = st.slider("👑 Liderazgo", 1, 10, 5, key="new_leadership")
        
        if st.button("🌟 CREAR", type="primary", use_container_width=True):
            if new_player_name and new_player_name not in st.session_state.players:
                st.session_state.players[new_player_name] = {
                    'speed': new_speed,
                    'strength': new_strength,
                    'shooting': new_shooting,
                    'dribble': new_dribble,
                    'liderazgo': new_leadership
                }
                st.success(f"¡{new_player_name} creado!")
                st.rerun()
            elif new_player_name in st.session_state.players:
                st.error(f"Ya existe: {new_player_name}")
            else:
                st.error("Ingresa un nombre")

with tab2:
    if st.session_state.players:
        # Mostrar tabla de jugadores ultra-compacta
        df_players = pd.DataFrame.from_dict(st.session_state.players, orient='index')
        df_players.index.name = 'Jugador'
        df_players['Total'] = df_players.sum(axis=1)
        
        # Columnas ultra-abreviadas para móvil
        df_display = df_players.copy()
        df_display.columns = ['V', 'F', 'D', 'R', 'L', 'T']
        
        st.dataframe(df_display, use_container_width=True, height=150)
        
        # Editar en expander compacto
        with st.expander("✏️ Editar", expanded=False):
            player_to_edit = st.selectbox(
                "Jugador:",
                ["Selecciona..."] + list(st.session_state.players.keys()),
                key="edit_selector"
            )
            
            if player_to_edit != "Selecciona...":
                current_stats = st.session_state.players[player_to_edit]
                
                st.markdown(f"**{player_to_edit}**")
                
                # Sliders ultra-compactos
                edit_speed = st.slider("🏃V", 1, 10, current_stats['speed'], key=f"edit_speed_{player_to_edit}")
                edit_strength = st.slider("💪F", 1, 10, current_stats['strength'], key=f"edit_strength_{player_to_edit}")
                edit_shooting = st.slider("⚽D", 1, 10, current_stats['shooting'], key=f"edit_shooting_{player_to_edit}")
                edit_dribble = st.slider("🎯R", 1, 10, current_stats['dribble'], key=f"edit_dribble_{player_to_edit}")
                edit_leadership = st.slider("👑L", 1, 10, current_stats['liderazgo'], key=f"edit_leadership_{player_to_edit}")
                
                if st.button(f"💾 ACTUALIZAR", type="primary", use_container_width=True):
                    st.session_state.players[player_to_edit] = {
                        'speed': edit_speed,
                        'strength': edit_strength,
                        'shooting': edit_shooting,
                        'dribble': edit_dribble,
                        'liderazgo': edit_leadership
                    }
                    st.success(f"¡{player_to_edit} actualizado!")
                    st.rerun()
        
        # Eliminar en expander compacto
        with st.expander("🗑️ Eliminar", expanded=False):
            players_list = list(st.session_state.players.keys())
            
            # Grid ultra-compacto
            cols = st.columns(3)
            for i, player in enumerate(players_list):
                with cols[i % 3]:
                    if st.button(f"❌ {player}", key=f"remove_{player}", use_container_width=True):
                        del st.session_state.players[player]
                        st.success(f"{player} eliminado")
                        st.rerun()
    else:
        st.info("📝 No hay jugadores. Ve a la pestaña '👥 Jugadores' para agregar.")

with tab3:
    if len(st.session_state.players) >= 10:
        # Botón compacto para generar equipos
        if st.button("🎲 GENERAR EQUIPOS", type="primary", use_container_width=True, key="generate_main"):
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
        
        # Mostrar resultados si existen
        if 'team_results' in st.session_state:
            results = st.session_state.team_results
            
            st.success(f"✅ Diferencia: {results['actual_diff']} pts")
            
            # EQUIPO A - Ultra compacto
            st.markdown(f"**🔵 EQUIPO A** - Total: {results['team_a_total']} pts")
            for name in results['team_a']:
                metrics = st.session_state.players[name]
                st.markdown(f"⚽ **{name}** V:{metrics['speed']} F:{metrics['strength']} D:{metrics['shooting']} R:{metrics['dribble']} L:{metrics['liderazgo']}")
            
            # EQUIPO B - Ultra compacto
            st.markdown(f"**🔴 EQUIPO B** - Total: {results['team_b_total']} pts")
            for name in results['team_b']:
                metrics = st.session_state.players[name]
                st.markdown(f"⚽ **{name}** V:{metrics['speed']} F:{metrics['strength']} D:{metrics['shooting']} R:{metrics['dribble']} L:{metrics['liderazgo']}")
            
            # Botón para regenerar
            if st.button("🔄 OTROS EQUIPOS", use_container_width=True):
                # Algoritmo simplificado
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
    
    else:
        # Mensaje cuando no hay suficientes jugadores
        remaining = 10 - len(st.session_state.players)
        if remaining > 0:
            st.warning(f"⏳ Necesitas {remaining} jugadores más")
            if st.button(f"🚀 COMPLETAR AUTOMÁTICO", type="primary", use_container_width=True, key="auto_complete"):
                available = [name for name in DEFAULT_PLAYERS.keys() if name not in st.session_state.players]
                needed = min(remaining, len(available))
                for i in range(needed):
                    player_name = available[i]
                    st.session_state.players[player_name] = DEFAULT_PLAYERS[player_name].copy()
                st.success(f"¡{needed} agregados!")
                st.rerun()
        else:
            st.info("📝 No hay jugadores. Ve a la pestaña '👥 Jugadores'.")

# Ayuda ultra-compacta al final
with st.expander("❓ Ayuda", expanded=False):
    st.markdown("**🚀 Uso:** Jugadores → Gestionar → Equipos\n\n**👥 Predefinidos:** David, Dan, Diego, Morales, Buco, Joao, Nestor, Nico, Ribery, Sergio")

# Ocultar sidebar
st.sidebar.write("") 