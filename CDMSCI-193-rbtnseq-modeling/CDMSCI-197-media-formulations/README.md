# CDMSCI-197: Translate to Computational Media Formulations

**Parent**: CDMSCI-193 - RBTnSeq Modeling Analysis

## Objective

Map filtered carbon sources from CDMSCI-196 to ModelSEED compound IDs and create computational media formulations for metabolic modeling.

## Input

Uses the filtered growth matrix from CDMSCI-196:
- 141 carbon sources (after removing unsuitable compounds)
- 44 organisms (after filtering organisms with no growth data)
- Input file: `../CDMSCI-196-carbon-sources/results/combined_growth_matrix_filtered.csv`

## Workflow

### Notebook: Map Carbon Sources to ModelSEED IDs

**File**: `01-map-carbon-sources-to-modelseed.ipynb`

**Three-round mapping strategy**:

**Round 1: Automated Mapping** (~1 minute)
- Search local template + ModelSEED database (offline, 238K aliases)
- Result: 87 compounds mapped (61.7%)
- Outputs:
  - `results/round1_mapped.csv` - Successfully mapped compounds
  - `results/round1_unmapped.txt` - Compounds needing Round 2

**Round 2: AI-Assisted Mapping with GPT-4o** (~30 minutes)
- LLM suggests ModelSEED IDs for 54 unmapped compounds
- Verifies suggestions exist in template
- Result: 44 additional compounds mapped (31.2%)
- Outputs:
  - `results/round2_all_mappings.csv` - All mappings after Round 2
  - `results/round2_still_unmapped.csv` - 10 compounds still unmapped (7.1%)

**Round 3: Optional Deep Dive with GPT-5** (optional, ~15 minutes)
- For the 10 remaining unmapped compounds
- More detailed biochemical analysis
- Commented out by default (uncomment to run)

**Final Results**:
- Total: 141 carbon sources processed
- Mapped: 131 compounds (92.9%)
- Unmapped: 10 compounds (7.1%)

## Outputs

### Mapping Tables
1. `results/round1_mapped.csv` - 87 compounds from automated search
2. `results/round1_unmapped.txt` - 54 compounds for Round 2
3. `results/round2_all_mappings.csv` - All 141 compounds after Round 2
4. `results/round2_still_unmapped.csv` - 10 compounds still unmapped
5. `results/carbon_source_mapping.csv` - Final combined mapping table (141 rows)

### Media Formulations
- `media/*.json` - 131 individual media files (one per mapped carbon source)
- Each file contains base nutrients plus one carbon source
- Format: ModelSEEDpy-compatible JSON

## Results Summary

**Mapping Success Rate**: 92.9% (131/141)

**Round 1 (Automated)**: 87 mapped
- Template matches: 52
- ModelSEED local database: 35

**Round 2 (GPT-4o)**: 44 mapped
- Verified in template: 44
- LLM suggestions: 54 (10 unverified)

**Unmapped (10 compounds)**:
- 1,5-Pentanediol
- 4-Hydroxyvalerate
- 6-O-Acetyl-D-glucose
- D-Gluconic Acid sodium salt (unverified: cpd00257)
- D-Glucuronic Acid (unverified: cpd00257)
- Dodecandioic acid (unverified: cpd29696)
- L-Rhamnose monohydrate (unverified: cpd08395)
- Lacto-N-neotetraose
- Maltitol
- Methyl-B-D-galactopyranoside

## Next Steps

1. Optional: Run Round 3 (GPT-5 deep dive) for 10 unmapped compounds
2. Manual curation for any remaining unmapped compounds
3. Proceed to CDMSCI-198: Build metabolic models using mapped carbon sources
4. Proceed to CDMSCI-199: Run FBA simulations with media formulations

## Prerequisites

**Completed**: CDMSCI-196 (Carbon source data compilation and filtering)
- Provides filtered growth matrix with 141 carbon sources
- Provides organism filtering (44 organisms with growth data)

Last updated: 2025-10-15
