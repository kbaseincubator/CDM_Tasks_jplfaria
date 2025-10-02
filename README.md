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

Validate genome-scale metabolic models by comparing experimental growth data from Fitness Browser against computational predictions.

See [CDMSCI-193-rbtnseq-modeling/PROJECT_README.md](CDMSCI-193-rbtnseq-modeling/PROJECT_README.md) for full details.

## How This Repository Works

Each ticket or task assigned gets its own folder at the root level:
- Folder name format: `CDMSCI-{ticket-number}-{short-description}`
- Each folder contains all code, data, notebooks, and documentation for that specific task
- Subtasks are organized as subfolders within parent ticket folders

## What's in GitHub vs What's Local

**In This Repository:**
- Ticket folders with analysis code
- Jupyter notebooks for data processing
- Python scripts for automation
- Small result files (CSV, JSON, PNG < 100MB)
- Documentation and READMEs

**Local Only (Gitignored):**
- Large databases (> 100MB)
- Downloaded organism data
- Shared resources and reference materials
- Large model files (SBML > 100MB)

## Quick Start

1. Clone this repository:
```bash
git clone git@github.com:kbaseincubator/CDM_Tasks_jplfaria.git
cd CDM_Tasks_jplfaria
```

2. Navigate to the ticket folder you want to work on:
```bash
cd CDMSCI-193-rbtnseq-modeling
```

3. Follow the instructions in that ticket's README

## Contact

**José Pedro Faria**
**Email**: jplfaria@gmail.com
**Organization**: KBase / DOE Systems Biology

## License

This work is part of the DOE Systems Biology Knowledgebase (KBase) project.
