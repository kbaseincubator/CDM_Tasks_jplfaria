# Analysis of Supplementary Table S2 (Carbon Sources) from BigFIT Paper

**Date**: 2025-10-03
**Source**: https://genomics.lbl.gov/supplemental/bigfit/Supplementary_Tables_final.xlsx
**Citation**: Price et al. (2018) Nature 557:503-509

## Background

Morgan Price clarified that absence of RBTnSeq data in feba.db could mean:
1. The experiment was done but the organism didn't grow
2. That experiment combination was never tested
3. The organism grew but data quality was poor

He directed us to **Supplementary Table S2** which contains **curated growth/no-growth data** for carbon sources.

## Supplementary Table S2 Contents

**Format**:
- **TRUE**: Positive for growth on the indicated carbon substrate (or successful genome-wide mutant fitness assay was done)
- **FALSE**: No growth on the indicated carbon substrate with the wild-type bacterium
- Note: FALSE doesn't necessarily mean the bacterium cannot grow - threshold is conservative

**Data**:
- 28 organisms
- 96 carbon sources
- 931 confirmed growth cases (TRUE)
- 1,757 confirmed no-growth cases (FALSE)

## Overlap with Our CDMSCI-196 Matrix

### Organisms

**27 of 28 organisms** from Supplementary Table S2 are in our 57-organism dataset:

| # | Supplementary Table Name | Fitness Browser OrgID | In Our Matrix |
|---|--------------------------|----------------------|---------------|
| 1 | Acidovorax sp. GW101-3H11 | acidovorax_3H11 | Yes |
| 2 | Azospirillum brasilense sp. 245 | azobra | Yes |
| 3 | Burkholderia phytofirmans PsJN | Burk376 | Yes |
| 4 | Caulobacter crescentus NA1000 | Caulo | Yes |
| 5 | Cupriavidus basilensis 4G11 | Cup4G11 | Yes |
| 6 | Dechlorosoma suillum PS | PS | Yes |
| 7 | Dinoroseobacter shibae DFL-12 | Dino | Yes |
| 8 | Dyella japonica UNC79MFTsu3.2 | Dyella79 | Yes |
| 9 | Echinicola vietnamensis DSM 17526 | (not in our matrix) | No |
| 10 | Escherichia coli BW25113 | Keio | Yes |
| 11 | Herbaspirillum seropedicae SmR1 | HerbieS | Yes |
| 12 | Klebsiella michiganensis M5a1 | Koxy | Yes |
| 13 | Marinobacter adhaerens HP15 | Marino | Yes |
| 14 | Pedobacter sp. GW460-11-11-14-LB5 | Pedo557 | Yes |
| 15 | Phaeobacter inhibens BS107 | Phaeo | Yes |
| 16 | Pseudomonas fluorescens FW300-N1B4 | pseudo1_N1B4 | Yes |
| 17 | Pseudomonas fluorescens FW300-N2C3 | pseudo5_N2C3_1 | Yes |
| 18 | Pseudomonas fluorescens FW300-N2E2 | pseudo6_N2E2 | Yes |
| 19 | Pseudomonas fluorescens FW300-N2E3 | pseudo3_N2E3 | Yes |
| 20 | Pseudomonas fluorescens GW456-L13 | pseudo13_GW456_L13 | Yes |
| 21 | Pseudomonas simiae WCS417 | WCS417 | Yes |
| 22 | Pseudomonas stutzeri RCH2 | psRCH2 | Yes |
| 23 | Shewanella amazonensis SB2B | SB2B | Yes |
| 24 | Shewanella loihica PV-4 | PV4 | Yes |
| 25 | Shewanella oneidensis MR-1 | MR1 | Yes |
| 26 | Shewanella sp. ANA-3 | ANA3 | Yes |
| 27 | Sinorhizobium meliloti 1021 | Smeli | Yes |
| 28 | Sphingomonas koreensis DSMZ 15582 | Korea | Yes |

Note: Echinicola vietnamensis is not in our matrix. Morgan mentioned they didn't collect wild-type carbon screening data for this organism.

### Carbon Sources

**96 carbon sources** in Supplementary Table S2 vs **198 carbon sources** in our CDMSCI-196 matrix

- Supplementary table has curated subset of most reliable carbon source experiments
- Our matrix includes all carbon sources with quality filters (gMed >= 50, mad12 <= 0.5)

### Data Comparison (27 overlapping organisms)

| Dataset | Organisms | Carbon Sources | Growth | No-Growth |
|---------|-----------|----------------|--------|-----------|
| **Supplementary Table S2** | 27 | 96 | 914 | 1,678 |
| **Our CDMSCI-196 Matrix** | 27 | 198 | 660 | 4,686 |

**Observations**:
1. Supplementary table has MORE growth calls (914) than our matrix (660) for same organisms
   - Suggests our quality filters (gMed >= 50, mad12 <= 0.5) may be too conservative
   - OR supplementary table includes lower-quality experiments we filtered out
   - OR our assumption that "no data = no growth" is incorrect for many cases

2. Supplementary table has fewer carbon sources but MORE defined growth data
   - This is the **curated validation dataset** from 2018 paper
   - Should be used for validation of our metabolic models
   - From same lab as Fitness Browser (Morgan Price's team)

## Files Created

1. `supplementary_table_s2_carbon.csv` - Full supplementary table data (96 carbon sources × 28 organisms)
2. `organism_name_mapping_supplementary_to_FIT.csv` - Mapping between full names and Fitness Browser OrgIDs

## Implications for CDMSCI-193 Project

### For CDMSCI-196 (Current)
- **Our assumption that "absence of data = no growth" is INCORRECT**
- Need to revise our growth matrix to only include cases where we have definitive data
- Supplementary Table S2 provides ground truth for 27 organisms × 96 carbon sources

### For CDMSCI-199 (FBA Simulations)
- Use Supplementary Table S2 as the **curated validation dataset** for model validation
- Compare model predictions against these 27 organisms × 96 carbon sources
- This gives us 2,592 confirmed growth/no-growth cases to validate against

### Recommended Next Steps
1. Update CDMSCI-196 to use curated growth data from Supplementary Table S2
2. For organisms not in supplementary table, continue using Fitness Browser data with quality filters
3. Clearly distinguish between:
   - **Confirmed growth** (TRUE in supp table or high-quality FIT data)
   - **Confirmed no-growth** (FALSE in supp table)
   - **Unknown** (no data in either source)

## Morgan's Upcoming Dataset

Morgan mentioned they're working on a much larger curated dataset covering:
- Additional carbon sources
- Most bacteria in Fitness Browser
- Not yet ready for release (still validating)

Once available, this will significantly expand our validation dataset.

## Contact

For questions about this data:
- Morgan Price (Fitness Browser): morganp@lbl.gov
- Adam Deutschbauer: AEDeutschbauer@lbl.gov
- Hans Carlson: HCarlson@lbl.gov
