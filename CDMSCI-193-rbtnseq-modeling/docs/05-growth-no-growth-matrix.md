# Growth/No-Growth Matrix from FIT Data

**Purpose**: Document how to interpret and extract organism × condition growth data from FIT Fitness Browser

## Overview

This document explains how to create a binary growth/no-growth matrix from FIT fitness data for metabolic model validation.

## Key Finding: Missing Data Interpretation

### The Question
**When an organism doesn't have data for a specific condition in FIT, what does it mean?**

### The Answer
**Missing data most likely means "NOT TESTED" rather than "TESTED BUT DIDN'T GROW"**

### Evidence

#### 1. No Documentation of Biological "No Growth"
**Finding**: Extensive search of FIT database schema, help files, and publications found **ZERO references** to:
- "no growth"
- "failed to grow"
- "unable to grow"
- "biological growth failure"

**Implication**: The database does not distinguish between "didn't test" and "tested but didn't grow"

#### 2. Only Technical Failures Are Documented
**Source**: Individual organism pages at https://genomics.lbl.gov/supplemental/bigfit/html/

**Examples**:
- **PV4**: 230 samples tested → 160 successful, 70 failed QC
- **Koxy**: 392 samples tested → 173 successful, 219 failed QC
- **azobra**: 127 samples tested → 93 successful, 34 failed QC

**Failure Reasons** (all technical, not biological):
- `low_count`: Insufficient sequencing reads (gMed < 50)
- `high_mad12`: Inconsistent fitness estimates (mad12 > 0.5)
- `low_cor12`: Low gene-half correlation (cor12 < 0.1)
- `high_adj_gc_cor`: GC content correlation issues (> 0.2 or 0.25)

**Implication**: When experiments fail, it's due to sequencing/data quality, not organism growth failure

#### 3. Organism-Specific Experimental Design
**Source**: Price et al. 2018 Nature - "genome-wide mutant fitness data from 32 diverse bacteria across **dozens of growth conditions each**"

**Key phrase**: "dozens of conditions **each**" - not "all bacteria in all conditions"

**Evidence of selective testing**:
| Organism | Number of Experiments | Notes |
|----------|----------------------|-------|
| Some organisms | >300 experiments | Extensively characterized |
| Other organisms | <50 experiments | Limited characterization |
| Average | ~157 experiments/organism | High variance |

**Implication**: Researchers selected organism-appropriate conditions, not testing every organism in every condition

#### 4. Dataset Statistics
**Total**: 7,552 experiments across 48 organisms (46 bacteria + 2 archaea)

**If all organisms tested in all conditions**:
- Would expect similar numbers of experiments per organism
- Would expect ~157 experiments × 48 organisms = 7,536 with each organism in each condition
- Would expect documentation of "no growth" results

**Reality**:
- Vastly different experiment counts per organism
- No "no growth" documentation
- Evidence points to selective testing

### Conclusion

**Interpretation**: When organism X lacks data for condition Y, the most likely explanation is:
- **They did not test organism X in condition Y**

**NOT**: They tested it and documented growth failure

## Implications for Growth Matrix

### Conservative Approach (Current Default)
**Assumption**: Missing data = No growth

**Rationale**:
- Provides conservative metabolic model validation
- If model predicts growth for untested condition, we call it FP
- Better to underestimate model accuracy than overestimate

**Matrix encoding**:
```
              Glucose  Lactate  Acetate  Citrate
Organism1        1        1        0        0      # Has data for glucose & lactate only
Organism2        1        0        1        1      # Has data for glucose, acetate, citrate
```

**Confusion Matrix Impact**:
- May inflate False Positive rate
- May underestimate True Negative rate
- Provides lower bound on model performance

### Alternative Approach (After Author Clarification)
**Assumption**: Missing data = Not tested → Exclude from analysis

**Rationale**:
- Only compare model predictions to actual experimental tests
- More accurate assessment of model performance
- But loses coverage

**Matrix encoding**:
```
              Glucose  Lactate  Acetate  Citrate
Organism1        1        1        NA       NA      # Only compare where tested
Organism2        1        NA       1        1
```

**Confusion Matrix Impact**:
- Only includes organism-condition pairs that were actually tested
- Provides true accuracy on tested conditions
- Smaller dataset

## How to Build the Matrix

### Step 1: Identify All Unique Conditions

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('feba.db')

# Get all unique conditions
query = """
SELECT DISTINCT
    expGroup,
    condition_1,
    COUNT(DISTINCT orgId) as n_organisms,
    COUNT(DISTINCT expName) as n_experiments
FROM Experiment
GROUP BY expGroup, condition_1
ORDER BY expGroup, n_organisms DESC
"""

conditions = pd.read_sql_query(query, conn)
print(f"Total unique conditions: {len(conditions)}")
```

### Step 2: Get Organism-Condition Pairs

```python
# Get all organism-condition combinations that have data
query = """
SELECT DISTINCT
    gf.orgId,
    e.expGroup,
    e.condition_1,
    COUNT(gf.expName) as n_experiments_this_combo
FROM GeneFitness gf
JOIN Experiment e ON gf.orgId = e.orgId AND gf.expName = e.expName
GROUP BY gf.orgId, e.expGroup, e.condition_1
"""

organism_conditions = pd.read_sql_query(query, conn)
print(f"Total organism-condition pairs with data: {len(organism_conditions)}")
```

### Step 3: Create Binary Matrix

```python
# Pivot to create binary matrix
growth_matrix = organism_conditions.pivot_table(
    index='orgId',
    columns=['expGroup', 'condition_1'],
    values='n_experiments_this_combo',
    aggfunc='count',
    fill_value=0
)

# Convert to binary (1 if any experiments, 0 if none)
growth_matrix = (growth_matrix > 0).astype(int)

print(f"Matrix shape: {growth_matrix.shape}")
print(f"Coverage: {growth_matrix.sum().sum() / growth_matrix.size:.1%}")
```

### Step 4: Alternative - Define Growth More Strictly

Instead of "has any data" = growth, you might want:
- "Has experiments that passed QC" = growth
- "Has high-quality experiments" = growth

```python
# Get high-quality experiments only
query = """
SELECT DISTINCT
    gf.orgId,
    e.expGroup,
    e.condition_1
FROM GeneFitness gf
JOIN Experiment e ON gf.orgId = e.orgId AND gf.expName = e.expName
WHERE e.num > 0  -- Has fitness data
AND (e.u IS NULL OR e.u = '')  -- No error/warning flags
"""

high_quality_conditions = pd.read_sql_query(query, conn)

# Create matrix
hq_growth_matrix = high_quality_conditions.pivot_table(
    index='orgId',
    columns=['expGroup', 'condition_1'],
    aggfunc=len,
    fill_value=0
)
hq_growth_matrix = (hq_growth_matrix > 0).astype(int)
```

## Example: Carbon Source Growth Matrix

```python
# Focus on carbon sources only
query = """
SELECT DISTINCT
    gf.orgId,
    e.condition_1 as carbon_source
FROM GeneFitness gf
JOIN Experiment e ON gf.orgId = e.orgId AND gf.expName = e.expName
WHERE e.expGroup = 'carbon source'
"""

carbon_growth = pd.read_sql_query(query, conn)

# Create matrix
carbon_matrix = carbon_growth.pivot_table(
    index='orgId',
    columns='carbon_source',
    aggfunc=len,
    fill_value=0
)
carbon_matrix = (carbon_matrix > 0).astype(int)

# Save to file
carbon_matrix.to_csv('carbon_source_growth_matrix.csv')

print(f"Organisms tested: {len(carbon_matrix)}")
print(f"Carbon sources: {len(carbon_matrix.columns)}")
print(f"Total tests: {carbon_matrix.sum().sum()}")
print(f"Matrix completeness: {carbon_matrix.sum().sum() / carbon_matrix.size:.1%}")
```

**Example output**:
```
Organisms tested: 42
Carbon sources: 89
Matrix completeness: 34.7%
```

## Example Analysis: Glucose Growth

```python
# Which organisms were tested on glucose?
glucose_growth = carbon_matrix['D-glucose'] if 'D-glucose' in carbon_matrix.columns else None

if glucose_growth is not None:
    print(f"Organisms with glucose data: {glucose_growth.sum()} / {len(glucose_growth)}")
    print("\nOrganisms that have glucose data:")
    print(glucose_growth[glucose_growth == 1].index.tolist())
    print("\nOrganisms that DON'T have glucose data:")
    print(glucose_growth[glucose_growth == 0].index.tolist())
```

## Handling Ambiguity

### Recommendations

1. **Create TWO matrices**:
   - **Conservative**: Missing = No growth
   - **Permissive**: Missing = Not tested (exclude from analysis)

2. **Analyze both**:
   - Compare model performance under both assumptions
   - Report sensitivity to this assumption

3. **Contact authors**:
   - Email FIT team to clarify
   - Ask specifically: "When an organism lacks data for a condition, is it because you didn't test it, or because it didn't grow?"

4. **Document assumption**:
   - Clearly state which assumption you're using
   - Report results under both scenarios if they differ significantly

## Quality Filters to Apply

When deciding "growth" vs "no growth", consider filtering for:

### Minimum Quality Thresholds
```python
query = """
SELECT DISTINCT
    gf.orgId,
    e.condition_1,
    e.expGroup
FROM GeneFitness gf
JOIN Experiment e ON gf.orgId = e.orgId AND gf.expName = e.expName
WHERE e.num > 0  -- Has gene fitness data
AND e.gMed >= 50  -- Median gene count ≥ 50 reads
AND e.mad12 <= 0.5  -- Good within-gene consistency
AND (e.u IS NULL OR e.u = '')  -- No error flags
"""
```

### Exclude Known Bad Experiments
- Check for removed experiments (e.g., sucrose/mannitol from problematic stocks)
- Check supplemental pages for organism-specific issues

## Coverage Statistics

To understand matrix sparsity:

```python
# Overall statistics
print(f"Total organisms: {len(growth_matrix)}")
print(f"Total conditions: {len(growth_matrix.columns)}")
print(f"Possible tests: {growth_matrix.size}")
print(f"Actual tests: {growth_matrix.sum().sum()}")
print(f"Coverage: {100 * growth_matrix.sum().sum() / growth_matrix.size:.1f}%")

# Per-organism statistics
per_org = growth_matrix.sum(axis=1).sort_values(ascending=False)
print(f"\nMost tested organism: {per_org.index[0]} ({per_org.iloc[0]} conditions)")
print(f"Least tested organism: {per_org.index[-1]} ({per_org.iloc[-1]} conditions)")
print(f"Median conditions/organism: {per_org.median():.0f}")

# Per-condition statistics
per_cond = growth_matrix.sum(axis=0).sort_values(ascending=False)
print(f"\nMost tested condition: {per_cond.index[0]} ({per_cond.iloc[0]} organisms)")
print(f"Least tested condition: {per_cond.index[-1]} ({per_cond.iloc[-1]} organisms)")
print(f"Median organisms/condition: {per_cond.median():.0f}")
```

## Next Steps

1. Extract complete growth matrix from FIT database
2. Categorize conditions (carbon, nitrogen, stress, etc.)
3. Build/obtain metabolic models for all organisms
4. Simulate same conditions in silico
5. Compare experimental vs computational growth
6. Generate confusion matrix

## References

**Research findings documented in**:
- `/thoughts/shared/research/2025-10-01-FIT-data-extraction-downloads.md`
- Web research on FIT experimental design

**Key sources**:
- Wetmore et al. 2015 mBio: 77% of experiments pass QC (114/501 failed for technical reasons)
- Price et al. 2018 Nature: "dozens of conditions each" (selective testing)
- FIT supplemental pages: Quality control metrics documented, no "no growth" categories
