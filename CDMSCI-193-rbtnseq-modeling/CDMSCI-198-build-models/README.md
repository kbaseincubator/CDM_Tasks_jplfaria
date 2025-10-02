# CDMSCI-198: Build Genome-Scale Metabolic Models

**Parent**: CDMSCI-193 - RBTnSeq Modeling Analysis

## Objective

Generate genome-scale metabolic models for all 57 organisms in the Fitness Browser database using RAST functional annotations.

## Input

From **shared_resources**:
- Protein sequences for 57 organisms (FASTA format)
- Fitness Browser database (`feba.db`) with gene annotations

## Approach

### 1. Obtain RAST Annotations

**Option A**: Use existing annotations from Fitness Browser
```python
import sqlite3
conn = sqlite3.connect('feba.db')
annotations = pd.read_sql_query("""
    SELECT orgId, locusId, desc, scaffoldId, begin, end, strand, type
    FROM Gene
    WHERE type = 1  -- protein-coding genes
""", conn)
```

**Option B**: Re-annotate with RAST API
```bash
# Submit genomes to RAST
rast-submit-genome --fasta organism.fna --domain Bacteria --genetic-code 11
```

### 2. Build Draft Models with ModelSEED/KBase

Use automated model reconstruction:

```python
from modelseedpy import MSBuilder

# For each organism
for organism in organisms:
    builder = MSBuilder(
        genome_id=organism,
        annotation_file=f"{organism}_rast.gff",
        template="GramNegative"  # or GramPositive based on organism
    )

    draft_model = builder.build_draft_model()
    draft_model.save(f"models/{organism}_draft.xml")
```

### 3. Gap-Fill Models

Fill missing reactions to enable biomass production:

```python
from modelseedpy import MSGapfill

for model in draft_models:
    gapfiller = MSGapfill(
        model=model,
        default_gapfill_templates=['GramNegative'],
        default_gapfill_models=['iJO1366'],  # E. coli reference
        test_conditions=[
            {'media': 'complete', 'is_max_production': True, 'objective': 'bio1'},
        ]
    )

    gapfilled_model = gapfiller.run_gapfilling()
    gapfilled_model.save(f"models/{organism}_gapfilled.xml")
```

### 4. Validate Models

Check model quality:

```python
import cobra
from memote import test_model

model = cobra.io.read_sbml_model('organism_model.xml')

# Basic validation
print(f"Genes: {len(model.genes)}")
print(f"Reactions: {len(model.reactions)}")
print(f"Metabolites: {len(model.metabolites)}")

# Test biomass production
solution = model.optimize()
print(f"Biomass flux: {solution.objective_value}")

# Run MEMOTE quality tests
results = test_model(model, 'reports/memote_report.html')
```

## Outputs

### Model Files

All models saved to `models/` directory:

1. **{organism}_draft.xml** (57 files)
   - Draft SBML models from RAST annotations
   - Before gap-filling

2. **{organism}_gapfilled.xml** (57 files)
   - Final models after gap-filling
   - Ready for FBA simulations

3. **{organism}_gapfill_report.json** (57 files)
   - Reactions added during gap-filling
   - Evidence and justification

### Results Files

All outputs saved to `results/` directory:

1. **model_statistics.csv**
   - Columns: `organism`, `n_genes`, `n_reactions`, `n_metabolites`, `biomass_flux_complete_media`
   - Summary statistics for all 57 models

2. **gapfilling_summary.csv**
   - Columns: `organism`, `n_reactions_added`, `n_reactions_removed`, `gapfill_success`
   - Gap-filling report for each model

3. **validation_report.txt**
   - Mass/charge balance check
   - Dead-end metabolites
   - Orphan reactions
   - MEMOTE scores

4. **model_comparison.png**
   - Bar chart comparing model sizes
   - Reaction counts per organism

## Expected Model Statistics

Based on typical bacterial genomes:

| Metric | Expected Range |
|--------|---------------|
| Genes | 1,000 - 8,000 |
| Reactions | 800 - 2,500 |
| Metabolites | 600 - 1,800 |
| Biomass flux (rich media) | 0.5 - 2.0 h⁻¹ |

## Dependencies

**Python packages**:
```bash
pip install cobra modelseedpy memote escher
```

**Databases**:
- ModelSEED Biochemistry
- SEED Subsystems
- KEGG/MetaCyc pathways

## Quality Checks

### 1. Mass/Charge Balance
- All reactions should be balanced
- Flag violations for manual curation

### 2. Dead-End Metabolites
- Metabolites produced but not consumed (or vice versa)
- May indicate missing reactions

### 3. Biomass Production
- All models should grow on complete media
- Growth rate > 0.1 h⁻¹

### 4. Gene Coverage
- % of genes with assigned reactions
- Target: > 40% of protein-coding genes

## Usage for Downstream Tasks

### For CDMSCI-199 (FBA Simulations)

```python
import cobra
import pandas as pd

# Load model
model = cobra.io.read_sbml_model('models/Keio_gapfilled.xml')

# Load media from CDMSCI-197
media = pd.read_csv('../CDMSCI-197-media-formulations/results/media_D-Glucose.csv')

# Apply media
model.medium = dict(zip(media['compound_id'], media['uptake_rate']))

# Run FBA
solution = model.optimize()
growth_prediction = 1 if solution.objective_value > 0.01 else 0
```

## Known Challenges

1. **Annotation quality**: RAST may miss organism-specific pathways
2. **Gap-filling artifacts**: May add non-physiological reactions
3. **Biomass composition**: Generic biomass may not match organism
4. **Transport reactions**: Often under-predicted

## Next Steps

1. ← Wait for organism list confirmation
2. → Obtain RAST annotations for all 57 organisms
3. → Build and gap-fill models
4. → Validate model quality
5. → Pass models to CDMSCI-199 for FBA

## Status

- [ ] RAST annotations obtained
- [ ] Draft models built
- [ ] Gap-filling performed
- [ ] Model validation completed
- [ ] Statistics generated
- [ ] Models ready for FBA

## Last Updated

2025-10-02
