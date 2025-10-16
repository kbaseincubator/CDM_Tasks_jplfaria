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

**Status**: COMPLETE (with manual corrections applied)

**Final Mapping Statistics** (after 4 rounds + manual review):
- **Total carbon sources**: 140 (reduced from 141 after Sucrose exclusion)
- **Successfully mapped**: 122 (87.1%)
- **Unmapped**: 18 (12.9%)

### Mapping Rounds

**Round 1 (Automated)**: 86 mapped
- Template matches + ModelSEED local database
- All reliable and verified

**Round 2 (GPT-4o)**: 44 mapped (initially)
- AI-assisted suggestions
- **CRITICAL**: 16 incorrect mappings flagged in Round 3

**Round 3 (GPT-5 Validation)**: Identified errors
- Validated all Round 2 duplicate mappings
- Flagged 16 incorrect mappings (LLM hallucinations)
- Prevented ~750 bogus FBA comparisons

**Round 4 (GPT-5 Deep Dive)**: 3 additional mapped
- Deep analysis of remaining unmapped compounds
- Final 8 confirmed as UNMAPPED

**Manual Review (2025-10-16)**: 16 corrections applied
- 8 successfully remapped to correct ModelSEED IDs
- 8 marked UNMAPPED (not in template GramNegModelTemplateV6.json)

### Key Corrections from Manual Review

**Successfully Corrected**:
1. Sodium octanoate: cpd00211 (Butyrate, C4) → cpd03846 (octanoate, C8)
2. Sodium adipate: cpd00751 (L-Fucose) → cpd03642 (Adipate)
3. D-(-)-tagatose: cpd00751 (L-Fucose) → cpd00589 (D-Tagatose)
4. D-Glucosamine Hydrochloride: cpd00122 → cpd00276 (GLUM)
5. D-Raffinose pentahydrate: cpd00795 → cpd00382 (Melitose)
6. palatinose hydrate: cpd19020 → cpd01200 (Palatinose)
7. 3-methyl-2-oxopentanoic acid: cpd11493 → cpd00508 (3MOP)
8. 4-Methyl-2-oxovaleric acid: cpd11493 → cpd00200 (4MOP)

**Template Validation**: All 122 mapped compounds verified to exist in GramNegModelTemplateV6.json

### Final Unmapped Compounds (18 total)

**Not in template** (7):
- 1,4-Butanediol
- 1,5-Pentanediol
- 4-Hydroxyvalerate
- 5-Keto-D-Gluconic Acid potassium salt
- Azelaic acid
- D-Maltose monohydrate
- Lactitol
- Suberic acid

**No valid mapping found** (11):
- 6-O-Acetyl-D-glucose
- D-Gluconic Acid sodium salt
- D-Glucuronic Acid
- Dodecandioic acid
- Gly-DL-Asp
- L-(-)-sorbose
- L-Rhamnose monohydrate
- Lacto-N-neotetraose
- Maltitol
- Methyl-B-D-galactopyranoside

### Documentation

- **MANUAL_CORRECTIONS_SUMMARY.md**: Detailed explanation of all corrections
- **verify_final_mappings.py**: Verification script confirming CDMSCI-199 readiness

## Ready for CDMSCI-199

All systems verified:
- All mapped compounds exist in ModelSEED template
- 122 media JSON files generated and verified
- Total FBA simulations possible: 5,368 (44 organisms × 122 sources)
- Lost to unmapping: 792 simulations (44 organisms × 18 sources)

## Next Steps

1. ~~Optional: Run Round 3 (GPT-5 deep dive) for unmapped compounds~~ COMPLETE
2. ~~Manual curation for incorrect mappings~~ COMPLETE
3. CDMSCI-198: Build metabolic models COMPLETE
4. CDMSCI-199: Run FBA simulations with validated media formulations READY

## Prerequisites

**Completed**: CDMSCI-196 (Carbon source data compilation and filtering)
- Provides filtered growth matrix with 141 carbon sources
- Provides organism filtering (44 organisms with growth data)

Last updated: 2025-10-15
