# CDMSCI-198: Build Genome-Scale Metabolic Models

**Parent**: CDMSCI-193 - RBTnSeq Modeling Analysis

## Objective

Build genome-scale metabolic models for 44 organisms using ModelSEEDpy and RAST annotation, then gap-fill for growth on pyruvate minimal media.

## Workflow

### 01: Annotate Genomes with RAST

**File**: `01-annotate-genomes-with-rast.ipynb`

**What it does**:
1. Loads 57 protein FASTA files
2. Submits to RAST for annotation
3. Saves annotated genomes as pickle files

**Outputs**:
- `results/genomes/{organism_id}_genome.pkl` (57 files)
- `results/rast_annotation_log.txt`

### 02: Build and Gap-Fill Models

**File**: `02-build-and-gapfill-models.ipynb`

**What it does**:
1. Filters to 44 organisms with carbon source data from CDMSCI-196
2. Builds draft models using ModelSEEDpy dev branch
3. Adds ATPM reaction
4. Gap-fills for biomass production on pyruvate minimal media
5. Saves both draft and gap-filled models as JSON files

**Outputs**:
- `models/{organism_id}_draft.json` (44 files)
- `models/{organism_id}_gapfilled.json` (44 files)
- `results/model_statistics.csv`
- `results/gapfill_report.csv`

### Visualization

**File**: `create_model_stats_viewer.py`

Creates interactive HTML viewer showing:
- Draft model size distributions
- Gap-filling statistics
- Per-organism growth rates
- Model size vs growth analysis

**Output**: `results/model_statistics_viewer.html`

## Results Summary

- 44 organisms successfully modeled (filtered from 57 based on CDMSCI-196)
- 100% success rate (all 44 models growing after gap-filling)
- Average: 1221 ± 269 reactions, 1197 ± 224 metabolites, 1107 ± 248 genes
- Gap-filling: 13 reactions added on average
- Growth rates: 0.31 - 0.97 1/hr (average: 0.42 1/hr)

## Status

- [x] RAST annotations (57/57)
- [x] Filter to organisms with carbon source data (44/57)
- [x] Build draft models (44/44)
- [x] Gap-fill models (44/44)
- [x] Generate statistics and visualization

Last updated: 2025-10-15
