# Cofitness and Functional Relationships

**Purpose**: Explain how cofitness identifies functionally related genes

## What is Cofitness?

### The Concept

**Cofitness** = similarity of fitness patterns across multiple experimental conditions

**Key idea**:
- Genes in the same pathway/complex tend to have similar phenotypes
- If gene A is important in condition X, and gene B is in the same pathway, gene B will likely also be important in condition X
- Measure similarity across ALL conditions using correlation

### The Formula

**Cofitness** = Spearman correlation of fitness vectors

```
For genes A and B:
  fitness_A = [fitA_exp1, fitA_exp2, ..., fitA_expN]
  fitness_B = [fitB_exp1, fitB_exp2, ..., fitB_expN]

  cofitness(A, B) = Spearman_correlation(fitness_A, fitness_B)
```

**Range**: -1 to +1
- +1 = perfect positive correlation (always same fitness)
- 0 = no correlation (unrelated)
- -1 = perfect negative correlation (opposite fitness)

## Why Cofitness Works

### Biological Basis

**Genes in same pathway**:
- Required together for specific function
- Loss of either gene → same phenotype
- Fitness patterns correlate across conditions

**Example - Amino acid biosynthesis**:
```
Tryptophan synthesis pathway:
  trpA → trpB → trpC → trpD → trpE

All genes required to make tryptophan
- In tryptophan media: all show fitness ≈ 0 (tryptophan provided)
- Without tryptophan: all show fitness < -2 (can't grow)
- Result: high cofitness among all trp genes
```

### Why NOT Same Pathway

**Low cofitness despite interaction**:
- Regulator vs. target (opposite fitness patterns)
- One gene has broader role across conditions
- One gene has redundancy (paralog masks phenotype)
- Different points in branching pathway

## Cofitness Thresholds

### High Cofitness: > 0.75

**Interpretation**: Likely same pathway/complex

**Confidence**: If cofitness > 0.75 AND rank 1 or 2 (top cofit partners)

**Statistics from FIT**:
- 35% of poorly annotated genes in Z. mobilis had cofitness > 0.75 with another gene
- This helped predict function for unknown genes

**Example**:
```
Gene X (unknown function):
  Top cofit partner: Gene Y (known DNA repair gene)
  Cofitness: 0.82, rank: 1

Prediction: Gene X likely involved in DNA repair
Validation: Check if Gene X and Y show similar condition dependencies
```

### Conserved Cofitness: > 0.6

**Definition**: Cofitness conserved across species

**Criteria**:
- Gene pair A-B has cofitness > 0.6 in organism 1
- AND orthologous pair A'-B' has cofitness > 0.6 in organism 2

**Interpretation**: Strong evidence of conserved functional relationship

**Statistics from Nature 2018**:
- 2,316 poorly annotated genes had conserved cofitness associations
- These are high-confidence functional predictions
- Used to propose specific functions for unknown genes

### Moderate Cofitness: 0.4 to 0.75

**Interpretation**: Possibly related, but less certain

**Could indicate**:
- Same biological process but different sub-pathways
- Indirect relationship
- One gene more pleiotropic (affects multiple processes)

### Low/No Cofitness: < 0.4

**Interpretation**: Likely unrelated or opposite regulation

**Note**: Absence of cofitness doesn't mean genes are unrelated
- May work in same pathway but tested conditions don't reveal it
- May have redundancy
- May have insufficient data

## How to Use Cofitness

### 1. Function Prediction for Unknown Genes

**Workflow**:
```
1. Find genes with unknown/poor annotation
2. Get their top cofit partners (highest cofitness scores)
3. Check if cofit partners have known functions
4. Predict unknown gene has similar function
```

**Example**:
```
Unknown Gene: YadB (no annotation)

Top cofit partners:
  1. dnaA (DNA replication initiation): cofitness = 0.85
  2. dnaN (DNA polymerase subunit): cofitness = 0.83
  3. dnaE (DNA polymerase III): cofitness = 0.79

Prediction: YadB likely involved in DNA replication
```

### 2. Pathway/Complex Member Identification

**Workflow**:
```
1. Start with known pathway member (e.g., trpA in tryptophan synthesis)
2. Find all genes with high cofitness (> 0.75)
3. Check if they cluster together
4. Validate with gene neighborhoods, domain annotations
```

**Example**:
```
Known: trpA (tryptophan synthase subunit)

High cofit genes:
  - trpB: 0.91 (same operon, same complex)
  - trpC, trpD, trpE: 0.85-0.88 (same pathway)
  - aroH: 0.72 (upstream in aromatic amino acid biosynthesis)

Conclusion: Successfully identifies tryptophan pathway members
```

### 3. Cross-Species Function Validation

**Workflow**:
```
1. Find gene pair with high cofitness in organism 1
2. Find orthologs in organism 2
3. Check if orthologs also have high cofitness
4. If yes → conserved functional relationship (high confidence)
```

**Example**:
```
E. coli: geneA ↔ geneB, cofitness = 0.78
P. putida: geneA' ↔ geneB' (orthologs), cofitness = 0.81

Conclusion: Functional relationship conserved across species
Confidence: Very high
```

## Cofitness in the FIT Database

### Cofit Table

**Schema**:
```sql
CREATE TABLE Cofit(
    orgId TEXT NOT NULL,
    locusId TEXT NOT NULL,
    hitId TEXT NOT NULL,      -- cofit partner
    rank INT NOT NULL,         -- 1 = top partner, 2 = 2nd, etc.
    cofit REAL NOT NULL,       -- cofitness score
    PRIMARY KEY (orgId,locusId,hitId)
);
```

**What's stored**:
- Only top cofit partners (not all gene pairs)
- Ranked by cofitness score
- Threshold for inclusion varies (typically top 10-50 partners)

### How to Query

**Get top cofit partners for a gene**:
```sql
SELECT
    c.locusId as gene,
    c.hitId as cofit_partner,
    c.rank,
    c.cofit,
    g.gene as partner_name,
    g.desc as partner_description
FROM Cofit c
JOIN Gene g ON c.orgId = g.orgId AND c.hitId = g.locusId
WHERE c.orgId = 'Keio'
  AND c.locusId = 'b0001'
  AND c.rank <= 10
ORDER BY c.rank;
```

**Find genes with high cofitness to known function**:
```sql
-- Find DNA repair genes by cofitness to known DNA repair gene
SELECT
    c.locusId,
    g.gene,
    g.desc,
    c.cofit,
    c.rank
FROM Cofit c
JOIN Gene g ON c.orgId = g.orgId AND c.locusId = g.locusId
WHERE c.orgId = 'Keio'
  AND c.hitId = 'b4059'  -- recA (known DNA repair)
  AND c.cofit > 0.75
ORDER BY c.cofit DESC;
```

### ConservedCofit Table

**Schema**:
```sql
CREATE TABLE ConservedCofit (
    orgId TEXT NOT NULL,
    locusId TEXT NOT NULL,
    hitId TEXT NOT NULL,
    rank INT NOT NULL,
    cofit REAL NOT NULL,
    orth_orgId TEXT NOT NULL,
    orth_locusId TEXT NOT NULL,
    orth_hitId TEXT NOT NULL,
    orth_rank INT NOT NULL,
    orth_cofit REAL NOT NULL,
    PRIMARY KEY (orgId,locusId,hitId,orth_orgId)
);
```

**What's stored**:
- Gene pairs with cofitness in organism 1
- AND their orthologs also have cofitness in organism 2
- Evidence for conserved functional relationships

## Advanced Concepts

### Positive vs. Negative Cofitness

**Positive cofitness (> 0)**:
- Genes have similar fitness patterns
- Both important in same conditions
- Typically same pathway/complex

**Negative cofitness (< 0)**:
- Genes have opposite fitness patterns
- One benefits when other is deleted
- May indicate:
  - Activator vs. repressor of same pathway
  - Antagonistic functions
  - Compensatory mechanisms

**Example - Transcription factor and target**:
```
TF is activator:
  TF deleted → target genes not expressed → similar phenotype
  → Positive cofitness

TF is repressor:
  TF deleted → target genes over-expressed → opposite phenotype
  → Negative cofitness
```

### Network Analysis

**Cofitness network**:
- Nodes = genes
- Edges = high cofitness (> 0.75)
- Clusters = functional modules

**Applications**:
- Identify gene clusters (pathways, complexes)
- Find hub genes (central to multiple processes)
- Detect novel functional modules

**Example**:
```
Cluster 1: All genes connected with cofitness > 0.8
  - trpA, trpB, trpC, trpD, trpE (tryptophan synthesis)
  - Prediction: Functional module for tryptophan biosynthesis

Cluster 2: Different set of genes
  - Might represent different pathway or complex
```

### Specificity vs. Pleiotropy

**Specific genes**:
- Strong phenotypes in few conditions
- High cofitness with pathway partners
- Easy to assign function

**Pleiotropic genes**:
- Phenotypes in many different conditions
- Lower cofitness (no single strong partner)
- Harder to assign specific function
- Example: Global regulators, RNA polymerase subunits

## Limitations and Caveats

### When Cofitness Fails

**1. Insufficient condition diversity**:
- Need conditions that distinguish pathways
- If all conditions similar, many genes will have similar fitness

**2. Gene redundancy**:
- Paralogous genes can compensate
- Both genes in pathway, but one has backup
- Only one shows phenotype → low cofitness

**3. Essential genes**:
- If gene is essential in most conditions
- Always has strong negative fitness
- Cofitness high with many essential genes (not specific)

**4. Condition-specific functions**:
- Gene A and B work together only in rare condition
- Most conditions don't test this interaction
- Low overall cofitness despite real relationship

### Best Practices

**Do**:
- Use cofitness as one line of evidence
- Check conserved cofitness across species
- Validate with gene neighborhoods, domains
- Look at multiple cofit partners (not just top 1)

**Don't**:
- Rely on cofitness alone for function prediction
- Ignore biological context
- Assume low cofitness means unrelated
- Forget to check if conditions tested are relevant

## Practical Example Workflow

### Goal: Predict function for unknown gene

**Step 1: Get cofitness data**
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('feba.db')

# Get top cofit partners
query = """
SELECT
    c.hitId as partner,
    g.gene as partner_name,
    g.desc as partner_function,
    c.cofit,
    c.rank
FROM Cofit c
JOIN Gene g ON c.orgId = g.orgId AND c.hitId = g.locusId
WHERE c.orgId = 'Keio'
  AND c.locusId = 'b1234'  -- your unknown gene
  AND c.cofit > 0.6
ORDER BY c.rank
LIMIT 20
"""

cofit_partners = pd.read_sql_query(query, conn)
print(cofit_partners)
```

**Step 2: Analyze partner functions**
```python
# Group by common terms in descriptions
from collections import Counter

# Extract key words from partner functions
functions = []
for desc in cofit_partners['partner_function']:
    # Simple word extraction (you could use NLP here)
    words = desc.lower().split()
    functions.extend([w for w in words if len(w) > 4])

# Count most common functions
common = Counter(functions).most_common(10)
print("Most common functional terms:", common)
```

**Step 3: Check conserved cofitness**
```python
# Check if relationship is conserved in other organisms
query_conserved = """
SELECT
    cc.orth_orgId as other_organism,
    cc.orth_locusId as ortholog,
    cc.orth_cofit as cofit_in_other_org,
    cc.cofit as cofit_here
FROM ConservedCofit cc
WHERE cc.orgId = 'Keio'
  AND cc.locusId = 'b1234'
  AND cc.cofit > 0.6
  AND cc.orth_cofit > 0.6
"""

conserved = pd.read_sql_query(query_conserved, conn)
print(f"Found {len(conserved)} conserved relationships")
```

**Step 4: Make prediction**
```python
if len(conserved) > 0 and common[0][1] > 5:
    print(f"High-confidence prediction: Gene involved in {common[0][0]}")
else:
    print("Moderate-confidence: Check additional evidence")
```

## Summary

**Key Points**:
1. **Cofitness** = correlation of fitness patterns across conditions
2. **> 0.75** suggests same pathway/complex
3. **Conserved cofitness > 0.6** across species = high confidence
4. Use to predict function for poorly annotated genes
5. Combine with other evidence (gene neighborhoods, domains, literature)
6. Check for consistency across organisms

**For More Information**:
- `/thoughts/shared/research/2025-10-01-FIT-database-schema-structure.md` - Cofit table schema
- Nature 2018 paper - Conserved cofitness analysis
- PLOS One 2017 paper - Cofitness validation of TF predictions
