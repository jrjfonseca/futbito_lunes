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

# CSS elegante para ordenador - diseño desktop
st.markdown("""
<style>
    /* Ocultar sidebar */
    .css-1d391kg {
        display: none !important;
    }
    
    /* Contenedor principal para desktop */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Títulos elegantes */
    h1 {
        text-align: center;
        font-size: 3rem;
        margin: 1rem 0;
        color: #1f77b4;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    h2 {
        text-align: center;
        font-size: 1.8rem;
        margin: 1.5rem 0;
        color: #2c3e50;
        font-weight: 600;
    }
    
    h3 {
        font-size: 1.4rem;
        margin: 1rem 0;
        color: #34495e;
        font-weight: 600;
    }
    
    /* Botones elegantes para desktop */
    .stButton > button {
        width: 100%;
        height: 3.5rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 12px;
        margin: 0.5rem 0;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Progress bar elegante */
    .stProgress .st-bo {
        height: 1.5rem;
        border-radius: 10px;
    }
    
    /* Elementos de formulario elegantes */
    .stSelectbox, .stTextInput {
        margin: 0.8rem 0;
        font-size: 1rem;
    }
    
    .stSlider {
        margin: 1rem 0;
    }
    
    /* Dataframe elegante */
    .stDataFrame {
        font-size: 1rem;
        margin: 1rem 0;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Expanders elegantes */
    .streamlit-expanderHeader {
        font-size: 1.2rem;
        font-weight: bold;
        padding: 1rem !important;
        background-color: #f8f9fa;
        border-radius: 10px;
    }
    
    .streamlit-expanderContent {
        padding: 1.5rem !important;
        background-color: #ffffff;
        border-radius: 0 0 10px 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Alertas elegantes */
    .stAlert {
        margin: 1rem 0;
        padding: 1rem;
        border-radius: 10px;
        font-size: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Tabs elegantes */
    .stTabs {
        margin: 1rem 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 10px 10px 0 0;
        background-color: #f8f9fa;
    }
    
    /* Espaciado elegante */
    .element-container {
        margin: 0.8rem 0;
    }
    
    /* Cards para equipos */
    .team-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    
    .team-card-a {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .team-card-b {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    /* Métricas elegantes */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #1f77b4;
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

# TÍTULO ELEGANTE PARA DESKTOP
st.title("⚽ Generador de Equipos Balanceados")
st.markdown("<p style='text-align: center; color: #7f8c8d; font-size: 1.2rem; margin-top: -0.5rem;'>🤖 <i>Algoritmo inteligente para equipos perfectamente balanceados</i></p>", unsafe_allow_html=True)

# TABS ELEGANTES PARA DESKTOP
tab1, tab2, tab3 = st.tabs(["👥 Agregar Jugadores", "⚙️ Gestionar Jugadores", "🎲 Generar Equipos"])

with tab1:
    # Contador de progreso elegante
    st.markdown("### 📊 **Estado Actual del Equipo**")
    
    if st.session_state.players:
        progress = len(st.session_state.players) / 10
        st.progress(progress)
        
        col_prog1, col_prog2, col_prog3 = st.columns(3)
        with col_prog1:
            st.metric("👥 Jugadores", len(st.session_state.players), f"{10 - len(st.session_state.players)} faltan")
        with col_prog2:
            if len(st.session_state.players) >= 10:
                st.metric("✅ Estado", "COMPLETO", "Listo para generar")
            else:
                st.metric("⏳ Estado", "INCOMPLETO", f"Faltan {10 - len(st.session_state.players)}")
        with col_prog3:
            if st.session_state.players:
                total_avg = sum(sum(player.values()) for player in st.session_state.players.values()) / len(st.session_state.players)
                st.metric("📊 Promedio", f"{total_avg:.1f}", "pts por jugador")
    else:
        st.progress(0)
        st.info("🎯 **¡Comienza agregando jugadores para formar tu equipo!**")

    st.markdown("---")

    # Botones principales elegantes
    st.markdown("### 🚀 **Carga Rápida de Jugadores**")
    
    col_main1, col_main2, col_main3 = st.columns(3)
    
    with col_main1:
        if st.button("🚀 **CARGAR TODOS LOS JUGADORES**", type="primary", use_container_width=True):
            st.session_state.players = DEFAULT_PLAYERS.copy()
            st.success("✅ ¡10 jugadores predefinidos cargados exitosamente!")
            st.balloons()
            st.rerun()
    
    with col_main2:
        if st.button("🗑️ **LIMPIAR TODOS**", type="secondary", use_container_width=True):
            st.session_state.players = {}
            if 'team_results' in st.session_state:
                del st.session_state.team_results
            st.success("✅ Todos los jugadores eliminados")
            st.rerun()
    
    with col_main3:
        # Completar automático si faltan
        if 0 < len(st.session_state.players) < 10:
            remaining = 10 - len(st.session_state.players)
            if st.button(f"➕ **COMPLETAR ({remaining} más)**", use_container_width=True):
                available = [name for name in DEFAULT_PLAYERS.keys() if name not in st.session_state.players]
                needed = min(remaining, len(available))
                for i in range(needed):
                    player_name = available[i]
                    st.session_state.players[player_name] = DEFAULT_PLAYERS[player_name].copy()
                st.success(f"✅ ¡{needed} jugadores agregados!")
                st.rerun()

    # Agregar jugadores individuales elegante
    if len(st.session_state.players) < 10:
        available_players = [name for name in DEFAULT_PLAYERS.keys() if name not in st.session_state.players]
        
        if available_players:
            st.markdown("---")
            st.markdown("### 👥 **Agregar Jugadores Predefinidos Individualmente**")
            st.markdown("*Haz clic en cualquier jugador para agregarlo a tu equipo:*")
            
            # Grid elegante de botones de jugadores
            num_cols = min(4, len(available_players))
            cols = st.columns(num_cols)
            
            for i, player in enumerate(available_players):
                with cols[i % num_cols]:
                    player_stats = DEFAULT_PLAYERS[player]
                    player_total = sum(player_stats.values())
                    
                    # Botón con información del jugador
                    if st.button(
                        f"➕ **{player}**\n📊 {player_total} pts",
                        key=f"add_{player}",
                        use_container_width=True,
                        help=f"V:{player_stats['speed']} | F:{player_stats['strength']} | D:{player_stats['shooting']} | R:{player_stats['dribble']} | L:{player_stats['liderazgo']}"
                    ):
                        st.session_state.players[player] = DEFAULT_PLAYERS[player].copy()
                        st.success(f"✅ ¡{player} agregado al equipo!")
                        st.rerun()

    # Crear jugador personalizado elegante
    st.markdown("---")
    st.markdown("### ✨ **Crear Jugador Personalizado**")
    
    with st.expander("➕ **Diseñar Nuevo Jugador**", expanded=False):
        st.markdown("*Personaliza completamente las habilidades de tu jugador:*")
        
        # Nombre del jugador
        col_name1, col_name2 = st.columns([2, 1])
        with col_name1:
            new_player_name = st.text_input("**Nombre del jugador:**", key="new_player_name", placeholder="Ingresa el nombre...")
        
        # Sliders elegantes en dos columnas
        col_skills1, col_skills2 = st.columns(2)
        
        with col_skills1:
            st.markdown("**🏃 Habilidades Físicas**")
            new_speed = st.slider("🏃 Velocidad", 1, 10, 5, key="new_speed", help="Rapidez y agilidad del jugador")
            new_strength = st.slider("💪 Fuerza", 1, 10, 5, key="new_strength", help="Potencia física del jugador")
            new_shooting = st.slider("⚽ Disparo", 1, 10, 5, key="new_shooting", help="Precisión y potencia de tiro")
        
        with col_skills2:
            st.markdown("**🎯 Habilidades Técnicas**")
            new_dribble = st.slider("🎯 Regate", 1, 10, 5, key="new_dribble", help="Habilidad técnica con el balón")
            new_leadership = st.slider("👑 Liderazgo", 1, 10, 5, key="new_leadership", help="Capacidad de liderazgo en el campo")
        
        # Preview del jugador
        total_new = new_speed + new_strength + new_shooting + new_dribble + new_leadership
        col_preview1, col_preview2 = st.columns([2, 1])
        
        with col_preview1:
            st.markdown(f"""
            **📊 Preview del Jugador:**
            - **Total:** {total_new} puntos
            - **Promedio:** {total_new/5:.1f} por habilidad
            """)
        
        with col_preview2:
            if st.button("🌟 **CREAR JUGADOR**", type="primary", use_container_width=True):
                if new_player_name and new_player_name not in st.session_state.players:
                    st.session_state.players[new_player_name] = {
                        'speed': new_speed,
                        'strength': new_strength,
                        'shooting': new_shooting,
                        'dribble': new_dribble,
                        'liderazgo': new_leadership
                    }
                    st.success(f"✅ ¡{new_player_name} creado exitosamente!")
                    st.balloons()
                    st.rerun()
                elif new_player_name in st.session_state.players:
                    st.error(f"❌ Ya existe un jugador llamado '{new_player_name}'")
                else:
                    st.error("❌ Por favor ingresa un nombre para el jugador")

with tab2:
    if st.session_state.players:
        st.markdown("### 📊 **Tabla de Jugadores Registrados**")
        
        # Crear DataFrame más elegante
        df_players = pd.DataFrame.from_dict(st.session_state.players, orient='index')
        df_players.index.name = 'Jugador'
        df_players['Total'] = df_players.sum(axis=1)
        
        # Renombrar columnas con emojis elegantes
        df_display = df_players.copy()
        df_display.columns = ['🏃 Velocidad', '💪 Fuerza', '⚽ Disparo', '🎯 Regate', '👑 Liderazgo', '📊 Total']
        
        # Aplicar estilo de colores a la tabla
        def color_scale(val):
            if val >= 8:
                return 'background-color: #d4edda; color: #155724; font-weight: bold'
            elif val >= 6:
                return 'background-color: #fff3cd; color: #856404'
            else:
                return 'background-color: #f8d7da; color: #721c24'
        
        # Mostrar tabla con estilo
        styled_df = df_display.style.applymap(color_scale, subset=['🏃 Velocidad', '💪 Fuerza', '⚽ Disparo', '🎯 Regate', '👑 Liderazgo']) \
                                   .format(precision=0) \
                                   .set_table_styles([
                                       {'selector': 'th', 'props': [('background-color', '#f8f9fa'), ('color', '#495057'), ('font-weight', 'bold')]},
                                       {'selector': 'td', 'props': [('text-align', 'center'), ('padding', '10px')]},
                                       {'selector': 'tr:nth-of-type(even)', 'props': [('background-color', '#f8f9fa')]}
                                   ])
        
        st.dataframe(styled_df, use_container_width=True, height=400)
        
        # Mostrar estadísticas generales
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        
        with col_stats1:
            st.metric(
                label="🎯 Promedio General", 
                value=f"{df_players['Total'].mean():.1f}",
                delta=f"Rango: {df_players['Total'].min():.0f}-{df_players['Total'].max():.0f}"
            )
        
        with col_stats2:
            best_player = df_players['Total'].idxmax()
            st.metric(
                label="🏆 Mejor Jugador", 
                value=best_player,
                delta=f"{df_players.loc[best_player, 'Total']:.0f} puntos"
            )
        
        with col_stats3:
            st.metric(
                label="⚖️ Desviación", 
                value=f"{df_players['Total'].std():.1f}",
                delta="Equilibrio del equipo"
            )

        # Sección de gestión elegante
        st.markdown("---")
        
        col_edit, col_delete = st.columns(2)
        
        with col_edit:
            with st.expander("✏️ **Editar Jugador**", expanded=False):
                player_to_edit = st.selectbox(
                    "Selecciona jugador para editar:",
                    ["Selecciona un jugador..."] + list(st.session_state.players.keys()),
                    key="edit_selector"
                )
                
                if player_to_edit != "Selecciona un jugador...":
                    current_stats = st.session_state.players[player_to_edit]
                    
                    st.markdown(f"### 🎯 **Editando: {player_to_edit}**")
                    
                    # Sliders elegantes en dos columnas
                    col_edit1, col_edit2 = st.columns(2)
                    
                    with col_edit1:
                        edit_speed = st.slider("🏃 Velocidad", 1, 10, current_stats['speed'], key=f"edit_speed_{player_to_edit}")
                        edit_shooting = st.slider("⚽ Disparo", 1, 10, current_stats['shooting'], key=f"edit_shooting_{player_to_edit}")
                        edit_leadership = st.slider("👑 Liderazgo", 1, 10, current_stats['liderazgo'], key=f"edit_leadership_{player_to_edit}")
                    
                    with col_edit2:
                        edit_strength = st.slider("💪 Fuerza", 1, 10, current_stats['strength'], key=f"edit_strength_{player_to_edit}")
                        edit_dribble = st.slider("🎯 Regate", 1, 10, current_stats['dribble'], key=f"edit_dribble_{player_to_edit}")
                    
                    # Mostrar preview del total
                    new_total = edit_speed + edit_strength + edit_shooting + edit_dribble + edit_leadership
                    st.info(f"📊 **Total nuevo:** {new_total} puntos (anterior: {current_stats['speed'] + current_stats['strength'] + current_stats['shooting'] + current_stats['dribble'] + current_stats['liderazgo']})")
                    
                    if st.button(f"💾 **ACTUALIZAR {player_to_edit.upper()}**", type="primary", use_container_width=True):
                        st.session_state.players[player_to_edit] = {
                            'speed': edit_speed,
                            'strength': edit_strength,
                            'shooting': edit_shooting,
                            'dribble': edit_dribble,
                            'liderazgo': edit_leadership
                        }
                        st.success(f"✅ ¡{player_to_edit} actualizado exitosamente!")
                        st.balloons()
                        st.rerun()
        
        with col_delete:
            with st.expander("🗑️ **Eliminar Jugadores**", expanded=False):
                st.markdown("**Selecciona jugadores para eliminar:**")
                
                players_list = list(st.session_state.players.keys())
                
                # Crear checkboxes para selección múltiple
                selected_for_deletion = []
                for player in players_list:
                    if st.checkbox(f"❌ {player}", key=f"delete_check_{player}"):
                        selected_for_deletion.append(player)
                
                if selected_for_deletion:
                    st.warning(f"⚠️ Se eliminarán {len(selected_for_deletion)} jugador(es): {', '.join(selected_for_deletion)}")
                    
                    if st.button("🗑️ **CONFIRMAR ELIMINACIÓN**", type="secondary", use_container_width=True):
                        for player in selected_for_deletion:
                            del st.session_state.players[player]
                        
                        # Limpiar resultados si existían
                        if 'team_results' in st.session_state:
                            del st.session_state.team_results
                        
                        st.success(f"✅ {len(selected_for_deletion)} jugador(es) eliminado(s) exitosamente!")
                        st.rerun()

    else:
        st.info("📝 No hay jugadores registrados. Ve a la pestaña '👥 Agregar Jugadores' para comenzar.")

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
            
            st.markdown("---")
            st.markdown("## 🏆 **RESULTADOS: EQUIPOS BALANCEADOS**")
            
            # Mostrar diferencia total
            col_diff1, col_diff2, col_diff3 = st.columns([1, 2, 1])
            with col_diff2:
                st.metric(
                    label="⚖️ Diferencia entre Equipos", 
                    value=f"{results['actual_diff']} puntos",
                    delta="¡Perfectamente balanceado!" if results['actual_diff'] <= 2 else "Bien balanceado" if results['actual_diff'] <= 5 else "Aceptable"
                )
            
            # Mostrar equipos en columnas elegantes
            col_team_a, col_team_b = st.columns(2)
            
            with col_team_a:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                           color: white; padding: 1.5rem; border-radius: 15px; margin: 1rem 0;
                           box-shadow: 0 8px 16px rgba(79, 172, 254, 0.3);'>
                    <h3 style='margin: 0; text-align: center;'>🔵 EQUIPO A</h3>
                    <h4 style='margin: 0.5rem 0; text-align: center;'>Total: {results['team_a_total']} puntos</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Mostrar jugadores del equipo A
                for name in results['team_a']:
                    metrics = st.session_state.players[name]
                    total_player = sum(metrics.values())
                    st.markdown(f"""
                    <div style='background: white; padding: 0.8rem; margin: 0.5rem 0; border-radius: 10px;
                               border-left: 4px solid #4facfe; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                        <strong>⚽ {name}</strong> ({total_player} pts)<br>
                        🏃{metrics['speed']} | 💪{metrics['strength']} | ⚽{metrics['shooting']} | 🎯{metrics['dribble']} | 👑{metrics['liderazgo']}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Mostrar promedios del equipo A
                st.markdown("### 📊 **Promedios del Equipo A**")
                
                col_a1, col_a2 = st.columns(2)
                with col_a1:
                    st.metric("🏃 Velocidad", f"{results['team_a_avg']['speed']:.1f}")
                    st.metric("⚽ Disparo", f"{results['team_a_avg']['shooting']:.1f}")
                    st.metric("👑 Liderazgo", f"{results['team_a_avg']['liderazgo']:.1f}")
                
                with col_a2:
                    st.metric("💪 Fuerza", f"{results['team_a_avg']['strength']:.1f}")
                    st.metric("🎯 Regate", f"{results['team_a_avg']['dribble']:.1f}")
            
            with col_team_b:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                           color: white; padding: 1.5rem; border-radius: 15px; margin: 1rem 0;
                           box-shadow: 0 8px 16px rgba(250, 112, 154, 0.3);'>
                    <h3 style='margin: 0; text-align: center;'>🔴 EQUIPO B</h3>
                    <h4 style='margin: 0.5rem 0; text-align: center;'>Total: {results['team_b_total']} puntos</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Mostrar jugadores del equipo B
                for name in results['team_b']:
                    metrics = st.session_state.players[name]
                    total_player = sum(metrics.values())
                    st.markdown(f"""
                    <div style='background: white; padding: 0.8rem; margin: 0.5rem 0; border-radius: 10px;
                               border-left: 4px solid #fa709a; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                        <strong>⚽ {name}</strong> ({total_player} pts)<br>
                        🏃{metrics['speed']} | 💪{metrics['strength']} | ⚽{metrics['shooting']} | 🎯{metrics['dribble']} | 👑{metrics['liderazgo']}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Mostrar promedios del equipo B
                st.markdown("### 📊 **Promedios del Equipo B**")
                
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    st.metric("🏃 Velocidad", f"{results['team_b_avg']['speed']:.1f}")
                    st.metric("⚽ Disparo", f"{results['team_b_avg']['shooting']:.1f}")
                    st.metric("👑 Liderazgo", f"{results['team_b_avg']['liderazgo']:.1f}")
                
                with col_b2:
                    st.metric("💪 Fuerza", f"{results['team_b_avg']['strength']:.1f}")
                    st.metric("🎯 Regate", f"{results['team_b_avg']['dribble']:.1f}")
            
            # Comparación de promedios
            st.markdown("---")
            st.markdown("### 📈 **Comparación de Promedios por Métrica**")
            
            comparison_data = {
                'Métrica': ['🏃 Velocidad', '💪 Fuerza', '⚽ Disparo', '🎯 Regate', '👑 Liderazgo'],
                'Equipo A': [
                    f"{results['team_a_avg']['speed']:.1f}",
                    f"{results['team_a_avg']['strength']:.1f}",
                    f"{results['team_a_avg']['shooting']:.1f}",
                    f"{results['team_a_avg']['dribble']:.1f}",
                    f"{results['team_a_avg']['liderazgo']:.1f}"
                ],
                'Equipo B': [
                    f"{results['team_b_avg']['speed']:.1f}",
                    f"{results['team_b_avg']['strength']:.1f}",
                    f"{results['team_b_avg']['shooting']:.1f}",
                    f"{results['team_b_avg']['dribble']:.1f}",
                    f"{results['team_b_avg']['liderazgo']:.1f}"
                ],
                'Diferencia': [
                    f"{abs(results['team_a_avg']['speed'] - results['team_b_avg']['speed']):.1f}",
                    f"{abs(results['team_a_avg']['strength'] - results['team_b_avg']['strength']):.1f}",
                    f"{abs(results['team_a_avg']['shooting'] - results['team_b_avg']['shooting']):.1f}",
                    f"{abs(results['team_a_avg']['dribble'] - results['team_b_avg']['dribble']):.1f}",
                    f"{abs(results['team_a_avg']['liderazgo'] - results['team_b_avg']['liderazgo']):.1f}"
                ]
            }
            
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)
            
            # Botón para regenerar
            st.markdown("---")
            col_regen1, col_regen2, col_regen3 = st.columns([1, 2, 1])
            with col_regen2:
                if st.button("🔄 **GENERAR OTROS EQUIPOS**", type="secondary", use_container_width=True):
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
                    
                    st.success("✅ ¡Nuevos equipos generados!")
                    st.rerun()
    
    else:
        # Mensaje cuando no hay suficientes jugadores
        remaining = 10 - len(st.session_state.players)
        if remaining > 0:
            st.warning(f"⏳ **Necesitas {remaining} jugadores más para generar equipos**")
            
            col_auto1, col_auto2, col_auto3 = st.columns([1, 2, 1])
            with col_auto2:
                if st.button(f"🚀 **COMPLETAR AUTOMÁTICAMENTE**", type="primary", use_container_width=True, key="auto_complete"):
                    available = [name for name in DEFAULT_PLAYERS.keys() if name not in st.session_state.players]
                    needed = min(remaining, len(available))
                    for i in range(needed):
                        player_name = available[i]
                        st.session_state.players[player_name] = DEFAULT_PLAYERS[player_name].copy()
                    st.success(f"✅ ¡{needed} jugadores agregados automáticamente!")
                    st.balloons()
                    st.rerun()
        else:
            st.info("📝 **No hay jugadores registrados.** Ve a la pestaña '👥 Agregar Jugadores' para comenzar.")

# Ayuda elegante para desktop
with st.expander("❓ **Ayuda y Información**", expanded=False):
    col_help1, col_help2 = st.columns(2)
    
    with col_help1:
        st.markdown("""
        ### 🚀 **Cómo usar la aplicación:**
        
        1. **👥 Agregar Jugadores:** Carga jugadores predefinidos o crea personalizados
        2. **⚙️ Gestionar Jugadores:** Ve, edita o elimina jugadores existentes
        3. **🎲 Generar Equipos:** Crea equipos perfectamente balanceados
        
        ### 🎯 **Algoritmo de Balanceo:**
        - Analiza **todas las combinaciones posibles** de equipos 5v5
        - Encuentra la división con **menor diferencia** de puntos totales
        - Considera **todas las métricas** para máximo equilibrio
        """)
    
    with col_help2:
        st.markdown("""
        ### 👥 **Jugadores Predefinidos:**
        
        **David, Dan, Diego, Morales, Buco**  
        **Joao, Nestor, Nico, Ribery, Sergio**
        
        ### 📊 **Métricas Evaluadas:**
        - 🏃 **Velocidad:** Rapidez y agilidad
        - 💪 **Fuerza:** Potencia física  
        - ⚽ **Disparo:** Precisión y potencia de tiro
        - 🎯 **Regate:** Habilidad técnica con el balón
        - 👑 **Liderazgo:** Capacidad de liderazgo en el campo
        """)

# Ocultar sidebar elegantemente
st.sidebar.write("") 