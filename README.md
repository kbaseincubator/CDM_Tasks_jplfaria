# CDM_Tasks_jplfaria

This repository contains ticket-based work for CDM (Collaborative Data Management) science projects. Each parent ticket folder contains subtasks organized as subfolders.

## How This Repository Works

Each ticket or task assigned gets its own folder at the root level:
- Folder name format: `CDMSCI-{ticket-number}-{short-description}`
- Each folder contains all code, data, notebooks, and documentation for that specific task
- Subtasks are organized as subfolders within parent ticket folders

## What's in GitHub vs What's Local

**In This Repository:**
- Ticket folders with analysis code
- Jupyter notebooks for data processing
- Python scripts
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
**Email**: jplfaria@anl.gov

## License

This work is part of the DOE Systems Biology Knowledgebase (KBase) project.
