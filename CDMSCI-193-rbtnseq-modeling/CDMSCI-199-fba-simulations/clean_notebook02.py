#!/usr/bin/env python3
"""
Remove misleading "missing exchange" analysis from Notebook 02

The gap-filling was done on pyruvate minimal media, so calling exchanges
"missing" when they're only needed for other carbon sources is misleading.
"""

import json
from pathlib import Path

notebook_path = Path('02-analyze-predictions.ipynb')

with open(notebook_path, 'r') as f:
    nb = json.load(f)

# Cells to remove (by their markdown titles or first line of code)
cells_to_remove = []

for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))

    # Remove "Identify Which Compounds Are Missing" section (cells 41-43)
    if 'Identify Which Compounds Are Missing' in source:
        cells_to_remove.append(i)
        print(f"Removing cell {i}: 'Identify Which Compounds Are Missing' (markdown)")
    elif 'missing_compound_counts = Counter()' in source:
        cells_to_remove.append(i)
        print(f"Removing cell {i}: missing compound frequency analysis (code)")
    elif 'fn_missing_compounds = Counter()' in source:
        cells_to_remove.append(i)
        print(f"Removing cell {i}: FN missing compounds analysis (code)")

    # Remove "Issues to Investigate" section (cells 51-52)
    elif 'Issues to Investigate' in source:
        cells_to_remove.append(i)
        print(f"Removing cell {i}: 'Issues to Investigate' (markdown)")
    elif 'KEY ISSUES TO INVESTIGATE' in source:
        cells_to_remove.append(i)
        print(f"Removing cell {i}: KEY ISSUES summary (code)")

# Remove cells in reverse order to preserve indices
for i in reversed(cells_to_remove):
    del nb['cells'][i]

print(f"\nRemoved {len(cells_to_remove)} cells")
print(f"Notebook now has {len(nb['cells'])} cells (was {len(nb['cells']) + len(cells_to_remove)})")

# Add clarification note in place of removed section
clarification_markdown = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Analysis Scope Note\n\n",
        "**Important Context**: The gap-filled models used in this analysis were gap-filled specifically to enable growth on **pyruvate minimal media** (CDMSCI-198), not on all 121 carbon sources tested here.\n\n",
        "Therefore:\n",
        "- This analysis evaluates **draft model quality** and **gap-filled model generalization**\n",
        "- Models were never designed to grow on all carbon sources\n",
        "- Performance metrics reflect how well models predict phenotypes beyond their gap-filling objective\n\n",
        "**For future analysis**, consider:\n",
        "1. Compare draft models (pre-gap-filling) vs experimental data\n",
        "2. Perform condition-specific gap-filling for each false negative case\n",
        "3. Analyze whether condition-specific gap-filling produces meaningful biological additions or overfitting"
    ]
}

# Insert clarification where "Issues to Investigate" was
# Find cell 50 (should be just before where we removed 51-52)
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    if 'Context for Perfect Accuracy Cases' in source or 'perfect_carbon = carbon_df' in source:
        # Insert after the perfect accuracy analysis
        nb['cells'].insert(i + 2, clarification_markdown)
        print(f"\nInserted clarification note at position {i + 2}")
        break

# Save updated notebook
with open(notebook_path, 'w') as f:
    json.dump(nb, f, indent=1)

print(f"\nUpdated notebook saved: {notebook_path}")
print("\nRemoved misleading analysis sections:")
print("  - Cells 41-43: Which compounds are missing")
print("  - Cells 51-52: Issues to investigate (missing exchanges)")
print("\nAdded:")
print("  - Analysis scope clarification note")
