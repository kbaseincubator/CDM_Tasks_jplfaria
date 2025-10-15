# CDMSCI-198: Build Genome-Scale Metabolic Models

**Parent**: CDMSCI-193 - RBTnSeq Modeling Analysis

## Objective

Build genome-scale metabolic models for 57 organisms using ModelSEEDpy and RAST annotation.

## Workflow

### Notebook: Annotate Genomes with RAST

**File**: `01-annotate-genomes-with-rast.ipynb`

**What it does**:
1. Loads 57 protein FASTA files
2. Submits to RAST for annotation (2-4 hours each)
3. Saves annotated genomes as pickle files
4. Allows stop/resume (progress saved)

**Outputs**:
- `results/genomes/{organism_id}_genome.pkl` (57 files)
- `results/rast_annotation_log.txt`

**Time**: ~114-228 hours total if serial (can parallelize)

## Status

- [x] Annotation notebook created
- [ ] RAST annotations (0/57)
- [ ] Ready for model building

Last updated: 2025-10-07
