# Metabolic Model Building Reference Analysis

Analysis date: 2025-10-07

## Overview

This directory contains reference materials for building genome-scale metabolic models using ModelSEEDpy. The workflow demonstrates how to:
1. Build metabolic models from genome sequences
2. Use templates (core and genome-scale)
3. Create media formulations
4. Perform gapfilling to enable growth predictions
5. Validate models with experimental data

## Files in This Directory

### 1. build_model.ipynb (314K)
**Purpose**: Jupyter notebook demonstrating complete metabolic model building workflow

**Key Workflow Steps**:

#### Phase 1: Build Base Model
- Load templates (Core-V5.2.json, GramNegModelTemplateV6.json)
- Load genome from protein FASTA file
- Annotate genome with RAST (online service)
- Build base model using MSBuilder
- Add ATP maintenance reaction (ATPM)

#### Phase 2: ATP Gapfill/Analysis
- Test model on 54 default ATP metabolism medias
- Use MSATPCorrection to:
  - Evaluate which medias support growth
  - Apply gapfilling to fix metabolic gaps
  - Expand to genome scale
  - Build test conditions for validation

#### Phase 3: Genome Scale Gapfilling
- Create custom media formulations (in ModelSEED format)
- Run MSGapfill to identify missing reactions
- Integrate gapfill solutions into model
- Validate model growth on target media

**Key Python Classes**:
- `MSTemplateBuilder` - Loads JSON templates into Python objects
- `MSGenome` - Represents genome with gene annotations
- `RastClient` - Annotates genome with functional roles
- `MSBuilder` - Builds metabolic models from genome + template
- `MSATPCorrection` - ATP-based model validation and gapfilling
- `MSMedia` - Media formulation management
- `MSGapfill` - Identifies and adds missing reactions

### 2. Core-V5.2.json (891K)
**Purpose**: Core metabolic template

**Structure**:
- 252 reactions (core metabolism)
- 197 compounds
- 2 compartments (c=cytosol, e=extracellular)
- 0 biomass reactions (provided by genome-scale template)
- Used for ATP correction phase

**Key Components**:
- Central carbon metabolism (glycolysis, TCA cycle, PPP)
- Amino acid biosynthesis pathways
- Nucleotide metabolism
- Cofactor synthesis
- Energy metabolism

### 3. GramNegModelTemplateV6.json (23M)
**Purpose**: Genome-scale template for Gram-negative bacteria

**Structure**:
- 8,584 reactions (comprehensive metabolism)
- 6,573 compounds
- 2 compartments (c=cytosol, e=extracellular)
- 1 biomass reaction (bio1 = GramNegativeBiomass)
- Main template for model building

**Biomass Reaction**:
- ID: bio1
- 69 components across classes:
  - Protein (amino acids)
  - RNA (nucleotides)
  - DNA (nucleotides)
  - Lipids (cell membrane)
  - Cell wall components
  - Cofactors
  - Energy (ATP requirement)

**Reaction Structure**:
Each reaction has:
- `id` - Unique identifier (e.g., rxn00001_c)
- `name` - Human-readable name
- `direction` - = (reversible), > (forward), < (reverse)
- `lower_bound`, `upper_bound` - Flux constraints
- `templateReactionReagents` - Stoichiometry
  - `compound_ref` - Compound ID
  - `coefficient` - Stoichiometric coefficient (negative=consumed, positive=produced)
  - `compartment_ref` - Localization

**Compound Structure**:
Each compound has:
- `id` - ModelSEED ID (e.g., cpd00027)
- `name` - Common name (e.g., D-Glucose)
- `formula` - Chemical formula (e.g., C6H12O6)
- `mass` - Molecular weight
- `charge` - Default charge state

### 4. ModelSEEDpy_dev_required.rtf (936B)
**Purpose**: Dependency documentation

**Requirements**:
- ModelSEEDpy (dev branch): https://github.com/Fxe/ModelSEEDpy/tree/dev
- RAST annotation service (online, requires internet)
- Runs offline except for RAST annotation

## Media Formulation Format

Media in ModelSEEDpy uses compound IDs with flux bounds:

```python
media_glucose = MSMedia.from_dict({
    'cpd00027': (-5, 100),      # D-Glucose (carbon source, limited uptake)
    'cpd00007': (-10, 100),     # O2 (aerobic conditions)
    'cpd00001': (-100, 100),    # H2O
    'cpd00009': (-100, 100),    # Phosphate
    'cpd00013': (-100, 100),    # NH3 (nitrogen source)
    'cpd00048': (-100, 100),    # Sulfate (sulfur source)
    'cpd00099': (-100, 100),    # Cl-
    'cpd00067': (-100, 100),    # H+
    'cpd00205': (-100, 100),    # K+
    'cpd00254': (-100, 100),    # Mg2+
    'cpd00971': (-100, 100),    # Na+
    'cpd00149': (-100, 100),    # Co2+
    'cpd00063': (-100, 100),    # Ca2+
    'cpd00058': (-100, 100),    # Cu2+
    'cpd00034': (-100, 100),    # Zn2+
    'cpd00030': (-100, 100),    # Mn2+
    'cpd10515': (-100, 100),    # Fe2+
    'cpd10516': (-100, 100),    # Fe3+
    'cpd11574': (-100, 100),    # Molybdate
    'cpd00244': (-100, 100),    # Ni2+
})
```

**Format**: `'cpd#####': (lower_bound, upper_bound)`
- Negative lower bound = uptake allowed
- Positive upper bound = secretion allowed
- Carbon source typically has limited uptake (-5 to -10 mmol/gDW/hr)
- Other nutrients unlimited (-100 mmol/gDW/hr)

## Common Carbon Source Compound IDs

From template analysis, key carbon sources map to:

| Carbon Source | ModelSEED ID | Formula | Notes |
|--------------|--------------|---------|-------|
| D-Glucose | cpd00027 | C6H12O6 | Primary carbon source |
| Glycerol | cpd00100 | C3H8O3 | |
| Acetate | cpd00029 | C2H3O2 | |
| Pyruvate | cpd00020 | C3H3O3 | |
| Succinate | cpd00036 | C4H4O4 | |
| Fumarate | cpd00106 | C4H2O4 | |
| L-Alanine | cpd00035 | C3H7NO2 | |
| L-Serine | cpd00054 | C3H7NO3 | |
| L-Aspartate | cpd00041 | C4H7NO4 | |
| L-Glutamate | cpd00023 | C5H9NO4 | |
| Citrate | cpd00137 | C6H5O7 | |
| Galactose | cpd01112 | C6H12O6 | |
| Xylose | cpd00154 | C5H10O5 | |
| Maltose | cpd00179 | C12H22O11 | |

**Critical Note**: Some carbon sources may need manual mapping if names don't exactly match. Use ModelSEED compound database search or biochemistry knowledge to find correct IDs.

## Application to CDMSCI Tasks

### CDMSCI-196: Compile Carbon Sources List ✓ COMPLETE
**Status**: Complete - 206 carbon sources identified, 57 organisms

**Data Generated**:
- `combined_growth_matrix.csv` - 57 organisms × 206 carbon sources
- Values: "Growth" / "No Growth" / blank
- 2,408 high-confidence test cases for validation

### CDMSCI-197: Translate to Computational Media Formulations
**Status**: Next task - map carbon sources to ModelSEED format

**Required Steps**:
1. Load carbon source list (206 carbon sources)
2. Map each carbon source name → ModelSEED compound ID
   - Use template compound index (6,573 compounds available)
   - Manual curation for ambiguous names
   - Document mappings in CSV file
3. Create media formulation for each carbon source
   - Base media (same for all): salts, nitrogen, sulfur, trace metals
   - Variable component: carbon source (cpd##### with limited uptake)
   - Format: Python dict with compound IDs and flux bounds
4. Save as reusable media library

**Example Output Format**:
```csv
Carbon_Source_Name,ModelSEED_ID,Formula,Uptake_Rate
D-Glucose,cpd00027,C6H12O6,-5
Glycerol,cpd00100,C3H8O3,-5
Acetate,cpd00029,C2H3O2,-5
...
```

**Tools Needed**:
- Manual mapping for 206 carbon sources
- ModelSEED compound database search
- Validation against template (ensure all compounds exist)

### CDMSCI-198: Build Genome-Scale Metabolic Models
**Status**: Pending CDMSCI-197

**Required Inputs**:
1. Protein FASTA files for 57 organisms
   - Source: NCBI GenBank (we have NCBI TaxIDs in organism_metadata.csv)
   - Format: .faa (amino acid sequences)
2. Model template (GramNegModelTemplateV6.json - already have)
3. Core template (Core-V5.2.json - already have)
4. ModelSEEDpy (dev branch) - need to install

**Workflow** (per organism):
1. Load genome from FASTA
2. Annotate with RAST (online, may take hours per genome)
3. Build base model with MSBuilder
4. Add ATPM reaction
5. ATP correction with 54 default medias
6. Gapfill to enable growth
7. Save model as SBML or JSON

**Output**: 57 genome-scale metabolic models

**Time Estimate**:
- RAST annotation: ~2-4 hours per genome (57 genomes = 114-228 hours)
- Model building: ~10 minutes per genome (57 genomes = 9.5 hours)
- Total: ~5-10 days (if run serially), can parallelize

### CDMSCI-199: Run FBA Simulations and Generate Confusion Matrix
**Status**: Pending CDMSCI-197 and CDMSCI-198

**Required Inputs**:
1. 57 metabolic models (from CDMSCI-198)
2. 206 media formulations (from CDMSCI-197)
3. Experimental growth data (from CDMSCI-196: combined_growth_matrix.csv)

**Workflow**:
1. For each organism (57):
   - Load metabolic model
   - For each carbon source (206):
     - Apply media formulation
     - Run FBA (optimize biomass)
     - Record: growth predicted if objective > 0.001
2. Compare predictions vs experimental data:
   - True Positive (TP): Model predicts growth AND experimental shows Growth
   - False Positive (FP): Model predicts growth BUT experimental shows No Growth
   - True Negative (TN): Model predicts no growth AND experimental shows No Growth
   - False Negative (FN): Model predicts no growth BUT experimental shows Growth
3. Generate confusion matrix:
   - Sensitivity (TPR) = TP / (TP + FN) - % of actual growth correctly predicted
   - Specificity (TNR) = TN / (TN + FP) - % of actual no-growth correctly predicted
   - Precision (PPV) = TP / (TP + FP) - % of predicted growth that's correct
   - Accuracy = (TP + TN) / Total

**Output**:
- Confusion matrix (overall and per-organism)
- Prediction accuracy metrics
- Analysis of systematic errors (which carbon sources or organisms have poor predictions)

**Expected Results**:
- TPR: 70-90% (models should predict most growth)
- TNR: 60-80% (harder to predict no-growth, many false positives)
- False positives common due to:
  - Model may have pathways organism doesn't actually use
  - Experimental "No Growth" is conservative (different conditions might support growth)
  - Missing regulatory constraints in FBA

## Key Insights

### 1. Templates Define Metabolic Capabilities
- Core template (252 reactions): Essential metabolism for ATP correction
- Genome-scale template (8,584 reactions): Comprehensive bacterial metabolism
- Gram-negative specific (includes LPS, outer membrane)

### 2. Gapfilling is Essential
- Base models rarely grow on minimal media
- ATP correction identifies essential pathways
- Genome-scale gapfilling adds organism-specific reactions
- Gapfilling adds reactions from template, doesn't invent new chemistry

### 3. Media Formulation is Critical
- Must use exact ModelSEED compound IDs
- Carbon source uptake rate affects predictions
- Base media must provide all essential nutrients
- Format: compound ID → (lower_bound, upper_bound)

### 4. FBA Predicts Potential, Not Regulation
- FBA asks: "CAN organism grow?" not "WILL organism grow?"
- Doesn't account for:
  - Gene regulation
  - Transport limitations (beyond model)
  - Toxicity
  - Environmental conditions (pH, temperature)
- False positives expected (model says yes, experiment says no)
- False negatives suggest missing pathways or incorrect model

### 5. Validation Requires Experimental Data
- Gold standard: 2,408 test cases from CDMSCI-196
- Compare model predictions to RBTnSeq fitness data
- Systematic errors reveal model gaps or data issues

## Critical Next Steps

### Immediate (CDMSCI-197):
1. Map 206 carbon sources to ModelSEED compound IDs
   - Start with template compound index
   - Manual curation for unclear matches
   - Document all mappings
2. Create base media formulation (salts, nitrogen, sulfur, metals)
3. Generate 206 media formulations (base + each carbon source)
4. Save as Python dict or JSON for reproducibility

### Soon (CDMSCI-198):
1. Install ModelSEEDpy (dev branch)
2. Download protein FASTA files for 57 organisms from NCBI
3. Set up RAST annotation pipeline
4. Build 57 metabolic models
5. Validate models can grow on basic media

### Later (CDMSCI-199):
1. Run FBA simulations (57 models × 206 media = 11,742 simulations)
2. Compare to experimental data
3. Generate confusion matrix
4. Analyze prediction errors
5. Identify systematic biases

## References

- ModelSEEDpy: https://github.com/Fxe/ModelSEEDpy
- RAST: http://rast.nmpdr.org
- ModelSEED: https://modelseed.org
- Fitness Browser: https://fit.genomics.lbl.gov
- BigFIT Paper: Price MN et al. (2018) Nature 557:503-509

## Questions for Morgan (if needed)

1. Are there alternative annotation methods besides RAST? (RAST can be slow)
2. Recommended ATP correction settings for Fitness Browser organisms?
3. Known issues with ModelSEED templates for any of our 57 organisms?
4. Best practices for mapping Fitness Browser carbon sources to ModelSEED compounds?

## Last Updated

2025-10-07
