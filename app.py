import streamlit as st
import pandas as pd
import itertools
import random

st.set_page_config(page_title="Generador de Equipos Balanceados", page_icon="⚽", layout="wide")

st.title("⚽ Generador de Equipos Balanceados 5v5")
st.markdown("---")

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

# Main content
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
with st.expander("📖 Instrucciones"):
    st.markdown("""
    ### Cómo usar esta aplicación:
    
    1. **Agregar Jugadores**: Usa la barra lateral para agregar jugadores con sus métricas (velocidad, fuerza, disparo, regate, liderazgo)
    
    2. **Editar/Eliminar**: Puedes modificar o eliminar jugadores existentes en la sección principal
    
    3. **Generar Equipos**: Una vez que tengas 10 jugadores, podrás generar equipos balanceados
    
    4. **Tolerancia**: Ajusta la tolerancia para permitir más variedad en los equipos generados
    
    5. **Resultados**: Los equipos se mostrarán con sus promedios y comparaciones detalladas
    
    ### Métricas:
    - **Velocidad**: Rapidez del jugador
    - **Fuerza**: Potencia física
    - **Disparo**: Habilidad de tiro
    - **Regate**: Habilidad técnica
    - **Liderazgo**: Capacidad de liderazgo en el campo
    """) 