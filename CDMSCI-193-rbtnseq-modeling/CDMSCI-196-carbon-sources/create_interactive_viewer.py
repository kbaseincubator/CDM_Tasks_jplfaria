#!/usr/bin/env python3
"""
Create Interactive Growth Matrix Viewer

Generates interactive HTML visualization of combined growth matrix with:
- Interactive heatmap with zoom/pan controls
- Color-coded: Green (Growth), Red (No Growth), Gray (Unknown)
- Searchable organism and carbon source lists with smart filtering
- Summary statistics
- Hover tooltips with details
- Standalone HTML file for sharing
"""

import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
import json

# Configuration
RESULTS_DIR = Path("results")
INPUT_FILE = RESULTS_DIR / "combined_growth_matrix.csv"
OUTPUT_FILE = RESULTS_DIR / "growth_matrix_viewer.html"

print("Loading combined growth matrix...")
data = pd.read_csv(INPUT_FILE, index_col=0)

# Replace NaN with empty strings for consistency
data = data.fillna('')

print(f"\nLoaded matrix:")
print(f"  Carbon sources: {len(data.index)}")
print(f"  Organisms: {len(data.columns)}")
print(f"  Total cells: {data.size:,}")

# Count values
n_growth = (data == 'Growth').sum().sum()
n_no_growth = (data == 'No Growth').sum().sum()
n_unknown = (data == '').sum().sum()

print(f"\nOverall statistics:")
print(f"  Growth: {n_growth:,} ({100*n_growth/data.size:.1f}%)")
print(f"  No Growth: {n_no_growth:,} ({100*n_no_growth/data.size:.1f}%)")
print(f"  Unknown: {n_unknown:,} ({100*n_unknown/data.size:.1f}%)")

# Calculate data coverage statistics
# For each carbon source: how many organisms have data (Growth or No Growth)?
carbon_coverage = []
for carbon in data.index:
    n_tested = ((data.loc[carbon] == 'Growth') | (data.loc[carbon] == 'No Growth')).sum()
    carbon_coverage.append(n_tested)

# For each organism: how many carbon sources have data?
organism_coverage = []
for organism in data.columns:
    n_tested = ((data[organism] == 'Growth') | (data[organism] == 'No Growth')).sum()
    organism_coverage.append(n_tested)

print(f"\nData coverage:")
print(f"  Carbon sources tested on 1-10 organisms: {sum(1 for x in carbon_coverage if 1 <= x <= 10)}")
print(f"  Carbon sources tested on >10 organisms: {sum(1 for x in carbon_coverage if x > 10)}")
print(f"  Organisms tested on 1-50 carbons: {sum(1 for x in organism_coverage if 1 <= x <= 50)}")
print(f"  Organisms tested on >50 carbons: {sum(1 for x in organism_coverage if x > 50)}")

# Convert to numeric: Growth=1, No Growth=-1, Unknown=0
data_numeric = data.replace({'Growth': 1, 'No Growth': -1, '': 0})
data_numeric = data_numeric.astype(float)

print(f"\nCreating interactive heatmap...")

# Create hover text
hover_text = []
for carbon_idx, carbon in enumerate(data.index):
    hover_text_row = []
    for org_idx, organism in enumerate(data.columns):
        value = data.iloc[carbon_idx, org_idx]
        if value == '':
            value_text = 'Unknown'
        else:
            value_text = value
        hover_text_row.append(
            f"<b>{organism}</b><br>"
            f"Carbon: {carbon}<br>"
            f"Result: <b>{value_text}</b>"
        )
    hover_text.append(hover_text_row)

# Create heatmap
fig = go.Figure(data=go.Heatmap(
    z=data_numeric.values,
    x=data.columns.tolist(),
    y=data.index.tolist(),
    colorscale=[
        [0.0, '#d62728'],   # Red for No Growth (-1)
        [0.5, '#e0e0e0'],   # Gray for Unknown (0)
        [1.0, '#2ca02c']    # Green for Growth (1)
    ],
    zmid=0,
    zmin=-1,
    zmax=1,
    hovertemplate='%{hovertext}<extra></extra>',
    hovertext=hover_text,
    colorbar=dict(
        title="Growth",
        tickvals=[-1, 0, 1],
        ticktext=['No Growth', 'Unknown', 'Growth'],
        len=0.4
    )
))

# Update layout
fig.update_layout(
    title={
        'text': f'Combined Growth Matrix<br><sub>{len(data.index)} Carbon Sources × {len(data.columns)} Organisms</sub>',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis=dict(
        title='Organisms',
        tickangle=-45,
        tickfont=dict(size=9)
    ),
    yaxis=dict(
        title='Carbon Sources',
        tickfont=dict(size=8)
    ),
    width=None,  # Auto width
    height=1000,
    margin=dict(l=200, r=50, t=100, b=150),
    dragmode='pan'  # Enable pan by default
)

print("Creating coverage distribution plots...")

# Create coverage distribution plots
from plotly.subplots import make_subplots

# Create subplot figure with 2 histograms
coverage_fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=(
        'Carbon Sources: Number of Organisms Tested',
        'Organisms: Number of Carbon Sources Tested'
    )
)

# Histogram 1: Carbon source coverage
coverage_fig.add_trace(
    go.Histogram(
        x=carbon_coverage,
        nbinsx=20,
        marker_color='#2196F3',
        name='Carbon Sources',
        hovertemplate='%{x} organisms tested<br>%{y} carbon sources<extra></extra>'
    ),
    row=1, col=1
)

# Histogram 2: Organism coverage
coverage_fig.add_trace(
    go.Histogram(
        x=organism_coverage,
        nbinsx=20,
        marker_color='#4CAF50',
        name='Organisms',
        hovertemplate='%{x} carbon sources tested<br>%{y} organisms<extra></extra>'
    ),
    row=1, col=2
)

coverage_fig.update_xaxes(title_text="Number of organisms tested", row=1, col=1)
coverage_fig.update_xaxes(title_text="Number of carbon sources tested", row=1, col=2)
coverage_fig.update_yaxes(title_text="Count", row=1, col=1)
coverage_fig.update_yaxes(title_text="Count", row=1, col=2)

coverage_fig.update_layout(
    height=350,
    showlegend=False,
    margin=dict(l=50, r=50, t=50, b=50)
)

coverage_html = coverage_fig.to_html(
    include_plotlyjs=False,  # Already included from main heatmap
    div_id='coverage',
    full_html=False,
    config={'displayModeBar': False, 'responsive': True}
)

print("Generating HTML...")

# Create organism and carbon source lists
organism_list = "<br>".join([f"<div class='organism-item' data-name='{org}'>{org}</div>" for org in sorted(data.columns.astype(str))])
carbon_list = "<br>".join([f"<div class='carbon-item' data-name='{carbon}'>{carbon}</div>" for carbon in sorted(data.index.astype(str))])

# Create data matrix as JSON for JavaScript filtering
# Format: {carbon_source: {organism: "Growth/No Growth/Unknown"}}
data_dict = {}
for carbon in data.index:
    data_dict[carbon] = {}
    for organism in data.columns:
        value = data.loc[carbon, organism]
        if value == '':
            value = 'Unknown'
        data_dict[carbon][organism] = value

data_json = json.dumps(data_dict)

# Get heatmap div with better config
heatmap_div = fig.to_html(
    include_plotlyjs='cdn',
    div_id='heatmap',
    full_html=False,
    config={
        'scrollZoom': True,
        'displayModeBar': True,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
        'displaylogo': False,
        'responsive': True
    }
)

# Build HTML in parts to avoid f-string issues
html_header = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Growth Matrix Viewer</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .stats {{
            display: flex;
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-box {{
            flex: 1;
            padding: 15px;
            border-radius: 6px;
            text-align: center;
        }}
        .stat-box.growth {{
            background-color: #2ca02c;
            color: white;
        }}
        .stat-box.no-growth {{
            background-color: #d62728;
            color: white;
        }}
        .stat-box.unknown {{
            background-color: #e0e0e0;
            color: #333;
        }}
        .stat-number {{
            font-size: 32px;
            font-weight: bold;
        }}
        .stat-label {{
            font-size: 14px;
            margin-top: 5px;
        }}
        .search-section {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .search-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        .search-box {{
            width: 100%;
            padding: 10px;
            font-size: 14px;
            border: 2px solid #ddd;
            border-radius: 4px;
            margin-bottom: 10px;
        }}
        .search-box:focus {{
            outline: none;
            border-color: #2196F3;
        }}
        .list-container {{
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 10px;
            background-color: #fafafa;
        }}
        .organism-item, .carbon-item {{
            padding: 5px;
            margin: 2px 0;
            cursor: pointer;
            border-radius: 3px;
        }}
        .organism-item:hover, .carbon-item:hover {{
            background-color: #e3f2fd;
        }}
        .organism-item.selected, .carbon-item.selected {{
            background-color: #2196F3;
            color: white;
        }}
        .organism-item.filtered-out, .carbon-item.filtered-out {{
            display: none;
        }}
        .clear-filter {{
            padding: 8px 16px;
            background-color: #f44336;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-bottom: 10px;
            display: none;
        }}
        .clear-filter:hover {{
            background-color: #d32f2f;
        }}
        .clear-filter.active {{
            display: inline-block;
        }}
        .heatmap-container {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow-x: auto;
            max-width: 100%;
        }}
        #heatmap {{
            width: 100%;
            max-width: 100%;
        }}
        h1 {{
            color: #333;
            margin: 0 0 10px 0;
        }}
        h3 {{
            color: #555;
            margin-top: 0;
        }}
        .info {{
            color: #666;
            font-size: 14px;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>RBTnSeq database Growth / NO Growth Viewer</h1>
        <div class="info">
            <strong>Data Source:</strong> Combined Fitness Browser + 2018 Nature Paper (Price et al.)<br>
            <strong>Matrix Size:</strong> {len(data.index)} carbon sources × {len(data.columns)} organisms = {data.size:,} total cells<br>
            <strong>Last Updated:</strong> 2025-10-14
        </div>
    </div>

    <div class="header">
        <h3>Summary Statistics</h3>
        <div class="stats">
            <div class="stat-box growth">
                <div class="stat-number">{n_growth:,}</div>
                <div class="stat-label">Growth ({100*n_growth/data.size:.1f}%)</div>
            </div>
            <div class="stat-box no-growth">
                <div class="stat-number">{n_no_growth:,}</div>
                <div class="stat-label">No Growth ({100*n_no_growth/data.size:.1f}%)</div>
            </div>
            <div class="stat-box unknown">
                <div class="stat-number">{n_unknown:,}</div>
                <div class="stat-label">Unknown ({100*n_unknown/data.size:.1f}%)</div>
            </div>
        </div>
        <div class="info" style="margin-top: 15px;">
            <strong>Note on "Unknown":</strong> High proportion of Unknown data reflects the combinatorial challenge of testing 208 carbon sources × 57 organisms.
            Many carbon sources were only tested on a subset of organisms. See distribution below for data coverage patterns.
        </div>
    </div>

    <div class="search-section">
        <h3>Search & Filter by Growth Data</h3>
        <div class="search-container">
            <div>
                <input type="text" class="search-box" id="organismSearch" placeholder="Search organisms...">
                <button class="clear-filter" id="clearOrganismFilter">Clear organism filter</button>
                <div class="list-container" id="organismList">
                    {organism_list}
                </div>
            </div>
            <div>
                <input type="text" class="search-box" id="carbonSearch" placeholder="Search carbon sources...">
                <button class="clear-filter" id="clearCarbonFilter">Clear carbon filter</button>
                <div class="list-container" id="carbonList">
                    {carbon_list}
                </div>
            </div>
        </div>
        <div class="info" style="margin-top: 15px;">
            <strong>Tip:</strong> Click an organism to filter carbon sources where it grows, or click a carbon source to filter organisms that grow on it.
        </div>
    </div>

    <div class="heatmap-container">
        <h3>Interactive Heatmap</h3>
        <p class="info">
            <strong>Controls:</strong> Use toolbar to zoom/pan, or scroll to zoom, click-drag to pan, hover for details, double-click to reset<br>
            <strong>Colors:</strong> Green = Growth | Red = No Growth | Gray = Unknown
        </p>
"""

html_middle = f"""
    </div>

    <div class="header">
        <h3>Data Coverage Distribution</h3>
        <div class="info" style="margin-bottom: 15px;">
            These histograms show testing coverage across the matrix.
            <strong>Left:</strong> How many organisms each carbon source was tested on.
            <strong>Right:</strong> How many carbon sources each organism was tested on.
        </div>
        {coverage_html}
    </div>
"""

html_footer = f"""
    <script>
        // Load data matrix
        const dataMatrix = {data_json};

        let selectedOrganism = null;
        let selectedCarbon = null;

        // Search functionality for organisms
        document.getElementById('organismSearch').addEventListener('input', function(e) {{
            const searchTerm = e.target.value.toLowerCase();
            const items = document.querySelectorAll('.organism-item');
            items.forEach(item => {{
                if (item.classList.contains('filtered-out')) return; // Don't show filtered out items
                const text = item.textContent.toLowerCase();
                item.style.display = text.includes(searchTerm) ? 'block' : 'none';
            }});
        }});

        // Search functionality for carbon sources
        document.getElementById('carbonSearch').addEventListener('input', function(e) {{
            const searchTerm = e.target.value.toLowerCase();
            const items = document.querySelectorAll('.carbon-item');
            items.forEach(item => {{
                if (item.classList.contains('filtered-out')) return; // Don't show filtered out items
                const text = item.textContent.toLowerCase();
                item.style.display = text.includes(searchTerm) ? 'block' : 'none';
            }});
        }});

        // Click organism to filter carbon sources where it has Growth
        document.querySelectorAll('.organism-item').forEach(item => {{
            item.addEventListener('click', function() {{
                const organismName = this.getAttribute('data-name');

                // Clear previous selection
                document.querySelectorAll('.organism-item').forEach(i => i.classList.remove('selected'));
                this.classList.add('selected');
                selectedOrganism = organismName;

                // Clear search box
                document.getElementById('carbonSearch').value = '';

                // Separate matching and non-matching items
                const carbonList = document.getElementById('carbonList');
                const carbonItems = Array.from(document.querySelectorAll('.carbon-item'));
                const matching = [];
                const nonMatching = [];

                carbonItems.forEach(carbonItem => {{
                    const carbonName = carbonItem.getAttribute('data-name');
                    const value = dataMatrix[carbonName] && dataMatrix[carbonName][organismName];

                    if (value === 'Growth') {{
                        carbonItem.classList.remove('filtered-out');
                        carbonItem.style.display = 'block';
                        matching.push(carbonItem);
                    }} else {{
                        carbonItem.classList.add('filtered-out');
                        carbonItem.style.display = 'none';
                        nonMatching.push(carbonItem);
                    }}
                }});

                // Re-order: matching items first, then non-matching
                carbonList.innerHTML = '';
                matching.forEach(item => carbonList.appendChild(item));
                nonMatching.forEach(item => carbonList.appendChild(item));

                // Scroll to top
                carbonList.scrollTop = 0;

                // Show clear filter button
                document.getElementById('clearOrganismFilter').classList.add('active');
            }});
        }});

        // Click carbon source to filter organisms that have Growth on it
        document.querySelectorAll('.carbon-item').forEach(item => {{
            item.addEventListener('click', function() {{
                const carbonName = this.getAttribute('data-name');

                // Clear previous selection
                document.querySelectorAll('.carbon-item').forEach(i => i.classList.remove('selected'));
                this.classList.add('selected');
                selectedCarbon = carbonName;

                // Clear search box
                document.getElementById('organismSearch').value = '';

                // Separate matching and non-matching items
                const organismList = document.getElementById('organismList');
                const organismItems = Array.from(document.querySelectorAll('.organism-item'));
                const matching = [];
                const nonMatching = [];

                organismItems.forEach(orgItem => {{
                    const organismName = orgItem.getAttribute('data-name');
                    const value = dataMatrix[carbonName] && dataMatrix[carbonName][organismName];

                    if (value === 'Growth') {{
                        orgItem.classList.remove('filtered-out');
                        orgItem.style.display = 'block';
                        matching.push(orgItem);
                    }} else {{
                        orgItem.classList.add('filtered-out');
                        orgItem.style.display = 'none';
                        nonMatching.push(orgItem);
                    }}
                }});

                // Re-order: matching items first, then non-matching
                organismList.innerHTML = '';
                matching.forEach(item => organismList.appendChild(item));
                nonMatching.forEach(item => organismList.appendChild(item));

                // Scroll to top
                organismList.scrollTop = 0;

                // Show clear filter button
                document.getElementById('clearCarbonFilter').classList.add('active');
            }});
        }});

        // Clear organism filter
        document.getElementById('clearOrganismFilter').addEventListener('click', function() {{
            selectedOrganism = null;
            document.querySelectorAll('.organism-item').forEach(i => i.classList.remove('selected'));

            // Restore original alphabetical order
            const carbonList = document.getElementById('carbonList');
            const carbonItems = Array.from(document.querySelectorAll('.carbon-item'));
            carbonItems.sort((a, b) => a.getAttribute('data-name').localeCompare(b.getAttribute('data-name')));

            carbonList.innerHTML = '';
            carbonItems.forEach(item => {{
                item.classList.remove('filtered-out');
                item.style.display = 'block';
                carbonList.appendChild(item);
            }});

            carbonList.scrollTop = 0;
            this.classList.remove('active');
        }});

        // Clear carbon filter
        document.getElementById('clearCarbonFilter').addEventListener('click', function() {{
            selectedCarbon = null;
            document.querySelectorAll('.carbon-item').forEach(i => i.classList.remove('selected'));

            // Restore original alphabetical order
            const organismList = document.getElementById('organismList');
            const organismItems = Array.from(document.querySelectorAll('.organism-item'));
            organismItems.sort((a, b) => a.getAttribute('data-name').localeCompare(b.getAttribute('data-name')));

            organismList.innerHTML = '';
            organismItems.forEach(item => {{
                item.classList.remove('filtered-out');
                item.style.display = 'block';
                organismList.appendChild(item);
            }});

            organismList.scrollTop = 0;
            this.classList.remove('active');
        }});
    </script>
</body>
</html>
"""

# Combine all parts
html_content = html_header + heatmap_div + html_middle + html_footer

print(f"\nSaving interactive viewer to: {OUTPUT_FILE}")

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"\n✓ Saved successfully!")
print(f"\nTo view:")
print(f"  Open in browser: {OUTPUT_FILE.absolute()}")
print(f"\nFile size: {OUTPUT_FILE.stat().st_size / 1e6:.2f} MB")
print("\n" + "="*70)
print("INTERACTIVE VIEWER CREATED")
print("="*70)
print(f"\nFeatures:")
print(f"  ✓ Summary statistics with color coding")
print(f"  ✓ Searchable organism list ({len(data.columns)} organisms)")
print(f"  ✓ Searchable carbon source list ({len(data.index)} sources)")
print(f"  ✓ Smart filtering: Click organism → see carbon sources where it grows")
print(f"  ✓ Smart filtering: Click carbon source → see organisms that grow on it")
print(f"  ✓ Interactive heatmap with zoom/pan controls")
print(f"  ✓ Hover tooltips showing organism + carbon + result")
print(f"  ✓ Color coding: Green (Growth), Red (No Growth), Gray (Unknown)")
print(f"  ✓ Standalone HTML (no external dependencies except Plotly CDN)")
print(f"\nShare with co-workers:")
print(f"  - Send the HTML file via email/Slack")
print(f"  - Recipients can open directly in any browser")
print(f"  - No installation required")
print("\n" + "="*70)
