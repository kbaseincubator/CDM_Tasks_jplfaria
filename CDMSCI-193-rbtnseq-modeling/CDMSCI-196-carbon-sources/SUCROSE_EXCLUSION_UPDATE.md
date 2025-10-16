# Sucrose Exclusion Update

**Date**: 2025-10-15
**Ticket**: CDMSCI-196 - Compile Carbon Sources List
**Issue**: Stock solution contamination

## Background

Email from experiment author (2025-10-15):
> "Also, I forgot to mention -- please ignore the growth results for sucrose. There was apparently a problem with our stock solution."

## Changes Made

### 1. Updated `carbon_source_evaluation_final.csv`

**Before**:
```
Sucrose,True,simple_metabolite,use,Sucrose is a defined chemical compound and a common carbon source for many bacteria.,
```

**After**:
```
Sucrose,False,experimental_issue,exclude,"Sucrose growth data should be excluded due to stock solution contamination issue (reported by experiment author, 2025-10-15).",
```

### 2. Updated `06-filter-growth-matrix.ipynb`

Added new section after data loading:

**Section**: "Exclude Sucrose (Experimental Issue)"

**Purpose**: Explicitly remove Sucrose from the growth matrix before filtering

**Code**:
```python
# Remove Sucrose from growth matrix due to experimental issue
print("Checking for Sucrose in growth matrix...")
if "Sucrose" in full_matrix.index:
    print("  Found Sucrose - removing due to stock solution contamination issue")
    full_matrix = full_matrix.drop("Sucrose")
    print(f"  Updated matrix shape: {full_matrix.shape[0]} carbon sources × {full_matrix.shape[1]} organisms")
else:
    print("  Sucrose not found in matrix (already excluded)")
```

## Impact

### On CDMSCI-196
- Final filtered matrix: **140 carbon sources** (down from 141)
- Recommendation breakdown changes:
  - `use`: 140 (was 141)
  - `exclude`: 15 (was 14)

### On CDMSCI-197 (Media Formulations)
- Sucrose will not be mapped to ModelSEED compounds
- One fewer media formulation file generated

### On CDMSCI-199 (FBA Simulations)
- Sucrose will not be included in FBA validation
- Prevents unreliable experimental data from affecting model quality metrics

## Files Modified

1. `results/carbon_source_evaluation_final.csv`
2. `06-filter-growth-matrix.ipynb`
3. `SUCROSE_EXCLUSION_UPDATE.md` (this file)

## Next Steps

1. Re-run `06-filter-growth-matrix.ipynb` to regenerate filtered matrix
2. Verify Sucrose is excluded from downstream workflows
3. Update CDMSCI-196 Jira ticket with this information

---

**Note**: This exclusion is based on experimental quality control, not chemical/modeling considerations. Sucrose itself is a valid carbon source for metabolic modeling, but the experimental data for this compound is unreliable.
