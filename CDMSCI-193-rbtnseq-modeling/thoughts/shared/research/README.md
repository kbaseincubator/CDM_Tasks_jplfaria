# FIT Fitness Browser Research Documentation

**Date**: 2025-10-01
**Researcher**: Jose P. Faria
**Project**: Comprehensive analysis of FIT Fitness Browser for data extraction and confusion matrix analysis

## Overview

This directory contains comprehensive research documentation for the FIT (Fitness Browser) genomics resource at https://fit.genomics.lbl.gov/cgi-bin/myFrontPage.cgi. The research covers database structure, data extraction methods, phenotype classification, and practical implementation strategies.

## Research Documents

### Part 1: Database Schema and Structure
**File**: `2025-10-01-FIT-database-schema-structure.md`

**Contents**:
- Complete SQLite database schema (39 tables)
- Core tables: Organism, Gene, GeneFitness, Experiment
- Table relationships and join patterns
- Identifier formats and conventions
- External data files (db.StrainFitness)

**Key Findings**:
- feba.db is ~5 GB SQLite3 database
- GeneFitness table: orgId, locusId, expName, fit, t
- 48 organisms, ~168,000 genes, 7,552 experiments

### Part 2: Data Extraction and Downloads
**File**: `2025-10-01-FIT-data-extraction-downloads.md`

**Contents**:
- Figshare releases (primary download method)
- Direct downloads from fit.genomics.lbl.gov
- BigFit supplemental data (84 GB complete dataset)
- Per-organism downloads
- Programmatic access via SQLite
- URL-based queries (CGI scripts)
- Batch download strategies

**Key Findings**:
- February 2024 release: https://figshare.com/articles/dataset/25236931
- Files: feba.db, aaseqs, db.StrainFitness.*, code.tar
- Python/R code examples for querying database

### Part 3: Phenotype Classification and Confusion Matrix
**File**: `2025-10-01-FIT-phenotype-classification-confusion-matrix.md`

**Contents**:
- Phenotype definition and classification criteria
- Statistical significance thresholds (|t| > 4)
- Quality metrics for experiments
- Dataset scale: "all genomes across all conditions"
- Multiple confusion matrix interpretations
- Cofitness thresholds
- Statistical methods from source code

**Key Findings**:
- Significant phenotype: |fitness| > 2 AND |t| > 4
- Dataset: 500K-1M gene-experiment measurements
- Confusion matrix interpretations:
  1. Gene essentiality prediction (75-81% AUC)
  2. Function prediction from fitness (39.7% accuracy)
  3. Ortholog phenotype conservation
  4. Regulatory prediction validation
  5. Replicate agreement

### Part 4: Practical Extraction Plan
**File**: `2025-10-01-FIT-practical-extraction-plan.md`

**Contents**:
- Step-by-step extraction workflow
- Phase 1: Download and setup
- Phase 2: Explore data
- Phase 3: Extract core data
- Phase 4: Create custom tables
- Phase 5: Build confusion matrices
- Phase 6: Additional analyses
- Complete Python script template (FITAnalyzer class)
- Performance optimization tips
- Pitfalls and solutions

**Key Findings**:
- Recommended workflow using Python + pandas + SQLite
- Code examples for all major tasks
- Memory management and optimization strategies

## Quick Start Guide

### 1. Download Database
```bash
wget https://figshare.com/ndownloader/files/44580544 -O fit_data.tar.gz
tar -xzf fit_data.tar.gz
gunzip feba.db.gz
```

### 2. Verify Database
```python
import sqlite3
conn = sqlite3.connect('feba.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM Organism")
print(f"Organisms: {cursor.fetchone()[0]}")
```

### 3. Extract Data
```python
import pandas as pd
query = """
SELECT g.orgId, g.locusId, g.desc, gf.fit, gf.t, e.expDesc
FROM GeneFitness gf
JOIN Gene g ON gf.orgId = g.orgId AND gf.locusId = gf.locusId
JOIN Experiment e ON gf.orgId = e.orgId AND gf.expName = e.expName
WHERE ABS(gf.fit) > 2 AND ABS(gf.t) > 4
LIMIT 100
"""
df = pd.read_sql_query(query, conn)
```

## Key Resources

### Primary Data Source
- **Main website**: https://fit.genomics.lbl.gov/
- **Help page**: https://fit.genomics.lbl.gov/cgi-bin/help.cgi
- **Figshare (Feb 2024)**: https://figshare.com/articles/dataset/25236931
- **BigFit supplement**: https://genomics.lbl.gov/supplemental/bigfit/
- **Source code**: https://bitbucket.org/berkeleylab/feba

### Publications
- **Nature 2018**: Price et al. "Mutant phenotypes for thousands of bacterial genes of unknown function" (DOI: 10.1038/s41586-018-0124-0)
- **mBio 2015**: Wetmore et al. "Rapid quantification of mutant fitness" (DOI: 10.1128/mBio.00306-15)

### Additional Documentation
- Initial review: `/references/FIT_Fitness_Browser_Comprehensive_Review.md`
- Database schema: `lib/db_setup_tables.sql` in source code

## Dataset Summary

| Metric | Value |
|--------|-------|
| Organisms | 48 (46 bacteria + 2 archaea) |
| Genes | ~168,000 total (3,500-4,500 per organism) |
| Experiments | 7,552 (Feb 2024) |
| Gene-Experiment Pairs | 500,000-1,000,000 |
| Database Size | ~5 GB (SQLite3) |
| License | Creative Commons Attribution 4.0 |

## Phenotype Thresholds

| Classification | Criteria |
|----------------|----------|
| Significant phenotype | \|fitness\| > 2 AND \|t\| > 4 |
| Strong positive selection | fitness > 2, t > 5, SE < 1, reads ≥ 10 |
| Conditionally essential | fitness < -2 in most conditions |
| High cofitness | cofitness > 0.75 |
| Conserved cofitness | cofitness > 0.6 in both organisms |

## Confusion Matrix Applications

Based on literature review, the most likely interpretations for "confusion matrix for all genomes across all conditions":

1. **Gene Essentiality**: Predict essential vs. non-essential genes
2. **Function Prediction**: Predict gene function from fitness patterns
3. **Ortholog Conservation**: Predict phenotype conservation across species
4. **Regulatory Validation**: Validate TF-target predictions via cofitness
5. **Replicate Agreement**: Compare biological replicate experiments

## Next Steps

1. **Clarify Requirements**: Determine which confusion matrix interpretation your boss wants
2. **Download Data**: Get feba.db from Figshare (5 GB)
3. **Explore Database**: Run verification and exploration scripts
4. **Extract Data**: Create gene × experiment matrices
5. **Build Confusion Matrix**: Implement chosen approach
6. **Validate Results**: Check against literature benchmarks
7. **Document**: Create visualizations and summary reports

## Contact

For questions about this research documentation, contact the researcher or refer to the FIT help page.

## License

This research documentation is provided for educational and research purposes. The FIT Fitness Browser data is licensed under Creative Commons Attribution 4.0.
