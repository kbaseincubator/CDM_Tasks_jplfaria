# Condition-Specific Gap-Filling Experimental Design

## Date: 2025-10-16

## Background

**Problem Identified**: The original analysis (Notebook 02-03) compared gap-filled models (optimized for pyruvate) against experimental data for 121 different carbon sources. This is fundamentally flawed because:

1. Gap-filling was performed on **pyruvate minimal media only** (CDMSCI-198)
2. Models were never intended to grow on all 121 carbon sources
3. Calling exchanges "missing" when they're only needed for non-pyruvate conditions is misleading
4. The 571 false negatives reflect **expected behavior**, not bugs to fix

## Research Question

**Can condition-specific gap-filling rescue the 571 false negatives, and if so, is it adding meaningful biology or just overfitting?**

## Experimental Design

### Approach: Condition-Specific Gap-Filling

For each of the 571 false negative cases (organism × carbon source where experimental=1, predicted=0):

1. Load the **draft model** (pre-gap-filling)
2. Apply the specific carbon source media
3. Run gap-filling with universal template model
4. Track comprehensive metrics (see below)
5. Compare to pyruvate gap-filling results

### Data Collection

For each gap-filling attempt, record:

#### Primary Metrics:
- `organism`: Organism name
- `orgId`: Organism ID
- `carbon_source`: Carbon source name
- `media_filename`: Media file used
- `pre_gapfill_flux`: Biomass flux before gap-filling
- `post_gapfill_flux`: Biomass flux after gap-filling
- `gapfill_success`: Boolean (flux > 0.001 after gap-filling)
- `num_reactions_added`: Count of reactions added
- `gapfill_solutions_count`: Number of alternative solutions found

#### Detailed Reaction Data:
- `reaction_id`: Each reaction added
- `reaction_name`: Human-readable name
- `reaction_formula`: Stoichiometry
- `subsystem`: Metabolic subsystem

### Analysis Plan

Once data is collected, analyze:

1. **Success Rate**:
   - How many FNs are "fixable" via gap-filling?
   - Are some organisms more amenable than others?

2. **Reaction Analysis**:
   - What reactions are most frequently added?
   - How many reactions per successful gap-fill?
   - Are reactions biologically plausible?

3. **Comparison to Pyruvate Gap-filling**:
   - Are condition-specific reactions different from pyruvate gap-fill reactions?
   - Is there overlap in added reactions?

4. **Overfitting Assessment**:
   - Do added reactions make biological sense for that carbon source?
   - Are we adding exchange reactions vs metabolic reactions?
   - Are reaction counts suspiciously high (indicating overfitting)?

5. **Stratification**:
   - By organism type (Gram+/-, aerobe/anaerobe)
   - By carbon source chemistry (sugars, amino acids, organic acids)
   - By number of reactions needed

## Expected Runtime

- 571 gap-filling experiments
- Estimated ~30-60 seconds per experiment
- **Total time**: 5-10 hours

**Recommendation**: Run overnight or on compute server

## Output Files

1. `results/condition_specific_gapfilling_results.csv` - Main results (571 rows)
2. `results/condition_specific_gapfilling_reactions.csv` - Detailed reactions (many rows)
3. `results/condition_specific_gapfilling_errors.csv` - Failed experiments

## Success Criteria

A "successful" experiment is one where we can answer:
- Can gap-filling work for this case?
- If yes, what reactions are needed?
- Are those reactions reasonable additions?

## Next Steps After Data Collection

1. Create analysis notebook (Notebook 05 or 06)
2. Generate summary statistics and visualizations
3. Identify patterns in successful vs unsuccessful gap-filling
4. Make recommendations for:
   - Which models benefit from multi-condition gap-filling
   - Which carbon sources are problematic regardless
   - Whether condition-specific gap-filling is worth the complexity

## Why This Matters

This experiment will provide data-driven evidence to answer:
- **Is gap-filling a useful tool** for phenotype prediction beyond the training condition?
- **How much can we trust** gap-filled models to generalize?
- **Should we invest** in multi-condition gap-filling pipelines?

## How to Run

```bash
cd /Users/jplfaria/Projects/CDM_Tasks_jplfaria/CDMSCI-193-rbtnseq-modeling/CDMSCI-199-fba-simulations

# Run the experiment (will take 5-10 hours)
/Users/jplfaria/miniconda3/bin/python3 run_condition_specific_gapfilling.py
```

## Contact

José Pedro Faria
KBase / DOE Systems Biology
jplfaria@gmail.com
