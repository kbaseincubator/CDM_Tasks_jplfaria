# CDMSCI-193: Modeling Analysis of Growth/No-Growth Predictions for RBTnSeq Genomes

**Project**: Validate genome-scale metabolic models by comparing experimental growth data from Fitness Browser RBTnSeq (Deutschbauer lab) against in silico growth predictions.

## Objective

Compare experimental bacterial growth data from the Fitness Browser with computational predictions from genome-scale metabolic models to validate model accuracy.

## Workflow

```
Experimental Data (Fitness Browser)
          ↓
    Carbon Sources Matrix → Media Formulations → Metabolic Models → FBA Simulations
          ↓                        ↓                    ↓                ↓
    CDMSCI-196               CDMSCI-197          CDMSCI-198        CDMSCI-199
                                                                        ↓
                                                              Confusion Matrix
                                                              (Experimental vs In Silico)
```

## Subtasks

### 📁 CDMSCI-196: Compile Carbon Sources
**Goal**: Extract all carbon sources tested across all 57 genomes

**Outputs**:
- Binary growth matrix (57 organisms × ~80-100 carbon sources)
- Carbon source list with coverage statistics
- Visualization heatmap

**Status**: ✅ Complete - Notebook and script ready

---

### 📁 CDMSCI-197: Translate to Media Formulations
**Goal**: Convert experimental carbon sources to computational media definitions

**Outputs**:
- Media formulation files (JSON/TSV)
- Mapping table: Fitness Browser carbon source → ModelSEED compound ID
- Basal media composition

**Status**: ⏳ Pending

---

### 📁 CDMSCI-198: Build Metabolic Models
**Goal**: Generate genome-scale metabolic models for all 57 organisms using RAST annotations

**Outputs**:
- 57 SBML model files
- Model statistics table
- Gap-filling reports

**Status**: ⏳ Pending

---

### 📁 CDMSCI-199: FBA Simulations & Validation
**Goal**: Simulate growth and compare predictions with experimental data

**Outputs**:
- In silico growth prediction matrix
- Confusion matrix (experimental vs computational)
- Performance metrics (precision, recall, F1-score)
- Analysis of false positives/negatives

**Status**: ⏳ Pending

## Confusion Matrix Definition

```
                    Experimental Growth (Fitness Browser)
                    YES         NO
In Silico   YES     TP          FP
Growth      NO      FN          TN
```

**Interpretations**:
- **TP (True Positive)**: Grows experimentally AND grows in silico ✓
- **TN (True Negative)**: Doesn't grow experimentally AND doesn't grow in silico ✓
- **FP (False Positive)**: Doesn't grow experimentally BUT grows in silico (model over-predicts)
- **FN (False Negative)**: Grows experimentally BUT doesn't grow in silico (model missing capabilities)

## Data Sources

**Shared Resources** (not in GitHub repo):
- Fitness Browser database (`feba.db`, 8 GB)
- Downloaded organism data (protein sequences, experiment metadata)
- Documentation and references

**Location**: `../shared_resources/` (local only, gitignored)

## Quick Start

1. Clone this repository
2. Download feba.db from: https://figshare.com/articles/dataset/25236931
3. Place feba.db in `../shared_resources/database/`
4. Start with CDMSCI-196 to extract carbon sources

## Team

- **Assigned to**: José Pedro Faria
- **Project**: CDM Science - Data, Analysis, and Agents
- **Last updated**: 2025-10-02
