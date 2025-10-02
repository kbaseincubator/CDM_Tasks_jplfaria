# Scripts Directory

Python scripts for processing and analyzing FIT Fitness Browser data

## Scripts

### create_growth_matrix.py

**Purpose**: Create organism × condition growth/no-growth binary matrix from FIT database

**Input**: feba.db (FIT SQLite database)

**Output**: CSV matrix with organisms as rows, conditions as columns, 1=growth/0=no growth

**Usage**:

```bash
# Basic usage (with quality filters)
python create_growth_matrix.py --db ../data/feba.db --output growth_matrix.csv

# Without quality filters (include all experiments)
python create_growth_matrix.py --db ../data/feba.db --output growth_matrix.csv --no-quality-filter

# Create hierarchical matrix (expGroup × condition columns)
python create_growth_matrix.py --db ../data/feba.db --output growth_matrix.csv --hierarchical

# Create separate matrices for each condition group
python create_growth_matrix.py --db ../data/feba.db --output growth_matrix.csv --by-group --output-dir ../data/processed/matrices/

# Full example with all options
python create_growth_matrix.py \
  --db ../data/feba.db \
  --output ../data/processed/growth_matrix_full.csv \
  --by-group \
  --output-dir ../data/processed/matrices/
```

**Quality Filters** (applied by default):
- `e.gMed >= 50` - Sufficient read depth (median reads per gene)
- `e.mad12 <= 0.5` - Good within-gene consistency
- `e.num > 0` - Has fitness data
- No error flags in experiment

**Output Files**:
- `growth_matrix.csv` - Binary matrix (main output)
- `growth_matrix.stats.txt` - Summary statistics
- `growth_matrix_<group>.csv` - One matrix per condition group (if --by-group)

**Matrix Interpretation**:
- **1** = Organism has fitness data for this condition (likely grows)
- **0** = No data for this condition (either not tested OR doesn't grow)

**Note**: Based on research, missing data most likely means "not tested" rather than "tested but didn't grow". See `docs/05-growth-no-growth-matrix.md` for details.

## Requirements

```bash
pip install pandas sqlite3
```

## Data Download

Download the FIT database (feba.db, ~5GB) from:
- https://figshare.com/articles/dataset/25236931 (February 2024 release)
- Or extract from source code: https://bitbucket.org/berkeleylab/feba/

## Next Steps

After creating growth matrix:
1. Build genome-scale metabolic models for each organism
2. Simulate the same conditions in silico
3. Compare experimental growth (from matrix) vs in silico growth
4. Generate confusion matrix for model validation
