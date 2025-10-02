# Notebooks Directory

This directory contains Jupyter notebooks for downloading and analyzing FIT Fitness Browser data.

## Notebooks

### 01-download-organism-data.ipynb
**Purpose**: Download protein sequences and experiment metadata for all organisms

**Downloads**:
- Protein sequences (FASTA format) - one file per organism
- Experiment metadata (tab-delimited) - one file per organism

**Output locations**:
- `../data/raw/protein_sequences/` - Protein FASTA files
- `../data/raw/experiment_metadata/` - Experiment TSV files
- `../data/raw/logs/` - Download logs and summaries

**How to run**:
1. Open notebook in Jupyter Lab/Notebook
2. Run all cells sequentially
3. First test with single organism, then run full download
4. Check logs for any errors

**Estimated time**: 30-60 minutes for all organisms

**Requirements**:
- Python 3.7+
- pandas
- requests
- tqdm (for progress bars)
- cloudscraper (to bypass Cloudflare protection)

Install requirements:
```bash
pip install pandas requests tqdm jupyter cloudscraper
```

### 02-create-carbon-source-growth-matrix.ipynb
**Purpose**: Create organism × carbon source growth/no-growth binary matrix from experiment metadata

**Input**:
- Experiment metadata TSV files from `../data/raw/experiment_metadata/`

**Output**:
- `../data/processed/carbon_source_growth_matrix.csv` - Binary matrix (1=growth, 0=no growth)
- `../data/processed/carbon_source_growth_matrix_stats.txt` - Statistics
- `../data/processed/carbon_source_growth_heatmap.png` - Visualization

**Assumption**:
- Organism has data for carbon source → **Growth = 1**
- Organism lacks data for carbon source → **No growth = 0**

**How to run**:
1. Ensure experiment metadata files are downloaded (run notebook 01 first)
2. Open notebook in Jupyter Lab/Notebook
3. Run all cells sequentially
4. Check output files in `../data/processed/`

**Estimated time**: <5 minutes

**Requirements**:
- Python 3.7+
- pandas
- numpy
- matplotlib
- seaborn

Install requirements:
```bash
pip install pandas numpy matplotlib seaborn jupyter
```

## Running Notebooks

### Start Jupyter
```bash
# From project root
cd notebooks
jupyter notebook
# or
jupyter lab
```

### Run Notebook
1. Click on `01-download-organism-data.ipynb`
2. Run cells one by one (Shift+Enter)
3. Or run all: Cell → Run All

## Data Organization

After running notebooks, your data directory will look like:

```
data/
├── raw/
│   ├── protein_sequences/
│   │   ├── acidovorax_3H11_proteins.fasta
│   │   ├── Keio_proteins.fasta
│   │   ├── WCS417_proteins.fasta
│   │   └── ... (one per organism)
│   ├── experiment_metadata/
│   │   ├── acidovorax_3H11_experiments.tsv
│   │   ├── Keio_experiments.tsv
│   │   ├── WCS417_experiments.tsv
│   │   └── ... (one per organism)
│   └── logs/
│       ├── download_log.txt
│       └── download_summary_YYYYMMDD_HHMMSS.csv
└── processed/
    ├── carbon_source_growth_matrix.csv
    ├── carbon_source_growth_matrix_stats.txt
    └── carbon_source_growth_heatmap.png
```

## Next Steps

After running the notebooks:

1. **Review download results** (notebook 01):
   - Check `data/raw/logs/download_log.txt` for any errors
   - Verify all organism files downloaded successfully

2. **Review growth matrix** (notebook 02):
   - Check `data/processed/carbon_source_growth_matrix.csv`
   - Review statistics in `carbon_source_growth_matrix_stats.txt`
   - Examine heatmap visualization

3. **Next analysis steps**:
   - Build genome-scale metabolic models for each organism
   - Simulate growth on carbon sources in silico
   - Compare experimental growth matrix vs in silico predictions
   - Generate confusion matrix for model validation

## Troubleshooting

### Import errors
```bash
pip install -r requirements.txt  # if requirements file exists
# or manually install
pip install pandas requests tqdm jupyter
```

### Download failures
- Check internet connection
- Some organisms might not be available - this is normal
- Check `data/raw/logs/download_log.txt` for specific errors
- Can retry failed downloads using retry cell in notebook

### Slow downloads
- Normal - downloading data for 48 organisms takes time
- Server may rate-limit requests
- Notebook includes delays between requests to be polite

## Tips

- Run test download first before full download
- Keep terminal/notebook window open during download
- Don't close browser while download is running
- Check disk space before downloading (expect ~500 MB - 2 GB total)
