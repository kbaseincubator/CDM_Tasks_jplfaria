# CDMSCI-199: Run FBA Simulations and Compare with Experimental Data

**Parent**: CDMSCI-193 - RBTnSeq Modeling Analysis

## Objective

Simulate growth for all organism × carbon source combinations using Flux Balance Analysis (FBA) and compare computational predictions against experimental Fitness Browser growth data.

## Input

From **CDMSCI-196**:
- Experimental growth matrix (57 organisms × carbon sources)
- Binary values: 1 = growth, 0 = no growth

From **CDMSCI-197**:
- Media formulation files for each carbon source (~80-100 files)

From **CDMSCI-198**:
- Genome-scale metabolic models for 57 organisms (SBML format)

## Workflow

### 1. Run FBA Simulations

For each organism × carbon source combination:

```python
import cobra
import pandas as pd

results = []

for organism in organisms:
    # Load model
    model = cobra.io.read_sbml_model(f'../CDMSCI-198-build-models/models/{organism}_gapfilled.xml')

    for carbon_source in carbon_sources:
        # Load media
        media = load_media(f'../CDMSCI-197-media-formulations/media_formulations/media_{carbon_source}.json')

        # Apply media to model
        model.medium = media

        # Run FBA
        solution = model.optimize()

        # Classify growth (threshold: biomass flux > 0.01 h⁻¹)
        growth_prediction = 1 if solution.objective_value > 0.01 else 0

        results.append({
            'organism': organism,
            'carbon_source': carbon_source,
            'biomass_flux': solution.objective_value,
            'prediction': growth_prediction
        })
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

### 3. Compare with Experimental Data

```python
# Load experimental growth matrix from CDMSCI-196
experimental = pd.read_csv('../CDMSCI-196-carbon-sources/results/carbon_source_growth_matrix.csv', index_col=0)

# Align matrices (same organisms and carbon sources)
common_organisms = experimental.index.intersection(insilico_matrix.index)
common_carbons = experimental.columns.intersection(insilico_matrix.columns)

exp_aligned = experimental.loc[common_organisms, common_carbons]
pred_aligned = insilico_matrix.loc[common_organisms, common_carbons]

# Calculate confusion matrix
from sklearn.metrics import confusion_matrix, classification_report

y_true = exp_aligned.values.flatten()
y_pred = pred_aligned.values.flatten()

cm = confusion_matrix(y_true, y_pred)
report = classification_report(y_true, y_pred)
```

## Outputs

### Results Files

All outputs saved to `results/` directory:

1. **insilico_growth_predictions.csv**
   - Binary matrix: 57 organisms × carbon sources
   - Values: 1 = model predicts growth, 0 = model predicts no growth

2. **biomass_flux_values.csv**
   - Continuous values: actual biomass flux rates
   - Useful for understanding prediction confidence

3. **confusion_matrix.csv**
   - 2×2 matrix comparing experimental vs in silico
   - Rows: Experimental (0, 1)
   - Columns: Predicted (0, 1)

4. **classification_metrics.json**
   - Precision, Recall, F1-score, Accuracy
   - Per-class metrics (growth vs no-growth)

5. **error_analysis.csv**
   - List of all False Positives and False Negatives
   - Columns: `organism`, `carbon_source`, `experimental`, `predicted`, `biomass_flux`, `error_type`

6. **comparison_heatmap.png**
   - Side-by-side heatmaps: experimental vs in silico
   - Color-coded by agreement/disagreement

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

## Next Steps

1. ← Receive models from CDMSCI-198
2. ← Receive media formulations from CDMSCI-197
3. → Run FBA simulations
4. → Generate confusion matrix
5. → Analyze prediction errors
6. → Identify model improvement opportunities

## Status

- [ ] FBA simulations completed
- [ ] In silico matrix generated
- [ ] Confusion matrix calculated
- [ ] Performance metrics computed
- [ ] Error analysis completed
- [ ] Results visualized

## Last Updated

2025-10-02
