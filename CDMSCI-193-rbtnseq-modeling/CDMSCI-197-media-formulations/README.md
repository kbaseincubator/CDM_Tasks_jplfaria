# CDMSCI-197: Translate Carbon Sources to In Silico Media Formulations

**Parent**: CDMSCI-193 - RBTnSeq Modeling Analysis

## Objective

Convert experimental carbon source conditions from Fitness Browser RBTnSeq into computational media formulations suitable for Flux Balance Analysis (FBA) simulations.

## Input

From **CDMSCI-196**:
- List of ~80-100 unique carbon sources tested
- Carbon source coverage statistics

## Tasks

### 1. Map Carbon Sources to Metabolite IDs

Convert Fitness Browser carbon source names to ModelSEED/BiGG compound identifiers:

**Example mappings**:
```
Fitness Browser Name  →  ModelSEED ID     →  Chemical Formula
D-Glucose             →  cpd00027         →  C6H12O6
Acetate              →  cpd00029         →  C2H3O2
Pyruvate             →  cpd00020         →  C3H3O3
L-Glutamate          →  cpd00023         →  C5H8NO4
```

### 2. Define Basal Media Composition

Create minimal media formulation with essential nutrients:

**Components**:
- Carbon source (variable - from CDMSCI-196 list)
- Nitrogen source (NH4+ or defined amino acids)
- Sulfur source (SO4²⁻)
- Phosphate (PO4³⁻)
- Trace minerals (Fe²⁺, Mg²⁺, Ca²⁺, Mn²⁺, Zn²⁺, etc.)
- Vitamins (if required)

### 3. Create Media Formulation Files

Generate computational media definitions for each carbon source.

**Format options**:
- JSON (ModelSEED/KBase format)
- TSV (simple exchange reaction list)
- Python dictionaries

## Outputs

### Results Files

All outputs saved to `results/` directory:

1. **carbon_source_to_modelseed_mapping.csv**
   - Columns: `fitness_browser_name`, `modelseed_id`, `compound_name`, `formula`
   - Mapping table for all ~80-100 carbon sources

2. **basal_media_composition.json**
   - Minimal media definition (without carbon source)
   - Exchange reactions with uptake/secretion bounds

3. **media_formulations/** _(directory)_
   - Individual media files per carbon source
   - Files named: `media_{carbon_source}.json`
   - Ready for FBA simulations

4. **unmapped_carbon_sources.txt**
   - List of carbon sources without ModelSEED matches
   - Requires manual curation or alternative databases

## Approach

### Step 1: Automated Mapping

Use ModelSEED database to map compound names:

```python
from modelseed import get_compound_by_name

for carbon_source in carbon_source_list:
    compound = get_compound_by_name(carbon_source)
    # Store mapping
```

### Step 2: Manual Curation

For unmapped compounds:
- Search BiGG database
- Search KEGG/MetaCyc
- Consult literature for chemical structure
- Add custom compound definitions if needed

### Step 3: Media File Generation

For each carbon source:

```python
media = {
    "id": f"media_{carbon_source_id}",
    "name": f"Minimal media with {carbon_source_name}",
    "compounds": [
        {"id": carbon_compound_id, "concentration": 10, "min_flux": -10, "max_flux": 0},  # Carbon source
        {"id": "cpd00013", "concentration": 1000, "min_flux": -1000, "max_flux": 1000},   # NH4
        {"id": "cpd00009", "concentration": 1000, "min_flux": -1000, "max_flux": 1000},   # Phosphate
        # ... other basal components
    ]
}
```

### Step 4: Validation

- Check all carbon sources mapped
- Verify exchange reaction bounds
- Test media files with example model

## Dependencies

**Python packages**:
```bash
pip install modelseedpy cobra pandas
```

**Databases**:
- ModelSEED Biochemistry database
- BiGG Models database
- KEGG Compound database

## Usage for Downstream Tasks

### For CDMSCI-199 (FBA Simulations)

```python
import json
import cobra

# Load model
model = cobra.io.read_sbml_model('organism_model.xml')

# Load media formulation
with open('media_formulations/media_D-Glucose.json', 'r') as f:
    media = json.load(f)

# Apply media to model
model.medium = {cpd['id']: abs(cpd['min_flux']) for cpd in media['compounds']}

# Run FBA
solution = model.optimize()
```

## Expected Challenges

1. **Name ambiguity**: "Glucose" vs "D-Glucose" vs "alpha-D-Glucose"
2. **Stereoisomers**: L- vs D- forms may have different IDs
3. **Salts vs acids**: "Acetate" vs "Acetic acid" vs "Sodium acetate"
4. **Unmapped compounds**: Novel or rare carbon sources may lack database entries

## Next Steps

1. ← Receive carbon source list from CDMSCI-196
2. → Map all carbon sources to ModelSEED IDs
3. → Create media formulation files
4. → Pass to CDMSCI-199 for FBA simulations

## Status

- [ ] Carbon source list received from CDMSCI-196
- [ ] Automated mapping performed
- [ ] Manual curation completed
- [ ] Basal media defined
- [ ] Media files generated
- [ ] Validation completed

## Last Updated

2025-10-02
