import pandas as pd
import random
import numpy as np
from deap import base, creator, tools, algorithms
from utils import generate_plot_map

ZONES = ['Residential', 'Commercial', 'Green']

def assign_subtype(zone, x, y, grid_size):
    if zone == 'Residential':
        return 'Apartment' if y < grid_size // 2 else 'Independent House'
    elif zone == 'Commercial':
        return 'Mall' if y < grid_size // 3 else 'Local Shop'
    elif zone == 'Green':
        return 'Park'
    else:
        return 'Road'

def run_zoning_ga(grid_size, min_area, max_area, res_range, com_range, green_range, manual_areas=None):
    num_plots = grid_size * grid_size
    plots = []

    for i in range(num_plots):
        row = i // grid_size
        col = i % grid_size
        area = manual_areas[i] if manual_areas else random.randint(min_area, max_area)
        plots.append({
            'PlotID': i,
            'X': col,
            'Y': row,
            'Area': area,
            'Zone': 'Unassigned',
            'Subtype': '',
            'Reason': ''
        })

    df = pd.DataFrame(plots)

    # Road zone
    df.loc[
        (df['X'] == 0) | (df['X'] == grid_size - 1) |
        (df['Y'] == 0) | (df['Y'] == grid_size - 1) |
        (df['X'] % 3 == 0) | (df['Y'] % 3 == 0),
        'Zone'
    ] = 'Road'

    assignable_indices = df[df['Zone'] == 'Unassigned'].index.tolist()

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_zone", lambda: random.choice(ZONES))
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_zone, n=len(assignable_indices))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evaluate(ind):
        temp_df = df.copy()
        temp_df.loc[assignable_indices, 'Zone'] = ind
        total_area = temp_df[temp_df['Zone'] != 'Road']['Area'].sum()
        area_by_zone = temp_df.groupby('Zone')['Area'].sum()
        ratios = {z: area_by_zone.get(z, 0) / total_area for z in ZONES}
        constraints = {'Residential': res_range, 'Commercial': com_range, 'Green': green_range}
        score = 100
        for zone in ZONES:
            r = ratios[zone] * 100
            if r < constraints[zone][0]: score -= (constraints[zone][0] - r)
            if r > constraints[zone][1]: score -= (r - constraints[zone][1])
        return (score,)

    def mutate_individual(ind, indpb):
        for i in range(len(ind)):
            if random.random() < indpb:
                ind[i] = random.choice(ZONES)
        return (ind,)

    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutate_individual, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    population = toolbox.population(n=50)
    for _ in range(50):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
        for ind in offspring:
            ind.fitness.values = toolbox.evaluate(ind)
        population = toolbox.select(offspring, len(population))

    best = tools.selBest(population, 1)[0]
    df.loc[assignable_indices, 'Zone'] = best

    # Assign subtypes and reasoning
    for idx, row in df.iterrows():
        if row['Zone'] not in ['Unassigned', 'Road']:
            x, y = row['X'], row['Y']
            zone = row['Zone']
            subtype = assign_subtype(zone, x, y, grid_size)

            # Reason
            if zone == 'Commercial':
                reason = "Near road → good for business" if y < grid_size // 3 else "Mid-block → ideal for shops"
            elif zone == 'Residential':
                reason = "Inner area → peaceful housing"
            elif zone == 'Green':
                reason = "Scattered for public access"
            else:
                reason = "Traffic management"

            df.at[idx, 'Subtype'] = subtype
            df.at[idx, 'Reason'] = reason

    return df, generate_plot_map(df, grid_size)

# ---------- Layout Evaluation Function ----------
def evaluate_layout(df):
    grid_size = int(df['X'].max()) + 1  # 🔥 This fixes the undefined error
    score = 100
    reasons = []
    suggestions = []

    center_x = df['X'].median()
    center_y = df['Y'].median()


    # 1. Commercial zones near roads
    malls = df[df['Subtype'] == 'Mall']
    near_road = malls[malls['Y'] < df['Y'].max() // 3]
    if len(near_road) >= 1:
        reasons.append("✅ Malls placed near road → good visibility")
    else:
        suggestions.append("⚠️ Move malls near road edges")

    # 2. Hospitals in center
    hospitals = df[df['Subtype'] == 'Hospital']
    if not hospitals.empty:
        dists = ((hospitals['X'] - center_x)**2 + (hospitals['Y'] - center_y)**2)**0.5
        avg_dist = dists.mean()
        if avg_dist > grid_size / 3:
            suggestions.append("⚠️ Place hospital closer to center")
        else:
            reasons.append("✅ Hospital is centrally located")

    # 3. Parks near homes
    parks = df[df['Subtype'] == 'Park']
    apartments = df[df['Subtype'] == 'Apartment']
    if not parks.empty and not apartments.empty:
        close_count = 0
        for _, apt in apartments.iterrows():
            dists = ((parks['X'] - apt['X'])**2 + (parks['Y'] - apt['Y'])**2)**0.5
            if any(d < 3 for d in dists):
                close_count += 1
        if close_count > len(apartments) * 0.6:
            reasons.append("✅ Parks accessible from most apartments")
        else:
            suggestions.append("⚠️ Improve park proximity to housing")
            score -= 10

    # 4. Balanced layout
    counts = df['Zone'].value_counts(normalize=True) * 100
    if counts.get('Residential', 0) < 30:
        suggestions.append("⚠️ Residential area too small")
        score -= 10
    if counts.get('Green', 0) < 10:
        suggestions.append("⚠️ Green space under-represented")
        score -= 10

    # Final adjustments
    score = max(0, min(100, score))
    return score, reasons, suggestions
