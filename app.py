import streamlit as st
import pandas as pd
import itertools
import random

st.set_page_config(
    page_title="Generador de Equipos Balanceados", 
    page_icon="⚽", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para dispositivos móviles
st.markdown("""
<style>
    /* Mejor responsive design */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* Botones más grandes para móviles */
    .stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 1.1rem;
        font-weight: bold;
    }
    
    /* Sliders más fáciles de usar en móvil */
    .stSlider {
        padding: 0.5rem 0;
    }
    
    /* Texto más grande para móviles */
    .metric-text {
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    /* Mejor espaciado en móviles */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        
        .stSelectbox label, .stTextInput label, .stSlider label {
            font-size: 1.1rem;
            font-weight: bold;
        }
        
        /* Sidebar más ancha en móviles */
        .css-1d391kg {
            width: 100%;
        }
        
        /* Input text más grande en móviles */
        .stTextInput input {
            font-size: 1.2rem;
            height: 3rem;
        }
        
        /* Dataframe responsive */
        .stDataFrame {
            font-size: 0.9rem;
        }
        
        /* Mejorar spacing entre elementos */
        .element-container {
            margin-bottom: 1rem;
        }
    }
    
    /* Mejorar checkbox de modo móvil */
    .stCheckbox {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border: 2px dashed #4CAF50;
        margin-bottom: 1rem;
    }
    
    /* Emojis más grandes para mejor visualización */
    .metric-emoji {
        font-size: 1.5rem;
    }
    
    /* Títulos más compactos */
    h1 {
        margin-bottom: 0.5rem;
    }
    
    h2, h3 {
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚽ Generador de Equipos Balanceados 5v5")
st.markdown("### 🤖 *Cuando el humano falla, vente al verdadero algoritmo.*")
st.markdown("---")

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

# Initialize session state for players
if 'players' not in st.session_state:
    st.session_state.players = {}

# Sidebar for adding players
st.sidebar.header("➕ Agregar Jugadores")

with st.sidebar:
    st.subheader("Nuevo Jugador")
    player_name = st.text_input("Nombre del Jugador")
    
    col1, col2 = st.columns(2)
    with col1:
        speed = st.slider("Velocidad", 1, 10, 5, key="speed")
        shooting = st.slider("Disparo", 1, 10, 5, key="shooting")
        leadership = st.slider("Liderazgo", 1, 10, 5, key="leadership")
    
    with col2:
        strength = st.slider("Fuerza", 1, 10, 5, key="strength")
        dribble = st.slider("Regate", 1, 10, 5, key="dribble")
    
    if st.button("Agregar Jugador", type="primary"):
        if player_name and player_name not in st.session_state.players:
            st.session_state.players[player_name] = {
                'speed': speed,
                'strength': strength,
                'shooting': shooting,
                'dribble': dribble,
                'liderazgo': leadership
            }
            st.success(f"¡{player_name} agregado!")
            st.rerun()
        elif player_name in st.session_state.players:
            st.error("Este jugador ya existe")
        else:
            st.error("Por favor ingresa un nombre")
    
    st.markdown("---")
    
    st.subheader("⚡ Carga Rápida")
    
    # Botón para cargar todos los jugadores por defecto
    if st.button("🚀 Cargar Todos los Jugadores", type="secondary", use_container_width=True):
        st.session_state.players = DEFAULT_PLAYERS.copy()
        st.success("¡Todos los jugadores cargados!")
        st.rerun()
    
    # Selector para cargar jugadores individuales
    st.write("**Cargar jugador individual:**")
    available_players = [name for name in DEFAULT_PLAYERS.keys() if name not in st.session_state.players]
    
    if available_players:
        selected_default_player = st.selectbox(
            "Seleccionar jugador:", 
            [""] + available_players,
            key="default_player_select"
        )
        
        if selected_default_player and st.button(f"➕ Agregar {selected_default_player}", use_container_width=True):
            st.session_state.players[selected_default_player] = DEFAULT_PLAYERS[selected_default_player].copy()
            st.success(f"¡{selected_default_player} agregado!")
            st.rerun()
    else:
        if len(st.session_state.players) >= len(DEFAULT_PLAYERS):
            st.info("✅ Todos los jugadores ya están cargados")
        else:
            st.info("ℹ️ Jugadores disponibles ya agregados")
    
    # Mostrar resumen de jugadores cargados
    if st.session_state.players:
        st.write(f"**Jugadores actuales:** {len(st.session_state.players)}/10")
        if len(st.session_state.players) >= 10:
            st.success("🎯 ¡Listos para generar equipos!")
        else:
            remaining = 10 - len(st.session_state.players)
            st.warning(f"⏰ Faltan {remaining} jugadores para generar equipos")

# Main content - Layout responsive
# Detección automática de dispositivo móvil (JavaScript)
st.markdown("""
<script>
    if (window.innerWidth <= 768) {
        // Auto-detectar móvil, pero permitir que el usuario lo cambie
        const checkbox = document.querySelector('input[type="checkbox"]');
        if (checkbox && !checkbox.checked) {
            checkbox.click();
        }
    }
</script>
""", unsafe_allow_html=True)

# Checkbox para modo móvil con mejor estilo
col_check, col_info = st.columns([3, 1])
with col_check:
    is_mobile = st.checkbox("📱 Modo Móvil Optimizado", value=False, 
                           help="✨ Activa para una experiencia optimizada en dispositivos móviles\n\n🚀 Beneficios:\n• Layout de una sola columna\n• Botones más grandes\n• Mejor espaciado\n• Interfaz más táctil")
with col_info:
    if is_mobile:
        st.markdown("🟢 **Activo**")
    else:
        st.markdown("⚪ Escritorio")

if is_mobile:
    # Layout de una sola columna para móviles
    st.header("👥 Lista de Jugadores")
    
    if st.session_state.players:
        # Display current players
        df_players = pd.DataFrame.from_dict(st.session_state.players, orient='index')
        df_players.index.name = 'Jugador'
        
        # Add total score column
        df_players['Total'] = df_players.sum(axis=1)
        
        st.dataframe(df_players, use_container_width=True)
        
        # Allow editing existing players
        st.subheader("✏️ Editar Jugadores")
        selected_player = st.selectbox("Seleccionar jugador para editar:", list(st.session_state.players.keys()))
        
        if selected_player:
            current_stats = st.session_state.players[selected_player]
            
            # En móvil, usar una sola columna para los sliders
            new_speed = st.slider("Velocidad", 1, 10, current_stats['speed'], key=f"edit_speed_{selected_player}")
            new_strength = st.slider("Fuerza", 1, 10, current_stats['strength'], key=f"edit_strength_{selected_player}")
            new_shooting = st.slider("Disparo", 1, 10, current_stats['shooting'], key=f"edit_shooting_{selected_player}")
            new_dribble = st.slider("Regate", 1, 10, current_stats['dribble'], key=f"edit_dribble_{selected_player}")
            new_leadership = st.slider("Liderazgo", 1, 10, current_stats['liderazgo'], key=f"edit_leadership_{selected_player}")
            
            col_update, col_delete = st.columns(2)
            with col_update:
                if st.button("🔄 Actualizar", type="secondary", key="mobile_update"):
                    st.session_state.players[selected_player] = {
                        'speed': new_speed,
                        'strength': new_strength,
                        'shooting': new_shooting,
                        'dribble': new_dribble,
                        'liderazgo': new_leadership
                    }
                    st.success(f"¡{selected_player} actualizado!")
                    st.rerun()
            
            with col_delete:
                if st.button("🗑️ Eliminar", type="secondary", key="mobile_delete"):
                    del st.session_state.players[selected_player]
                    st.success(f"{selected_player} eliminado")
                    st.rerun()
    else:
        st.info("📱 No hay jugadores agregados. Usa la barra lateral para agregar jugadores.")
    
    # Configuración móvil
    st.header("⚙️ Configuración")
    
    if len(st.session_state.players) >= 10:
        tolerance = st.slider("Tolerancia de Diferencia", 0, 5, 1, 
                            help="Permite variaciones en la diferencia de puntos para mayor variedad")
        
        if st.button("🎲 Generar Equipos", type="primary", use_container_width=True):
            # Team generation algorithm (same as desktop)
            def team_score(team, players_data):
                return sum(sum(players_data[name].values()) for name in team)
            
            def compute_team_averages(team, df):
                team_data = df.loc[team]
                return team_data.mean()
            
            players = list(st.session_state.players.keys())
            df = pd.DataFrame.from_dict(st.session_state.players, orient='index')
            
            best_diff = float('inf')
            best_splits = []
            
            # First pass: find the minimum difference
            for combo in itertools.combinations(players, 5):
                team_a = list(combo)
                team_b = [p for p in players if p not in team_a]
                diff = abs(team_score(team_a, st.session_state.players) - team_score(team_b, st.session_state.players))
                if diff < best_diff:
                    best_diff = diff
            
            # Second pass: collect all combinations within tolerance
            for combo in itertools.combinations(players, 5):
                team_a = list(combo)
                team_b = [p for p in players if p not in team_a]
                diff = abs(team_score(team_a, st.session_state.players) - team_score(team_b, st.session_state.players))
                if diff <= best_diff + tolerance:
                    best_splits.append((team_a, team_b, diff))
            
            # Randomly select one of the best combinations
            team_a, team_b, actual_diff = random.choice(best_splits)
            
            # Compute team averages
            team_a_avg = compute_team_averages(team_a, df)
            team_b_avg = compute_team_averages(team_b, df)
            team_a_total = team_score(team_a, st.session_state.players)
            team_b_total = team_score(team_b, st.session_state.players)
            
            # Store results in session state
            st.session_state.team_results = {
                'team_a': team_a,
                'team_b': team_b,
                'team_a_avg': team_a_avg,
                'team_b_avg': team_b_avg,
                'team_a_total': team_a_total,
                'team_b_total': team_b_total,
                'actual_diff': actual_diff
            }
            
            st.success("¡Equipos generados!")
    
    elif len(st.session_state.players) > 0:
        st.warning(f"Necesitas al menos 10 jugadores. Tienes {len(st.session_state.players)}")
    
    if st.button("🗑️ Limpiar Todos", type="secondary", use_container_width=True):
        st.session_state.players = {}
        if 'team_results' in st.session_state:
            del st.session_state.team_results
        st.rerun()

else:
    # Layout de escritorio (dos columnas)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("👥 Lista de Jugadores")
        
        if st.session_state.players:
            # Display current players
            df_players = pd.DataFrame.from_dict(st.session_state.players, orient='index')
            df_players.index.name = 'Jugador'
            
            # Add total score column
            df_players['Total'] = df_players.sum(axis=1)
            
            st.dataframe(df_players, use_container_width=True)
            
            # Allow editing existing players
            st.subheader("✏️ Editar Jugadores")
            selected_player = st.selectbox("Seleccionar jugador para editar:", list(st.session_state.players.keys()))
            
            if selected_player:
                current_stats = st.session_state.players[selected_player]
                
                col_edit1, col_edit2 = st.columns(2)
                with col_edit1:
                    new_speed = st.slider("Velocidad", 1, 10, current_stats['speed'], key=f"edit_speed_{selected_player}")
                    new_shooting = st.slider("Disparo", 1, 10, current_stats['shooting'], key=f"edit_shooting_{selected_player}")
                    new_leadership = st.slider("Liderazgo", 1, 10, current_stats['liderazgo'], key=f"edit_leadership_{selected_player}")
                
                with col_edit2:
                    new_strength = st.slider("Fuerza", 1, 10, current_stats['strength'], key=f"edit_strength_{selected_player}")
                    new_dribble = st.slider("Regate", 1, 10, current_stats['dribble'], key=f"edit_dribble_{selected_player}")
                
                col_update, col_delete = st.columns(2)
                with col_update:
                    if st.button("Actualizar Jugador", type="secondary"):
                        st.session_state.players[selected_player] = {
                            'speed': new_speed,
                            'strength': new_strength,
                            'shooting': new_shooting,
                            'dribble': new_dribble,
                            'liderazgo': new_leadership
                        }
                        st.success(f"¡{selected_player} actualizado!")
                        st.rerun()
                
                with col_delete:
                    if st.button("Eliminar Jugador", type="secondary"):
                        del st.session_state.players[selected_player]
                        st.success(f"{selected_player} eliminado")
                        st.rerun()
        else:
            st.info("No hay jugadores agregados. Usa la barra lateral para agregar jugadores.")

    with col2:
        st.header("⚙️ Configuración")
        
        if len(st.session_state.players) >= 10:
            tolerance = st.slider("Tolerancia de Diferencia", 0, 5, 1, 
                                help="Permite variaciones en la diferencia de puntos para mayor variedad")
            
            if st.button("🎲 Generar Equipos", type="primary", use_container_width=True):
                # Team generation algorithm
                def team_score(team, players_data):
                    return sum(sum(players_data[name].values()) for name in team)
                
                def compute_team_averages(team, df):
                    team_data = df.loc[team]
                    return team_data.mean()
                
                players = list(st.session_state.players.keys())
                df = pd.DataFrame.from_dict(st.session_state.players, orient='index')
                
                best_diff = float('inf')
                best_splits = []
                
                # First pass: find the minimum difference
                for combo in itertools.combinations(players, 5):
                    team_a = list(combo)
                    team_b = [p for p in players if p not in team_a]
                    diff = abs(team_score(team_a, st.session_state.players) - team_score(team_b, st.session_state.players))
                    if diff < best_diff:
                        best_diff = diff
                
                # Second pass: collect all combinations within tolerance
                for combo in itertools.combinations(players, 5):
                    team_a = list(combo)
                    team_b = [p for p in players if p not in team_a]
                    diff = abs(team_score(team_a, st.session_state.players) - team_score(team_b, st.session_state.players))
                    if diff <= best_diff + tolerance:
                        best_splits.append((team_a, team_b, diff))
                
                # Randomly select one of the best combinations
                team_a, team_b, actual_diff = random.choice(best_splits)
                
                # Compute team averages
                team_a_avg = compute_team_averages(team_a, df)
                team_b_avg = compute_team_averages(team_b, df)
                team_a_total = team_score(team_a, st.session_state.players)
                team_b_total = team_score(team_b, st.session_state.players)
                
                # Store results in session state
                st.session_state.team_results = {
                    'team_a': team_a,
                    'team_b': team_b,
                    'team_a_avg': team_a_avg,
                    'team_b_avg': team_b_avg,
                    'team_a_total': team_a_total,
                    'team_b_total': team_b_total,
                    'actual_diff': actual_diff
                }
                
                st.success("¡Equipos generados!")
        
        elif len(st.session_state.players) > 0:
            st.warning(f"Necesitas al menos 10 jugadores. Tienes {len(st.session_state.players)}")
        
        if st.button("🗑️ Limpiar Todos", type="secondary", use_container_width=True):
            st.session_state.players = {}
            if 'team_results' in st.session_state:
                del st.session_state.team_results
            st.rerun()

# Display team results
if 'team_results' in st.session_state:
    st.markdown("---")
    st.header("🏆 Equipos Generados")
    
    results = st.session_state.team_results
    
    st.subheader(f"Diferencia de suma de métricas: {results['actual_diff']}")
    
    # Layout adaptativo para resultados de equipos
    if is_mobile:
        # En móvil, mostrar equipos uno tras otro
        st.subheader("🔵 Equipo A")
        for name in results['team_a']:
            metrics = st.session_state.players[name]
            st.markdown(f"**{name}**: V={metrics['speed']}, F={metrics['strength']}, D={metrics['shooting']}, R={metrics['dribble']}, L={metrics['liderazgo']}")
        
        st.markdown("**📊 Promedios del Equipo A:**")
        st.markdown(f"🏃 Velocidad: **{results['team_a_avg']['speed']:.2f}** | 💪 Fuerza: **{results['team_a_avg']['strength']:.2f}**")
        st.markdown(f"⚽ Disparo: **{results['team_a_avg']['shooting']:.2f}** | 🎯 Regate: **{results['team_a_avg']['dribble']:.2f}**")
        st.markdown(f"👑 Liderazgo: **{results['team_a_avg']['liderazgo']:.2f}** | 🏆 Total: **{results['team_a_total']}**")
        
        st.markdown("---")
        
        st.subheader("🔴 Equipo B")
        for name in results['team_b']:
            metrics = st.session_state.players[name]
            st.markdown(f"**{name}**: V={metrics['speed']}, F={metrics['strength']}, D={metrics['shooting']}, R={metrics['dribble']}, L={metrics['liderazgo']}")
        
        st.markdown("**📊 Promedios del Equipo B:**")
        st.markdown(f"🏃 Velocidad: **{results['team_b_avg']['speed']:.2f}** | 💪 Fuerza: **{results['team_b_avg']['strength']:.2f}**")
        st.markdown(f"⚽ Disparo: **{results['team_b_avg']['shooting']:.2f}** | 🎯 Regate: **{results['team_b_avg']['dribble']:.2f}**")
        st.markdown(f"👑 Liderazgo: **{results['team_b_avg']['liderazgo']:.2f}** | 🏆 Total: **{results['team_b_total']}**")
        
    else:
        # En escritorio, mostrar en dos columnas
        col_team1, col_team2 = st.columns(2)
        
        with col_team1:
            st.subheader("🔵 Equipo A")
            for name in results['team_a']:
                metrics = st.session_state.players[name]
                st.write(f"**{name}**: Vel={metrics['speed']}, Fue={metrics['strength']}, Dis={metrics['shooting']}, Reg={metrics['dribble']}, Lid={metrics['liderazgo']}")
            
            st.write("**Promedios del Equipo A:**")
            st.write(f"- Velocidad: {results['team_a_avg']['speed']:.2f}")
            st.write(f"- Fuerza: {results['team_a_avg']['strength']:.2f}")
            st.write(f"- Disparo: {results['team_a_avg']['shooting']:.2f}")
            st.write(f"- Regate: {results['team_a_avg']['dribble']:.2f}")
            st.write(f"- Liderazgo: {results['team_a_avg']['liderazgo']:.2f}")
            st.write(f"- **Puntuación Total: {results['team_a_total']}**")
        
        with col_team2:
            st.subheader("🔴 Equipo B")
            for name in results['team_b']:
                metrics = st.session_state.players[name]
                st.write(f"**{name}**: Vel={metrics['speed']}, Fue={metrics['strength']}, Dis={metrics['shooting']}, Reg={metrics['dribble']}, Lid={metrics['liderazgo']}")
            
            st.write("**Promedios del Equipo B:**")
            st.write(f"- Velocidad: {results['team_b_avg']['speed']:.2f}")
            st.write(f"- Fuerza: {results['team_b_avg']['strength']:.2f}")
            st.write(f"- Disparo: {results['team_b_avg']['shooting']:.2f}")
            st.write(f"- Regate: {results['team_b_avg']['dribble']:.2f}")
            st.write(f"- Liderazgo: {results['team_b_avg']['liderazgo']:.2f}")
            st.write(f"- **Puntuación Total: {results['team_b_total']}**")
    
    # Team comparison
    st.subheader("📊 Comparación de Equipos")
    metric_translations = {'speed': 'Velocidad', 'strength': 'Fuerza', 'shooting': 'Disparo', 'dribble': 'Regate', 'liderazgo': 'Liderazgo'}
    
    comparison_data = []
    for metric in ['speed', 'strength', 'shooting', 'dribble', 'liderazgo']:
        diff = abs(results['team_a_avg'][metric] - results['team_b_avg'][metric])
        comparison_data.append({
            'Métrica': metric_translations[metric],
            'Equipo A': f"{results['team_a_avg'][metric]:.2f}",
            'Equipo B': f"{results['team_b_avg'][metric]:.2f}",
            'Diferencia': f"{diff:.2f}"
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    st.write(f"**Diferencia de puntuación total: {abs(results['team_a_total'] - results['team_b_total'])}**")

# Instructions
with st.expander("📖 Instrucciones y Ayuda"):
    st.markdown("""
    ### 🚀 Cómo usar esta aplicación:
    
    1. **📱 Modo Móvil**: Activa el "Modo Móvil Optimizado" para una mejor experiencia en tu teléfono
    
    2. **⚡ Carga Rápida**: Usa "Cargar Todos los Jugadores" para agregar automáticamente los 10 jugadores predefinidos
    
    3. **➕ Agregar Jugadores**: Usa la barra lateral para agregar jugadores manualmente con sus métricas (1-10 puntos cada una)
    
    4. **✏️ Editar/Eliminar**: Modifica o elimina jugadores existentes en la sección principal
    
    5. **🎲 Generar Equipos**: Una vez que tengas 10+ jugadores, podrás generar equipos balanceados
    
    6. **⚙️ Tolerancia**: Ajusta la tolerancia para permitir más variedad en los equipos generados
    
    7. **🏆 Resultados**: Los equipos se mostrarán con sus promedios y comparaciones detalladas
    
    ### 📊 Métricas (1-10 puntos):
    - **🏃 Velocidad**: Rapidez y aceleración del jugador
    - **💪 Fuerza**: Potencia física y resistencia
    - **⚽ Disparo**: Habilidad de tiro y precisión
    - **🎯 Regate**: Habilidad técnica y control del balón
    - **👑 Liderazgo**: Capacidad de liderazgo y comunicación en el campo
    
    ### 📱 Características Móviles:
    - **Layout optimizado** para pantallas pequeñas
    - **Botones más grandes** para facilitar el toque
    - **Interfaz simplificada** para mejor navegación
    - **Texto compacto** con emojis para fácil lectura
    
    ### 👥 Jugadores Predefinidos:
    **David**: V=7, F=6, D=7, R=7, L=6 | **Dan**: V=4, F=8, D=6, R=5, L=3
    
    **Diego**: V=7, F=7, D=5, R=5, L=5 | **Morales**: V=6, F=6, D=6, R=7, L=6
    
    **Buco**: V=5, F=6, D=6, R=5, L=9 | **Joao**: V=5, F=6, D=6, R=5, L=4
    
    **Nestor**: V=5, F=5, D=5, R=5, L=5 | **Nico**: V=6, F=6, D=8, R=6, L=4
    
    **Ribery**: V=8, F=6, D=8, R=8, L=7 | **Sergio**: V=7, F=7, D=6, R=7, L=5
    
    *V=Velocidad, F=Fuerza, D=Disparo, R=Regate, L=Liderazgo*
    
    ### 🤖 Algoritmo:
    El sistema calcula todas las combinaciones posibles y selecciona la más balanceada,
    garantizando equipos justos y competitivos. ¡Confía en el algoritmo! 🎯
    """) 