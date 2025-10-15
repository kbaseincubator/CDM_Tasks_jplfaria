# ModelSEED Database and Compound Mapping Guide

Analysis date: 2025-10-07

## Overview

This guide explains how to use the ModelSEED Database to map our 206 carbon sources from Fitness Browser data to ModelSEED compound IDs for metabolic modeling.

## Key Concepts

### Database vs Templates vs ModelSEEDpy

**ModelSEED Database** (https://github.com/ModelSEED/ModelSEEDDatabase/tree/dev)
- Complete biochemistry repository
- 33,978 compounds
- 36,645 reactions
- Integrated from KEGG, MetaCyc, BiGG, AraCyc, and other sources
- TSV files are master data (JSON auto-generated)

**ModelSEED Templates** (GramNegModelTemplateV6.json)
- Curated, modeling-ready subsets
- Only high-quality, balanced reactions
- Organism-specific (Gram-negative, Gram-positive, Archaea)
- Used for model building
- Our template has 8,584 reactions, 6,573 compounds

**ModelSEEDpy** (https://github.com/ModelSEED/ModelSEEDpy)
- Python package for metabolic model building
- Uses templates + database
- Performs gapfilling, FBA, media management
- Integrates with COBRApy

## Compound ID Format

All compounds use format: **cpd#####**

Examples:
- cpd00027 = D-Glucose
- cpd00001 = H2O
- cpd00029 = Acetate
- cpd00020 = Pyruvate

Compartmentalized compounds add suffix:
- cpd00027_c = Glucose in cytoplasm
- cpd00027_e = Glucose in extracellular space
- cpd00027_p = Glucose in periplasm

## Compound Search Methods

### Method 1: Solr REST API (Online Search)

**URL**: https://modelseed.org/solr/compounds/select

**Example Python Code**:
```python
from urllib.request import urlopen
import json

def search_compound(name):
    url = f"https://modelseed.org/solr/compounds/select?wt=json&q=aliases:{name}&fl=name,id,formula,charge,aliases,mass"
    response = json.load(urlopen(url))

    for doc in response['response']['docs']:
        print(f"{doc['id']}: {doc['name']} ({doc['formula']})")

    return response['response']['docs']

# Search for glucose
results = search_compound('glucose')
```

**Query Parameters**:
- `q=aliases:glucose` - Search query
- `fl=name,id,formula,charge,aliases,mass` - Fields to return
- `wt=json` - Response format

**Search Fields**:
- `aliases:glucose` - Search in all aliases
- `name:Glucose` - Search in compound name only
- `id:cpd00027` - Search by specific ID
- `formula:C6H12O6` - Search by chemical formula

### Method 2: Alias Files (Batch Lookup)

**Location in Database**: `/Biochemistry/Aliases/`

**Key Files**:

1. **Unique_ModelSEED_Compound_Aliases.txt**
   - Maps external database IDs to ModelSEED IDs
   - Format: `ModelSEED_ID <TAB> External_ID <TAB> Source`
   - Example:
     ```
     cpd00001    C00001    KEGG
     cpd00027    C00031    KEGG
     cpd00027    glc__D    BiGG
     cpd00027    GLUCOSE   AraCyc
     ```

2. **Unique_ModelSEED_Compound_Names.txt**
   - Maps compound names to ModelSEED IDs
   - Format: `ModelSEED_ID <TAB> Compound_Name <TAB> Type`
   - Example:
     ```
     cpd00001    Water         name
     cpd00001    H2O           name
     cpd00027    D-Glucose     name
     cpd00027    Glucose       name
     cpd00027    Dextrose      name
     ```

**Usage**:
```python
# Load alias mapping
def load_alias_map(alias_file):
    alias_map = {}
    with open(alias_file) as f:
        next(f)  # Skip header
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                msid, alias = parts[0], parts[1]
                alias_map[alias.lower()] = msid
    return alias_map

# Search
alias_map = load_alias_map('Unique_ModelSEED_Compound_Names.txt')
glucose_id = alias_map.get('glucose')  # Returns: cpd00027
```

### Method 3: Local Template (Fast, Offline)

**Our Template**: GramNegModelTemplateV6.json (already have this file)

**Advantage**: Fast, offline, matches exactly what we'll use for modeling

**Code**:
```python
import json

def search_template(compound_name, template_path):
    with open(template_path) as f:
        template = json.load(f)

    matches = []
    for compound in template['compounds']:
        # Search in name
        if compound_name.lower() in compound['name'].lower():
            matches.append({
                'id': compound['id'],
                'name': compound['name'],
                'formula': compound.get('formula', ''),
                'charge': compound.get('defaultCharge', 0)
            })
            continue

        # Search in aliases
        for alias in compound.get('aliases', []):
            if compound_name.lower() in alias.lower():
                matches.append({
                    'id': compound['id'],
                    'name': compound['name'],
                    'formula': compound.get('formula', ''),
                    'aliases': compound.get('aliases', [])
                })
                break

    return matches

# Usage
template_path = '/path/to/GramNegModelTemplateV6.json'
results = search_template('glucose', template_path)
```

### Method 4: Web Interface

**URL**: https://modelseed.org

- Search box at top
- Individual compound pages: https://modelseed.org/biochem/compounds/cpd00027
- Shows: name, formula, structure, aliases, pathways, reactions

## Compound Database Fields

Each compound has:

**Core Identification**:
- `id` - ModelSEED ID (cpd#####)
- `name` - Full compound name
- `abbreviation` - Short name (e.g., Glc for Glucose)
- `aliases` - Alternative names from KEGG, BiGG, MetaCyc, etc.

**Chemical Properties**:
- `formula` - Chemical formula (protonated form at pH 7.5)
- `mass` - Molecular weight
- `charge` - Electric charge at pH 7.5
- `smiles` - SMILES notation
- `inchikey` - InChI key

**Functional Properties**:
- `is_cofactor` - Whether compound is a cofactor (0 or 1)
- `is_core` - Whether in core metabolism (0 or 1)
- `is_obsolete` - Whether replaced by another compound (0 or 1)
- `linked_compound` - Related compound IDs

**Thermodynamic Data**:
- `deltag` - Standard Gibbs free energy (ΔG)
- `deltagerr` - Free energy error
- `pka` - Acid dissociation constants
- `pkb` - Base dissociation constants

## Practical Workflow for CDMSCI-197

### Step 1: Extract Carbon Source List

We already have this from CDMSCI-196:
- File: `combined_growth_matrix.csv`
- 206 carbon sources (row names)
- Example sources: D-Glucose, Glycerol, Acetate, Pyruvate, etc.

### Step 2: Search Strategy (Priority Order)

**For each carbon source**:

1. **Try exact name match** in template
   - Most reliable
   - Offline, fast
   - Guaranteed to work with our models

2. **Try Solr API search** if no exact match
   - Online search
   - Searches aliases, synonyms
   - Returns all matches

3. **Manual curation** if ambiguous
   - Multiple matches
   - Complex/proprietary names
   - Polymers (e.g., amylose, amylopectin)

4. **Flag as unmappable** if truly not in database
   - Proprietary prebiotics
   - Complex mixtures
   - Will need to skip these in FBA

### Step 3: Handle Special Cases

**Complex Carbohydrates** (e.g., amylose, starch):
- May not have single ModelSEED ID
- May need to use monomer (e.g., glucose for amylose)
- Document assumptions

**Proprietary Supplements** (e.g., Bimuno-prebiotic):
- Likely not in ModelSEED
- Research composition (e.g., galacto-oligosaccharides)
- Use closest representative compound

**Stereospecific Forms**:
- Be careful: D-Glucose ≠ L-Glucose
- D-Lactate ≠ L-Lactate
- Check stereochemistry in formula/name

**Salts and Hydrates**:
- "Citric Acid" vs "Citric Acid monohydrate"
- ModelSEED typically uses base compound
- Strip "sodium salt", "potassium salt", "monohydrate", etc.

### Step 4: Output Format

Create CSV file: `carbon_source_mapping.csv`

**Columns**:
- `Carbon_Source_Original` - Name from Fitness Browser
- `ModelSEED_ID` - Mapped compound ID (cpd#####)
- `ModelSEED_Name` - Official ModelSEED name
- `Formula` - Chemical formula
- `Mass` - Molecular weight
- `Charge` - Default charge
- `Mapping_Method` - How we found it (template_exact, solr_search, manual_curated)
- `Confidence` - High/Medium/Low
- `Notes` - Any special considerations

**Example**:
```csv
Carbon_Source_Original,ModelSEED_ID,ModelSEED_Name,Formula,Mass,Charge,Mapping_Method,Confidence,Notes
D-Glucose,cpd00027,D-Glucose,C6H12O6,180.156,0,template_exact,High,
Glycerol,cpd00100,Glycerol,C3H8O3,92.094,0,template_exact,High,
Citric Acid,cpd00137,Citrate,C6H5O7,189.101,-3,template_search,High,Base form without protons
Amylose from potato,cpd00027,D-Glucose,C6H12O6,180.156,0,manual_curated,Medium,Using glucose as monomer proxy
Bimuno-prebiotic,UNMAPPED,,,,,manual_curation,Low,Proprietary GOS mixture - no single compound
```

### Step 5: Create Media Formulations

For each mapped carbon source, create media formulation:

```python
from modelseedpy import MSMedia

# Base media (same for all)
base_nutrients = {
    'cpd00007': (-10, 100),    # O2
    'cpd00001': (-100, 100),   # H2O
    'cpd00009': (-100, 100),   # Phosphate
    'cpd00013': (-100, 100),   # NH3 (nitrogen)
    'cpd00048': (-100, 100),   # Sulfate (sulfur)
    'cpd00099': (-100, 100),   # Cl-
    'cpd00067': (-100, 100),   # H+
    'cpd00205': (-100, 100),   # K+
    'cpd00254': (-100, 100),   # Mg2+
    'cpd00971': (-100, 100),   # Na+
    'cpd00149': (-100, 100),   # Co2+
    'cpd00063': (-100, 100),   # Ca2+
    'cpd00058': (-100, 100),   # Cu2+
    'cpd00034': (-100, 100),   # Zn2+
    'cpd00030': (-100, 100),   # Mn2+
    'cpd10515': (-100, 100),   # Fe2+
    'cpd10516': (-100, 100),   # Fe3+
    'cpd11574': (-100, 100),   # Molybdate
    'cpd00244': (-100, 100),   # Ni2+
}

# Create media for each carbon source
def create_media(carbon_cpd_id, carbon_uptake_rate=-5):
    media_dict = base_nutrients.copy()
    media_dict[carbon_cpd_id] = (carbon_uptake_rate, 100)
    return MSMedia.from_dict(media_dict)

# Example: Glucose media
media_glucose = create_media('cpd00027', -5)  # -5 mmol/gDW/hr uptake

# Save media library as JSON
media_library = {
    'D-Glucose': {'carbon_cpd': 'cpd00027', 'uptake': -5},
    'Glycerol': {'carbon_cpd': 'cpd00100', 'uptake': -5},
    'Acetate': {'carbon_cpd': 'cpd00029', 'uptake': -5},
    # ... etc
}

import json
with open('media_library.json', 'w') as f:
    json.dump(media_library, f, indent=2)
```

## Common Carbon Sources - Quick Reference

Based on our data and ModelSEED database:

| Carbon Source | ModelSEED ID | Formula | Charge | Notes |
|--------------|--------------|---------|--------|-------|
| D-Glucose | cpd00027 | C6H12O6 | 0 | Primary carbon source |
| Glycerol | cpd00100 | C3H8O3 | 0 | |
| Acetate | cpd00029 | C2H3O2 | -1 | |
| Pyruvate | cpd00020 | C3H3O3 | -1 | |
| Succinate | cpd00036 | C4H4O4 | -2 | |
| Fumarate | cpd00106 | C4H2O4 | -2 | |
| Citrate | cpd00137 | C6H5O7 | -3 | |
| L-Alanine | cpd00035 | C3H7NO2 | 0 | |
| L-Serine | cpd00054 | C3H7NO3 | 0 | |
| L-Aspartate | cpd00041 | C4H7NO4 | -1 | |
| L-Glutamate | cpd00023 | C5H9NO4 | -1 | |
| L-Lactate | cpd00159 | C3H5O3 | -1 | |
| Formate | cpd00047 | CH1O2 | -1 | |
| Galactose | cpd01112 | C6H12O6 | 0 | |
| Fructose | cpd00082 | C6H12O6 | 0 | |
| Xylose | cpd00154 | C5H10O5 | 0 | |
| Ribose | cpd00105 | C5H10O5 | 0 | |
| Mannose | cpd00179 | C6H12O6 | 0 | D-Mannose |
| Maltose | cpd00179 | C12H22O11 | 0 | |
| Trehalose | cpd00794 | C12H22O11 | 0 | |
| Lactose | cpd00281 | C12H22O11 | 0 | Beta-Lactose |

## Validation Steps

After mapping all compounds:

1. **Check coverage**: How many of 206 carbon sources successfully mapped?
2. **Check confidence**: How many high/medium/low confidence?
3. **Check unmapped**: Document why unmapped (not in database, proprietary, etc.)
4. **Validate formulas**: Do formulas make chemical sense?
5. **Check for duplicates**: Multiple source names → same ModelSEED ID?
6. **Verify compartments**: Do we need to specify compartment? (Usually extracellular = _e)

## Expected Challenges

**Challenge 1: Ambiguous Names**
- Example: "Glucose" could be D-Glucose, alpha-D-glucose, beta-D-glucose
- Solution: Check Fitness Browser for specifics, default to D-Glucose

**Challenge 2: Complex Mixtures**
- Example: "casamino acids" (mixture of amino acids)
- Solution: May need to skip or create custom mixture formulation

**Challenge 3: Proprietary Prebiotics**
- Example: "Bimuno-prebiotic", "Bioecolians-prebiotic"
- Solution: Research composition, use representative oligosaccharide

**Challenge 4: Polymers**
- Example: "Amylose from potato" (glucose polymer)
- Solution: Use monomer (glucose) as proxy, note in documentation

**Challenge 5: Modified Sugars**
- Example: "6-O-Acetyl-D-glucose"
- Solution: Search carefully, may be in database but with different name

## Tools to Download/Clone

For comprehensive compound mapping:

1. **ModelSEEDDatabase** (Optional but helpful):
   ```bash
   git clone -b dev https://github.com/ModelSEED/ModelSEEDDatabase.git
   ```
   - Access alias files directly
   - Use BiochemPy library
   - Run local searches

2. **ModelSEEDpy** (Required for CDMSCI-198):
   ```bash
   git clone -b dev https://github.com/ModelSEED/ModelSEEDpy.git
   cd ModelSEEDpy
   pip install -e .
   ```
   - Required for model building
   - Media management
   - FBA simulations

## Summary

**For CDMSCI-197**, we need to:

1. Extract 206 carbon source names from combined_growth_matrix.csv
2. Map each to ModelSEED compound ID (cpd#####) using:
   - Local template search (fast, offline)
   - Solr API (comprehensive, online)
   - Manual curation (complex cases)
3. Create CSV mapping file with metadata
4. Create media library (base nutrients + each carbon source)
5. Save as reusable Python/JSON data structure

**Expected outcome**:
- ~150-180 successful mappings (75-85%)
- ~20-30 manual curations needed
- ~10-20 unmappable (proprietary, complex mixtures)

**Timeline estimate**: 1-2 days for initial mapping, 1 day for validation and curation

## Next Steps

After CDMSCI-197 complete:

1. **CDMSCI-198**: Use media library to build 57 metabolic models
2. **CDMSCI-199**: Run FBA on all model × media combinations
3. **Validation**: Compare FBA predictions to experimental growth data

## Resources

- ModelSEED Database: https://github.com/ModelSEED/ModelSEEDDatabase
- ModelSEEDpy: https://github.com/ModelSEED/ModelSEEDpy
- Solr Search: https://modelseed.org/solr/compounds/select
- Web Interface: https://modelseed.org
- Documentation: https://modelseedpy.readthedocs.io
- KEGG Database: https://www.genome.jp/kegg/ (for cross-referencing)
- BiGG Database: http://bigg.ucsd.edu (for cross-referencing)

## Last Updated

2025-10-07
