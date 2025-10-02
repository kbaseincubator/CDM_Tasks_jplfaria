# FIT Fitness Browser - Documentation

**Purpose**: Educational documentation explaining key concepts for working with FIT fitness data

## Overview

This directory contains detailed explanations of core concepts needed to understand and analyze data from the FIT (Fitness Browser) at https://fit.genomics.lbl.gov. Each document focuses on a specific topic and provides examples.

## Documents

### 01. Understanding Statistical Thresholds
**File**: `01-understanding-statistical-thresholds.md`

**Topics**:
- What is FDR (False Discovery Rate)?
- Why |t| > 4 threshold? (not the usual |t| > 2)
- Fitness value thresholds (|fit| > 2)
- Quality metrics (mad12, replicate correlation)
- Conditionally essential genes

**Read this if**: You want to know where the thresholds come from and what they mean

### 02. Project Objective: Confusion Matrix Analysis
**File**: `02-project-objective-confusion-matrix.md`

**Topics**:
- Project workflow: Experimental growth → Metabolic models → In silico predictions → Confusion matrix
- Comparing experimental FIT data vs computational metabolic model predictions
- What the confusion matrix means for this project (TP/TN/FP/FN definitions)
- Missing data interpretation (not tested vs no growth)
- Evaluation metrics for model validation

**Read this if**: You want to understand the overall project objective and workflow

### 03. Understanding Fitness Values
**File**: `03-understanding-fitness-values.md`

**Topics**:
- What is a fitness value?
- How to interpret positive vs. negative fitness
- Why use log₂?
- Context: number of generations matters
- Strain-level vs. gene-level fitness
- When to trust a fitness value

**Read this if**: You want to understand what the numbers mean biologically

### 04. Cofitness and Functional Relationships
**File**: `04-cofitness-functional-relationships.md`

**Topics**:
- What is cofitness?
- Cofitness thresholds (> 0.75, conserved > 0.6)
- How to use cofitness to predict gene function
- Cofit and ConservedCofit tables
- Network analysis
- Limitations and best practices

**Read this if**: You want to use cofitness to predict gene functions or find functionally related genes

### 05. Growth/No-Growth Matrix Construction
**File**: `05-growth-no-growth-matrix.md`

**Topics**:
- Interpreting missing data in FIT (not tested vs failed to grow)
- Evidence that missing data = "not tested" not "no growth"
- How to build organism × condition growth matrix
- Quality filters to apply
- Conservative vs permissive approaches
- Coverage statistics and sparsity

**Read this if**: You need to extract growth/no-growth data for metabolic model validation

## Quick Reference

### Key Thresholds

| Metric | Threshold | Meaning | Source |
|--------|-----------|---------|--------|
| **T-score** | \|t\| > 4 | Statistically significant, FDR < 2% | mBio 2015 |
| **Fitness** | \|fit\| > 2 | Biologically significant, 4-fold change | FIT Help |
| **Phenotype** | \|fit\| > 2 AND \|t\| > 4 | Recommended for calling phenotypes | Standard |
| **mad12** | ≤ 0.5 | Good experiment quality | mBio 2015 |
| **Cofitness** | > 0.75 | Likely same pathway | FIT analysis |
| **Conserved cofit** | > 0.6 (both species) | High-confidence functional relationship | Nature 2018 |

### Fitness Value Interpretation

| Fitness | Fold-change | Meaning |
|---------|-------------|---------|
| +3 | 8× | Very strong advantage (gene detrimental) |
| +2 | 4× | Strong advantage |
| +1 | 2× | Moderate advantage |
| 0 | 1× | No phenotype |
| -1 | 0.5× | Moderate disadvantage (gene beneficial) |
| -2 | 0.25× | Strong disadvantage |
| -4 | 0.0625× | Very strong disadvantage (near-essential) |
| -6 | 0.016× | Essential in this condition |

### Confusion Matrix Components

```
                    Actual
                Yes         No
Predicted  Yes   TP         FP      Precision = TP/(TP+FP)
           No    FN         TN      Recall = TP/(TP+FN)

Accuracy = (TP+TN)/Total
F1 = 2 × (Precision × Recall)/(Precision + Recall)
```

## Related Documentation

### For Detailed Technical Information:
- `/thoughts/shared/research/` - Comprehensive research documents
  - Database schema and structure
  - Data extraction methods
  - Practical extraction plan with code

### For Quick Start:
- `/thoughts/shared/research/README.md` - Overview and quick start guide

### For Reference Data:
- `/references/FIT_Fitness_Browser_Comprehensive_Review.md` - Initial comprehensive overview

## Key Publications

1. **Wetmore et al., mBio 2015**
   - "Rapid quantification of mutant fitness in diverse bacteria by sequencing randomly barcoded transposons"
   - DOI: 10.1128/mBio.00306-15
   - **Key paper**: Defines RB-TnSeq methodology and statistical thresholds

2. **Price et al., Nature 2018**
   - "Mutant phenotypes for thousands of bacterial genes of unknown function"
   - DOI: 10.1038/s41586-018-0124-0
   - **Key paper**: Describes 11,779 genes characterized, conserved cofitness

3. **Price et al., Database 2024**
   - "Interactive tools for functional annotation of bacterial genomes"
   - DOI: 10.1093/database/baae089
   - **Key paper**: Describes all integrated tools (PaperBLAST, GapMind, etc.)

## Glossary

**Cofitness**: Correlation of fitness patterns across conditions; high cofitness suggests genes work together

**Essential gene**: Gene required for growth; mutants cannot survive

**FDR (False Discovery Rate)**: Proportion of false positives among significant results

**Fitness**: Log₂ ratio of mutant abundance at end vs. beginning of experiment

**mad12**: Median absolute difference between fitness calculated from first vs. second half of genes; measures data quality

**Ortholog**: Corresponding gene in different species (arose from common ancestor)

**Phenotype**: Observable change in mutant growth; gene has phenotype if |fit| > 2 and |t| > 4

**RB-TnSeq**: Random Barcode Transposon Sequencing; method for high-throughput fitness measurement

**T-statistic**: Measure of statistical confidence; accounts for variability; |t| > 4 recommended

## Questions?

If you have questions about these concepts:
1. Check the relevant documentation file
2. Look in the detailed research documents in `/thoughts/shared/research/`
3. Consult the FIT Help page: https://fit.genomics.lbl.gov/cgi-bin/help.cgi
4. Read the original publications

## Contributing

These documents are living documentation. If you find errors or have suggestions for improvement, please update them!
