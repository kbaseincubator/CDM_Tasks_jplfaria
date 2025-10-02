---
date: 2025-10-01
researcher: Jose P. Faria
topic: "FIT Fitness Browser - Practical Data Extraction Plan and Code Examples"
tags: [research, fitness-browser, data-extraction, python, sql, tutorial]
status: complete
last_updated: 2025-10-01
last_updated_by: Jose P. Faria
---

# Research: FIT Fitness Browser Practical Data Extraction Plan

**Date**: 2025-10-01
**Researcher**: Jose P. Faria
**Resource**: https://fit.genomics.lbl.gov/cgi-bin/myFrontPage.cgi

## Research Question

Provide a practical, step-by-step plan for downloading, extracting, and reorganizing FIT Fitness Browser data into custom table structures suitable for confusion matrix analysis and other custom analyses.

## Summary

The recommended approach is: (1) Download feba.db SQLite database from Figshare, (2) Query using Python/pandas for flexible data manipulation, (3) Create custom tables with gene × experiment matrices, (4) Apply phenotype thresholds (|fit| > 2, |t| > 4), (5) Build confusion matrices for essentiality, function prediction, or ortholog conservation. This document provides complete code examples for each step.

## Detailed Findings

### 1. Step-by-Step Extraction Plan

#### Phase 1: Download and Setup (30 minutes - 2 hours depending on connection)

**Step 1.1**: Download Database
```bash
# Create project directory
mkdir -p FIT_analysis
cd FIT_analysis

# Download February 2024 release from Figshare
wget https://figshare.com/ndownloader/files/44580544 -O fitness_browser.tar.gz

# Extract
tar -xzf fitness_browser.tar.gz

# Decompress database (takes a few minutes)
gunzip feba.db.gz

# Verify size (should be ~5-10 GB)
ls -lh feba.db
```

**Step 1.2**: Install Required Python Packages
```bash
pip install pandas numpy sqlite3 scipy scikit-learn matplotlib seaborn
```

**Step 1.3**: Verify Database
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('feba.db')

# List tables
tables = pd.read_sql_query(
    "SELECT name FROM sqlite_master WHERE type='table'",
    conn
)
print(f"Found {len(tables)} tables")
print(tables)

# Count organisms
n_orgs = pd.read_sql_query("SELECT COUNT(*) as count FROM Organism", conn)
print(f"Organisms: {n_orgs['count'][0]}")

# Count experiments
n_exps = pd.read_sql_query("SELECT COUNT(DISTINCT expName) as count FROM Experiment", conn)
print(f"Experiments: {n_exps['count'][0]}")

conn.close()
```

#### Phase 2: Explore and Understand Data (1-2 hours)

**Step 2.1**: Examine Organisms
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('feba.db')

# Get all organisms
orgs = pd.read_sql_query("""
    SELECT orgId, genus, species, strain
    FROM Organism
    ORDER BY genus, species
""", conn)

print(orgs)
orgs.to_csv('organisms.csv', index=False)

# Count genes per organism
gene_counts = pd.read_sql_query("""
    SELECT orgId, COUNT(*) as n_genes
    FROM Gene
    WHERE type = 1  -- protein-coding only
    GROUP BY orgId
    ORDER BY n_genes DESC
""", conn)

print(gene_counts)
```

**Step 2.2**: Examine Experimental Conditions
```python
# Get unique condition types
condition_summary = pd.read_sql_query("""
    SELECT
        expGroup,
        COUNT(DISTINCT expName) as n_experiments,
        COUNT(DISTINCT orgId) as n_organisms,
        COUNT(DISTINCT condition_1) as n_unique_conditions
    FROM Experiment
    GROUP BY expGroup
    ORDER BY n_experiments DESC
""", conn)

print(condition_summary)

# Get all carbon source experiments
carbon = pd.read_sql_query("""
    SELECT orgId, expName, expDesc, condition_1, concentration_1
    FROM Experiment
    WHERE expGroup = 'carbon source'
    ORDER BY orgId, condition_1
""", conn)

carbon.to_csv('carbon_source_experiments.csv', index=False)
```

**Step 2.3**: Examine Data Completeness
```python
# Check fitness data coverage
coverage = pd.read_sql_query("""
    SELECT
        g.orgId,
        COUNT(DISTINCT g.locusId) as total_genes,
        COUNT(DISTINCT gf.locusId) as genes_with_fitness,
        COUNT(DISTINCT gf.expName) as n_experiments,
        COUNT(*) as total_measurements
    FROM Gene g
    LEFT JOIN GeneFitness gf ON g.orgId = gf.orgId AND g.locusId = gf.locusId
    WHERE g.type = 1
    GROUP BY g.orgId
""", conn)

coverage['coverage_pct'] = 100 * coverage['genes_with_fitness'] / coverage['total_genes']
print(coverage)
```

#### Phase 3: Extract Core Data (30 minutes - 1 hour)

**Step 3.1**: Extract Gene Information
```python
# Get all genes with annotations
genes = pd.read_sql_query("""
    SELECT
        orgId, locusId, sysName, gene, desc, type,
        scaffoldId, begin, end, strand, GC
    FROM Gene
    WHERE type = 1  -- protein-coding
""", conn)

print(f"Total genes: {len(genes)}")
genes.to_csv('all_genes.csv', index=False)

# Get genes by organism
for org in ['Keio', 'WCS417', 'MR1']:  # Example organisms
    org_genes = genes[genes['orgId'] == org]
    org_genes.to_csv(f'genes_{org}.csv', index=False)
```

**Step 3.2**: Extract Fitness Data
```python
# Extract all fitness data (WARNING: large query, may take several minutes)
# Consider doing per-organism instead

def extract_fitness_by_organism(conn, orgId, output_file):
    """Extract fitness data for one organism"""
    query = f"""
    SELECT
        gf.locusId, gf.expName, gf.fit, gf.t
    FROM GeneFitness gf
    WHERE gf.orgId = '{orgId}'
    """
    df = pd.read_sql_query(query, conn)
    df.to_csv(output_file, index=False)
    return df

# Extract for E. coli
keio_fitness = extract_fitness_by_organism(conn, 'Keio', 'fitness_Keio.csv')
print(f"E. coli fitness measurements: {len(keio_fitness)}")
```

**Step 3.3**: Extract Experiment Metadata
```python
# Get all experiment metadata
experiments = pd.read_sql_query("""
    SELECT
        orgId, expName, expDesc, expGroup,
        media, temperature, pH,
        condition_1, concentration_1, units_1,
        condition_2, concentration_2, units_2,
        nGenerations, mad12, cor12, gccor
    FROM Experiment
""", conn)

experiments.to_csv('all_experiments.csv', index=False)

# Get by organism
keio_exps = experiments[experiments['orgId'] == 'Keio']
keio_exps.to_csv('experiments_Keio.csv', index=False)
```

#### Phase 4: Create Custom Table Structures (1-2 hours)

**Step 4.1**: Create Gene × Experiment Fitness Matrix
```python
def create_fitness_matrix(conn, orgId, output_prefix):
    """
    Create gene × experiment matrices for fitness and t-scores
    """
    # Get fitness data
    query = f"""
    SELECT gf.locusId, gf.expName, gf.fit, gf.t
    FROM GeneFitness gf
    WHERE gf.orgId = '{orgId}'
    """
    df = pd.read_sql_query(query, conn)

    # Create fitness matrix
    fit_matrix = df.pivot(
        index='locusId',
        columns='expName',
        values='fit'
    )

    # Create t-score matrix
    t_matrix = df.pivot(
        index='locusId',
        columns='expName',
        values='t'
    )

    # Save
    fit_matrix.to_csv(f'{output_prefix}_fitness_matrix.csv')
    t_matrix.to_csv(f'{output_prefix}_t_matrix.csv')

    print(f"Fitness matrix shape: {fit_matrix.shape}")
    print(f"T-score matrix shape: {t_matrix.shape}")

    return fit_matrix, t_matrix

# Create for E. coli
fit_mat, t_mat = create_fitness_matrix(conn, 'Keio', 'Keio')
```

**Step 4.2**: Create Phenotype Classification Table
```python
def create_phenotype_table(conn, orgId, fit_threshold=2, t_threshold=4):
    """
    Create table classifying each gene-experiment pair as having phenotype or not
    """
    query = f"""
    SELECT
        g.locusId, g.sysName, g.gene, g.desc,
        e.expName, e.expDesc, e.expGroup, e.condition_1,
        gf.fit, gf.t,
        CASE
            WHEN ABS(gf.fit) > {fit_threshold} AND ABS(gf.t) > {t_threshold}
            THEN 1 ELSE 0
        END as has_phenotype,
        CASE
            WHEN gf.fit < -{fit_threshold} AND gf.t < -{t_threshold}
            THEN 'negative'
            WHEN gf.fit > {fit_threshold} AND gf.t > {t_threshold}
            THEN 'positive'
            ELSE 'none'
        END as phenotype_type
    FROM Gene g
    JOIN GeneFitness gf ON g.orgId = gf.orgId AND g.locusId = gf.locusId
    JOIN Experiment e ON gf.orgId = e.orgId AND gf.expName = e.expName
    WHERE g.orgId = '{orgId}' AND g.type = 1
    """
    df = pd.read_sql_query(query, conn)

    # Add classification details
    df['is_strong_negative'] = (df['fit'] < -fit_threshold) & (df['t'] < -t_threshold)
    df['is_strong_positive'] = (df['fit'] > fit_threshold) & (df['t'] > t_threshold)

    return df

# Create for E. coli
keio_phenotypes = create_phenotype_table(conn, 'Keio')
keio_phenotypes.to_csv('Keio_phenotype_classifications.csv', index=False)

# Summary statistics
print(f"Total gene-experiment pairs: {len(keio_phenotypes)}")
print(f"With significant phenotype: {keio_phenotypes['has_phenotype'].sum()}")
print(f"Phenotype rate: {100*keio_phenotypes['has_phenotype'].mean():.1f}%")
```

**Step 4.3**: Create Per-Gene Phenotype Summary
```python
def create_gene_summary(conn, orgId):
    """
    Summarize phenotypes per gene across all experiments
    """
    query = f"""
    SELECT
        g.locusId, g.sysName, g.gene, g.desc,
        COUNT(gf.expName) as n_experiments,
        SUM(CASE WHEN ABS(gf.fit) > 2 AND ABS(gf.t) > 4 THEN 1 ELSE 0 END) as n_phenotypes,
        MIN(gf.fit) as min_fit,
        MAX(gf.fit) as max_fit,
        AVG(ABS(gf.fit)) as avg_abs_fit,
        MAX(ABS(gf.t)) as max_abs_t
    FROM Gene g
    LEFT JOIN GeneFitness gf ON g.orgId = gf.orgId AND g.locusId = gf.locusId
    WHERE g.orgId = '{orgId}' AND g.type = 1
    GROUP BY g.locusId
    """
    df = pd.read_sql_query(query, conn)

    # Calculate phenotype rate
    df['phenotype_rate'] = df['n_phenotypes'] / df['n_experiments']

    # Classify genes
    df['has_any_phenotype'] = df['n_phenotypes'] > 0
    df['has_frequent_phenotypes'] = df['phenotype_rate'] > 0.1
    df['possibly_essential'] = (df['min_fit'] < -2) & (df['phenotype_rate'] > 0.5)

    return df

gene_summary = create_gene_summary(conn, 'Keio')
gene_summary.to_csv('Keio_gene_summary.csv', index=False)

# Show interesting genes
print("Genes with phenotypes in >50% of experiments:")
print(gene_summary[gene_summary['phenotype_rate'] > 0.5].sort_values('phenotype_rate', ascending=False).head(20))
```

#### Phase 5: Build Confusion Matrix Data (1-2 hours)

**Step 5.1**: Extract Ortholog Relationships
```python
# Get ortholog pairs with fitness data
orthologs = pd.read_sql_query("""
    SELECT
        o.orgId1, o.locusId1,
        o.orgId2, o.locusId2,
        o.ratio as ortholog_score,
        g1.gene as gene1, g1.desc as desc1,
        g2.gene as gene2, g2.desc as desc2
    FROM Ortholog o
    JOIN Gene g1 ON o.orgId1 = g1.orgId AND o.locusId1 = g1.locusId
    JOIN Gene g2 ON o.orgId2 = g2.orgId AND o.locusId2 = g2.locusId
    WHERE o.ratio > 0.5  -- good ortholog match
""", conn)

print(f"Total ortholog pairs: {len(orthologs)}")
orthologs.to_csv('ortholog_pairs.csv', index=False)
```

**Step 5.2**: Create Confusion Matrix for Ortholog Phenotype Conservation
```python
def create_ortholog_confusion_matrix(conn, orgId1, orgId2, condition):
    """
    Compare phenotypes between orthologs in same condition
    """
    query = f"""
    SELECT
        o.locusId1, o.locusId2,
        gf1.fit as fit1, gf1.t as t1,
        gf2.fit as fit2, gf2.t as t2,
        e.condition_1
    FROM Ortholog o
    JOIN GeneFitness gf1 ON o.orgId1 = gf1.orgId AND o.locusId1 = gf1.locusId
    JOIN GeneFitness gf2 ON o.orgId2 = gf2.orgId AND o.locusId2 = gf2.locusId
    JOIN Experiment e ON gf1.expName = e.expName AND gf1.orgId = e.orgId
    WHERE o.orgId1 = '{orgId1}'
        AND o.orgId2 = '{orgId2}'
        AND e.condition_1 = '{condition}'
        AND o.ratio > 0.5
    """
    df = pd.read_sql_query(query, conn)

    # Classify phenotypes
    df['pheno1'] = (df['fit1'].abs() > 2) & (df['t1'].abs() > 4)
    df['pheno2'] = (df['fit2'].abs() > 2) & (df['t2'].abs() > 4)

    # Create confusion matrix
    from sklearn.metrics import confusion_matrix, classification_report

    cm = confusion_matrix(df['pheno2'], df['pheno1'])
    report = classification_report(df['pheno2'], df['pheno1'])

    print(f"Ortholog phenotype conservation: {orgId1} vs {orgId2} in {condition}")
    print(f"Confusion Matrix:")
    print(cm)
    print(f"\nClassification Report:")
    print(report)

    return df, cm

# Example: Compare E. coli vs. P. simiae in glucose
ortholog_data, cm = create_ortholog_confusion_matrix(
    conn, 'Keio', 'WCS417', 'D-glucose'
)
```

**Step 5.3**: Create Confusion Matrix for All Genomes/Conditions
```python
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
import numpy as np

def create_comprehensive_confusion_matrix(conn, fit_threshold=2, t_threshold=4):
    """
    Create confusion matrix for phenotype conservation across all ortholog pairs
    """
    # Get all ortholog pairs with fitness in matching experiments
    query = f"""
    SELECT
        o.orgId1, o.locusId1,
        o.orgId2, o.locusId2,
        e1.condition_1,
        gf1.fit as fit1, gf1.t as t1,
        gf2.fit as fit2, gf2.t as t2
    FROM Ortholog o
    JOIN GeneFitness gf1 ON o.orgId1 = gf1.orgId AND o.locusId1 = gf1.locusId
    JOIN GeneFitness gf2 ON o.orgId2 = gf2.orgId AND o.locusId2 = gf2.locusId
    JOIN Experiment e1 ON gf1.orgId = e1.orgId AND gf1.expName = e1.expName
    JOIN Experiment e2 ON gf2.orgId = e2.orgId AND gf2.expName = e2.expName
    WHERE o.ratio > 0.5
        AND e1.condition_1 = e2.condition_1
        AND e1.expGroup = e2.expGroup
    """

    print("Executing large query... may take several minutes")
    df = pd.read_sql_query(query, conn)

    print(f"Retrieved {len(df)} ortholog-condition pairs")

    # Classify phenotypes
    df['has_pheno1'] = (df['fit1'].abs() > fit_threshold) & (df['t1'].abs() > t_threshold)
    df['has_pheno2'] = (df['fit2'].abs() > fit_threshold) & (df['t2'].abs() > t_threshold)

    # Prediction: if organism1 has phenotype, predict organism2 has phenotype
    y_true = df['has_pheno2']
    y_pred = df['has_pheno1']

    # Calculate confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()

    # Calculate metrics
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    accuracy = (tp + tn) / (tp + tn + fp + fn)

    # Print results
    print("\n" + "="*50)
    print("COMPREHENSIVE CONFUSION MATRIX")
    print("All Genomes Across All Conditions")
    print("="*50)
    print(f"\nTotal ortholog-condition pairs analyzed: {len(df)}")
    print(f"\nConfusion Matrix:")
    print(f"                 Predicted No  Predicted Yes")
    print(f"Actual No        {tn:>12}  {fp:>13}")
    print(f"Actual Yes       {fn:>12}  {tp:>13}")

    print(f"\nMetrics:")
    print(f"True Positives:  {tp:>8} ({100*tp/len(df):.1f}%)")
    print(f"True Negatives:  {tn:>8} ({100*tn/len(df):.1f}%)")
    print(f"False Positives: {fp:>8} ({100*fp/len(df):.1f}%)")
    print(f"False Negatives: {fn:>8} ({100*fn/len(df):.1f}%)")

    print(f"\nPrecision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print(f"F1-Score:  {f1:.3f}")
    print(f"Accuracy:  {accuracy:.3f}")

    # Save results
    results = {
        'confusion_matrix': cm,
        'tn': tn, 'fp': fp, 'fn': fn, 'tp': tp,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'accuracy': accuracy,
        'n_pairs': len(df)
    }

    # Save detailed data
    df.to_csv('ortholog_confusion_matrix_data.csv', index=False)

    return results, df

# Run comprehensive analysis
results, ortholog_cm_data = create_comprehensive_confusion_matrix(conn)
```

#### Phase 6: Additional Analyses (Optional)

**Step 6.1**: Cofitness Analysis
```python
# Get top cofit genes
cofit = pd.read_sql_query("""
    SELECT
        c.orgId, c.locusId, c.hitId,
        c.rank, c.cofit,
        g1.gene as gene1, g1.desc as desc1,
        g2.gene as gene2, g2.desc as desc2
    FROM Cofit c
    JOIN Gene g1 ON c.orgId = g1.orgId AND c.locusId = g1.locusId
    JOIN Gene g2 ON c.orgId = g2.orgId AND c.hitId = g2.locusId
    WHERE c.cofit > 0.75 AND c.rank <= 5
    ORDER BY c.orgId, c.locusId, c.rank
""", conn)

cofit.to_csv('top_cofit_genes.csv', index=False)
```

**Step 6.2**: Condition-Specific Phenotypes
```python
# Find genes specific to carbon sources
carbon_specific = pd.read_sql_query("""
    SELECT
        g.orgId, g.locusId, g.gene, g.desc,
        e.condition_1,
        AVG(gf.fit) as avg_fit,
        AVG(gf.t) as avg_t,
        COUNT(*) as n_experiments
    FROM Gene g
    JOIN GeneFitness gf ON g.orgId = gf.orgId AND g.locusId = gf.locusId
    JOIN Experiment e ON gf.orgId = e.orgId AND gf.expName = e.expName
    WHERE e.expGroup = 'carbon source'
        AND ABS(gf.fit) > 2
        AND ABS(gf.t) > 4
    GROUP BY g.orgId, g.locusId, e.condition_1
    HAVING COUNT(*) >= 1
    ORDER BY g.orgId, ABS(avg_fit) DESC
""", conn)

carbon_specific.to_csv('carbon_source_specific_phenotypes.csv', index=False)
```

### 2. Complete Python Script Template

```python
#!/usr/bin/env python3
"""
FIT Fitness Browser Data Extraction and Analysis
Complete workflow for extracting and analyzing fitness data
"""

import sqlite3
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

class FITAnalyzer:
    """Class for analyzing FIT Fitness Browser data"""

    def __init__(self, db_path='feba.db'):
        """Initialize connection to database"""
        self.conn = sqlite3.connect(db_path)
        print(f"Connected to {db_path}")

    def get_organisms(self):
        """Get list of all organisms"""
        return pd.read_sql_query(
            "SELECT * FROM Organism ORDER BY genus, species",
            self.conn
        )

    def get_gene_fitness(self, orgId):
        """Get all fitness data for one organism"""
        query = f"""
        SELECT g.locusId, g.sysName, g.gene, g.desc,
               e.expName, e.expDesc, e.condition_1,
               gf.fit, gf.t
        FROM Gene g
        JOIN GeneFitness gf ON g.orgId = gf.orgId AND g.locusId = gf.locusId
        JOIN Experiment e ON gf.orgId = e.orgId AND gf.expName = e.expName
        WHERE g.orgId = '{orgId}' AND g.type = 1
        """
        return pd.read_sql_query(query, self.conn)

    def create_fitness_matrix(self, orgId):
        """Create gene × experiment matrix"""
        query = f"""
        SELECT locusId, expName, fit
        FROM GeneFitness
        WHERE orgId = '{orgId}'
        """
        df = pd.read_sql_query(query, self.conn)
        return df.pivot(index='locusId', columns='expName', values='fit')

    def classify_phenotypes(self, orgId, fit_threshold=2, t_threshold=4):
        """Classify all gene-experiment pairs"""
        df = self.get_gene_fitness(orgId)
        df['has_phenotype'] = (df['fit'].abs() > fit_threshold) & (df['t'].abs() > t_threshold)
        return df

    def confusion_matrix_orthologs(self, orgId1, orgId2):
        """Create confusion matrix for ortholog phenotypes"""
        query = f"""
        SELECT
            o.locusId1, o.locusId2,
            gf1.fit as fit1, gf1.t as t1,
            gf2.fit as fit2, gf2.t as t2
        FROM Ortholog o
        JOIN GeneFitness gf1 ON o.orgId1 = gf1.orgId AND o.locusId1 = gf1.locusId
        JOIN GeneFitness gf2 ON o.orgId2 = gf2.orgId AND o.locusId2 = gf2.locusId
        WHERE o.orgId1 = '{orgId1}' AND o.orgId2 = '{orgId2}'
            AND o.ratio > 0.5
        """
        df = pd.read_sql_query(query, self.conn)

        df['pheno1'] = (df['fit1'].abs() > 2) & (df['t1'].abs() > 4)
        df['pheno2'] = (df['fit2'].abs() > 2) & (df['t2'].abs() > 4)

        cm = confusion_matrix(df['pheno2'], df['pheno1'])
        return cm, df

    def close(self):
        """Close database connection"""
        self.conn.close()

# Usage example
if __name__ == "__main__":
    # Initialize
    analyzer = FITAnalyzer('feba.db')

    # Get organisms
    orgs = analyzer.get_organisms()
    print(f"Found {len(orgs)} organisms")

    # Analyze E. coli
    print("\nAnalyzing E. coli...")
    keio_fitness = analyzer.get_gene_fitness('Keio')
    print(f"E. coli measurements: {len(keio_fitness)}")

    # Create matrix
    fit_matrix = analyzer.create_fitness_matrix('Keio')
    print(f"Fitness matrix shape: {fit_matrix.shape}")

    # Classify phenotypes
    phenotypes = analyzer.classify_phenotypes('Keio')
    print(f"Phenotype rate: {100*phenotypes['has_phenotype'].mean():.1f}%")

    # Save results
    phenotypes.to_csv('Keio_phenotypes.csv', index=False)
    fit_matrix.to_csv('Keio_fitness_matrix.csv')

    # Close
    analyzer.close()
    print("\nAnalysis complete!")
```

### 3. Recommended Tools and Languages

**Python** (Recommended):
- pandas: Data manipulation
- sqlite3: Database queries
- scikit-learn: Confusion matrices, metrics
- numpy: Numerical operations
- matplotlib/seaborn: Visualization

**R** (Alternative):
- RSQLite: Database access
- dplyr: Data manipulation
- tidyr: Reshaping data
- ggplot2: Visualization

**Command-line**:
- sqlite3: Quick queries
- csvkit: CSV manipulation

### 4. Performance Optimization Tips

**For Large Queries**:
1. Filter by orgId first (most selective)
2. Use LIMIT for testing
3. Create temporary tables for multi-step analyses
4. Use indexes (already present in database)
5. Process one organism at a time

**Memory Management**:
```python
# Use chunking for very large queries
def query_in_chunks(conn, query, chunksize=10000):
    offset = 0
    while True:
        chunk_query = f"{query} LIMIT {chunksize} OFFSET {offset}"
        df = pd.read_sql_query(chunk_query, conn)
        if len(df) == 0:
            break
        yield df
        offset += chunksize

# Usage
for chunk in query_in_chunks(conn, "SELECT * FROM GeneFitness"):
    process(chunk)
```

### 5. Potential Pitfalls and Solutions

**Pitfall 1**: Running out of memory
- **Solution**: Process one organism at a time, use chunking

**Pitfall 2**: Slow queries
- **Solution**: Always filter by orgId, use indexes, avoid SELECT *

**Pitfall 3**: Missing data in joins
- **Solution**: Use LEFT JOIN to keep all records, check for NULLs

**Pitfall 4**: Confused about identifier formats
- **Solution**: orgId:locusId is unique, use both in joins

**Pitfall 5**: Not accounting for quality metrics
- **Solution**: Filter by |t| > 4, check mad12 for experiments

## Related Research

- Part 1: Database schema and structure
- Part 2: Data extraction and downloads
- Part 3: Phenotype classification and confusion matrix

## Next Steps

1. Download feba.db from Figshare
2. Run verification scripts
3. Extract data for your specific organisms
4. Create custom tables
5. Build confusion matrices
6. Visualize results
7. Iterate based on findings
