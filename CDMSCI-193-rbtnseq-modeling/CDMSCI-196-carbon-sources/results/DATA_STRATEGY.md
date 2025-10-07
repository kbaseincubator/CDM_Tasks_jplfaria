# Data Strategy for Growth/No-Growth Analysis

**Date**: 2025-10-03
**Updated**: After integrating Supplementary Table S2 with feba.db

---

## Data Source Hierarchy

We use a **tiered approach** based on data reliability:

### Tier 1: Supplementary Table S2 (Gold Standard)
- **Source**: BigFIT paper (Price et al. 2018) Supplementary Tables
- **Coverage**: 28 organisms × 94 carbon sources (minus water control)
- **Reliability**: Curated, peer-reviewed data
- **Use for**: Both "Growth" and "No Growth" calls
- **Note**: "No Growth" threshold is conservative - alternative conditions might support growth

### Tier 2: Fitness Browser Database (feba.db)
- **Source**: https://fit.genomics.lbl.gov database extract
- **Coverage**: 57 organisms × 198 carbon sources (with quality filters)
- **Reliability**: High quality (all experiments already pass gMed >= 50, mad12 <= 0.5)
- **Use for**: "Growth" calls ONLY (if experiment exists → growth occurred)
- **Important**: Do NOT assume absence of data means "No Growth"

---

## Why This Strategy?

### Discovery 1: Quality Filters Not the Issue
- ALL experiments in feba.db already pass quality thresholds (gMed >= 50, mad12 <= 0.5)
- Morgan's team pre-filtered the database before publishing
- 100% of 8,975 experiments pass quality filters

### Discovery 2: Supplementary Table Has Additional Data
- 287 growth cases exist in supplementary table but NOT in feba.db
- These experiments were conducted but not included in the public database
- Some may be from different experimental setups or pre-publication data

### Discovery 3: Absence of Data ≠ No Growth
- Many organism-carbon pairs have never been tested
- Missing data could mean: untested, failed experiment, or low quality data
- Only supplementary table provides definitive "No Growth" calls

---

## Data Files

### Primary Data Files

1. **supplementary_table_s2_clean.csv**
   - 28 organisms × 94 carbon sources
   - Values: "Growth" / "No Growth"
   - Use this as gold standard for validation
   - Column names: Species names (e.g., "Escherichia coli BW25113")

2. **combined_growth_matrix.csv**
   - 57 organisms × 206 carbon sources
   - Values: "Growth" / "No Growth" / blank (no data)
   - Integrates both data sources with proper hierarchy
   - Column names: Species names (e.g., "Burkholderia phytofirmans PsJN")

3. **organism_metadata.csv**
   - Reference table with all organism information
   - Links: orgId ↔ Species_Name ↔ NCBI_TaxID
   - Use for cross-referencing between datasets

### Supporting Files

4. **data_source_discrepancies.csv**
   - Documents 290 cases where sources disagree
   - Most (287) are: feba.db has no data, supp table shows growth
   - Very few (3) are: feba.db shows growth, supp table shows no growth

---

## Interpretation Guide

### "Growth"
**Meaning**: Organism confirmed to grow on this carbon source
**Confidence**: High
**Sources**:
- Supplementary table (curated)
- feba.db (high quality experiments exist)

### "No Growth"
**Meaning**: Organism did NOT grow on this carbon source under tested conditions
**Confidence**: Medium (conservative threshold)
**Sources**:
- Supplementary table ONLY
- Note: Alternative conditions (different concentrations, base media) might support growth

### Blank / Empty
**Meaning**: Unknown - not tested or no reliable data
**Confidence**: N/A
**Sources**: Neither source has data

---

## For Model Validation (CDMSCI-199)

### Recommended Test Set

Use **supplementary_table_s2_clean.csv** for FBA model validation:
- 28 organisms × 94 carbon sources = 2,632 potential comparisons
- 86 carbon sources overlap with our data = **2,408 usable comparisons**
- 931 confirmed growth cases
- 1,477 confirmed no-growth cases

### Metrics to Calculate

1. **For Growth Predictions**:
   - True Positive Rate (TPR): Model predicts growth AND supp table confirms growth
   - False Negative Rate (FNR): Model predicts no growth BUT supp table shows growth

2. **For No-Growth Predictions**:
   - True Negative Rate (TNR): Model predicts no growth AND supp table confirms no growth
   - False Positive Rate (FPR): Model predicts growth BUT supp table shows no growth
   - **CAVEAT**: Conservative threshold - some FPs might grow under different conditions

3. **For Unknown Cases**:
   - Report separately - cannot validate without ground truth
   - Use feba.db growth calls as secondary evidence

---

## Naming Conventions

### Species Names
All data files now use consistent **simple species names**:
- Format: `Genus species strain`
- Example: `Burkholderia phytofirmans PsJN`
- No division prefixes (removed "Betaproteobacteria:")

### File Columns
- **Species_Name**: Simple format for easy reading
- **Full_Species_Name**: With division prefix (in metadata only)
- **orgId**: Short identifier (in metadata only)
- **NCBI_TaxID**: For cross-referencing with NCBI databases

---

## Future Updates

### Morgan's Upcoming Dataset
Morgan Mentioned working on larger curated dataset:
- Will cover additional carbon sources
- Will include most bacteria in Fitness Browser
- Not yet ready for release (still validating)

**When available**: Upgrade to use that as Tier 1 gold standard

---

## Summary

**DO**:
- Trust supplementary table for both growth and no-growth calls
- Use feba.db for additional growth calls
- Report unknowns honestly
- Use species names consistently across analyses

**DON'T**:
- Assume absence of data means no growth
- Over-interpret "No Growth" as definitive (conservative threshold)
- Mix naming conventions between files

**REMEMBER**:
- ~2,400 high-confidence organism-carbon pairs for validation
- Limited ground truth is better than incorrect assumptions
- Model validation metrics should account for conservative thresholds
