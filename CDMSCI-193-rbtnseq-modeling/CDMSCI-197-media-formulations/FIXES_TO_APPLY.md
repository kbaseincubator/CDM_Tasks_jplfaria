# Fixes to Apply to Mapping Notebook

## Issue 1: Function Definition Order Bug

**Problem**: `search_template_by_id` is called in cell 16 but defined at the END of cell 16

**Fix**: Move the function definition to the "Search Functions" cell (after `search_compound_round1`)

Add this function to the "Search Functions" cell:

```python
def search_template_by_id(compound_id):
    """Search for compound by ID in local template"""
    for compound in template_compounds:
        if compound['id'] == compound_id:
            return compound
    return None
```

Then REMOVE the same function definition from the bottom of cell 16.

## Issue 2: Solr API Failures

**Problem**: Solr API returns HTTP 400 errors for many compounds

**Fix**: Replace Solr search with local ModelSEED alias file search

### Step 1: Update Configuration Cell

Change ARGO_MODEL line:
```python
ARGO_MODEL = 'argo:o3'  # Was 'gpt5'
```

Add paths to local database:
```python
# Local ModelSEED Database files
MODELSEED_ALIASES = Path('../data/modelseed_database/Unique_ModelSEED_Compound_Aliases.txt')
MODELSEED_NAMES = Path('../data/modelseed_database/Unique_ModelSEED_Compound_Names.txt')
```

### Step 2: Add Function to Load Local Aliases

Add new cell after "Load Template":

```python
# Load ModelSEED alias files (local, no internet needed)
print("Loading ModelSEED alias files...")

# Load compound names
compound_names = {}
with open(MODELSEED_NAMES) as f:
    next(f)  # Skip header
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) >= 2:
            cpd_id = parts[0]
            name = parts[1].lower()
            if name not in compound_names:
                compound_names[name] = []
            compound_names[name].append(cpd_id)

print(f"  Loaded {len(compound_names):,} compound names")

# Load compound aliases
compound_aliases = {}
with open(MODELSEED_ALIASES) as f:
    next(f)  # Skip header
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) >= 3:
            cpd_id = parts[0]
            alias = parts[1].lower()
            source = parts[2]
            if alias not in compound_aliases:
                compound_aliases[alias] = []
            compound_aliases[alias].append(cpd_id)

print(f"  Loaded {len(compound_aliases):,} compound aliases")
print("ModelSEED database ready for offline searching")
```

### Step 3: Replace search_solr Function

Replace the `search_solr` function in "Search Functions" cell with:

```python
def search_modelseed_local(compound_name):
    """Search ModelSEED using local alias files (offline)"""
    search_lower = compound_name.lower()
    found_ids = set()

    # Search in compound names
    if search_lower in compound_names:
        found_ids.update(compound_names[search_lower])

    # Search in aliases
    if search_lower in compound_aliases:
        found_ids.update(compound_aliases[search_lower])

    # Get compound details from template
    matches = []
    for cpd_id in found_ids:
        compound = search_template_by_id(cpd_id)
        if compound:
            matches.append({
                'id': cpd_id,
                'name': compound['name'],
                'formula': compound.get('formula', ''),
                'charge': compound.get('defaultCharge', 0),
                'mass': compound.get('mass', 0),
                'source': 'modelseed_local'
            })

    return matches
```

### Step 4: Update search_compound_round1 Function

Replace the line:
```python
solr_matches = search_solr(compound_name) if not template_matches else []
```

With:
```python
modelseed_matches = search_modelseed_local(compound_name) if not template_matches else []
```

And replace:
```python
for match in solr_matches:
```

With:
```python
for match in modelseed_matches:
```

And update source label from 'solr' to 'modelseed_local':
```python
'source': 'modelseed_local'  # Was 'solr'
```

## Summary of Changes

1. Move `search_template_by_id` to Search Functions cell
2. Load local ModelSEED alias files
3. Replace `search_solr` with `search_modelseed_local`
4. Update `search_compound_round1` to use local search
5. Fix ARGO_MODEL to `'argo:o3'`

## Result

- No more HTTP 400 errors
- Faster (offline search)
- More reliable (158K aliases available)
- Function definition order fixed
