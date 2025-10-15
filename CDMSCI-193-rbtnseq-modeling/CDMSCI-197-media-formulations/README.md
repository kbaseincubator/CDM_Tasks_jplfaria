# CDMSCI-197: Translate to Computational Media Formulations

**Parent**: CDMSCI-193 - RBTnSeq Modeling Analysis

## Objective

Map 206 carbon sources from Fitness Browser data to ModelSEED compound IDs and create computational media formulations for metabolic modeling.

## Workflow

### Notebook: Map Carbon Sources to ModelSEED IDs

**File**: `01-map-carbon-sources-to-modelseed.ipynb`

**Two-round mapping strategy**:
- Round 1: Automated search (template + Solr API)
- Round 2: AI-assisted mapping with GPT-5 (via Argo proxy)

**Outputs**:
- `results/carbon_source_mapping.csv` - Complete mapping table
- `media/*.json` - Individual media formulations (ready for ModelSEEDpy)

## Status

- [x] Notebook created
- [ ] Run mapping
- [ ] Review results
- [ ] Ready for CDMSCI-198

Last updated: 2025-10-07
