import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

def generate_plot_map(df, grid_size):
    colors = {
        'Road': '#A9A9A9',
        'Residential': '#87CEEB',
        'Commercial': '#FFA500',
        'Green': '#228B22'
    }

    icons = {
        'Road': '🛣️',
        'Residential': '🏠',
        'Commercial': '🏢',
        'Green': '🌳'
    }

    fig, ax = plt.subplots(figsize=(10, 10))

    for _, row in df.iterrows():
        x, y = row['X'], row['Y']
        zone = row['Zone']
        subtype = row.get('Subtype', zone)
        color = colors.get(zone, 'white')
        icon = icons.get(zone, '')

        rect = plt.Rectangle((x, y), 0.9, 0.9, facecolor=color, edgecolor='black', linewidth=0.8)
        ax.add_patch(rect)
        ax.text(x + 0.45, y + 0.35, icon, fontsize=12, ha='center', va='center')
        ax.text(x + 0.45, y + 0.65, subtype, fontsize=6.5, ha='center', va='center')

    ax.set_xlim(-1, grid_size + 1)
    ax.set_ylim(-1, grid_size + 1)
    ax.set_aspect('equal')
    ax.set_title("🧱 2D Semantic Zoning Layout", fontsize=14)
    ax.axis('off')
    return fig

def zoning_summary(df):
    summary = df[df['Zone'] != 'Road'].groupby('Zone')['Area'].sum().reset_index()
    total = summary['Area'].sum()
    summary['Percentage'] = (summary['Area'] / total * 100).round(1)
    return summary

def plotly_3d_map(df):
    zone_colors = {
        'Mall': 'orange', 'Local Shop': 'gold', 'Hospital': 'red',
        'Apartment': 'skyblue', 'Independent House': 'blue',
        'Park': 'green', 'Road': 'gray'
    }

    heights = {
        'Mall': 5, 'Local Shop': 3, 'Hospital': 4,
        'Apartment': 2.5, 'Independent House': 2,
        'Park': 1, 'Road': 0.5
    }

    x, y, z, color, text = [], [], [], [], []

    for _, row in df.iterrows():
        x.append(row['X'])
        y.append(row['Y'])
        subtype = row['Subtype']
        zone = row['Zone']
        z.append(heights.get(subtype, 1))
        color.append(zone_colors.get(subtype, 'gray'))

        hover_text = (
            f"🧱 Plot {row['PlotID']}<br>"
            f"Zone: {zone}<br>"
            f"Subtype: {subtype}<br>"
            f"Area: {row['Area']} sq.m<br>"
            f"Reason: {row.get('Reason', 'N/A')}"
        )
        text.append(hover_text)

    fig = go.Figure(data=[go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(size=10, color=color, opacity=0.9),
        text=text,
        hoverinfo='text'
    )])

    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Semantic Importance'
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        title="📊 UrbanBlocks 3D Zoning Map"
    )
    return fig
