# Complete Results Analysis - Notebooks 02 & 03

## Overview

Comprehensive analysis of FBA simulation results (5,324 simulations) comparing model predictions to experimental Fitness Browser data (2,020 valid comparisons).

**Generated**: 2025-10-16
**Notebooks**: 02-analyze-predictions.ipynb, 03-exchange-reaction-gap-analysis.ipynb

---

## Overall Performance Metrics

### Confusion Matrix

|                    | Predicted: No Growth | Predicted: Growth |
|--------------------|---------------------|-------------------|
| **Experimental: No Growth** | 847 (TN) | 170 (FP) |
| **Experimental: Growth**    | **571 (FN)** | 432 (TP) |

### Classification Metrics

- **Accuracy**: 63.3% - Moderate overall correctness
- **Precision**: 71.8% - Good (when we predict growth, usually correct)
- **Recall**: 43.1% - **POOR** (miss 57% of actual growth cases)
- **F1-Score**: 0.538 - Moderate balance
- **Specificity**: 83.3% - Good (correctly identify no-growth cases)

### Key Insight

Models are **overly conservative**: High specificity (83%) but low recall (43%). They correctly identify when organisms won't grow, but miss most cases where organisms actually do grow.

---

## Root Cause Analysis: Missing Exchange Reactions

### Critical Finding

**ALL 571 False Negatives have biomass_flux ≈ 0**, indicating complete pathway absence, not just low activity or threshold issues.

### Missing Essential Metal Transporters

33 missing exchange reactions across 23 organisms for 3 priority metals:

| Compound | Name | Organisms Missing | Impact on FN Rate | Impact on Accuracy |
|----------|------|-------------------|-------------------|-------------------|
| **cpd10515** | Fe2+ | 14 | +12.5% | -13.4% |
| **cpd11574** | Molybdate | 5 | +19.2% | -16.4% |
| **cpd00244** | Ni2+ | 14 | +5.0% | -6.9% |

### Detailed Impact by Metal

#### Fe2+ (cpd10515) - Most Impactful

**Has exchange (30 organisms):**
- Avg FN count: 9.2
- Avg FN rate: 30.4%
- Avg accuracy: 64.8%

**Missing exchange (14 organisms):**
- Avg FN count: 21.0
- Avg FN rate: 42.9%
- Avg accuracy: 51.4%

**Difference**: +11.8 more FNs per organism, +12.5% higher FN rate

#### Molybdate (cpd11574) - Strongest Effect

**Has exchange (39 organisms):**
- Avg FN count: 13.6
- Avg FN rate: 32.2%
- Avg accuracy: 62.4%

**Missing exchange (5 organisms):**
- Avg FN count: 7.8
- Avg FN rate: 51.4%
- Avg accuracy: 46.0%

**Difference**: +19.2% higher FN rate (strongest effect per organism)

#### Ni2+ (cpd00244) - Moderate Effect

**Has exchange (30 organisms):**
- Avg FN count: 14.8
- Avg FN rate: 32.8%
- Avg accuracy: 62.7%

**Missing exchange (14 organisms):**
- Avg FN count: 9.0
- Avg FN rate: 37.8%
- Avg accuracy: 55.8%

**Difference**: +5.0% higher FN rate

### Organisms Missing Multiple Metals

5 organisms missing 2+ priority metals (highest risk):

1. **Bacteroides thetaiotaomicron VPI-5482**: Missing Ni2+ + Molybdate
   - 18 FNs, 90.0% FN rate, 10% accuracy

2. **Bifidobacterium breve UCC2003**: Missing Fe2+ + Molybdate
   - 7 FNs, 77.8% FN rate, 22% accuracy

3. **Phocaeicola vulgatus CL09T03C04**: Missing Ni2+ + Molybdate
   - 3 FNs, 75.0% FN rate, 25% accuracy

4. **Pedobacter sp. GW460-11-11-14-LB5**: Missing Ni2+ + Molybdate
   - 11 FNs, 14.3% FN rate, 73% accuracy (better despite missing 2)

5. **Brevundimonas sp. GW460-12-10-14-LB2**: Missing Ni2+ + Molybdate
   - 0 FNs, 0% FN rate, 100% accuracy (only 1 comparison)

---

## Per-Organism Performance

### High-Confidence Organisms (n ≥ 10 comparisons)

29 organisms meet statistical reliability threshold.

#### Top 5 Performers

1. **Cupriavidus basilensis FW507-4G11**: 100% accuracy (31/31)
   - All 31 predictions were True Positives
   - Has all three priority metals

2. **Dechlorosoma suillum PS**: 89.5% accuracy (68/76)
   - Balanced: TP=7, TN=61, FP=2, FN=6
   - Has all three priority metals

3. **Marinobacter adhaerens HP15**: 81.3% accuracy (61/75)
   - TP=8, TN=53, FP=5, FN=9
   - **Missing Fe2+** but still performs well

4. **Sphingomonas koreensis DSMZ 15582**: 78.7% accuracy (59/75)
   - Very conservative: TP=1, TN=58, FP=8, FN=8
   - **Missing Ni2+**

5. **Caulobacter crescentus NA1000**: 77.3% accuracy (58/75)
   - Extremely conservative: TP=1, TN=57, FP=5, FN=12
   - **Missing Ni2+**

#### Bottom 5 Performers

1. **Bacteroides thetaiotaomicron VPI-5482**: 10.0% accuracy (2/20)
   - TP=2, TN=0, FP=0, FN=18 (90% FN rate)
   - **Missing Ni2+ + Molybdate**

2. **Ralstonia sp. UNC404CL21Col**: 13.3% accuracy (2/15)
   - TP=2, TN=0, FP=0, FN=13 (87% FN rate)
   - **Has all metals** (missing exchanges NOT the only issue)

3. **Pseudomonas putida KT2440**: 19.6% accuracy (9/46)
   - TP=9, TN=0, FP=0, FN=37 (80% FN rate)
   - **Missing Fe2+**

4. **Echinicola vietnamensis**: 25.0% accuracy (3/12)
   - TP=3, TN=0, FP=0, FN=9 (75% FN rate)
   - **Missing Ni2+**

5. **Paraburkholderia bryophila 376MFSha3.1**: 28.6% accuracy (4/14)
   - TP=4, TN=0, FP=0, FN=10 (71% FN rate)
   - **Missing Fe2+**

### Key Observation: Bottom Performers Pattern

All bottom 5 performers show **TN=0** (never correctly predict no-growth). This means:
- They predict growth for ALL carbon sources tested
- When experimental data shows growth → True Positive
- When experimental data shows no growth → False Positive (but there are 0 FPs!)
- Actually, they predict NO growth for everything that's actually no-growth (that's why TN=0 and FP=0)

**Correction**: Bottom performers predict **NO GROWTH for everything**, so:
- When experimental = growth → False Negative
- When experimental = no-growth → would be True Negative, but there ARE no no-growth cases in their test set

This pattern indicates these organisms were only tested on carbon sources where growth was expected experimentally, but the models failed to predict it.

---

## Per-Carbon Source Performance

### High-Confidence Carbon Sources (n ≥ 5 comparisons)

~70 carbon sources meet statistical reliability threshold.

#### Perfect Accuracy Cases - Context Matters

**Type 1: True Perfect (Impressive)** - Mixed TP and TN

1. **Glycerol**: 93.3% accuracy (28/30)
   - TP=21, TN=7, FP=2, FN=0
   - Precision=0.91, Recall=1.00
   - Models handle glycerol metabolism well

2. **L-Histidine**: 92.3% accuracy (24/26)
   - TP=12, TN=12, FP=1, FN=1
   - Perfect balance, precision=recall=0.92

3. **D-Ribose**: 88.9% accuracy (24/27)
   - TP=13, TN=11, FP=1, FN=2
   - Good mixed predictions

**Type 2: All True Negatives (Not Impressive)** - Models just always predict no-growth

1. **L-Sorbose**: 100% accuracy (22/22)
   - TP=0, TN=22, FP=0, FN=0
   - Precision=0, Recall=0 (models NEVER predict growth)

2. **L-Methionine**: 100% accuracy (22/22)
   - TP=0, TN=22, FP=0, FN=0
   - Same pattern - always predicts no-growth

3. **Itaconic Acid**: 90.9% accuracy (20/22)
   - TP=0, TN=20, FP=0, FN=2
   - Never predicts growth

#### Worst Performers

1. **Sodium Formate**: 21.7% accuracy (5/23)
   - TP=1, TN=4, FP=18, FN=0
   - Many False Positives (predicts growth when shouldn't)

2. **D-Trehalose dihydrate**: 34.5% accuracy (10/29)
   - TP=0, TN=10, FP=0, FN=19
   - Never predicts growth when it should

3. **D-Glucosamine Hydrochloride**: 32.1% accuracy (9/28)
   - TP=0, TN=9, FP=0, FN=19
   - Models lack glucosamine utilization pathways

4. **N-Acetyl-D-Glucosamine**: 26.9% accuracy (7/26)
   - TP=0, TN=7, FP=0, FN=19
   - Related to above - amino sugar metabolism

5. **D-Mannose**: 29.6% accuracy (8/27)
   - TP=1, TN=7, FP=0, FN=19
   - Poor mannose metabolism predictions

### Carbon Source Patterns

**Well-modeled compound classes:**
- Glycerol and simple alcohols (when pathways present)
- Amino acids: L-Histidine, L-Ornithine (high accuracy)
- Organic acids: Pyruvate, Succinate, Fumarate (good performance)

**Poorly-modeled compound classes:**
- Amino sugars: Glucosamine, N-Acetyl-glucosamine
- Disaccharides: Trehalose, Raffinose (when transporters missing)
- Some rare sugars: L-Sorbose, L-Fucose

---

## Missing Compounds Impact

### By Number of Missing Compounds

| Missing Count | Accuracy | N Comparisons |
|---------------|----------|---------------|
| 0 | 72.7% | 315 |
| 1 | 60.3% | 843 |
| 2 | 63.5% | 780 |
| 3 | 57.3% | 82 |

**Interpretation**:
- Clean models (0 missing): 72.7% accuracy baseline
- Any missing compounds: drops to ~60% accuracy
- **Loss of ~12% accuracy** when compounds are missing

### False Negatives by Missing Compounds

Out of 571 False Negatives:
- **45 (7.9%)** have 0 missing compounds (baseline model gaps)
- **216 (37.8%)** have 1 missing compound
- **275 (48.2%)** have 2 missing compounds
- **35 (6.1%)** have 3 missing compounds

**Key Insight**: 86% of False Negatives involve ≥1 missing compound, supporting the hypothesis that missing transporters are the primary cause.

---

## Gap-Filling Process Analysis

### Critical Finding from Notebook 03

**Gap-filling added ZERO of the 33 missing exchanges.**

Comparison of draft vs gap-filled models for priority metals:
- All 14 organisms missing Fe2+ (cpd10515): Missing in BOTH draft and gap-filled
- All 14 organisms missing Ni2+ (cpd00244): Missing in BOTH draft and gap-filled
- All 5 organisms missing Molybdate (cpd11574): Missing in BOTH draft and gap-filled

### Why Gap-Filling Failed

Possible reasons:
1. **Gap-filling objective**: Optimized for growth on pyruvate minimal media only
2. **Alternative pathways**: Some organisms can use Fe3+ instead of Fe2+, so gap-filling didn't add Fe2+ transporter
3. **Internal pools**: Models may have internal metal pools that satisfy pyruvate growth without external uptake
4. **Scope limitation**: Gap-filling not designed to ensure complete metabolic capability across all carbon sources

---

## Predicted Impact of Corrections

### Expected Improvements (Conservative Estimates)

If adding the 33 missing exchanges fixes 60% of related False Negatives:

**Before Correction:**
- FN count: 571
- Recall: 43.1%
- Accuracy: 63.3%

**After Correction (Estimated):**
- FN count: ~230-285 (-286 to -341 FNs)
- Recall: ~65-75% (+22-32%)
- Accuracy: ~78-82% (+15-19%)

### Organisms Expected to Improve Most

1. **Pseudomonas putida KT2440**: Currently 19.6% accuracy, 37 FNs
   - Missing Fe2+, expect ~22 FNs to resolve
   - Estimated: 48-52% accuracy

2. **Paraburkholderia graminis OAS925**: Currently 41.5% accuracy, 31 FNs
   - Missing Fe2+, expect ~19 FNs to resolve
   - Estimated: 61-65% accuracy

3. **Bacteroides thetaiotaomicron VPI-5482**: Currently 10% accuracy, 18 FNs
   - Missing Ni2+ + Molybdate, expect ~11 FNs to resolve
   - Estimated: 55-65% accuracy

4. **Sinorhizobium meliloti 1021**: Currently 57.3% accuracy, 28 FNs
   - Missing Fe2+, expect ~17 FNs to resolve
   - Estimated: 76-80% accuracy

---

## Remaining Challenges

### Issues NOT Explained by Missing Exchanges

1. **Ralstonia sp. UNC404CL21Col**: 13.3% accuracy, 13 FNs
   - Has all three priority metals
   - Suggests deeper model quality issues

2. **Baseline False Negatives**: 45 FNs with 0 missing compounds
   - Represents ~8% of FNs
   - Indicates fundamental pathway gaps beyond metal transporters

3. **False Positives**: 170 cases where models predict growth but experiments show no-growth
   - Missing metal transporters don't explain these
   - Possible causes:
     - Growth rate threshold (experimental detection limit)
     - Missing regulatory constraints in models
     - Incorrect uptake reactions for carbon sources

### Carbon Sources That Will Still Be Challenging

Even after adding metal transporters:
- **Amino sugars**: D-Glucosamine, N-Acetyl-D-Glucosamine (likely missing utilization pathways)
- **Disaccharides**: D-Trehalose, D-Raffinose (may need additional transporters)
- **Rare sugars**: L-Sorbose, L-Fucose (specialized metabolism)

---

## Key Insights for Publication

### 1. Gap-Filling Limitations

The gap-filling process (CDMSCI-198) successfully created models that grow on pyruvate but failed to add essential metal transporters despite these metals being present in gap-filling media. This represents a **scope limitation** of single-condition optimization.

### 2. Systematic and Correctable Failures

Model failures are not random - they correlate strongly with missing specific exchange reactions (12-19% higher FN rates). This makes failures **predictable and systematically correctable**.

### 3. Metabolic Flexibility vs Completeness

Some organisms (e.g., using Fe3+ instead of Fe2+) demonstrate partial metabolic flexibility, but this is insufficient for complete phenotype coverage across diverse carbon sources. **Both iron forms are required** for comprehensive predictions.

### 4. Zero Flux Diagnostic

ALL False Negatives showing biomass_flux = 0 provides a clear diagnostic: these are not threshold issues or regulatory problems but represent **complete pathway absence**. This simplifies troubleshooting.

### 5. Model Quality Spectrum

High-confidence organisms show accuracy ranging from 10% to 89%, reflecting genuine differences in:
- Draft reconstruction completeness
- Organism metabolic complexity
- Availability of reference data
- Gap-filling success rate

### 6. Perfect Accuracy Can Be Misleading

Without examining confusion matrix details, 100% accuracy for L-Sorbose (precision=recall=0, all TN) appears successful but actually indicates the model **never predicts growth**. This highlights the importance of **multi-metric evaluation**.

---

## Recommendations for Notebook 04

### Scope

Manually add the 33 missing exchange reactions to affected models:
- 14 organisms need Fe2+ (cpd10515)
- 14 organisms need Ni2+ (cpd00244)
- 5 organisms need Molybdate (cpd11574)

### Approach

1. **Targeted re-simulation**: Only re-run FBA for organism-carbon combinations with FN=1 and missing exchanges
2. **Before-after comparison**: Track improvement per organism
3. **Validation**: Confirm biomass_flux increases from 0 to >0.001

### Success Criteria

- Reduce overall FN count by 200-300 (35-50% reduction)
- Improve recall from 43% to 65-75%
- Improve accuracy from 63% to 78-82%
- Bring bottom performers up to 50-60% accuracy range

---

## Files Generated

### Result Files
- `results/classification_metrics.json` - Overall performance metrics
- `results/per_organism_accuracy.csv` - 44 organisms with metrics
- `results/per_carbon_source_accuracy.csv` - 121 carbon sources with metrics
- `results/false_positives.csv` - 170 FP cases with details
- `results/false_negatives.csv` - 571 FN cases with details
- `results/exchange_reaction_matrix.csv` - 44 organisms × 19 compound exchange presence
- `results/missing_exchanges_details.csv` - 33 missing exchanges listed
- `results/exchange_performance_correlation.csv` - Exchange presence vs performance

### Visualizations
- `results/confusion_matrix.png`
- `results/organism_accuracy_top20.png`
- `results/carbon_source_accuracy_top20.png`
- `results/biomass_flux_distributions.png`

---

## Summary

The comprehensive analysis reveals that **missing metal transporter exchanges** are the primary cause of poor model recall (43%). Adding 33 missing exchanges for Fe2+, Ni2+, and Molybdate should improve accuracy from 63% to ~78-82% by fixing 60% of the 571 False Negatives. The analysis also identifies that perfect accuracy scores can be misleading without examining confusion matrix details, and establishes high-confidence filtering thresholds (n≥10 for organisms, n≥5 for carbon sources) for reliable statistical interpretation.

**Next Step**: Create Notebook 04 to systematically add missing exchanges and re-run simulations to validate predicted improvements.

---

**Analysis Date**: 2025-10-16
**Analyst**: José Pedro Faria
**Project**: CDMSCI-199 FBA Simulations
