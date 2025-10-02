# Understanding Fitness Values in RB-TnSeq

**Purpose**: Explain what fitness values mean and how to interpret them

## What is a Fitness Value?

### The Concept

**Fitness** measures how well a mutant grows compared to the overall population.

**Key idea**:
- Start with pool of thousands of mutants
- Grow under specific condition
- Sequence barcodes to count each mutant
- Compare end abundance to beginning abundance

### The Formula

**Basic formula**:
```
fitness = log₂(abundance_end / abundance_beginning)
```

**More precisely**:
```
fitness = log₂((reads_end + pseudocount) / (reads_beginning + pseudocount))
```

Where pseudocount is a "smart" adjustment based on gene-level fitness to reduce bias.

### Why Log₂?

**Reasons for logarithm**:
1. **Symmetry**: 2-fold increase and 2-fold decrease have equal magnitude
   - 2-fold increase: log₂(2) = +1
   - 2-fold decrease: log₂(0.5) = -1

2. **Interpretability**: Each unit represents a doubling or halving
   - fitness = 1 → 2× more abundant
   - fitness = 2 → 4× more abundant
   - fitness = 3 → 8× more abundant

3. **Linear with growth rate**: In exponential growth, log abundance is linear with time

## Interpreting Fitness Values

### Positive Fitness (fitness > 0)

**Meaning**: Mutants grew BETTER than average

**Interpretation**:
- Gene was detrimental to growth
- Deleting it provides an advantage
- Mutants are more abundant at end

**Examples**:
| fitness | Fold-change | Interpretation |
|---------|-------------|----------------|
| +0.5 | 1.4× | Small advantage |
| +1.0 | 2× | Mutants doubled relative to population |
| +2.0 | 4× | Strong advantage |
| +3.0 | 8× | Very strong advantage |

**Biological scenarios**:
- Metabolic burden: Gene product costs energy to make
- Toxic protein: Gene product inhibits growth
- Resource competition: Gene product sequesters limiting resource

### Negative Fitness (fitness < 0)

**Meaning**: Mutants grew WORSE than average

**Interpretation**:
- Gene was beneficial/required for growth
- Deleting it provides a disadvantage
- Mutants are less abundant at end

**Examples**:
| fitness | Fold-change | Interpretation |
|---------|-------------|----------------|
| -0.5 | 0.7× | Small disadvantage |
| -1.0 | 0.5× | Mutants halved relative to population |
| -2.0 | 0.25× | Strong disadvantage |
| -4.0 | 0.0625× | Very strong disadvantage, near-essential |
| -6.0 | 0.016× | Essential in this condition |

**Biological scenarios**:
- Required for nutrient utilization
- Stress resistance gene
- DNA repair, cell division, etc.

### Zero or Near-Zero Fitness (fitness ≈ 0)

**Meaning**: Mutants grew at SAME rate as population

**Interpretation**:
- Gene not important in this condition
- May be important in different condition
- May be redundant with other genes

## Context Matters: Number of Generations

### Why Generations Matter

**Key concept**: Expected fitness depends on how many times cells divided

**Formula**:
```
Expected fitness (if essential) = -(number of generations)
```

### Examples

**Experiment 1**: 4 generations of growth
- Wild-type grows: 2^4 = 16-fold
- Essential gene mutant: doesn't grow (1-fold)
- Expected fitness: log₂(1/16) = **-4**

**Experiment 2**: 8 generations of growth
- Wild-type grows: 2^8 = 256-fold
- Essential gene mutant: doesn't grow (1-fold)
- Expected fitness: log₂(1/256) = **-8**

### Why This Matters

**Same gene, different experiments**:
- Experiment A (4 generations): fitness = -4
- Experiment B (8 generations): fitness = -8
- **Same phenotype** (essential), different fitness values!

**Normalization**: When comparing across experiments with different generations:
```
normalized_fitness = fitness / n_generations
```

## Common Fitness Ranges

### Typical Values Observed

**Distribution**:
- Most genes: fitness ≈ 0 (no phenotype)
- Some genes: |fitness| = 0.5 to 2 (subtle phenotypes)
- Few genes: |fitness| > 2 (strong phenotypes)

**Example from E. coli in glucose minimal medium**:
- ~3,000 genes: fitness ≈ 0 (not important for glucose growth)
- ~500 genes: -2 < fitness < -0.5 (somewhat important)
- ~200 genes: fitness < -2 (very important)
- ~50 genes: fitness < -4 (essential or near-essential)

### Threshold Guidelines

| Category | fitness range | Meaning |
|----------|---------------|---------|
| **No phenotype** | -0.5 to +0.5 | Gene not important in this condition |
| **Subtle phenotype** | -1 to -0.5 or +0.5 to +1 | Minor growth defect/advantage |
| **Moderate phenotype** | -2 to -1 or +1 to +2 | Clear growth defect/advantage |
| **Strong phenotype** | < -2 or > +2 | Major growth defect/advantage |
| **Near-essential** | < -4 | Severe growth defect |
| **Essential** | < -6 in typical experiment | Cannot grow without this gene |

## Fitness vs. T-Statistic

### Why You Need Both

**Fitness**: Magnitude of effect (biological significance)
**T-statistic**: Confidence in measurement (statistical significance)

**Both are needed**:
- Large fitness but small t → Noisy, unreliable
- Large t but small fitness → Reliable but not biologically meaningful

### Examples

**Gene A**: fitness = -3.0, t = 8.5
- **Conclusion**: Strong, significant phenotype ✓

**Gene B**: fitness = -3.2, t = 1.8
- **Conclusion**: Looks strong, but unreliable (high variance)

**Gene C**: fitness = -0.8, t = 12.0
- **Conclusion**: Reliable measurement, but small effect

**Gene D**: fitness = -2.5, t = 4.5
- **Conclusion**: Significant phenotype ✓

### Recommended Thresholds

**For significant phenotype**:
```
|fitness| > 2 AND |t| > 4
```

**Why**:
- |fitness| > 2: Biologically meaningful (4-fold change)
- |t| > 4: Statistically confident (FDR < 2%)

## Special Cases

### Fitness Ceiling Effects

**Problem**: Can't measure fitness > ~4 or 5

**Reason**:
- If mutants grow much faster, they dominate the pool
- Eventually they're 100% of reads
- Can't get more abundant than 100%!

**Example**:
- Mutant is 1000× more abundant at end
- But pool is only 99% this mutant
- Observed: fitness = log₂(0.99/0.01) ≈ 6.6
- This is near the upper limit

### Fitness Floor Effects

**Problem**: Can't reliably measure very negative fitness

**Reason**:
- If mutants completely die, they have zero reads
- log₂(0) = -∞
- In practice, pseudocounts prevent this
- But very low abundance → noisy measurements

**Example**:
- Mutant has 2 reads at end, 1000 reads at beginning
- fitness = log₂(2/1000) = -8.97
- But with only 2 reads, this is unreliable
- High standard error, low t-statistic

### Partially Essential Genes

**Scenario**: Gene required but some growth possible

**Example**: DNA repair gene in UV stress
- Mutants grow slowly: 10% of wild-type rate
- 6 generations: wild-type → 64-fold, mutant → 6.4-fold
- fitness = log₂(6.4/64) = log₂(0.1) = **-3.3**

**Interpretation**: Not completely essential, but strongly required

## Strain-Level vs. Gene-Level Fitness

### Strain-Level Fitness

**Definition**: Fitness for each individual transposon insertion

**Characteristics**:
- Each barcode/insertion has its own fitness value
- Can be noisy (based on single insertion location)
- Stored in db.StrainFitness files

### Gene-Level Fitness

**Definition**: Average fitness across all insertions in a gene

**Calculation**: Weighted average
```
gene_fitness = Σ(weight[i] × strain_fitness[i]) / Σ(weight[i])
```

Where weight is based on read counts (higher reads → higher weight)

**Characteristics**:
- More reliable (averages out noise)
- Stored in GeneFitness table
- This is what's typically used for analysis

### Why They Differ

**Insertion location matters**:
- Insertion near gene start: might not disrupt function
- Insertion near gene end: might not disrupt function
- Insertion in middle: more likely to disrupt

**Example**:
- Gene has 10 insertions
- 8 insertions in middle: fitness ≈ -2.5
- 2 insertions near start: fitness ≈ -0.3
- **Gene-level fitness**: ~-2.2 (weighted average)

## Quality Considerations

### When to Trust a Fitness Value

**Check these**:
1. **T-statistic**: |t| > 4 preferred
2. **Number of insertions**: More insertions → more reliable
3. **Read counts**: More reads → more reliable
4. **Replicate agreement**: Similar across replicates
5. **Gene halves**: fit1 ≈ fit2 (mad12 small)

### Red Flags

**Don't trust if**:
- Very few reads (< 10 total across all insertions)
- Only 1 or 2 insertions in gene
- Large difference between gene halves
- No replicate, or replicates disagree
- Experiment failed quality metrics (mad12 > 0.5)

## Practical Examples

### Example 1: Glucose Metabolism Gene

**Condition**: Glucose minimal medium

**Gene**: glucose transporter (ptsG in E. coli)

**Observed**: fitness = -3.8, t = 9.2

**Interpretation**:
- Mutants are 2^3.8 ≈ 14-fold less abundant
- Without glucose transporter, cells can't import glucose efficiently
- Strong, significant phenotype
- Gene is important for glucose utilization

### Example 2: Lactose Metabolism Gene

**Condition**: Glucose minimal medium

**Gene**: lactose utilization (lacZ)

**Observed**: fitness = +0.3, t = 2.1

**Interpretation**:
- Slight increase in abundance (not significant)
- Makes sense: lactose genes not needed when glucose present
- No phenotype in this condition
- (Would expect strong negative fitness in lactose condition)

### Example 3: Essential Gene

**Condition**: Rich medium (LB)

**Gene**: DNA polymerase III (dnaE)

**Observed**: fitness = -7.2, t = 12.5

**Interpretation**:
- Mutants almost completely absent
- Essential for DNA replication
- Cannot grow without it
- Fitness ≈ -(number of generations) indicates essential

## Summary

**Key Points**:
1. Fitness = log₂(end/beginning abundance)
2. Positive = gene detrimental; Negative = gene beneficial
3. |fitness| > 2 ≈ 4-fold change (biologically significant)
4. Always check t-statistic for reliability
5. Context matters (number of generations, condition)
6. Gene-level fitness averages multiple insertions
7. Use |fitness| > 2 AND |t| > 4 for significant phenotypes

**For More Details**:
- `/docs/01-understanding-statistical-thresholds.md` - Statistical significance
- `/thoughts/shared/research/2025-10-01-FIT-phenotype-classification-confusion-matrix.md` - Classification criteria
