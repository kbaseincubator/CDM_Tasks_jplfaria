# Data Integration Report: Fitness Browser vs Supplementary Table S2

**Date**: 2025-10-03
**Analyst**: Claude Code + José Pedro Faria

## Executive Summary

Integrated curated growth data from BigFIT paper (Supplementary Table S2) with Fitness Browser database extractions to create a comprehensive growth matrix for metabolic model validation.

**Key Finding**: Our assumption that "absence of data in Fitness Browser = no growth" is **INCORRECT**. The supplementary table contains 287 confirmed growth cases that were filtered out by our quality thresholds or marked as missing in the Fitness Browser database.

---

## Data Sources

### Source 1: Fitness Browser Database (feba.db)
- **Our extraction**: CDMSCI-196 carbon source growth matrix
- **Quality filters**: gMed >= 50, mad12 <= 0.5
- **Coverage**: 57 organisms × 198 carbon sources
- **Growth calls**: 1,089 (assumes absence = no growth)

### Source 2: Supplementary Table S2 (Curated)
- **Paper**: Price et al. (2018) Nature 557:503-509
- **URL**: https://genomics.lbl.gov/supplemental/bigfit/Supplementary_Tables_final.xlsx
- **Coverage**: 28 organisms × 95 carbon sources (minus water control)
- **Growth**: 931 confirmed
- **No Growth**: 1,701 confirmed
- **Note**: "No Growth" threshold is conservative - alternative conditions might support growth

---

## Organism Overlap

**All 28 organisms** from Supplementary Table S2 are in our 57-organism dataset:

| Supplementary Table Name | Fitness Browser OrgID | NCBI TaxID |
|--------------------------|----------------------|------------|
| Acidovorax sp. GW101-3H11 | acidovorax_3H11 | 12916 |
| Azospirillum brasilense sp. 245 | azobra | 1064539 |
| Burkholderia phytofirmans PsJN | Burk376 | 398527 |
| Caulobacter crescentus NA1000 | Caulo | 565050 |
| Cupriavidus basilensis 4G11 | Cup4G11 | 32035 |
| Dechlorosoma suillum PS | PS | 292415 |
| Dinoroseobacter shibae DFL-12 | Dino | 398580 |
| Dyella japonica UNC79MFTsu3.2 | Dyella79 | 2556921674 |
| **Echinicola vietnamensis DSM 17526** | **Cola** | **926556** |
| Escherichia coli BW25113 | Keio | 316407 |
| Herbaspirillum seropedicae SmR1 | HerbieS | 757424 |
| Klebsiella michiganensis M5a1 | Kang | 1134687 |
| Marinobacter adhaerens HP15 | Marino | 945713 |
| Pedobacter sp. GW460-11-11-14-LB5 | Pedo557 | 2556921033 |
| Phaeobacter inhibens BS107 | Phaeo | 1129364 |
| Pseudomonas fluorescens FW300-N1B4 | pseudo1_N1B4 | 2556922079 |
| Pseudomonas fluorescens FW300-N2C3 | pseudo5_N2C3_1 | 2556922243 |
| Pseudomonas fluorescens FW300-N2E2 | pseudo6_N2E2 | 2556922234 |
| Pseudomonas fluorescens FW300-N2E3 | pseudo3_N2E3 | 2556922257 |
| Pseudomonas fluorescens GW456-L13 | pseudo13_GW456_L13 | 2556921702 |
| Pseudomonas simiae WCS417 | WCS417 | 2743570 |
| Pseudomonas stutzeri RCH2 | psRCH2 | 379731 |
| Shewanella amazonensis SB2B | SB2B | 60478 |
| Shewanella loihica PV-4 | PV4 | 323850 |
| Shewanella oneidensis MR-1 | MR1 | 211586 |
| Shewanella sp. ANA-3 | ANA3 | 94122 |
| Sinorhizobium meliloti 1021 | Smeli | 266834 |
| Sphingomonas koreensis DSMZ 15582 | Korea | 569908 |

**Previously missed**: Cola (Echinicola vietnamensis) - now correctly identified!

---

## Carbon Source Overlap

**86 of 95** carbon sources from supplementary table matched our Fitness Browser extraction (90.5%).

### Improved Matching
After better name normalization:
- **D-Tagatose** → matched to **D-(-)-tagatose** ✓
- **L-Sorbose** → matched to **L-(-)-sorbose** ✓

### Unmatched Carbon Sources in Supplementary Table

8 carbon sources in supplementary table NOT in our Fitness Browser extraction:

1. 5-Keto-D-Gluconic Acid potassium salt
2. Cytosine
3. Itaconic Acid
4. L-Cysteine hydrochloride monohydrate
5. L-Methionine
6. Parabanic Acid
7. Potassium oxalate monohydrate
8. Thymine

These were likely filtered out by our quality thresholds or don't exist for our 57 organisms.

---

## Critical Discrepancies Found

Compared **28 organisms** across **86 matching carbon sources** = **2,408 total comparisons**

### Discrepancy Summary

| Discrepancy Type | Count | % of Comparisons |
|------------------|-------|------------------|
| FB shows "No Data" (0) but Supp shows "Growth" | **287** | **11.9%** |
| FB shows "Growth" (1) but Supp shows "No Growth" | **3** | **0.1%** |
| **Total Discrepancies** | **290** | **12.0%** |
| **Consistency Rate** | - | **88.0%** |

### Type 1: FB "No Data" but Supp "Growth" (287 cases)

**This is the major finding!**

Examples:
- Kang + D-Glucose: FB says "No Data", Supp says "Growth"
- Burk376 + D-Fructose: FB says "No Data", Supp says "Growth"
- acidovorax_3H11 + Sucrose: FB says "No Data", Supp says "Growth"

**Interpretation**:
- Our quality filters (gMed >= 50, mad12 <= 0.5) are too conservative
- Many growth experiments exist but were excluded due to lower quality metrics
- **Our assumption "absence of data = no growth" is WRONG**

### Type 2: FB "Growth" but Supp "No Growth" (3 cases)

**Very rare - only 3 cases:**
- Marino + Sodium Fumarate dibasic
- Burk376 + 2-Deoxy-D-Ribose
- Burk376 + Sodium propionate

**Interpretation**:
- Could be due to different experimental conditions
- Supplementary table uses conservative threshold (as noted in paper)
- Alternative conditions might support growth

---

## Files Created

### Core Data Files

1. **organism_metadata.csv**
   - All 57 organisms with full names, NCBI taxonomy IDs, divisions
   - Links shortnames to full species names

2. **supplementary_table_s2_clean.csv**
   - 28 organisms × 94 carbon sources (water control removed)
   - Values: "Growth" / "No Growth"
   - Curated gold-standard data from BigFIT paper

3. **combined_growth_matrix.csv**
   - **57 organisms** × **206 unique carbon sources**
   - Values: "Growth" / "No Growth" / blank (no data)
   - 28 organisms use supplementary table data (priority)
   - 29 organisms use Fitness Browser data
   - **1,341 Growth calls**
   - **1,701 No Growth calls**
   - **8,700 No data (blank)**

4. **data_source_discrepancies.csv**
   - All 290 discrepancies documented
   - Shows organism, carbon source, and conflicting calls

### Documentation

5. **supplementary_table_s2_README.md**
   - Metadata about supplementary table
   - Important notes about conservative thresholds

6. **organism_name_mapping_supplementary_to_FIT.csv**
   - Updated to include all 28 organisms (Cola added)

---

## Implications for Modeling (CDMSCI-199)

### For FBA Model Validation

**Gold Standard Test Set**: Use supplementary table data for 28 organisms × 86 carbon sources

- **2,408 definitive organism-carbon pairs** for validation
- **931 confirmed growth cases** to test true positives
- **1,477 confirmed no-growth cases** to test true negatives (note: conservative threshold)

### Confusion Matrix Interpretation

When comparing FBA predictions to experimental data:

|  | Experimental Growth | Experimental No Growth |
|---|---|---|
| **Model Predicts Growth** | TP | FP* |
| **Model Predicts No Growth** | FN | TN* |

**Important**: False positives (FP) and true negatives (TN) should be interpreted cautiously:
- Supplementary "No Growth" uses conservative threshold
- Alternative conditions might actually support growth

### Recommended Approach

1. **Primary validation**: Use supplementary table growth calls (conservative, high confidence)
2. **Secondary analysis**: Check Fitness Browser data for additional growth evidence
3. **Report**: Clearly distinguish between "confirmed no-growth" vs "untested/unknown"

---

## Recommendations

### Immediate Actions

1. **Stop assuming absence of data = no growth**
2. **Use combined_growth_matrix.csv** for all future analyses
3. **Prioritize supplementary table data** for the 28 organisms it covers
4. **Report uncertainty** for untested organism-carbon pairs

### For CDMSCI-196 (Current Task)

Update analysis to use three categories:
- **Growth**: Confirmed growth (from supp table or high-quality FB data)
- **No Growth**: Confirmed no-growth (from supp table only - conservative)
- **Unknown**: No data or low-quality data

### For CDMSCI-199 (FBA Validation)

- Focus validation on the 2,408 confirmed organism-carbon pairs
- Calculate separate metrics for:
  - Confirmed growth predictions (true positive rate)
  - Confirmed no-growth predictions (true negative rate, with caveats)
  - Unknown predictions (report separately)

### Future Work

Monitor for Morgan's updated curated dataset:
- Will cover more organisms and carbon sources
- Will provide even better gold standard for validation

---

## Conclusion

The integration revealed that **our Fitness Browser extraction significantly underestimates growth** due to conservative quality filters. The supplementary table provides curated gold-standard data that should take priority for the 28 organisms it covers.

**12% discrepancy rate** between sources is primarily driven by growth cases we missed (287) rather than false positives (3), validating that the supplementary table is more comprehensive and reliable for model validation purposes.

For the remaining 29 organisms not in supplementary table, we should use Fitness Browser data for "Growth" calls but avoid making "No Growth" assumptions based on absence of data.
