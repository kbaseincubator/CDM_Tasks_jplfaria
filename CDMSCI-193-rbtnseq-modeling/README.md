# CDMSCI-193: Modeling Analysis of Growth/No-Growth Predictions for RBTnSeq Genomes

**Project**: Validate genome-scale metabolic models by comparing experimental growth data from Fitness Browser RBTnSeq (Deutschbauer lab) against in silico growth predictions.

**Assigned to**: José Pedro Faria
**Organization**: KBase / DOE Systems Biology
**Last updated**: 2025-10-02

## Objective

Compare experimental bacterial growth data from the Fitness Browser with computational predictions from genome-scale metabolic models to validate model accuracy.

## Workflow

```
Experimental Data (Fitness Browser)
          ↓
    Carbon Sources Matrix → Media Formulations → Metabolic Models → FBA Simulations
          ↓                        ↓                    ↓                ↓
    CDMSCI-196               CDMSCI-197          CDMSCI-198        CDMSCI-199
                                                                        ↓
                                                              Confusion Matrix
                                                              (Experimental vs In Silico)
```

## Subtasks

### CDMSCI-196: Compile Carbon Sources
**Goal**: Extract all carbon sources tested across all 57 genomes

**Outputs**:
- Binary growth matrix (57 organisms × ~198 carbon sources)
- Carbon source list with coverage statistics
- Visualization heatmap

**Status**: Complete

---

### CDMSCI-197: Translate to Media Formulations
**Goal**: Convert experimental carbon sources to computational media definitions

**Outputs**:
- Media formulation files (JSON/TSV)
- Mapping table: Fitness Browser carbon source → ModelSEED compound ID
- Basal media composition

**Status**: Pending

**Dependencies**: CDMSCI-196 (carbon source list)

---

### CDMSCI-198: Build Metabolic Models
**Goal**: Generate genome-scale metabolic models for all 57 organisms using RAST annotations

**Outputs**:
- 57 SBML model files
- Model statistics table
- Gap-filling reports

**Status**: In Progress (protein sequences downloaded)

**Dependencies**: CDMSCI-196 (organism list)

---

### CDMSCI-199: FBA Simulations & Validation
**Goal**: Simulate growth and compare predictions with experimental data

**Outputs**:
- In silico growth prediction matrix
- Confusion matrix (experimental vs computational)
- Performance metrics (precision, recall, F1-score)
- Analysis of false positives/negatives

**Status**: Pending

**Dependencies**: CDMSCI-196 (experimental data), CDMSCI-197 (media), CDMSCI-198 (models)

## Confusion Matrix Definition

```
                    Experimental Growth (Fitness Browser)
                    YES         NO
In Silico   YES     TP          FP
Growth      NO      FN          TN
```

**Interpretations**:
- **TP (True Positive)**: Grows experimentally AND grows in silico (correct prediction)
- **TN (True Negative)**: Doesn't grow experimentally AND doesn't grow in silico (correct prediction)
- **FP (False Positive)**: Doesn't grow experimentally BUT grows in silico (model over-predicts)
- **FN (False Negative)**: Grows experimentally BUT doesn't grow in silico (model missing capabilities)

## Project Structure

```
CDMSCI-193-rbtnseq-modeling/
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore patterns
│
├── downloads/                       # Downloaded databases (local only)
│   └── feba.db                      # Fitness Browser database (8 GB, gitignored)
│
├── data/                            # Project data
│   ├── raw/                         # Immutable downloads
│   │   ├── protein_sequences/       # Organism FASTA files (gitignored)
│   │   ├── experiment_metadata/     # Experiment TSV files (gitignored)
│   │   └── logs/                    # Download logs
│   └── processed/                   # Generated outputs (gitignored)
│       ├── growth_matrices/
│       ├── media_formulations/
│       └── models/
│
├── docs/                            # Documentation and educational materials
│   ├── 01-understanding-statistical-thresholds.md
│   ├── 02-project-objective-confusion-matrix.md
│   ├── 03-understanding-fitness-values.md
│   ├── 04-cofitness-functional-relationships.md
│   ├── 05-growth-no-growth-matrix.md
│   └── research/                    # Research notes
│       └── 2025-10-01-*.md
│
├── references/                      # Papers and citations
│   └── FIT_Fitness_Browser_Comprehensive_Review.md
│
├── notebooks/                       # Shared exploratory notebooks
│   └── 01-download-organism-data.ipynb
│
├── scripts/                         # Shared utility scripts
│
├── CDMSCI-196-carbon-sources/       # Subtask 1
├── CDMSCI-197-media-formulations/   # Subtask 2
├── CDMSCI-198-build-models/         # Subtask 3
└── CDMSCI-199-fba-simulations/      # Subtask 4
```

## Data Sources

### Fitness Browser (Deutschbauer Lab)

- **Website**: https://fit.genomics.lbl.gov
- **Database**: feba.db (SQLite, 8 GB)
- **Download**: https://figshare.com/articles/dataset/25236931
- **License**: Creative Commons Attribution 4.0
- **Citation**: Price et al. (2018) Nature 557:503-509

### Key Publications

1. **Wetmore et al. (2015)** mBio 6(3):e00306-15 - RB-TnSeq methodology
2. **Price et al. (2018)** Nature 557:503-509 - Mutant phenotypes for bacterial genes
3. **Price et al. (2024)** Database - Fitness Browser interactive tools

## Quick Start

### Prerequisites

```bash
# Python environment
python >= 3.8

# Install dependencies
pip install -r requirements.txt
```

### Setup

1. Clone this repository:
```bash
git clone git@github.com:kbaseincubator/CDM_Tasks_jplfaria.git
cd CDM_Tasks_jplfaria/CDMSCI-193-rbtnseq-modeling
```

2. Download Fitness Browser database:
```bash
cd downloads
wget https://figshare.com/ndownloader/files/44580544 -O feba.db.gz
gunzip feba.db.gz
cd ..
```

3. Start with CDMSCI-196 to extract carbon sources:
```bash
cd CDMSCI-196-carbon-sources
jupyter notebook 02-create-carbon-source-growth-matrix.ipynb
```

## Style Guidelines

### No Emojis

Do NOT use emojis anywhere in this project:
- No emojis in README files
- No emojis in code comments
- No emojis in commit messages
- No emojis in documentation

Use clear, descriptive text instead.

### Documentation

**README files should include**:
- Objective
- Input/Output
- Workflow steps
- Status
- Dependencies

**Commit messages should**:
- Start with ticket number: "CDMSCI-XXX: "
- Be descriptive and specific
- Use present tense ("Add analysis" not "Added analysis")

### Code Organization

**Notebooks**:
- Numbered prefixes for workflow order (e.g., `01-download-data.ipynb`)
- Clear markdown cells explaining each step
- Outputs saved to subtask-specific `results/` directory

**Scripts**:
- Include docstrings and comments
- Use descriptive names (e.g., `create_growth_matrix.py`)
- Include usage instructions

**Results**:
- Save to `results/` subdirectory within subtask folder
- Use descriptive filenames with dates if needed
- Small files (< 100MB) tracked in git, large files gitignored

## File Management

### What to Track in Git

- Python scripts (`.py`)
- Jupyter notebooks (`.ipynb`)
- README and documentation (`.md`)
- Small data files (< 10MB CSV, JSON, TXT)
- Small figures and plots (< 5MB PNG, PDF)
- Configuration files

### What to Gitignore

- Database files (`.db`, `.sqlite`)
- Large FASTA files (`.fasta`, `.fna`, `.faa`)
- Large model files (`.xml`, `.sbml` > 100MB)
- Downloaded archives (`.tar.gz`, `.zip`)
- Python artifacts (`__pycache__/`, `*.pyc`)
- Jupyter checkpoints (`.ipynb_checkpoints/`)

## Git Workflow

```bash
# Add files
git add CDMSCI-XXX-subtask/

# Commit with descriptive message
git commit -m "CDMSCI-XXX: Complete analysis with detailed description"

# Push to GitHub
git push origin main
```

## Contact

**José Pedro Faria**
**Email**: jplfaria@anl.gov
**Organization**: KBase / DOE Systems Biology
