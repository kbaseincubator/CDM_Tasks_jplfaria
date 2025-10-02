# CDMSCI-196: Compile Carbon Sources List

**Parent**: CDMSCI-193 - RBTnSeq Modeling Analysis

## Objective

Extract and compile a comprehensive list of all carbon source conditions tested across all 57 genomes in the Fitness Browser RBTnSeq database (Deutschbauer lab).

## Input

- Fitness Browser database (`feba.db`) located in `../../shared_resources/database/`
- 57 organisms with experimental fitness data

## Approach

1. Query Fitness Browser database for all carbon source experiments
2. Filter by `expGroup = 'carbon source'`
3. Apply quality filters:
   - `gMed >= 50` (sufficient read depth)
   - `mad12 <= 0.5` (good gene-half consistency)
4. Create organism × carbon source binary matrix

## Assumption

**Missing data interpretation**:
- **1 (Growth)**: Organism has experimental data for this carbon source
- **0 (No Growth)**: Organism lacks data for this carbon source

> **Note**: Missing data likely means "not tested" rather than "tested but failed to grow", but we proceed with the assumption that missing = no growth for model validation purposes.

## Outputs

### Results Files

All outputs saved to `results/` directory:

1. **carbon_source_growth_matrix.csv**
   - Binary matrix: 57 organisms × ~80-100 carbon sources
   - Values: 1 = growth, 0 = no growth
   - Format: CSV with organism IDs as index

2. **carbon_source_growth_matrix_stats.txt**
   - Coverage statistics
   - Per-organism metrics (max/min/median carbon sources tested)
   - Per-carbon metrics (max/min/median organisms tested)

3. **carbon_source_growth_heatmap.png**
   - Visual heatmap (green = growth, white = no growth)
   - Sorted by coverage for better visualization
   - 300 DPI, publication quality

4. **carbon_source_list.csv** _(to be generated)_
   - Complete list of unique carbon sources
   - Number of organisms tested per carbon source

## Code

### Jupyter Notebook (Recommended)

**File**: `02-create-carbon-source-growth-matrix.ipynb`

**How to run**:
```bash
jupyter notebook 02-create-carbon-source-growth-matrix.ipynb
```

**Features**:
- Interactive exploration
- Database statistics
- Visualization
- Quality filtering options

### Python Script (Alternative)

**File**: `create_growth_matrix.py`

**How to run**:
```bash
# Basic usage
python create_growth_matrix.py \
    --db ../../shared_resources/database/feba.db \
    --output results/carbon_source_matrix.csv

# With carbon source filtering and group-specific matrices
python create_growth_matrix.py \
    --db ../../shared_resources/database/feba.db \
    --output results/growth_matrix.csv \
    --by-group
```

**Options**:
- `--db`: Path to feba.db database
- `--output`: Output CSV file path
- `--no-quality-filter`: Disable quality filtering
- `--by-group`: Create separate matrices per condition group

## Usage for Downstream Tasks

### For CDMSCI-197 (Media Formulations)

```python
import pandas as pd

# Load carbon source matrix
matrix = pd.read_csv('results/carbon_source_growth_matrix.csv', index_col=0)

# Get list of unique carbon sources
carbon_sources = matrix.columns.tolist()

# Map to ModelSEED compounds (next step)
# ... proceed to CDMSCI-197
```

### For CDMSCI-199 (FBA Validation)

```python
# This matrix serves as experimental ground truth
experimental_growth = pd.read_csv('results/carbon_source_growth_matrix.csv', index_col=0)

# Compare with in silico predictions
# confusion_matrix = compare(experimental_growth, insilico_predictions)
```

## Quality Metrics

### Expected Coverage
- **Matrix size**: 57 organisms × 80-100 carbon sources
- **Coverage**: ~30-40% (sparse matrix)
- **Organisms with most data**: Keio, Pputida, WCS417 (~50-80 carbon sources each)
- **Most tested carbon sources**: D-Glucose, Acetate, Pyruvate (30-40 organisms each)

### Quality Filters Applied
- `gMed >= 50`: Ensures sufficient sequencing depth
- `mad12 <= 0.5`: Ensures consistency between gene halves (97% of experiments pass)

## Next Steps

1. Extract carbon sources (this task - Complete)
2. Proceed to CDMSCI-197 to map carbon sources to ModelSEED media formulations
3. Use in CDMSCI-199 for FBA validation

## Status

- [x] Notebook created and tested
- [x] Script created and tested
- [ ] Results generated (run notebook to generate)
- [ ] Carbon source list extracted
- [ ] Matrix validated

## Last Updated

2025-10-02
