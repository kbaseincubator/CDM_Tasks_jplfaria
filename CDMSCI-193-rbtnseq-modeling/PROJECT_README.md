# CDM_Tasks_jplfaria

**Project**: CDM Science - Data, Analysis, and Agents
**Assignee**: José Pedro Faria
**Organization**: KBase / DOE Systems Biology

This repository contains ticket-based work for CDM (Collaborative Data Management) science projects. Each parent ticket folder contains subtasks organized as subfolders.

## Repository Structure

```
CDM_Tasks_jplfaria/
├── CDMSCI-193-rbtnseq-modeling/     # RBTnSeq growth/no-growth modeling
│   ├── CDMSCI-196-carbon-sources/
│   ├── CDMSCI-197-media-formulations/
│   ├── CDMSCI-198-build-models/
│   └── CDMSCI-199-fba-simulations/
│
└── CDMSCI-XXX-future-project/       # Future tickets (as assigned)
```

## Current Projects

### CDMSCI-193: RBTnSeq Modeling Analysis

**Objective**: Validate genome-scale metabolic models by comparing experimental growth data from Fitness Browser (Deutschbauer lab) against computational predictions.

**Status**: In Progress

**Workflow**:
1. CDMSCI-196: Extract carbon sources from experimental data (Complete)
2. CDMSCI-197: Translate to computational media formulations (Pending)
3. CDMSCI-198: Build genome-scale metabolic models (Pending)
4. CDMSCI-199: Run FBA simulations and generate confusion matrix (Pending)

See [`CDMSCI-193-rbtnseq-modeling/README.md`](CDMSCI-193-rbtnseq-modeling/README.md) for details.

## What's in GitHub vs What's Local

### In This Repository (GitHub)

- Ticket folders with analysis code
- Jupyter notebooks for data processing
- Python scripts for automation
- Small result files (CSV, JSON, PNG < 100MB)
- Documentation and READMEs

### Local Only (Gitignored)

- Large databases (feba.db, 8 GB)
- Downloaded organism data (protein sequences, experiment metadata)
- Shared resources and reference materials
- Large model files (SBML > 100MB)

**Reason**: These are either too large for GitHub or regenerable from source.

## Quick Start

### Prerequisites

```bash
# Python environment
python >= 3.8

# Core packages
pip install pandas numpy jupyter cobra scikit-learn matplotlib seaborn
```

### Running a Ticket

1. Clone this repository:
```bash
git clone git@github.com:kbaseincubator/CDM_Tasks_jplfaria.git
cd CDM_Tasks_jplfaria
```

2. Download shared resources (one-time setup):
```bash
# Create shared resources directory (local only)
mkdir -p ../shared_resources/database
cd ../shared_resources/database

# Download Fitness Browser database (8 GB)
wget https://figshare.com/ndownloader/files/44580544 -O feba.db.gz
gunzip feba.db.gz
```

3. Navigate to ticket folder:
```bash
cd CDMSCI-193-rbtnseq-modeling/CDMSCI-196-carbon-sources
```

4. Run notebook:
```bash
jupyter notebook 02-create-carbon-source-growth-matrix.ipynb
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

## File Organization

### Ticket Folder Structure

Each ticket follows this pattern:

```
CDMSCI-XXX-short-name/
├── README.md                 # Ticket objectives and instructions
├── notebook.ipynb            # Analysis code (if applicable)
├── script.py                 # Automation script (if applicable)
├── results/                  # Small output files
│   ├── data.csv
│   ├── plot.png
│   └── stats.txt
└── models/                   # Model files (if applicable)
```

### Naming Conventions

- **Folders**: `CDMSCI-{number}-{short-description}`
- **Notebooks**: Descriptive names (e.g., `02-create-carbon-source-growth-matrix.ipynb`)
- **Results**: Clear, timestamped if multiple runs

## Contributing

### Adding a New Ticket

1. Create parent folder: `CDMSCI-XXX-project-name/`
2. Add subtask folders: `CDMSCI-XXX-project-name/CDMSCI-YYY-subtask/`
3. Add README.md with objectives
4. Implement analysis code
5. Commit and push

### Git Workflow

```bash
# Add files
git add CDMSCI-XXX-project-name/

# Commit with descriptive message
git commit -m "CDMSCI-XXX: Complete carbon source extraction analysis"

# Push to GitHub
git push origin main
```

## Contact

**José Pedro Faria**
**Email**: jplfaria@gmail.com
**Organization**: KBase / DOE Systems Biology

## License

This work is part of the DOE Systems Biology Knowledgebase (KBase) project.
