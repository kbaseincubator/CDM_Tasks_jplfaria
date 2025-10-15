# Consistency Review - CDMSCI-196
**Date**: 2025-10-15

## Summary

Reviewed all documentation and data files in CDMSCI-196 for consistency in reporting metrics and findings.

## Corrected Metrics (Final)

All files now report consistent numbers:

### Combined Growth Matrix
- **Dimensions**: 208 carbon sources × 57 organisms = 11,856 total cells
- **Growth**: 1,256 (10.6%)
- **No Growth**: 1,331 (11.2%)  
- **Unknown**: 9,269 (78.2%)

### Data Discrepancies
- **Type 1** (FB No Data, Supp Growth): **170 cases**
- **Type 2** (FB Growth, Supp No Growth): **3 cases**
- **Total**: **173 discrepancies** (7.2% of 2,408 comparisons)
- **Consistency Rate**: 92.8%

### Supplementary Table S2
- 28 organisms × 94 carbon sources
- 931 Growth, 1,701 No Growth

### Fitness Browser
- 57 organisms × 198 carbon sources
- 1,089 organism-carbon pairs with data

## Files Updated

### Documentation
1. ✓ `README.md` - Fixed all occurrences (206→208, 168→170, 290→173)
2. ✓ `results/DATA_INTEGRATION_REPORT.md` - Updated summary table and conclusion
3. ✓ `results/DATA_STRATEGY.md` - Fixed discrepancy counts and matrix dimensions
4. ✓ `03-create-combined-growth-matrix.ipynb` - Updated header with correct numbers and date

### Files Verified (Already Correct)
- `01-download-supplementary-table-s2.ipynb` - No changes needed
- `02-extract-organism-metadata.ipynb` - No changes needed  
- `04-analyze-data-discrepancies.ipynb` - No changes needed
- `results/combined_growth_matrix.csv` - Data file verified correct
- `results/data_source_discrepancies.csv` - Contains 173 discrepancies (verified)
- `create_interactive_viewer.py` - Uses correct numbers from CSV

## Interactive Viewer

New tool created: `create_interactive_viewer.py`

**Outputs**: `results/growth_matrix_viewer.html` (2.71 MB)

**Features**:
- Summary statistics with explanatory notes
- Data coverage distribution histograms
- Interactive Plotly heatmap with zoom/pan
- Smart filtering: Click organism → see growth carbon sources
- Smart filtering: Click carbon → see organisms that grow
- Searchable organism and carbon source lists
- Shareable standalone HTML file

## Key Findings (Consistent Across All Docs)

1. **Quality filters not the issue**: 100% of feba.db experiments pass quality thresholds
2. **Additional data in paper**: 170 growth cases in supplementary table NOT in feba.db
3. **Cannot assume absence = no growth**: Only supplementary table provides definitive "No Growth" calls
4. **High Unknown percentage (78.2%)**: Due to combinatorial challenge of testing 208 × 57 = 11,856 combinations
5. **Data coverage**: 114 carbon sources tested on ≤10 organisms; 20 organisms tested on <50 carbons

## Validation for CDMSCI-199

Recommended test set: `supplementary_table_s2_clean.csv`
- 2,408 usable comparisons (28 organisms × 86 matching carbon sources)
- 931 confirmed growth cases
- 1,477 confirmed no-growth cases (conservative threshold)

## Status

✓ All documentation consistent
✓ All numbers verified against actual data files
✓ Interactive viewer created with correct metrics
✓ Ready for CDMSCI-199 (FBA validation)
