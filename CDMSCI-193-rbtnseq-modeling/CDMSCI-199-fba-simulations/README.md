# CDMSCI-199: Run FBA Simulations and Compare with Experimental Data

**Parent**: CDMSCI-193 - RBTnSeq Modeling Analysis

## Objective

Simulate growth for all organism × carbon source combinations using Flux Balance Analysis (FBA) and compare computational predictions against experimental Fitness Browser growth data.

## Scope

- **44 organisms** (filtered for organisms with carbon source data)
- **141 carbon sources** (filtered for modeling suitability)
- **6,204 total FBA simulations** (44 × 141)

## Input

From **CDMSCI-196**:
- Experimental growth matrix: 44 organisms × 141 carbon sources
- File: `../CDMSCI-196-carbon-sources/results/combined_growth_matrix_filtered.csv`
- Binary values: 1 = growth, 0 = no growth

From **CDMSCI-197**:
- 141 minimal media JSON files (one per carbon source)
- Directory: `../CDMSCI-197-media-formulations/media/`
- Format: `{Carbon_Source_Name}.json`

From **CDMSCI-198**:
- 44 gap-filled metabolic models (JSON format)
- Directory: `../CDMSCI-198-build-models/models/`
- Format: `{organism_id}_gapfilled.json`

## Workflow

### 1. Run FBA Simulations

For each of the 6,204 organism × carbon source combinations:

```python
import cobra
import pandas as pd
import json
from pathlib import Path

# Load organism list from experimental data
exp_matrix = pd.read_csv('../CDMSCI-196-carbon-sources/results/combined_growth_matrix_filtered.csv', index_col=0)
organisms = exp_matrix.index.tolist()  # 44 organisms
carbon_sources = exp_matrix.columns.tolist()  # 141 carbon sources

results = []

for organism in organisms:
    # Load gap-filled model (JSON format)
    model_path = f'../CDMSCI-198-build-models/models/{organism}_gapfilled.json'
    model = cobra.io.load_json_model(model_path)

    for carbon_source in carbon_sources:
        # Load media formulation
        media_path = f'../CDMSCI-197-media-formulations/media/{carbon_source}.json'

        with open(media_path) as f:
            media_dict = json.load(f)

        # Apply media to model
        model.medium = media_dict

        # Run FBA
        solution = model.optimize()

        # Classify growth (threshold: biomass flux > 0.001 h⁻¹)
        growth_prediction = 1 if solution.objective_value > 0.001 else 0

        results.append({
            'organism': organism,
            'carbon_source': carbon_source,
            'biomass_flux': solution.objective_value,
            'prediction': growth_prediction,
            'status': solution.status
        })

# Convert to DataFrame
results_df = pd.DataFrame(results)
results_df.to_csv('results/fba_simulation_results.csv', index=False)
```

### 2. Create In Silico Growth Matrix

```python
# Convert results to matrix
insilico_df = pd.DataFrame(results)
insilico_matrix = insilico_df.pivot_table(
    index='organism',
    columns='carbon_source',
    values='prediction',
    fill_value=0
)

# Save
insilico_matrix.to_csv('results/insilico_growth_predictions.csv')
```

### 3. Identify Shared ModelSEED Compounds

```python
# Load mapping to identify shared compounds
mapping = pd.read_csv('../CDMSCI-197-media-formulations/results/carbon_source_mapping.csv')
mapping_filtered = mapping[mapping['ModelSEED_ID'] != 'UNMAPPED']

# Find carbon sources that share ModelSEED compounds
shared_compounds = mapping_filtered[mapping_filtered.duplicated('ModelSEED_ID', keep=False)].copy()
shared_compounds = shared_compounds.sort_values('ModelSEED_ID')

# Create a dictionary mapping carbon sources to their ModelSEED compound
carbon_to_compound = dict(zip(mapping_filtered['Carbon_Source_Original'],
                               mapping_filtered['ModelSEED_ID']))

# Identify unique carbon sources
unique_carbons = [cs for cs in carbon_sources
                  if cs not in shared_compounds['Carbon_Source_Original'].values]

print(f"Total carbon sources: {len(carbon_sources)}")
print(f"Unique mappings: {len(unique_carbons)}")
print(f"Shared mappings: {len(carbon_sources) - len(unique_carbons)}")
```

### 4. Compare with Experimental Data - Multiple Approaches

```python
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score

# Load experimental growth matrix from CDMSCI-196
experimental = pd.read_csv('../CDMSCI-196-carbon-sources/results/combined_growth_matrix_filtered.csv', index_col=0)

# Approach 1: Overall comparison (all 141 carbon sources)
y_true_all = experimental.values.flatten()
y_pred_all = insilico_matrix.values.flatten()

metrics_all = calculate_metrics(y_true_all, y_pred_all, 'overall')

# Approach 2: Unique mappings only (109 carbon sources)
exp_unique = experimental[unique_carbons]
pred_unique = insilico_matrix[unique_carbons]

y_true_unique = exp_unique.values.flatten()
y_pred_unique = pred_unique.values.flatten()

metrics_unique = calculate_metrics(y_true_unique, y_pred_unique, 'unique_only')

# Approach 3: Per-compound aggregation (113 unique ModelSEED compounds)
# Group carbon sources by ModelSEED compound
compound_groups = {}
for cs in carbon_sources:
    cpd = carbon_to_compound.get(cs, 'UNMAPPED')
    if cpd not in compound_groups:
        compound_groups[cpd] = []
    compound_groups[cpd].append(cs)

# Aggregate experimental data by compound (if ANY source shows growth → growth)
exp_compound = pd.DataFrame(index=experimental.index)
pred_compound = pd.DataFrame(index=insilico_matrix.index)

for cpd, sources in compound_groups.items():
    if cpd != 'UNMAPPED':
        exp_compound[cpd] = experimental[sources].max(axis=1)
        pred_compound[cpd] = insilico_matrix[sources].iloc[:, 0]  # All same prediction

y_true_compound = exp_compound.values.flatten()
y_pred_compound = pred_compound.values.flatten()

metrics_compound = calculate_metrics(y_true_compound, y_pred_compound, 'per_compound')

# Helper function
def calculate_metrics(y_true, y_pred, analysis_type):
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()

    return {
        'analysis_type': analysis_type,
        'total_comparisons': len(y_true),
        'true_positives': int(tp),
        'true_negatives': int(tn),
        'false_positives': int(fp),
        'false_negatives': int(fn),
        'accuracy': float(accuracy_score(y_true, y_pred)),
        'precision': float(precision_score(y_true, y_pred)),
        'recall': float(recall_score(y_true, y_pred)),
        'f1_score': float(f1_score(y_true, y_pred))
    }

# Save all metrics
all_metrics = {
    'overall': metrics_all,
    'unique_only': metrics_unique,
    'per_compound': metrics_compound
}

with open('results/classification_metrics.json', 'w') as f:
    json.dump(all_metrics, f, indent=2)

# Print comparison
print("\n" + "="*70)
print("METRICS COMPARISON")
print("="*70)
for analysis_type in ['overall', 'unique_only', 'per_compound']:
    m = all_metrics[analysis_type]
    print(f"\n{analysis_type.upper()}:")
    print(f"  Comparisons: {m['total_comparisons']}")
    print(f"  Accuracy:    {m['accuracy']:.3f}")
    print(f"  Precision:   {m['precision']:.3f}")
    print(f"  Recall:      {m['recall']:.3f}")
    print(f"  F1-Score:    {m['f1_score']:.3f}")
```

## Outputs

### Results Files

All outputs saved to `results/` directory:

1. **fba_simulation_results.csv**
   - All 6,204 FBA simulation results
   - Columns: `organism`, `carbon_source`, `biomass_flux`, `prediction`, `status`

2. **insilico_growth_predictions.csv**
   - Binary matrix: 44 organisms × 141 carbon sources
   - Values: 1 = model predicts growth, 0 = model predicts no growth

3. **biomass_flux_matrix.csv**
   - Continuous values: actual biomass flux rates (44 × 141)
   - Useful for understanding prediction confidence

4. **confusion_matrix.csv**
   - 2×2 matrix comparing experimental vs in silico
   - Rows: Experimental (0, 1), Columns: Predicted (0, 1)

5. **classification_metrics.json**
   - Metrics calculated in 3 ways:
     - **overall**: All 141 carbon sources (6,204 comparisons)
     - **unique_only**: 109 unique ModelSEED mappings (~4,796 comparisons)
     - **per_compound**: 113 unique compounds (~4,972 comparisons)
   - For each: Precision, Recall, F1-score, Accuracy, TP, TN, FP, FN

6. **error_analysis.csv**
   - List of all False Positives and False Negatives
   - Columns: `organism`, `carbon_source`, `experimental`, `predicted`, `biomass_flux`, `error_type`, `shared_compound`
   - Includes flag for whether error involves a shared ModelSEED compound

7. **shared_compound_analysis.csv**
   - Details on 12 ModelSEED compounds shared by 32 carbon sources
   - Impact on prediction accuracy for each shared compound group
   - Columns: `ModelSEED_ID`, `compound_name`, `carbon_sources`, `count`, `prediction_agreement`

8. **per_organism_accuracy.csv**
   - Accuracy for each of 44 organisms (overall and unique-only)
   - Identifies which organisms have best/worst predictions

9. **per_carbon_source_accuracy.csv**
   - Accuracy for each of 141 carbon sources
   - Identifies which carbon sources are hardest to predict
   - Includes ModelSEED_ID and shared compound flag

10. **comparison_viewer.html**
   - Interactive visualization comparing experimental vs in silico
   - Side-by-side heatmaps with filtering and sorting
   - Toggle to show/hide carbon sources with shared ModelSEED compounds

## Confusion Matrix Definition

```
                    Experimental Growth
                    YES (1)     NO (0)
Predicted   YES     TP          FP
            NO      FN          TN
```

### Interpretations

**True Positive (TP)**:
- Experimental: Growth
- Predicted: Growth
- **Interpretation**: Model correctly predicts growth capability ✓

**True Negative (TN)**:
- Experimental: No growth
- Predicted: No growth
- **Interpretation**: Model correctly predicts lack of growth ✓

**False Positive (FP)**:
- Experimental: No growth
- Predicted: Growth
- **Interpretation**: Model over-predicts (predicts growth when organism can't actually grow)
- **Possible causes**: Missing constraints, incomplete media formulation, essential genes not in model

**False Negative (FN)**:
- Experimental: Growth
- Predicted: No growth
- **Interpretation**: Model under-predicts (misses actual growth capability)
- **Possible causes**: Missing metabolic pathways, incorrect gene annotations, alternative routes not captured

## Evaluation Metrics

### 1. Precision (Positive Predictive Value)
```
Precision = TP / (TP + FP)
```
Of all predicted growth, what % actually grows?

### 2. Recall (Sensitivity, True Positive Rate)
```
Recall = TP / (TP + FN)
```
Of all actual growth, what % did we predict?

### 3. F1-Score (Harmonic Mean)
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```
Balanced measure of model performance

### 4. Accuracy
```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```
Overall correct predictions

## Analysis Tasks

### 1. Overall Model Performance

```python
print(f"Accuracy: {accuracy:.2%}")
print(f"Precision: {precision:.2%}")
print(f"Recall: {recall:.2%}")
print(f"F1-Score: {f1:.2%}")
```

### 2. Per-Organism Performance

Which organisms have best/worst model predictions?

```python
per_organism_accuracy = []
for org in organisms:
    org_exp = experimental.loc[org]
    org_pred = insilico_matrix.loc[org]
    accuracy = (org_exp == org_pred).mean()
    per_organism_accuracy.append({'organism': org, 'accuracy': accuracy})
```

### 3. Per-Carbon Source Performance

Which carbon sources are hardest to predict?

```python
per_carbon_accuracy = []
for carbon in carbon_sources:
    carbon_exp = experimental[carbon]
    carbon_pred = insilico_matrix[carbon]
    accuracy = (carbon_exp == carbon_pred).mean()
    per_carbon_accuracy.append({'carbon': carbon, 'accuracy': accuracy})
```

### 4. Error Pattern Analysis

Are FPs/FNs random or systematic?

- Do errors cluster by organism phylogeny?
- Do errors cluster by carbon source chemistry?
- Are errors related to model quality metrics?

## Expected Results

Based on typical metabolic model validation:

| Metric | Expected Range | Interpretation |
|--------|---------------|----------------|
| Accuracy | 60-80% | Moderate to good |
| Precision | 70-85% | Most predicted growth is real |
| Recall | 50-75% | Misses some real growth |
| F1-Score | 60-80% | Balanced performance |

## Dependencies

**Python packages**:
```bash
pip install cobra pandas numpy scikit-learn matplotlib seaborn
```

## Workflow Steps

1. ✓ Receive models from CDMSCI-198 (44 gap-filled models, JSON format)
2. ✓ Receive media formulations from CDMSCI-197 (141 minimal media files)
3. ✓ Receive experimental data from CDMSCI-196 (44 × 141 growth matrix)
4. → Create notebook to run 6,204 FBA simulations
5. → Generate in silico growth prediction matrix
6. → Calculate confusion matrix and metrics
7. → Perform per-organism and per-carbon source analysis
8. → Identify systematic prediction errors
9. → Create interactive visualization
10. → Update Jira ticket with results

## Implementation Notes

**Computational Requirements:**
- 6,204 FBA simulations (44 organisms × 141 carbon sources)
- Estimated time: ~1-2 hours (depending on hardware)
- Memory: Models average ~1 MB each, should fit in RAM

**Growth Threshold:**
- Use 0.001 h⁻¹ as minimum biomass flux for growth classification
- This matches the threshold used in gap-filling (CDMSCI-198)

**Error Handling:**
- Track solver status for each simulation
- Flag any infeasible/unbounded solutions
- Record all warnings for later analysis

## Important Consideration: Duplicate ModelSEED Mappings

**Issue**: When mapping carbon sources to ModelSEED compounds, some different experimental carbon sources mapped to the same ModelSEED compound.

**Scale of Issue:**
- 32 out of 141 carbon sources share 12 ModelSEED compounds
- 109 carbon sources have unique ModelSEED mappings

**Examples:**
- **Reasonable**: Sodium acetate and Potassium acetate → both map to cpd00029 (Acetate)
- **Problematic**: L-Fucose, 1,4-Butanediol, Azelaic acid, and 4 others → all map to cpd00751

**Impact on Analysis:**
For carbon sources that share a ModelSEED compound:
- **In silico prediction**: Will be identical (same media formulation used)
- **Experimental data**: May differ (due to stereochemistry, salt effects, or incorrect mapping)
- **Result**: Can introduce false positives or false negatives

**Handling Strategy (Option 1 - Keep Separate):**
1. Run all 6,204 simulations with original carbon source names
2. Track which carbon sources share ModelSEED compounds
3. Calculate and report metrics in multiple ways:
   - **Overall**: All 141 carbon sources (standard comparison)
   - **Unique only**: 109 carbon sources with unique ModelSEED mappings (conservative estimate)
   - **Per-compound**: Group by ModelSEED compound (aggregated comparison)
4. In error analysis, flag mismatches involving shared compounds
5. Document limitations in final report

**Additional Output File:**
- `shared_compound_analysis.csv` - Lists all shared ModelSEED compounds and their impact on metrics

## Status

- [x] Prerequisites completed (CDMSCI-196, 197, 198)
- [x] README updated with actual data specifications
- [ ] Create FBA simulation notebook
- [ ] Run 6,204 FBA simulations
- [ ] Generate in silico matrix
- [ ] Calculate confusion matrix
- [ ] Compute performance metrics
- [ ] Perform error analysis
- [ ] Create interactive visualization
- [ ] Update Jira ticket with results

## Last Updated

2025-10-15
