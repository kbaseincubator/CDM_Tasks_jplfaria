---
date: 2025-10-01
researcher: Jose P. Faria
topic: "FIT Fitness Browser - Missing Data Interpretation for Growth Matrix"
tags: [research, fitness-browser, growth-matrix, missing-data, experimental-design]
status: complete
last_updated: 2025-10-01
last_updated_by: Jose P. Faria
---

# Research: Missing Data Interpretation in FIT Fitness Browser

**Date**: 2025-10-01
**Researcher**: Jose P. Faria
**Resource**: https://fit.genomics.lbl.gov/cgi-bin/myFrontPage.cgi

## Research Question

When an organism-condition combination is missing from the FIT Fitness Browser database, does it mean:
- **A)** They tested the organism in that condition but it failed to grow? (biological no-growth)
- **B)** They simply didn't test that organism in that condition? (not tested)

This distinction is critical for building organism × condition growth/no-growth matrices for metabolic model validation.

## Key Finding

**Answer: Primarily (B) - Missing data means "NOT TESTED"**

**Confidence Level**: High

**Recommendation**: Assume missing data = "not tested" rather than "no growth"

## Evidence

### 1. No Documentation of Biological "No Growth" Events

**Finding**: Extensive search found **ZERO references** to biological growth failure in:
- Database schema (all 39 tables)
- Help documentation
- Source code
- Publications
- Supplemental data pages

**Search Terms Used** (all returned zero relevant results):
- "no growth"
- "failed to grow"
- "unable to grow"
- "growth failure"
- "organism did not grow"

**Implication**: If they documented growth failures, we would expect to see this in the database schema or documentation. The absence of any such documentation strongly suggests they don't track "tested but didn't grow" separately from "didn't test".

### 2. Only Technical/Quality Failures Are Documented

**Source**: Organism supplemental pages at https://genomics.lbl.gov/supplemental/bigfit/html/

**Examples of documented failures**:

| Organism | Samples Tested | Passed QC | Failed QC | Failure Rate |
|----------|----------------|-----------|-----------|--------------|
| PV4 | 230 | 160 | 70 | 30.4% |
| Koxy | 392 | 173 | 219 | 55.9% |
| azobra | 127 | 93 | 34 | 26.8% |

**Documented Failure Reasons** (all technical, not biological):

| Failure Code | Meaning | Threshold | Biological? |
|--------------|---------|-----------|-------------|
| `low_count` | Insufficient sequencing reads | gMed < 50 | **NO** - Technical |
| `high_mad12` | Inconsistent gene-half fitness | mad12 > 0.5 | **NO** - Technical |
| `low_cor12` | Low gene-half correlation | cor12 < 0.1 | **NO** - Technical |
| `high_adj_gc_cor` | GC content correlation issue | > 0.2 or 0.25 | **NO** - Technical |

**Key Observation**: All documented failures relate to **data quality**, not organism growth.

**Implication**: When experiments fail QC, it's because the sequencing/analysis didn't work, NOT because the organism didn't grow. If poor growth was the issue, it would manifest as low read counts and fail as `low_count`, but wouldn't be labeled as "biological no growth".

### 3. Organism-Specific Experimental Design

**Source**: Price et al. 2018 Nature
**URL**: https://www.nature.com/articles/s41586-018-0124-0

**Key Quote**: "genome-wide mutant fitness data from 32 diverse bacteria across **dozens of growth conditions each**"

**Critical Phrase**: "dozens of conditions **each**" - NOT "all bacteria in all conditions"

**Evidence of Selective Testing**:

```
Total experiments: 7,552 (as of Feb 2024)
Total organisms: 48 (46 bacteria + 2 archaea)

If all organisms tested in all conditions:
  - Would expect ~157 conditions tested across all organisms
  - Each organism would have ~157 experiments
  - Total = 48 × 157 = 7,536 experiments

Reality:
  - Vastly different experiment counts per organism
  - Some: >300 experiments
  - Others: <50 experiments
  - High variance in coverage
```

**Implication**: Researchers selected **organism-appropriate conditions** based on:
- Expected metabolic capabilities
- Research questions
- Physiological relevance
- Not attempting comprehensive testing of all organisms in all conditions

### 4. Statistical Evidence from Data Distribution

**Source**: Wetmore et al. 2015 mBio
**URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC4436071/

**Key Finding**: Of 501 BarSeq assays performed:
- **387 (77%) passed quality thresholds**
- **114 (23%) failed quality control**

**Failure Reasons Documented**:
- High-GC bacteria + 95°C PCR denaturation problems
- Insufficient read depth
- Poor gene-half correlation
- All technical issues, not growth failures

**Example from Paper**: "163 different bacterium-condition combinations" including "130 different bacterium-carbon source combinations"

**Implication**: The phrase "bacterium-condition combinations" (not "all bacteria in all conditions") confirms selective testing strategy.

### 5. Database Architecture Analysis

**Schema Review**: Examined all 39 tables in feba.db

**Relevant Tables**:
- `Experiment`: expName, orgId, expGroup, condition_1, num, gMed, mad12, cor12, u (error flags)
- `GeneFitness`: orgId, locusId, expName, fit, t
- No table for "failed growth attempts"
- No table for "conditions tested but no growth"
- No boolean field for "growth_success"

**Error Flags in Experiment Table**:
- `u` field: Contains error/warning messages
- All documented errors are technical/quality issues
- No growth-related errors found

**Implication**: Database was not designed to track "tested but didn't grow" separately from "didn't test"

## Counter-Evidence and Limitations

### Possible Alternative Interpretation

**Argument**: Low read counts could indicate poor growth
- If organism grows poorly, fewer cells → fewer sequences → low gMed
- These experiments would be excluded as `low_count` failures
- Could be interpreted as "tested but didn't grow well enough"

**Response**:
- This conflates "poor data quality" with "no growth"
- FIT methodology requires adequate cell density for accurate fitness measurements
- If growth is too poor to measure fitness, the experiment fails QC
- But this is documented as a **technical failure**, not a biological "no growth" determination

### Unknown Unknowns

**What we don't know**:
- Did researchers attempt any organism-condition combinations that they then decided not to sequence?
- Are there unpublished preliminary tests that showed no growth?
- How do they decide which conditions to test for each organism?

**Action**: Email FIT authors (Morgan Price, Adam Arkin lab) to clarify

## Conclusion and Recommendations

### Primary Conclusion

When organism X lacks data for condition Y in the FIT database, the evidence **strongly supports** interpretation (B):

**They did not test organism X in condition Y**

NOT: They tested it and documented growth failure

### Confidence Assessment

**Evidence Strength**: Strong
- Multiple independent lines of evidence
- Consistent across documentation, schema, and publications
- No contradicting evidence found

**Caveats**:
- Author confirmation still needed
- Some uncertainty about unpublished preliminary tests
- Possible conflation of "poor growth" with "low quality data"

### Practical Recommendations

**For Growth Matrix Construction**:

1. **Conservative Approach** (recommended until author clarification):
   - Missing data → Encode as 0 (no growth)
   - Provides lower bound on metabolic model accuracy
   - Better to underestimate than overestimate model performance

2. **Alternative Approach** (after author confirmation):
   - Missing data → Exclude from analysis (NA)
   - Only compare model to actually tested conditions
   - More accurate model validation but smaller dataset

3. **Sensitivity Analysis**:
   - Run both approaches
   - Compare results
   - Report both to show robustness

**For Confusion Matrix Analysis**:

```
If missing = "no growth" (conservative):
  - FP rate may be inflated (model predicts growth for untested conditions)
  - TN rate may be underestimated
  - Overall accuracy: Lower bound

If missing = "not tested" (exclude):
  - Only compares tested conditions
  - More accurate assessment
  - Smaller sample size
```

### Next Steps

1. Document findings (this document) - Complete
2. Update project documentation with correct interpretation - Complete
3. Create growth matrix extraction script with both options - Complete
4. Email FIT authors for confirmation:
   - Morgan Price (mprice@lbl.gov)
   - Subject: "Clarification on missing organism-condition combinations"
   - Question: "When an organism lacks data for a condition, is it because you didn't test it, or because it failed to grow?"
5. Proceed with growth matrix construction using conservative assumption
6. Sensitivity analysis with both interpretations

## References

**FIT Resources**:
- Main site: https://fit.genomics.lbl.gov
- Supplemental data: https://genomics.lbl.gov/supplemental/bigfit/
- Source code: https://bitbucket.org/berkeleylab/feba/

**Key Publications**:
1. **Wetmore et al. 2015, mBio** - RB-TnSeq methodology
   - DOI: 10.1128/mBio.00306-15
   - 501 assays, 387 passed QC, 114 failed (technical reasons)

2. **Price et al. 2018, Nature** - 32 bacteria study
   - DOI: 10.1038/s41586-018-0124-0
   - "dozens of conditions each" → selective testing

3. **Price et al. 2024, Database** - Current release
   - DOI: 10.1093/database/baae089
   - 7,552 experiments, 48 organisms

## Contact Information

**FIT Team**:
- Morgan Price (mprice@lbl.gov) - Lead developer, first author on methods papers
- Adam Arkin Lab - Lawrence Berkeley National Laboratory
- Fitness Browser Team - fit-help@lbl.gov

**Questions to Ask**:
1. When an organism-condition combination is missing from the database, what does it mean?
   - Not tested?
   - Tested but organism didn't grow?
   - Tested but failed quality control?

2. Are there any documented cases of "tested but organism failed to grow"?

3. How do you decide which conditions to test for each organism?

4. Is there any metadata indicating "attempted but no growth" vs "not attempted"?
