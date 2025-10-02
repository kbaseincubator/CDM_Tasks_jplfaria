# Understanding Statistical Thresholds in FIT

**Purpose**: Explain what the statistical thresholds mean and why they're used

## What is FDR (False Discovery Rate)?

### The Problem

When you test **thousands of genes** across **hundreds of experiments**, you're doing millions of statistical tests. Some will appear "significant" just by random chance.

**Example**:
- E. coli: 4,000 genes
- Tested in 300 experiments
- Total tests: **1,200,000**

If you use a standard p-value threshold of 0.05 (5%), you'd expect:
- 1,200,000 × 0.05 = **60,000 false positives** just by chance!

### The Solution: False Discovery Rate

**FDR** controls the proportion of false discoveries among your significant results.

**FDR < 2%** means:
- Of all genes you call "significant", less than 2% are expected to be false positives
- If you find 1,000 significant genes, ~20 might be false discoveries
- The other 980 are likely real phenotypes

### How FIT Achieves FDR < 2%

**Standard approach**: |t-score| > 2 (p-value ~0.05)

**FIT approach**: |t-score| > 4

**Why stricter?**
- More tests = need stricter threshold
- |t| > 4 roughly corresponds to p-value < 0.0001
- Much lower chance of false positives

**Source**: Wetmore et al., mBio 2015
> "We usually ignore any fitness effects with |t| < 4"

## Fitness Value Thresholds

### What is a Fitness Value?

**Formula**: fitness = log₂(abundance_end / abundance_beginning)

**Interpretation**:
- fitness = 0: No change (mutants grew normally)
- fitness = -1: Mutants half as abundant (2^-1 = 0.5)
- fitness = -2: Mutants 1/4 as abundant (2^-2 = 0.25)
- fitness = -4: Mutants 1/16 as abundant (2^-4 = 0.0625)
- fitness = +2: Mutants 4× as abundant (2^2 = 4)

### Why fitness < -2 or > 2 for "Strong Fitness Effect"?

**Biological significance**:
- |fitness| > 2 = 4-fold change in abundance
- This is a large, biologically meaningful effect
- Easier to interpret and validate

**Comparison**:
- fitness = -1: 2-fold change (subtle, might be noise)
- fitness = -2: 4-fold change (clear phenotype)
- fitness = -4: 16-fold change (strong phenotype)

### Conditionally Essential: fitness = -4 to -8

**Logic**:
- Typical experiment: cells double 4-8 times
- If gene is essential, mutants can't grow at all
- Expected fitness = -(number of doublings)

**Example**:
- Experiment with 6 doublings
- Essential gene mutants don't grow
- Wild-type grows 2^6 = 64-fold
- Mutants stay same (or die)
- fitness = log₂(1/64) = **-6**

**Source**: FIT Help page
> "In typical experiments where the pool doubles 4-8 times, conditionally essential genes should have fitness of -4 to -8"

## Quality Metrics

### mad12 (Median Absolute Difference between gene halves)

**What it measures**:
- Split each gene into two halves: positions 10-50% and 50-90%
- Calculate fitness from insertions in each half separately
- mad12 = median |fitness_half1 - fitness_half2|

**Why it matters**:
- If data is good quality, both halves should give similar fitness
- High mad12 = noisy data or biological effect within gene
- **Threshold: mad12 ≤ 0.5** for good experiments

**Example**:
- Gene A: half1 = -2.1, half2 = -2.3, difference = 0.2 ✓
- Gene B: half1 = -3.5, half2 = +1.2, difference = 4.7 ✗ (noisy!)

**Performance**:
- 89 of 92 experiments (97%) passed mad12 ≤ 0.5
- This became standard quality metric

**Source**: Wetmore et al., mBio 2015

### Replicate Correlation

**What it measures**:
- Biological replicates = same experiment done twice independently
- Correlation = how similar are the fitness values?

**Observed performance**:
- **Median: 0.92** (very high reproducibility)
- Range: 0.79 to 0.97
- This is not a threshold, but evidence the method works well

**What good correlation means**:
- 0.92 = 92% of variance explained
- Very reproducible results
- Confidence in the data

## Combined Thresholds

### Identifying Significant Phenotypes

**Recommended criteria**:
```
Significant phenotype = |fitness| > 2 AND |t| > 4
```

**Why both?**:
- |fitness| > 2: Biologically meaningful (4-fold change)
- |t| > 4: Statistically significant (FDR < 2%)

**Example classifications**:

| Gene | fitness | t | Has phenotype? | Reason |
|------|---------|---|----------------|--------|
| geneA | -3.5 | 8.2 | **YES** | Strong effect, highly significant |
| geneB | -2.1 | 2.3 | NO | Significant effect but low t-score |
| geneC | -0.8 | 6.1 | NO | Significant but weak effect |
| geneD | -1.2 | 2.1 | NO | Weak and not significant |

### Strong Positive Selection (Highest Confidence)

**Criteria** (from Nature 2018 supplementary):
- fitness > 2
- t > 5
- Standard error < 1
- Mean reads ≥ 10
- fitness ≥ max(fitness in experiment) - 8

**When to use**: Very conservative, highest confidence results

## Practical Guidelines

### For Exploratory Analysis
- Use |t| > 4 as primary filter
- Look at |fitness| > 2 for strong effects
- Check mad12 for experiment quality

### For High-Confidence Results
- Use both |fitness| > 2 AND |t| > 4
- Check for replicate agreement
- Verify in multiple related conditions

### For Publication-Quality
- Apply strong positive selection criteria
- Validate with independent methods
- Check ortholog conservation

## Summary Table

| Metric | Threshold | Meaning | Source |
|--------|-----------|---------|--------|
| **t-score** | \|t\| > 4 | Statistically significant, FDR < 2% | mBio 2015 |
| **Fitness** | \|fit\| > 2 | Biologically significant, 4-fold change | FIT Help |
| **Combined** | Both above | Recommended for phenotype calling | Standard practice |
| **mad12** | ≤ 0.5 | Good experiment quality | mBio 2015 |
| **Replicate correlation** | ~0.92 | Expected reproducibility | mBio 2015 |
| **Conditionally essential** | fit = -4 to -8 | Gene required for growth | FIT Help |

## References

1. Wetmore KM, Price MN, Waters RJ, et al. (2015). "Rapid quantification of mutant fitness in diverse bacteria by sequencing randomly barcoded transposons." mBio 6(3):e00306-15. DOI: 10.1128/mBio.00306-15

2. Price MN, Wetmore KM, Waters RJ, et al. (2018). "Mutant phenotypes for thousands of bacterial genes of unknown function." Nature 557:503-509. DOI: 10.1038/s41586-018-0124-0

3. FIT Help Page: https://fit.genomics.lbl.gov/cgi-bin/help.cgi
