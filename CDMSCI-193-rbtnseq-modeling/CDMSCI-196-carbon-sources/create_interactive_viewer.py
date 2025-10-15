#!/usr/bin/env python3
"""
Create Interactive Growth Matrix Viewer with Dataset Selector

Generates interactive HTML visualization with:
- Dataset selector dropdown (Full vs Filtered)
- Interactive heatmap with zoom/pan controls
- Color-coded: Green (Growth), Red (No Growth), Gray (Unknown)
- Searchable organism and carbon source lists with smart filtering
- Summary statistics that update with dataset selection
- Hover tooltips with details
- Standalone HTML file for sharing
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# Configuration
RESULTS_DIR = Path("results")
FULL_MATRIX_FILE = RESULTS_DIR / "combined_growth_matrix.csv"
FILTERED_MATRIX_FILE = RESULTS_DIR / "combined_growth_matrix_filtered.csv"
OUTPUT_FILE = RESULTS_DIR / "growth_matrix_viewer.html"

print("Loading growth matrices...")
print("\n1. Loading FULL matrix...")
data_full = pd.read_csv(FULL_MATRIX_FILE, index_col=0).fillna('')
print(f"   Carbon sources: {len(data_full.index)}")
print(f"   Organisms: {len(data_full.columns)}")
print(f"   Total cells: {data_full.size:,}")

print("\n2. Loading FILTERED matrix (use only)...")
data_filtered = pd.read_csv(FILTERED_MATRIX_FILE, index_col=0).fillna('')
print(f"   Carbon sources: {len(data_filtered.index)}")
print(f"   Organisms: {len(data_filtered.columns)}")
print(f"   Total cells: {data_filtered.size:,}")


def process_dataset(data, dataset_name):
    """Process a dataset and return stats + data dict"""
    # Count values
    n_growth = int((data == 'Growth').sum().sum())
    n_no_growth = int((data == 'No Growth').sum().sum())
    n_unknown = int((data == '').sum().sum())

    # Calculate data coverage statistics
    # For each carbon source: how many organisms have data (Growth or No Growth)?
    carbon_coverage = []
    for carbon in data.index:
        n_tested = int(((data.loc[carbon] == 'Growth') | (data.loc[carbon] == 'No Growth')).sum())
        carbon_coverage.append(n_tested)

    # For each organism: how many carbon sources have data?
    organism_coverage = []
    for organism in data.columns:
        n_tested = int(((data[organism] == 'Growth') | (data[organism] == 'No Growth')).sum())
        organism_coverage.append(n_tested)

    # Create data matrix as JSON for JavaScript
    data_dict = {}
    for carbon in data.index:
        data_dict[carbon] = {}
        for organism in data.columns:
            value = data.loc[carbon, organism]
            if value == '':
                value = 'Unknown'
            data_dict[carbon][organism] = value

    return {
        'name': dataset_name,
        'n_carbons': int(len(data.index)),
        'n_organisms': int(len(data.columns)),
        'n_total': int(data.size),
        'n_growth': n_growth,
        'n_no_growth': n_no_growth,
        'n_unknown': n_unknown,
        'data_dict': data_dict,
        'carbons': sorted(data.index.astype(str).tolist()),
        'organisms': sorted(data.columns.astype(str).tolist()),
        'carbon_coverage': carbon_coverage,
        'organism_coverage': organism_coverage
    }


print("\nProcessing datasets...")
full_stats = process_dataset(data_full, "Full Dataset")
filtered_stats = process_dataset(data_filtered, "Filtered Dataset (use only)")

print(f"\nFull dataset:")
print(f"  Growth: {full_stats['n_growth']:,} ({100*full_stats['n_growth']/full_stats['n_total']:.1f}%)")
print(f"  No Growth: {full_stats['n_no_growth']:,} ({100*full_stats['n_no_growth']/full_stats['n_total']:.1f}%)")
print(f"  Unknown: {full_stats['n_unknown']:,} ({100*full_stats['n_unknown']/full_stats['n_total']:.1f}%)")

print(f"\nFiltered dataset:")
print(f"  Growth: {filtered_stats['n_growth']:,} ({100*filtered_stats['n_growth']/filtered_stats['n_total']:.1f}%)")
print(f"  No Growth: {filtered_stats['n_no_growth']:,} ({100*filtered_stats['n_no_growth']/filtered_stats['n_total']:.1f}%)")
print(f"  Unknown: {filtered_stats['n_unknown']:,} ({100*filtered_stats['n_unknown']/filtered_stats['n_total']:.1f}%)")

print("\nGenerating HTML...")

# Convert stats to JSON
full_stats_json = json.dumps(full_stats)
filtered_stats_json = json.dumps(filtered_stats)

# Build HTML
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Growth Matrix Viewer</title>
    <script src="https://cdn.plot.ly/plotly-2.26.0.min.js"></script>
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
        .dataset-selector {{
            margin: 20px 0;
            padding: 15px;
            background-color: #e3f2fd;
            border-radius: 6px;
            border-left: 4px solid #2196F3;
        }}
        .dataset-selector label {{
            font-weight: bold;
            margin-right: 10px;
            font-size: 16px;
        }}
        .dataset-selector select {{
            padding: 8px 12px;
            font-size: 14px;
            border: 2px solid #2196F3;
            border-radius: 4px;
            background-color: white;
            cursor: pointer;
        }}
        .dataset-selector select:focus {{
            outline: none;
            border-color: #1976D2;
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
            transition: all 0.3s;
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
            margin-bottom: 20px;
        }}
        #heatmap {{
            width: 100%;
            height: 800px;
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
        .comparison {{
            background-color: #fff3e0;
            padding: 12px;
            border-radius: 4px;
            border-left: 4px solid #ff9800;
            margin: 15px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>RBTnSeq Growth Matrix Viewer</h1>
        <div class="info">
            <strong>Data Source:</strong> Combined Fitness Browser + 2018 Nature Paper (Price et al.)<br>
            <strong>Last Updated:</strong> 2025-10-15
        </div>

        <div class="dataset-selector">
            <label for="datasetSelect">Select Dataset:</label>
            <select id="datasetSelect">
                <option value="full">Full Dataset ({full_stats['n_carbons']} carbon sources)</option>
                <option value="filtered">Filtered Dataset ({filtered_stats['n_carbons']} suitable carbon sources for modeling)</option>
            </select>
        </div>

        <div class="comparison" id="comparisonInfo">
            <strong>💡 Dataset Comparison:</strong><br>
            <strong>Full Dataset:</strong> All {full_stats['n_carbons']} carbon sources from experimental data<br>
            <strong>Filtered Dataset:</strong> Only {filtered_stats['n_carbons']} carbon sources with "use" recommendation (excludes polymers, proprietary blends, atypical compounds)<br>
            <strong>Removed:</strong> {full_stats['n_carbons'] - filtered_stats['n_carbons']} carbon sources ({100*(full_stats['n_carbons'] - filtered_stats['n_carbons'])/full_stats['n_carbons']:.1f}%)
        </div>
    </div>

    <div class="header">
        <h3>Summary Statistics - <span id="currentDatasetName">Full Dataset</span></h3>
        <div class="stats">
            <div class="stat-box growth">
                <div class="stat-number" id="growthCount">{full_stats['n_growth']:,}</div>
                <div class="stat-label" id="growthPercent">Growth ({100*full_stats['n_growth']/full_stats['n_total']:.1f}%)</div>
            </div>
            <div class="stat-box no-growth">
                <div class="stat-number" id="noGrowthCount">{full_stats['n_no_growth']:,}</div>
                <div class="stat-label" id="noGrowthPercent">No Growth ({100*full_stats['n_no_growth']/full_stats['n_total']:.1f}%)</div>
            </div>
            <div class="stat-box unknown">
                <div class="stat-number" id="unknownCount">{full_stats['n_unknown']:,}</div>
                <div class="stat-label" id="unknownPercent">Unknown ({100*full_stats['n_unknown']/full_stats['n_total']:.1f}%)</div>
            </div>
        </div>
        <div class="info" id="matrixInfo">
            <strong>Matrix Size:</strong> <span id="matrixSize">{full_stats['n_carbons']} carbon sources × {full_stats['n_organisms']} organisms = {full_stats['n_total']:,} total cells</span>
        </div>
    </div>

    <div class="search-section">
        <h3>Search & Filter</h3>
        <div class="search-container">
            <div>
                <input type="text" class="search-box" id="organismSearch" placeholder="Search organisms...">
                <button class="clear-filter" id="clearOrganismFilter">Clear organism filter</button>
                <div class="list-container" id="organismList"></div>
            </div>
            <div>
                <input type="text" class="search-box" id="carbonSearch" placeholder="Search carbon sources...">
                <button class="clear-filter" id="clearCarbonFilter">Clear carbon filter</button>
                <div class="list-container" id="carbonList"></div>
            </div>
        </div>
        <div class="info" style="margin-top: 15px;">
            <strong>Tip:</strong> Click an organism to filter carbon sources where it grows, or click a carbon source to filter organisms that grow on it.
        </div>
    </div>

    <div class="heatmap-container">
        <h3>Interactive Heatmap</h3>
        <p class="info">
            <strong>Controls:</strong> Scroll to zoom, click-drag to pan, hover for details, double-click to reset<br>
            <strong>Colors:</strong> Green = Growth | Red = No Growth | Gray = Unknown
        </p>
        <div id="heatmap"></div>
    </div>

    <div class="header">
        <h3>Data Coverage Distribution - <span id="currentDatasetNameCoverage">Full Dataset</span></h3>
        <div class="info" style="margin-bottom: 15px;">
            These histograms show testing coverage across the matrix.
            <strong>Left:</strong> How many organisms each carbon source was tested on.
            <strong>Right:</strong> How many carbon sources each organism was tested on.
        </div>
        <div id="coveragePlots"></div>
    </div>

    <script>
        // Load datasets
        const datasets = {{
            full: {full_stats_json},
            filtered: {filtered_stats_json}
        }};

        let currentDataset = 'full';
        let selectedOrganism = null;
        let selectedCarbon = null;

        // Initialize
        function initializeViewer() {{
            updateViewer();
        }}

        // Update viewer when dataset changes
        function updateViewer() {{
            const stats = datasets[currentDataset];

            // Update stats display
            document.getElementById('currentDatasetName').textContent = stats.name;
            document.getElementById('growthCount').textContent = stats.n_growth.toLocaleString();
            document.getElementById('growthPercent').textContent = `Growth (${{(100*stats.n_growth/stats.n_total).toFixed(1)}}%)`;
            document.getElementById('noGrowthCount').textContent = stats.n_no_growth.toLocaleString();
            document.getElementById('noGrowthPercent').textContent = `No Growth (${{(100*stats.n_no_growth/stats.n_total).toFixed(1)}}%)`;
            document.getElementById('unknownCount').textContent = stats.n_unknown.toLocaleString();
            document.getElementById('unknownPercent').textContent = `Unknown (${{(100*stats.n_unknown/stats.n_total).toFixed(1)}}%)`;
            document.getElementById('matrixSize').textContent = `${{stats.n_carbons}} carbon sources × ${{stats.n_organisms}} organisms = ${{stats.n_total.toLocaleString()}} total cells`;

            // Clear filters
            selectedOrganism = null;
            selectedCarbon = null;
            document.getElementById('clearOrganismFilter').classList.remove('active');
            document.getElementById('clearCarbonFilter').classList.remove('active');

            // Update lists
            updateLists();

            // Update heatmap
            updateHeatmap();

            // Update coverage plots
            updateCoveragePlots();
        }}

        // Update organism and carbon lists
        function updateLists() {{
            const stats = datasets[currentDataset];

            // Update organism list
            const organismList = document.getElementById('organismList');
            organismList.innerHTML = stats.organisms.map(org =>
                `<div class="organism-item" data-name="${{org}}">${{org}}</div>`
            ).join('');

            // Update carbon list
            const carbonList = document.getElementById('carbonList');
            carbonList.innerHTML = stats.carbons.map(carbon =>
                `<div class="carbon-item" data-name="${{carbon}}">${{carbon}}</div>`
            ).join('');

            // Re-attach event listeners
            attachListeners();
        }}

        // Update heatmap
        function updateHeatmap() {{
            const stats = datasets[currentDataset];

            // Convert to matrix
            const z = [];
            const hovertext = [];

            for (let carbon of stats.carbons) {{
                const row = [];
                const hoverRow = [];
                for (let organism of stats.organisms) {{
                    const value = stats.data_dict[carbon][organism];
                    let numValue;
                    if (value === 'Growth') numValue = 1;
                    else if (value === 'No Growth') numValue = -1;
                    else numValue = 0;

                    row.push(numValue);
                    hoverRow.push(`<b>${{organism}}</b><br>Carbon: ${{carbon}}<br>Result: <b>${{value}}</b>`);
                }}
                z.push(row);
                hovertext.push(hoverRow);
            }}

            const data = [{{
                z: z,
                x: stats.organisms,
                y: stats.carbons,
                type: 'heatmap',
                colorscale: [
                    [0.0, '#d62728'],   // Red for No Growth (-1)
                    [0.5, '#e0e0e0'],   // Gray for Unknown (0)
                    [1.0, '#2ca02c']    // Green for Growth (1)
                ],
                zmid: 0,
                zmin: -1,
                zmax: 1,
                hovertemplate: '%{{hovertext}}<extra></extra>',
                hovertext: hovertext,
                colorbar: {{
                    title: 'Growth',
                    tickvals: [-1, 0, 1],
                    ticktext: ['No Growth', 'Unknown', 'Growth'],
                    len: 0.4
                }}
            }}];

            const layout = {{
                title: `${{stats.name}}<br><sub>${{stats.n_carbons}} Carbon Sources × ${{stats.n_organisms}} Organisms</sub>`,
                xaxis: {{
                    title: 'Organisms',
                    tickangle: -45,
                    tickfont: {{ size: 9 }}
                }},
                yaxis: {{
                    title: 'Carbon Sources',
                    tickfont: {{ size: 8 }}
                }},
                margin: {{ l: 200, r: 50, t: 100, b: 150 }},
                dragmode: 'pan'
            }};

            const config = {{
                scrollZoom: true,
                displayModeBar: true,
                modeBarButtonsToRemove: ['lasso2d', 'select2d'],
                displaylogo: false,
                responsive: true
            }};

            Plotly.newPlot('heatmap', data, layout, config);
        }}

        // Update coverage plots
        function updateCoveragePlots() {{
            const stats = datasets[currentDataset];

            // Update coverage dataset name
            document.getElementById('currentDatasetNameCoverage').textContent = stats.name;

            // Create subplot data - use xaxis and yaxis to separate
            const trace1 = {{
                x: stats.carbon_coverage,
                type: 'histogram',
                nbinsx: 20,
                marker: {{ color: '#2196F3' }},
                name: 'Carbon Sources',
                xaxis: 'x1',
                yaxis: 'y1',
                hovertemplate: '%{{x}} organisms tested<br>Count: %{{y}}<extra></extra>'
            }};

            const trace2 = {{
                x: stats.organism_coverage,
                type: 'histogram',
                nbinsx: 20,
                marker: {{ color: '#4CAF50' }},
                name: 'Organisms',
                xaxis: 'x2',
                yaxis: 'y2',
                hovertemplate: '%{{x}} carbon sources tested<br>Count: %{{y}}<extra></extra>'
            }};

            const layout = {{
                height: 350,
                showlegend: false,
                margin: {{ l: 50, r: 50, t: 50, b: 50 }},
                xaxis: {{
                    title: 'Number of organisms tested',
                    domain: [0, 0.45]
                }},
                yaxis: {{
                    title: 'Count'
                }},
                xaxis2: {{
                    title: 'Number of carbon sources tested',
                    domain: [0.55, 1]
                }},
                yaxis2: {{
                    title: 'Count',
                    anchor: 'x2'
                }}
            }};

            const config = {{
                displayModeBar: false,
                responsive: true
            }};

            Plotly.newPlot('coveragePlots', [trace1, trace2], layout, config);
        }}

        // Attach event listeners to lists
        function attachListeners() {{
            // Organism search
            document.getElementById('organismSearch').addEventListener('input', function(e) {{
                const searchTerm = e.target.value.toLowerCase();
                document.querySelectorAll('.organism-item').forEach(item => {{
                    if (item.classList.contains('filtered-out')) return;
                    item.style.display = item.textContent.toLowerCase().includes(searchTerm) ? 'block' : 'none';
                }});
            }});

            // Carbon search
            document.getElementById('carbonSearch').addEventListener('input', function(e) {{
                const searchTerm = e.target.value.toLowerCase();
                document.querySelectorAll('.carbon-item').forEach(item => {{
                    if (item.classList.contains('filtered-out')) return;
                    item.style.display = item.textContent.toLowerCase().includes(searchTerm) ? 'block' : 'none';
                }});
            }});

            // Organism click
            document.querySelectorAll('.organism-item').forEach(item => {{
                item.addEventListener('click', function() {{
                    const organismName = this.getAttribute('data-name');
                    const stats = datasets[currentDataset];

                    document.querySelectorAll('.organism-item').forEach(i => i.classList.remove('selected'));
                    this.classList.add('selected');
                    selectedOrganism = organismName;

                    document.getElementById('carbonSearch').value = '';

                    const carbonList = document.getElementById('carbonList');
                    const carbonItems = Array.from(document.querySelectorAll('.carbon-item'));
                    const matching = [];
                    const nonMatching = [];

                    carbonItems.forEach(carbonItem => {{
                        const carbonName = carbonItem.getAttribute('data-name');
                        const value = stats.data_dict[carbonName] && stats.data_dict[carbonName][organismName];

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

                    carbonList.innerHTML = '';
                    matching.forEach(item => carbonList.appendChild(item));
                    nonMatching.forEach(item => carbonList.appendChild(item));
                    carbonList.scrollTop = 0;
                    document.getElementById('clearOrganismFilter').classList.add('active');
                }});
            }});

            // Carbon click
            document.querySelectorAll('.carbon-item').forEach(item => {{
                item.addEventListener('click', function() {{
                    const carbonName = this.getAttribute('data-name');
                    const stats = datasets[currentDataset];

                    document.querySelectorAll('.carbon-item').forEach(i => i.classList.remove('selected'));
                    this.classList.add('selected');
                    selectedCarbon = carbonName;

                    document.getElementById('organismSearch').value = '';

                    const organismList = document.getElementById('organismList');
                    const organismItems = Array.from(document.querySelectorAll('.organism-item'));
                    const matching = [];
                    const nonMatching = [];

                    organismItems.forEach(orgItem => {{
                        const organismName = orgItem.getAttribute('data-name');
                        const value = stats.data_dict[carbonName] && stats.data_dict[carbonName][organismName];

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

                    organismList.innerHTML = '';
                    matching.forEach(item => organismList.appendChild(item));
                    nonMatching.forEach(item => organismList.appendChild(item));
                    organismList.scrollTop = 0;
                    document.getElementById('clearCarbonFilter').classList.add('active');
                }});
            }});
        }}

        // Clear filters
        document.getElementById('clearOrganismFilter').addEventListener('click', function() {{
            selectedOrganism = null;
            document.querySelectorAll('.organism-item').forEach(i => i.classList.remove('selected'));

            const stats = datasets[currentDataset];
            const carbonList = document.getElementById('carbonList');
            carbonList.innerHTML = stats.carbons.map(carbon =>
                `<div class="carbon-item" data-name="${{carbon}}">${{carbon}}</div>`
            ).join('');

            carbonList.scrollTop = 0;
            this.classList.remove('active');
            attachListeners();
        }});

        document.getElementById('clearCarbonFilter').addEventListener('click', function() {{
            selectedCarbon = null;
            document.querySelectorAll('.carbon-item').forEach(i => i.classList.remove('selected'));

            const stats = datasets[currentDataset];
            const organismList = document.getElementById('organismList');
            organismList.innerHTML = stats.organisms.map(org =>
                `<div class="organism-item" data-name="${{org}}">${{org}}</div>`
            ).join('');

            organismList.scrollTop = 0;
            this.classList.remove('active');
            attachListeners();
        }});

        // Dataset selector
        document.getElementById('datasetSelect').addEventListener('change', function() {{
            currentDataset = this.value;
            updateViewer();
        }});

        // Initialize on load
        initializeViewer();
    </script>
</body>
</html>
"""

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
print(f"  ✓ Dataset selector dropdown (Full vs Filtered)")
print(f"  ✓ Summary statistics that update with dataset selection")
print(f"  ✓ Comparison info showing removed carbon sources")
print(f"  ✓ Searchable organism list")
print(f"  ✓ Searchable carbon source list")
print(f"  ✓ Smart filtering: Click organism → see carbon sources where it grows")
print(f"  ✓ Smart filtering: Click carbon source → see organisms that grow on it")
print(f"  ✓ Interactive heatmap with zoom/pan controls")
print(f"  ✓ Hover tooltips showing organism + carbon + result")
print(f"  ✓ Color coding: Green (Growth), Red (No Growth), Gray (Unknown)")
print(f"  ✓ Standalone HTML (requires Plotly CDN)")
print(f"\nDataset Comparison:")
print(f"  Full: {full_stats['n_carbons']} carbon sources")
print(f"  Filtered: {filtered_stats['n_carbons']} carbon sources")
print(f"  Removed: {full_stats['n_carbons'] - filtered_stats['n_carbons']} ({100*(full_stats['n_carbons'] - filtered_stats['n_carbons'])/full_stats['n_carbons']:.1f}%)")
print("\n" + "="*70)
