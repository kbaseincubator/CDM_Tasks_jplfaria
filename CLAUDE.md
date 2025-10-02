# Claude Code Instructions for CDM_Tasks_jplfaria

## Repository Purpose

This repository organizes ticket-based work for CDM (Collaborative Data Management) science projects. Each ticket gets its own folder containing all related code, data, documentation, and analysis.

## Repository Structure

```
CDM_Tasks_jplfaria/
├── README.md                        # Simple repo overview
├── CLAUDE.md                        # This file - instructions for Claude
├── .gitignore                       # Shared gitignore for all tickets
│
├── CDMSCI-193-rbtnseq-modeling/     # Parent ticket folder
│   ├── PROJECT_README.md            # Detailed project documentation
│   ├── data/                        # Project-specific data
│   ├── notebooks/                   # Jupyter notebooks
│   ├── scripts/                     # Python/shell scripts
│   ├── docs/                        # Documentation
│   ├── thoughts/                    # Research notes
│   ├── references/                  # Papers, citations
│   ├── CDMSCI-196-carbon-sources/   # Subtask 1
│   ├── CDMSCI-197-media-formulations/  # Subtask 2
│   ├── CDMSCI-198-build-models/     # Subtask 3
│   └── CDMSCI-199-fba-simulations/  # Subtask 4
│
└── CDMSCI-XXX-future-ticket/        # Future tickets follow same pattern
```

## Working with This Repository

### When a New Ticket is Assigned

1. Create a new parent folder at repository root: `CDMSCI-{number}-{short-description}/`
2. If the ticket has subtasks, create subfolders: `CDMSCI-{parent}/CDMSCI-{subtask}-{description}/`
3. Move all relevant data, notebooks, scripts, docs into the ticket folder
4. Create a `PROJECT_README.md` in the parent folder with full project details
5. Create individual `README.md` files in each subtask folder

### Folder Naming Convention

- **Format**: `CDMSCI-{ticket-number}-{brief-description}`
- **Examples**:
  - `CDMSCI-193-rbtnseq-modeling`
  - `CDMSCI-196-carbon-sources`
  - `CDMSCI-250-metabolic-pathways`

### What Goes in Each Ticket Folder

**Always included:**
- `README.md` or `PROJECT_README.md` - objectives, workflow, status
- Code files (notebooks, scripts)
- Small result files (< 100MB)
- Documentation specific to this ticket

**Never included (stays local, gitignored):**
- Large databases (> 100MB)
- Large model files (SBML, HDF5)
- Downloaded organism data
- Shared resources used across multiple tickets

### Git Workflow

**For new ticket work:**
```bash
# Create ticket folder
mkdir CDMSCI-XXX-short-name
cd CDMSCI-XXX-short-name

# Do your work, create files, notebooks, etc.

# Commit when done
git add CDMSCI-XXX-short-name/
git commit -m "CDMSCI-XXX: Brief description of work completed"
git push origin main
```

**For updates to existing tickets:**
```bash
# Make changes in the ticket folder
git add CDMSCI-XXX-short-name/
git commit -m "CDMSCI-XXX: Description of updates"
git push origin main
```

## Style Guidelines

### No Emojis

IMPORTANT: Do NOT use emojis anywhere in this repository.

- No emojis in README files
- No emojis in code comments
- No emojis in commit messages
- No emojis in documentation

Use clear, descriptive text instead:
- Instead of "Status: ✅ Complete" → "Status: Complete"
- Instead of "📊 Analysis" → "Analysis"
- Instead of "⏳ Pending" → "Pending"

### Documentation Style

**README files should:**
- Be clear and concise
- Include: Objective, Input, Workflow, Output, Status, Dependencies
- Use markdown formatting (headers, lists, code blocks)
- Reference other ticket folders when there are dependencies

**Commit messages should:**
- Start with ticket number: "CDMSCI-XXX: "
- Be descriptive and specific
- Use present tense ("Add analysis" not "Added analysis")
- Include Claude Code attribution if generated with Claude

### Code Organization

**Notebooks:**
- Numbered prefixes for workflow order (e.g., `01-download-data.ipynb`, `02-process-data.ipynb`)
- Clear markdown cells explaining each step
- Outputs should be committed when small (< 1MB)

**Scripts:**
- Include docstrings and comments
- Use descriptive names (e.g., `create_growth_matrix.py` not `script1.py`)
- Include usage instructions in comments

**Results:**
- Save to `results/` subdirectory within ticket folder
- Use descriptive filenames with dates if needed
- Keep files small (< 100MB) or gitignore them

## File Management Best Practices

### What to Track in Git

- All Python scripts (`.py`)
- All Jupyter notebooks (`.ipynb`)
- README and documentation files (`.md`)
- Small data files (< 10MB CSV, JSON, TXT)
- Small figures and plots (< 5MB PNG, PDF)
- Configuration files

### What to Gitignore

- Database files (`.db`, `.sqlite`)
- Large FASTA files (`.fasta`, `.fna`, `.faa`)
- Large model files (`.xml`, `.sbml` > 100MB)
- Large HDF5 files (`.h5`, `.hdf5`)
- Downloaded archives (`.tar.gz`, `.zip`)
- Python artifacts (`__pycache__/`, `*.pyc`)
- Jupyter checkpoints (`.ipynb_checkpoints/`)

## Working with Subtasks

When a parent ticket has multiple subtasks:

1. **Parent folder** contains:
   - `PROJECT_README.md` - overall project documentation
   - Shared resources (data, scripts used across subtasks)
   - Common directories (data/, docs/, thoughts/, references/)

2. **Subtask folders** contain:
   - `README.md` - specific to this subtask
   - Subtask-specific notebooks and scripts
   - `results/` directory for outputs
   - References to parent folder resources

3. **Dependencies between subtasks:**
   - Document in README which subtasks depend on others
   - Reference output files from other subtasks clearly
   - Use relative paths: `../CDMSCI-196-carbon-sources/results/data.csv`

## Tips for Claude

1. **Always check existing structure** before creating new folders
2. **Read the ticket README** to understand objectives before working
3. **Follow the naming conventions** exactly as specified
4. **Remove any emojis** if you find them in existing files
5. **Keep documentation concise** but complete
6. **Ask clarifying questions** if ticket requirements are unclear
7. **Update status** in README files as work progresses

## Common Tasks

### Creating a New Ticket Folder

```bash
# At repository root
mkdir CDMSCI-XXX-short-description
cd CDMSCI-XXX-short-description

# Create standard structure
mkdir results
touch README.md

# If it has subtasks
mkdir CDMSCI-YYY-subtask1
mkdir CDMSCI-ZZZ-subtask2
```

### Moving Existing Work into Ticket Structure

```bash
# Move relevant files into ticket folder
mv ../old_location/notebook.ipynb CDMSCI-XXX-ticket/
mv ../old_location/script.py CDMSCI-XXX-ticket/
mv ../old_location/data/ CDMSCI-XXX-ticket/

# Commit the reorganization
git add CDMSCI-XXX-ticket/
git commit -m "CDMSCI-XXX: Reorganize files into ticket folder structure"
```

### Checking What Should Be Committed

```bash
# See what's tracked vs ignored
git status

# Check file sizes before committing
du -sh CDMSCI-XXX-ticket/*

# If files are too large, add to .gitignore
echo "CDMSCI-XXX-ticket/large_file.db" >> .gitignore
```

## Contact

For questions about repository organization or ticket structure:

**José Pedro Faria**
**Email**: jplfaria@gmail.com
**Organization**: KBase / DOE Systems Biology
