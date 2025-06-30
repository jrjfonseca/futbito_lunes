import itertools
import pandas as pd
import random

# List of 10 players
names = [
    "No seas malo",
    "Me ha costado mucho hacerlo",
    "David",
    "Dan",
    "Diego",
    "Morales",
    "Nico",
    "Buco",
    "Ribery",
    "Sergio",
    # If you have exactly 10, remove the last or adjust names accordingly
]

# Metrics for each player: speed, strength, shooting, dribble, liderazgo
# Replace the example values below with your actual data
players_metrics = {
    "Joao":            {"speed": 5, "strength": 6, "shooting": 6, "dribble": 5, "liderazgo": 4},

    "Nestor": {"speed": 5, "strength": 5, "shooting": 5, "dribble": 5, "liderazgo": 5},

    "David":                   {"speed": 7, "strength": 6, "shooting": 7, "dribble": 7, "liderazgo": 6},

    "Dan":                     {"speed": 4, "strength": 8, "shooting": 6, "dribble": 5, "liderazgo": 3},

    "Diego":                   {"speed": 7, "strength": 7, "shooting": 5, "dribble": 5, "liderazgo": 5},

    "Morales":                 {"speed": 6, "strength": 6, "shooting": 6, "dribble": 7, "liderazgo": 6},
    
    "Nico":                    {"speed": 6, "strength": 6, "shooting": 8, "dribble": 6, "liderazgo": 4},

    "Buco":                    {"speed": 5, "strength": 6, "shooting": 6, "dribble": 5, "liderazgo": 9},

    "Ribery":                  {"speed": 8, "strength": 6, "shooting": 8, "dribble": 8, "liderazgo": 7},

    "Sergio":                  {"speed": 7, "strength": 7, "shooting": 6, "dribble": 7, "liderazgo": 5},
}

# Build DataFrame
df = pd.DataFrame.from_dict(players_metrics, orient='index')
df.index.name = 'Name'

# Compute team score as sum of all metrics (equal weighting)
def team_score(team):
    return sum(df.loc[name].sum() for name in team)

# Find best 5v5 split with randomization
players = list(players_metrics.keys())
best_diff = float('inf')
best_splits = []

# First pass: find the minimum difference
for combo in itertools.combinations(players, 5):
    team_a = list(combo)
    team_b = [p for p in players if p not in team_a]
    diff = abs(team_score(team_a) - team_score(team_b))
    if diff < best_diff:
        best_diff = diff

# Second pass: collect all combinations with the minimum difference (or very close)
tolerance = 1  # Allow combinations within 1 point of the best
for combo in itertools.combinations(players, 5):
    team_a = list(combo)
    team_b = [p for p in players if p not in team_a]
    diff = abs(team_score(team_a) - team_score(team_b))
    if diff <= best_diff + tolerance:
        best_splits.append((team_a, team_b, diff))

# Randomly select one of the best combinations
best_split = random.choice(best_splits)
team_a, team_b, actual_diff = best_split

# Compute team averages
def compute_team_averages(team):
    team_data = df.loc[team]
    return team_data.mean()

team_a_avg = compute_team_averages(team_a)
team_b_avg = compute_team_averages(team_b)
team_a_total = sum(df.loc[name].sum() for name in team_a)
team_b_total = sum(df.loc[name].sum() for name in team_b)

print(f"\nMejor división 5 vs 5 (diferencia de suma de métricas = {actual_diff}):\n")

print("Equipo A:")
for name in team_a:
    metrics = df.loc[name]
    print(f" - {name}: Velocidad={metrics['speed']}, Fuerza={metrics['strength']}, Disparo={metrics['shooting']}, Regate={metrics['dribble']}, Liderazgo={metrics['liderazgo']}")

print(f"\nPromedios del Equipo A:")
print(f" - Velocidad: {team_a_avg['speed']:.2f}")
print(f" - Fuerza: {team_a_avg['strength']:.2f}")
print(f" - Disparo: {team_a_avg['shooting']:.2f}")
print(f" - Regate: {team_a_avg['dribble']:.2f}")
print(f" - Liderazgo: {team_a_avg['liderazgo']:.2f}")
print(f" - Puntuación Total: {team_a_total}")

print("\nEquipo B:")
for name in team_b:
    metrics = df.loc[name]
    print(f" - {name}: Velocidad={metrics['speed']}, Fuerza={metrics['strength']}, Disparo={metrics['shooting']}, Regate={metrics['dribble']}, Liderazgo={metrics['liderazgo']}")

print(f"\nPromedios del Equipo B:")
print(f" - Velocidad: {team_b_avg['speed']:.2f}")
print(f" - Fuerza: {team_b_avg['strength']:.2f}")
print(f" - Disparo: {team_b_avg['shooting']:.2f}")
print(f" - Regate: {team_b_avg['dribble']:.2f}")
print(f" - Liderazgo: {team_b_avg['liderazgo']:.2f}")
print(f" - Puntuación Total: {team_b_total}")

print(f"\nComparación de Equipos:")
print(f"Diferencia promedio por métrica:")
metric_translations = {'speed': 'Velocidad', 'strength': 'Fuerza', 'shooting': 'Disparo', 'dribble': 'Regate', 'liderazgo': 'Liderazgo'}
for metric in ['speed', 'strength', 'shooting', 'dribble', 'liderazgo']:
    diff = abs(team_a_avg[metric] - team_b_avg[metric])
    print(f" - {metric_translations[metric]}: {diff:.2f}")
print(f"Diferencia de puntuación total: {abs(team_a_total - team_b_total)}")
