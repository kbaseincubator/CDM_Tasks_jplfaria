# Project Objective: Experimental vs In Silico Growth Prediction

**Purpose**: Document the actual project objective for confusion matrix analysis

## Project Overview

This project aims to validate genome-scale metabolic models by comparing experimental growth data (from FIT Fitness Browser) against in silico growth predictions.

## Workflow

### Phase 1: Extract Experimental Growth Data (Current Phase)
**Objective**: Build an organism × condition growth/no-growth matrix from FIT data

**Approach**:
1. Extract all organism-condition pairs from FIT Fitness Browser
2. If organism has data for a condition → **Growth = YES**
3. If organism lacks data for a condition → **Growth = NO** (assumption: not tested or couldn't grow)

**Assumption**:
- Missing data = No growth (conservative assumption until authors clarify)
- Alternative interpretation: Missing data = Not tested (see research findings)
- **Action**: Emailing authors to verify

**Output**: Binary growth matrix
```
              Glucose  Lactate  Acetate  Citrate  ...
Organism1        1        1        0        1     ...
Organism2        1        0        1        1     ...
Organism3        0        1        1        0     ...
...
```

### Phase 2: Build Genome-Scale Metabolic Models
**Objective**: Create metabolic models for all 48+ organisms in the dataset

**Tools**:
- CarveMe, ModelSEED, or other automated model building tools
- Manual curation where needed

**Output**: Metabolic models in SBML format for each organism

### Phase 3: In Silico Growth Simulations
**Objective**: Simulate the same conditions tested experimentally

**Approach**:
1. For each organism's metabolic model
2. For each experimental condition (carbon source, nitrogen source, stress, etc.)
3. Run Flux Balance Analysis (FBA) to predict growth/no-growth
4. Record in silico growth predictions

**Output**: Binary in silico growth matrix (same dimensions as experimental)

### Phase 4: Confusion Matrix Analysis (Final Goal)
**Objective**: Compare experimental vs in silico growth predictions

## Confusion Matrix Definition

```
                        Experimental Growth
                        YES         NO
In Silico      YES      TP          FP
Growth         NO       FN          TN
```

**Classifications**:

- **True Positive (TP)**: Grows experimentally AND grows in silico
  - Model correctly predicts growth
  - Best case scenario

- **True Negative (TN)**: Doesn't grow experimentally AND doesn't grow in silico
  - Model correctly predicts no growth
  - Also good prediction

- **False Positive (FP)**: Doesn't grow experimentally BUT grows in silico
  - Model predicts growth when organism can't actually grow
  - Possible causes:
    - Missing constraints in model
    - Missing essential genes
    - Unknown regulatory constraints
    - Or: Organism wasn't tested (data is "not tested" not "no growth")

- **False Negative (FN)**: Grows experimentally BUT doesn't grow in silico
  - Model predicts no growth when organism actually grows
  - Possible causes:
    - Missing metabolic capabilities
    - Incomplete genome annotation
    - Alternative pathways not in model
    - Gap in metabolic network

## Evaluation Metrics

**Precision** = TP / (TP + FP)
- Of all conditions where model predicts growth, what % actually grow?

**Recall** = TP / (TP + FN)
- Of all conditions where organism actually grows, what % does model predict?

**Accuracy** = (TP + TN) / Total
- Overall correct predictions

**F1-Score** = 2 × (Precision × Recall) / (Precision + Recall)
- Balanced measure of precision and recall

## Important Distinctions

### What This Project IS
- Validating metabolic models against experimental growth data
- Comparing **experimental growth** vs **computational growth predictions**
- Testing model accuracy across diverse organisms and conditions

### What This Project IS NOT
- Predicting gene essentiality from fitness values
- Predicting gene function from fitness patterns
- Analyzing ortholog phenotype conservation
- Analyzing gene-level fitness values

**Key Difference**: This project focuses on **organism-level growth** (can the organism grow?), not gene-level phenotypes (does mutating this gene affect fitness?).

## Data Interpretation Challenge

### The Core Question
**When an organism-condition pair is missing from FIT data, does it mean:**
A. They tested it but organism didn't grow? (biological no-growth)
B. They didn't test that organism in that condition? (not tested)

### Research Findings
Based on extensive review of FIT documentation and publications:

**Answer: Primarily (B) - They didn't test all organisms in all conditions**

**Evidence**:
1. No documentation of "biological no growth" in database schema or help files
2. Experimental design is organism-specific ("dozens of conditions **each**")
3. Different organisms have vastly different numbers of experiments:
   - Some organisms: >300 experiments
   - Other organisms: <50 experiments
4. Only documented failures are **technical QC failures**, not biological growth failures
5. Quality control metrics (mad12, cor12, gMed) filter for data quality, not growth vs no-growth

**Implication for Confusion Matrix**:
- Missing data might be "not tested" rather than "no growth"
- This affects FP interpretation:
  - If "no experimental data" = "not tested": FP doesn't necessarily mean wrong prediction
  - If "no experimental data" = "no growth": FP means model incorrectly predicts growth

**Resolution Strategy**:
1. Email FIT authors to clarify
2. For initial analysis: Assume missing = no growth (conservative)
3. Sensitivity analysis: Test both interpretations
4. Document assumptions clearly in results

## Conditions to Test

### Carbon Sources
- Glucose, fructose, lactose, sucrose, glycerol, acetate, succinate, citrate, pyruvate, etc.
- FIT has extensive carbon source testing

### Nitrogen Sources
- Ammonia, nitrate, nitrite, amino acids, urea, etc.

### Stress Conditions
- Antibiotics
- Heavy metals
- pH extremes
- Osmotic stress
- Oxygen levels

### Media Variations
- Minimal media
- Rich media (LB)
- Various supplements

## Expected Outcomes

### Well-Curated Models
- High TP rate (correctly predict growth)
- High TN rate (correctly predict no growth)
- Accuracy >80%

### Poorly-Curated Models
- High FN rate (miss growth capabilities)
- Lower accuracy
- Indicates gaps in metabolic network reconstruction

### Over-Complete Models
- High FP rate (predict growth when it doesn't occur)
- Indicates missing constraints or regulatory information

## Files Relevant to This Objective

### Keep (Still Relevant)
- `01-understanding-statistical-thresholds.md` - How FIT determines quality experiments
- `03-understanding-fitness-values.md` - Background on fitness measurement
- `04-cofitness-functional-relationships.md` - Background on functional analysis
- All research docs in `/thoughts/shared/research/` about database schema and data extraction

### Removed (Not Relevant to Current Objective)
- ~~`02-confusion-matrix-interpretations.md`~~ - Described gene-level phenotype prediction, not organism-level growth
  - Had 5 interpretations (essentiality, function prediction, ortholog conservation, TF validation, replicate agreement)
  - These are valid analyses but NOT what we're doing for this project

## Next Steps

1. Clarify missing data interpretation (research complete - likely "not tested")
2. Create organism × condition growth matrix from FIT data
3. Build/obtain genome-scale metabolic models
4. Simulate growth conditions in silico
5. Generate confusion matrix
6. Analyze results and iterate on models

## References

**FIT Fitness Browser**:
- Main site: https://fit.genomics.lbl.gov
- Help: https://fit.genomics.lbl.gov/cgi-bin/help.cgi

**Key Publications**:
- Wetmore et al. 2015, mBio - RB-TnSeq methodology
- Price et al. 2018, Nature - 32 bacteria, thousands of genes characterized
- Price et al. 2024, Database - Interactive tools and current data

**Metabolic Modeling**:
- COBRApy documentation
- CarveMe documentation
- ModelSEED documentation
