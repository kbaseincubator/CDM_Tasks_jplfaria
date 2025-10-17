# CRITICAL: CDMSCI-198 Model Building Protocol is Incomplete

## Date: 2025-10-16

## Problem Identified

The CDMSCI-198 model building workflow is **missing the ATP correction step**, which is a critical part of the proper ModelSEEDpy protocol.

### Current CDMSCI-198 Protocol (INCOMPLETE)

```
1. Build base model with GramNegModelTemplateV6
2. Add ATPM reaction
3. Test on pyruvate media
4. Gap-fill with GramNegModelTemplateV6 using MSGapfill
5. Save models
```

### Proper Protocol (from reference workflow)

```
1. Build base model with GramNegModelTemplateV6
2. Add ATPM reaction
3. **ATP CORRECTION** with Core-V5.2 template using MSATPCorrection
   - Evaluate growth on 54 default medias
   - Determine growth media
   - Apply growth media gap-filling
   - Expand model to genome scale
   - Build test conditions
4. Genome-scale gap-filling with GramNegModelTemplateV6 using MSGapfill
5. Save models
```

## Why ATP Correction Matters

From the reference workflow (`references/build_metabolic_model/build_model.ipynb`):

```python
from modelseedpy import MSATPCorrection
atp_correction = MSATPCorrection(model_base, template_core, default_medias,
                                 compartment='c0', atp_hydrolysis_id='ATPM_c0',
                                 load_default_medias=False)

# This critical step:
# 1. Tests ATP synthesis across 54 different media conditions
# 2. Ensures ATP metabolism is correctly configured
# 3. Gap-fills reactions needed for proper ATP flux
# 4. Creates test conditions for downstream gap-filling
# 5. Expands model to genome scale
media_eval = atp_correction.evaluate_growth_media()
atp_correction.determine_growth_media()
atp_correction.apply_growth_media_gapfilling()
atp_correction.expand_model_to_genome_scale()
tests = atp_correction.build_tests()
```

**The ATP correction step makes ATP fluxes more meaningful and ensures the model has correct energy metabolism before attempting genome-scale gap-filling.**

## Impact

### Models Affected
- All 44 draft models in `CDMSCI-198/models/*_draft.json`
- All 44 gap-filled models in `CDMSCI-198/models/*_gapfilled.json`

### Downstream Analysis Affected
- **CDMSCI-199**: All FBA simulations used incomplete models
- Confusion matrix (TP/TN/FP/FN) based on incomplete models
- 571 false negatives may be different with properly built models
- Gap-fill reactions analysis may be incomplete

## What Needs to Be Done

### Option 1: Complete Rebuild (Recommended but Time-Intensive)

1. **Update CDMSCI-198 notebook** to include ATP correction step
2. **Rebuild all 44 models** with proper protocol (estimated 2-4 hours)
3. **Re-run CDMSCI-199 FBA simulations** on corrected models
4. **Re-analyze results** and regenerate confusion matrix
5. **Re-run condition-specific gap-filling** on new false negatives

**Estimated total time**: 1-2 days

### Option 2: Document and Continue (Faster but Scientifically Incomplete)

1. Document that models were built without ATP correction
2. Note this as a limitation in analysis
3. Continue with current models
4. Plan to rebuild with proper protocol in future work

## Recommendation

**Option 1 is strongly recommended** because:

1. ATP correction is not optional - it's part of the proper protocol
2. Models without ATP correction may have incorrect energy metabolism
3. Gap-filling results may be affected by incomplete ATP metabolism
4. Scientific rigor requires following the established protocol
5. Rebuilding now is better than discovering issues later

## Files That Need Updates

### CDMSCI-198

- `02-build-and-gapfill-models.ipynb` - Add ATP correction step
- All model files need to be regenerated
- `results/model_statistics.csv` will change
- `results/gapfill_report.csv` will change

### CDMSCI-199

- Re-run `01-prepare-media-and-models.ipynb` (may be same)
- Re-run `02-analyze-predictions.ipynb` (confusion matrix will change)
- Re-run `03-analyze-discrepancies.ipynb` (FN list will change)
- Update condition-specific gap-filling with new FN list

## Decision Required

**User decision needed**: Should we rebuild all models with the proper protocol now, or document the limitation and continue?

This is a significant decision that affects the validity of all downstream analysis.

## References

- Reference workflow: `references/build_metabolic_model/build_model.ipynb`
- Current CDMSCI-198: `CDMSCI-198-build-models/02-build-and-gapfill-models.ipynb`
- ModelSEEDpy documentation on ATP correction

## Contact

José Pedro Faria
KBase / DOE Systems Biology
jplfaria@gmail.com
