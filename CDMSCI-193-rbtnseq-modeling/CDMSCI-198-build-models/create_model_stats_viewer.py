#!/usr/bin/env python3
"""
Create interactive HTML viewer for model building statistics
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from pathlib import Path

# Load data
stats_df = pd.read_csv('results/model_statistics.csv')
gapfill_df = pd.read_csv('results/gapfill_report.csv')

print(f"Loaded {len(stats_df)} rows from model_statistics.csv")
print(f"Columns: {stats_df.columns.tolist()}")
print(f"\nFirst few rows:")
print(stats_df.head())

# Filter to successful models
successful = stats_df[stats_df['Status'] == 'Success'].copy()
print(f"\nSuccessful models: {len(successful)}")
print(f"Draft Reactions range: {successful['Draft_Reactions'].min()} - {successful['Draft_Reactions'].max()}")
print(f"Gapfilled Growth range: {successful['Gapfilled_Growth'].min()} - {successful['Gapfilled_Growth'].max()}")

# Calculate summary statistics
total_organisms = len(stats_df)
successful_count = len(successful)
failed_count = total_organisms - successful_count
needed_gapfill = len(successful[successful['Gapfilled_Reactions_Added'] > 0])
growing_after_gapfill = len(successful[successful['Gapfilled_Growth'] > 0.001])

# Create HTML page
html_parts = []

# Header
header = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Model Building Statistics - CDMSCI-198</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .subtitle {{
            color: #7f8c8d;
            margin-bottom: 30px;
            font-size: 14px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 8px;
            color: white;
            text-align: center;
        }}
        .stat-card.success {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }}
        .stat-card.warning {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        .stat-card.info {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }}
        .stat-value {{
            font-size: 36px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stat-label {{
            font-size: 14px;
            opacity: 0.9;
        }}
        .plot-container {{
            margin-bottom: 40px;
        }}
        .plot-title {{
            font-size: 18px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 15px;
        }}
        .section-title {{
            font-size: 24px;
            font-weight: 600;
            color: #2c3e50;
            margin: 40px 0 20px 0;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #2c3e50;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .growth-yes {{
            color: #27ae60;
            font-weight: 600;
        }}
        .growth-no {{
            color: #e74c3c;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Model Building Statistics</h1>
        <p class="subtitle">CDMSCI-198: Build and Gap-Fill Metabolic Models on Pyruvate Minimal Media</p>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Organisms</div>
                <div class="stat-value">{total_organisms}</div>
            </div>
            <div class="stat-card success">
                <div class="stat-label">Successfully Built</div>
                <div class="stat-value">{successful_count}</div>
            </div>
            <div class="stat-card warning">
                <div class="stat-label">Needed Gap-filling</div>
                <div class="stat-value">{needed_gapfill}</div>
            </div>
            <div class="stat-card info">
                <div class="stat-label">Growing After Gap-fill</div>
                <div class="stat-value">{growing_after_gapfill}</div>
            </div>
        </div>
"""
html_parts.append(header)

# Figure 1: Model Size Distribution
fig1 = make_subplots(
    rows=1, cols=3,
    subplot_titles=('Draft Reactions', 'Draft Metabolites', 'Draft Genes')
)

fig1.add_trace(
    go.Histogram(x=successful['Draft_Reactions'].tolist(), nbinsx=20, name='Reactions',
                marker_color='#667eea'),
    row=1, col=1
)
fig1.add_trace(
    go.Histogram(x=successful['Draft_Metabolites'].tolist(), nbinsx=20, name='Metabolites',
                marker_color='#764ba2'),
    row=1, col=2
)
fig1.add_trace(
    go.Histogram(x=successful['Draft_Genes'].tolist(), nbinsx=20, name='Genes',
                marker_color='#f093fb'),
    row=1, col=3
)

fig1.update_xaxes(title_text="Reactions", row=1, col=1)
fig1.update_xaxes(title_text="Metabolites", row=1, col=2)
fig1.update_xaxes(title_text="Genes", row=1, col=3)
fig1.update_yaxes(title_text="Count", row=1, col=1)

fig1.update_layout(
    height=400,
    showlegend=False,
    title_text="Draft Model Size Distribution",
    title_font_size=18
)

html_parts.append('<div class="section-title">Draft Model Statistics</div>')
html_parts.append('<div class="plot-container">')
html_parts.append(fig1.to_html(include_plotlyjs=False, div_id="fig1", include_mathjax=False))
html_parts.append('</div>')

# Figure 2: Gap-filling Statistics
fig2 = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Reactions Added by Gap-filling', 'Final Growth Rate Distribution')
)

# Histogram of gapfill reactions added
fig2.add_trace(
    go.Histogram(x=successful['Gapfilled_Reactions_Added'].tolist(), nbinsx=20,
                marker_color='#11998e', name='Reactions Added'),
    row=1, col=1
)

# Histogram of final growth rates
fig2.add_trace(
    go.Histogram(x=successful['Gapfilled_Growth'].tolist(), nbinsx=20,
                marker_color='#667eea', name='Growth Rate'),
    row=1, col=2
)

fig2.update_xaxes(title_text="Reactions Added", row=1, col=1)
fig2.update_xaxes(title_text="Growth Rate (1/hr)", row=1, col=2)
fig2.update_yaxes(title_text="Count", row=1, col=1)
fig2.update_yaxes(title_text="Count", row=1, col=2)

fig2.update_layout(
    height=400,
    showlegend=False,
    title_text="Gap-filling Impact",
    title_font_size=18
)

html_parts.append('<div class="section-title">Gap-filling Analysis</div>')
html_parts.append('<div class="plot-container">')
html_parts.append(fig2.to_html(include_plotlyjs=False, div_id="fig2"))
html_parts.append('</div>')

# Figure 3: Per-organism bar chart
successful_sorted = successful.sort_values('Gapfilled_Growth', ascending=False)

fig3 = go.Figure()

fig3.add_trace(go.Bar(
    x=successful_sorted['Organism_ID'].tolist(),
    y=successful_sorted['Gapfilled_Growth'].tolist(),
    marker_color='#667eea',
    hovertemplate='<b>%{x}</b><br>Growth: %{y:.4f} 1/hr<extra></extra>'
))

fig3.update_layout(
    title="Growth Rate by Organism (Sorted by Growth Rate)",
    xaxis_title="Organism",
    yaxis_title="Growth Rate (1/hr)",
    height=500,
    showlegend=False,
    xaxis={'tickangle': -45},
    hovermode='closest'
)

html_parts.append('<div class="section-title">Per-Organism Results</div>')
html_parts.append('<div class="plot-container">')
html_parts.append(fig3.to_html(include_plotlyjs=False, div_id="fig3"))
html_parts.append('</div>')

# Figure 4: Reactions vs Growth
fig4 = go.Figure()

fig4.add_trace(go.Scatter(
    x=successful['Draft_Reactions'].tolist(),
    y=successful['Gapfilled_Growth'].tolist(),
    mode='markers',
    marker=dict(
        size=(successful['Gapfilled_Reactions_Added']*0.5 + 5).tolist(),
        color=successful['Gapfilled_Reactions_Added'].tolist(),
        colorscale='Plasma',
        showscale=True,
        colorbar=dict(title="Reactions<br>Added")
    ),
    text=successful['Organism_ID'].tolist(),
    hovertemplate='<b>%{text}</b><br>Reactions: %{x}<br>Growth: %{y:.4f}<extra></extra>'
))

fig4.update_layout(
    title="Model Size vs Growth Rate",
    xaxis_title="Draft Reactions",
    yaxis_title="Gap-filled Growth Rate (1/hr)",
    height=500,
    hovermode='closest'
)

html_parts.append('<div class="section-title">Model Size Analysis</div>')
html_parts.append('<div class="plot-container">')
html_parts.append(fig4.to_html(include_plotlyjs=False, div_id="fig4"))
html_parts.append('</div>')

# Figure 5: Top 20 Gap-filled Reactions Across All Models
print("\nAnalyzing gap-filled reactions across all models...")

# Parse gapfill report to count reaction frequency
from collections import Counter
gapfilled_reactions = Counter()

for _, row in gapfill_df.iterrows():
    if pd.notna(row['Reactions_Added']) and row['Reactions_Added']:
        # Split reaction IDs (assuming comma-separated or semicolon-separated)
        reactions = str(row['Reactions_Added']).replace(';', ',').split(',')
        for rxn in reactions:
            rxn = rxn.strip()
            if rxn:
                gapfilled_reactions[rxn] += 1

print(f"Total unique gap-filled reactions: {len(gapfilled_reactions)}")
print(f"Total gap-fill additions: {sum(gapfilled_reactions.values())}")

# Get top 20
top_20_reactions = gapfilled_reactions.most_common(20)

if top_20_reactions:
    reaction_ids = [rxn[0] for rxn in top_20_reactions]
    reaction_counts = [rxn[1] for rxn in top_20_reactions]

    fig5 = go.Figure()

    fig5.add_trace(go.Bar(
        y=reaction_ids[::-1],  # Reverse for better display (highest at top)
        x=reaction_counts[::-1],
        orientation='h',
        marker_color='#11998e',
        hovertemplate='<b>%{y}</b><br>Added to %{x} models<extra></extra>'
    ))

    fig5.update_layout(
        title="Top 20 Most Frequently Gap-filled Reactions",
        xaxis_title="Number of Models",
        yaxis_title="Reaction ID",
        height=600,
        hovermode='closest',
        yaxis={'tickfont': {'size': 10}}
    )

    html_parts.append('<div class="section-title">Gap-filled Reactions Analysis</div>')
    html_parts.append('<div class="plot-container">')
    html_parts.append(f'<p style="color: #7f8c8d; margin-bottom: 15px;">These are the reactions most commonly added during gap-filling across all {len(successful)} models. High-frequency reactions indicate common metabolic gaps in draft reconstructions.</p>')
    html_parts.append(fig5.to_html(include_plotlyjs=False, div_id="fig5"))
    html_parts.append('</div>')

    # Add top 20 table
    html_parts.append('<div class="plot-title">Top 20 Gap-filled Reactions (Detailed)</div>')
    html_parts.append('<table style="max-width: 800px;">')
    html_parts.append('<thead><tr>')
    html_parts.append('<th>Rank</th>')
    html_parts.append('<th>Reaction ID</th>')
    html_parts.append('<th>Models</th>')
    html_parts.append('<th>Frequency</th>')
    html_parts.append('</tr></thead>')
    html_parts.append('<tbody>')

    for i, (rxn_id, count) in enumerate(top_20_reactions, 1):
        freq_pct = 100 * count / len(successful)
        html_parts.append('<tr>')
        html_parts.append(f'<td><strong>{i}</strong></td>')
        html_parts.append(f'<td><code>{rxn_id}</code></td>')
        html_parts.append(f'<td>{count} / {len(successful)}</td>')
        html_parts.append(f'<td>{freq_pct:.1f}%</td>')
        html_parts.append('</tr>')

    html_parts.append('</tbody></table>')
else:
    print("WARNING: Could not parse gap-filled reactions from gapfill_report.csv")

# Detailed table
html_parts.append('<div class="section-title">Detailed Statistics</div>')
html_parts.append('<table>')
html_parts.append('<thead><tr>')
html_parts.append('<th>Organism</th>')
html_parts.append('<th>Draft Reactions</th>')
html_parts.append('<th>Draft Metabolites</th>')
html_parts.append('<th>Draft Genes</th>')
html_parts.append('<th>Draft Growth</th>')
html_parts.append('<th>Reactions Added</th>')
html_parts.append('<th>Gap-filled Growth</th>')
html_parts.append('<th>Growth?</th>')
html_parts.append('</tr></thead>')
html_parts.append('<tbody>')

for _, row in successful_sorted.iterrows():
    grows = 'Yes' if row['Gapfilled_Growth'] > 0.001 else 'No'
    grows_class = 'growth-yes' if grows == 'Yes' else 'growth-no'

    html_parts.append('<tr>')
    html_parts.append(f'<td><strong>{row["Organism_ID"]}</strong></td>')
    html_parts.append(f'<td>{row["Draft_Reactions"]}</td>')
    html_parts.append(f'<td>{row["Draft_Metabolites"]}</td>')
    html_parts.append(f'<td>{row["Draft_Genes"]}</td>')
    html_parts.append(f'<td>{row["Draft_Growth"]:.4f}</td>')
    html_parts.append(f'<td>{row["Gapfilled_Reactions_Added"]}</td>')
    html_parts.append(f'<td>{row["Gapfilled_Growth"]:.4f}</td>')
    html_parts.append(f'<td class="{grows_class}">{grows}</td>')
    html_parts.append('</tr>')

html_parts.append('</tbody></table>')

# Summary statistics
avg_reactions = successful['Draft_Reactions'].mean()
avg_metabolites = successful['Draft_Metabolites'].mean()
avg_genes = successful['Draft_Genes'].mean()
avg_gapfill = successful['Gapfilled_Reactions_Added'].mean()
avg_growth = successful[successful['Gapfilled_Growth'] > 0.001]['Gapfilled_Growth'].mean()

html_parts.append('<div class="section-title">Summary Statistics</div>')
html_parts.append('<table style="max-width: 600px;">')
html_parts.append('<tr><td><strong>Average Draft Reactions</strong></td><td>{:.0f} ± {:.0f}</td></tr>'.format(
    avg_reactions, successful['Draft_Reactions'].std()))
html_parts.append('<tr><td><strong>Average Draft Metabolites</strong></td><td>{:.0f} ± {:.0f}</td></tr>'.format(
    avg_metabolites, successful['Draft_Metabolites'].std()))
html_parts.append('<tr><td><strong>Average Draft Genes</strong></td><td>{:.0f} ± {:.0f}</td></tr>'.format(
    avg_genes, successful['Draft_Genes'].std()))
html_parts.append('<tr><td><strong>Average Reactions Added</strong></td><td>{:.0f}</td></tr>'.format(avg_gapfill))
html_parts.append('<tr><td><strong>Average Growth Rate (growing models)</strong></td><td>{:.4f}</td></tr>'.format(avg_growth))
html_parts.append('<tr><td><strong>Success Rate (growth > 0.001)</strong></td><td>{:.1f}%</td></tr>'.format(
    100 * growing_after_gapfill / successful_count))
html_parts.append('</table>')

# Footer
footer = f"""
        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #e0e0e0; color: #7f8c8d; font-size: 12px;">
            Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}<br>
            Ticket: CDMSCI-198 - Build genome-scale metabolic models<br>
            Template: GramNegModelTemplateV6<br>
            Gap-filling media: Pyruvate minimal media
        </div>
    </div>
</body>
</html>
"""
html_parts.append(footer)

# Write HTML file
output_file = Path('results/model_statistics_viewer.html')
with open(output_file, 'w') as f:
    f.write('\n'.join(html_parts))

print(f"Created interactive viewer: {output_file}")
print(f"Open in browser: file://{output_file.absolute()}")
