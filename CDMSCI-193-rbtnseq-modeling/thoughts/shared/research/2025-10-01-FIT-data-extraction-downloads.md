---
date: 2025-10-01
researcher: Jose P. Faria
topic: "FIT Fitness Browser - Data Extraction and Download Mechanisms"
tags: [research, fitness-browser, data-download, figshare, programmatic-access]
status: complete
last_updated: 2025-10-01
last_updated_by: Jose P. Faria
---

# Research: FIT Fitness Browser Data Extraction and Download Mechanisms

**Date**: 2025-10-01
**Researcher**: Jose P. Faria
**Resource**: https://fit.genomics.lbl.gov/cgi-bin/myFrontPage.cgi

## Research Question

Document ALL methods for downloading and extracting data from the FIT Fitness Browser, including file formats, programmatic access patterns, and practical extraction strategies.

## Summary

The FIT Fitness Browser provides multiple data access methods: (1) Figshare releases with complete SQLite database and organism files, (2) direct downloads from fit.genomics.lbl.gov, (3) BigFit supplemental repository with 84 GB complete dataset, and (4) per-organism downloads from web interface. The primary method is downloading feba.db (SQLite3, ~5 GB) from Figshare and querying it with SQL or Python/R.

## Detailed Findings

### 1. Figshare Releases (PRIMARY METHOD)

#### February 2024 Release (Most Current)
**URL**: https://figshare.com/articles/dataset/25236931
**DOI**: 10.6084/m9.figshare.25236931
**License**: Creative Commons Attribution 4.0

**Files Available**:

1. **feba.db** (gzipped)
   - SQLite3 database
   - ~5 GB (2017 reference, likely larger now)
   - Contains: Organism, Gene, GeneFitness, Experiment, and all annotation tables
   - **This is the main data source**

2. **aaseqs** (gzipped)
   - FASTA format protein sequences
   - Identifier format: `orgId:locusId`
   - All protein sequences for all 48 organisms
   - Used for BLAST searches

3. **db.StrainFitness.*** (gzipped, multiple files)
   - Tab-delimited per-strain fitness values
   - **One file per organism**
   - Naming: `db.StrainFitness.[orgId]`
   - **NOT in SQLite database** - must download separately
   - Contains barcode-level data

4. **code.tar** (gzipped)
   - Complete source code snapshot
   - Perl, R, and shell scripts
   - Database schema: `lib/db_setup_tables.sql`
   - Analysis tools: `lib/FEBA.R`, `bin/BarSeqR.pl`

**Download Commands**:
```bash
# Download complete release
wget https://figshare.com/ndownloader/files/44580544 -O fitnessbrowser_feb2024.tar.gz

# Extract all files
tar -xzf fitnessbrowser_feb2024.tar.gz

# Decompress individual files
gunzip feba.db.gz
gunzip aaseqs.gz
gunzip db.StrainFitness.*.gz
```

#### Previous Releases

**November 2021**: https://figshare.com/articles/dataset/16913530
- 6,726 experiments, 46 bacteria

**November 2020**: https://figshare.com/articles/dataset/13172087
- 6,570 experiments, 42 bacteria
- **Note**: Sucrose and D-mannitol data unreliable (contaminated stock solutions)

**June 2017**: https://figshare.com/articles/dataset/5134840
- 4,956 experiments, 33 bacteria
- Database was ~5 GB at this time

### 2. Direct Downloads from fit.genomics.lbl.gov

**feba.db**:
```bash
# Direct download (large file, may be slow)
curl -O https://fit.genomics.lbl.gov/cgi_data/feba.db
# or
wget https://fit.genomics.lbl.gov/cgi_data/feba.db
```

**aaseqs**:
```bash
curl -O https://fit.genomics.lbl.gov/cgi_data/aaseqs
```

**db.StrainFitness files** (per organism):
```bash
# Example: E. coli Keio collection
wget https://fit.genomics.lbl.gov/cgi_data/db.StrainFitness.Keio

# Example: Pseudomonas putida
wget https://fit.genomics.lbl.gov/cgi_data/db.StrainFitness.Putida
```

**Caveats**:
- Very large downloads
- May timeout or fail
- Figshare more reliable for bulk downloads

### 3. BigFit Supplemental Data Repository

**URL**: https://genomics.lbl.gov/supplemental/bigfit/
**Paper**: Price et al., Nature 2018
**Coverage**: 32 bacterial species

**Available Files**:

**Metadata Files**:
1. **orginfo.tab** - Organism information (32 bacteria)
   ```bash
   wget https://genomics.lbl.gov/supplemental/bigfit/orginfo.tab
   ```

2. **refseq_mapping.tsv** - Mapping to RefSeq IDs
   ```bash
   wget https://genomics.lbl.gov/supplemental/bigfit/refseq_mapping.tsv
   ```

3. **uniprot.map** - Mapping to UniProt (98% identity)
   ```bash
   wget https://genomics.lbl.gov/supplemental/bigfit/uniprot.map
   ```

4. **essential_proteins.tab** - Essential protein annotations
   ```bash
   wget https://genomics.lbl.gov/supplemental/bigfit/essential_proteins.tab
   ```

**Genome Data**:
```bash
# Download all genomes, proteins, and annotations
wget https://genomics.lbl.gov/supplemental/bigfit/genomes.tar.gz
tar -xzf genomes.tar.gz
```

**Per-Organism Fitness Tables**:
```bash
# Example: Burkholderia phytofirmans (BFirm)
wget https://genomics.lbl.gov/supplemental/bigfit/html/BFirm/fit_genes.tab

# Structure: locusId | sysName | desc | exp1_fit | exp1_t | exp2_fit | exp2_t | ...
```

**Complete Dataset** (84 GB):
- Mentioned but direct download URL not accessible
- Includes all TnSeq read mappings
- Available through Google Drive (link in documentation)

**32 Organism List**:
acidovorax_3H11, ANA3, azobra, BFirm, Caulo, Cola, Cup4G11, Dyella79, Dino, HerbieS, Kang, Keio, Korea, Koxy, Marino, Miya, MR1, Phaeo, Ponti, PS, pseudo1_N1B4, pseudo3_N2E3, pseudo5_N2C3_1, pseudo6_N2E2, pseudo13_GW456_L13, psRCH2, Pedo557, PV4, SB2B, Smeli, SynE, WCS417

### 4. Organism Page Downloads

**Location**: Bottom of each organism page on fit.genomics.lbl.gov

**URL Pattern**:
```
https://fit.genomics.lbl.gov/cgi-bin/org.cgi?orgId=[ORGANISM_ID]
```

**Available Tables** (per organism):
1. Gene fitness table (tab-delimited)
2. Strain fitness table (tab-delimited)
3. Experiment metadata table
4. Reannotations table

**Access Limitation**:
- Pages returned 403 errors during research
- May require browser access or authentication
- Figshare/BigFit more reliable for programmatic access

### 5. Programmatic Access via SQLite

#### Python Example (Recommended)
```python
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('feba.db')

# List all organisms
orgs = pd.read_sql_query("SELECT * FROM Organism", conn)
print(f"Found {len(orgs)} organisms")

# Get fitness data for specific organism
query = """
SELECT g.locusId, g.sysName, g.gene, g.desc,
       e.expDesc, e.condition_1, gf.fit, gf.t
FROM Gene g
JOIN GeneFitness gf ON g.orgId = gf.orgId AND g.locusId = gf.locusId
JOIN Experiment e ON gf.orgId = e.orgId AND gf.expName = e.expName
WHERE g.orgId = ? AND ABS(gf.t) > 4
ORDER BY ABS(gf.fit) DESC
LIMIT 100
"""
df = pd.read_sql_query(query, conn, params=['Keio'])
df.to_csv('ecoli_top_phenotypes.csv', index=False)

conn.close()
```

#### R Example
```r
library(RSQLite)
library(dplyr)

# Connect
conn <- dbConnect(SQLite(), "feba.db")

# Get experiment metadata
experiments <- dbReadTable(conn, "Experiment")

# Complex query with joins
query <- "
  SELECT g.orgId, g.locusId, g.desc, gf.fit, gf.t, e.condition_1
  FROM GeneFitness gf
  JOIN Gene g ON gf.orgId = g.orgId AND gf.locusId = gf.locusId
  JOIN Experiment e ON gf.orgId = e.orgId AND gf.expName = e.expName
  WHERE e.expGroup = 'carbon source' AND ABS(gf.fit) > 2
"
fitness_data <- dbGetQuery(conn, query)

dbDisconnect(conn)
```

#### Command-Line SQLite
```bash
# Query database directly
sqlite3 feba.db "SELECT orgId, genus, species FROM Organism;"

# Export table to CSV
sqlite3 feba.db -header -csv "SELECT * FROM GeneFitness WHERE orgId='Keio';" > keio_fitness.csv

# Get schema
sqlite3 feba.db ".schema GeneFitness"

# Get table list
sqlite3 feba.db ".tables"
```

### 6. URL-Based Queries (CGI Scripts)

#### Single Gene Fitness
```
https://fit.genomics.lbl.gov/cgi-bin/singleFit.cgi?orgId=Keio&locusId=17024&showAll=1
```

**Parameters**:
- `orgId`: Organism ID
- `locusId`: Gene locus ID
- `showAll`: 0 or 1 (show all experiments)

#### Multiple Genes
```
https://fit.genomics.lbl.gov/cgi-bin/genesFit.cgi?orgId=Putida&locusId=PP_1623&locusId=PP_4208&showAll=1
```

**Parameters**:
- Can specify `locusId` multiple times
- `around=N`: Include N neighboring genes

**Limitations**:
- Returns HTML, not structured data
- Would require HTML parsing
- Not recommended for bulk extraction
- Use SQLite database instead

### 7. Data Table Formats

#### db.StrainFitness Format
```
barcode | rcbarcode | scaffold | strand | pos | locusId | n | construct | locusStrand | [exp columns]
```

**Columns**:
- barcode: 20-nt DNA barcode sequence
- rcbarcode: Reverse complement
- scaffold: Genome scaffold/contig
- strand: + or -
- pos: Base pair position
- locusId: Gene locus tag
- [experiments]: One column per experiment with read counts or fitness

#### fit_genes.tab Format (BigFit)
```
locusId | sysName | type | scaffoldId | begin | end | strand | name | desc | GC | nTA | used
```

**Example Row**:
```
GFF1 | PGA1_c00010 | 1 | PGA1_c | 101 | 1528 | + | NA | chromosomal replication initiator DnaA | 0.5777 | 21 | FALSE
```

### 8. Batch Download Strategy

#### Complete Dataset Download
```bash
#!/bin/bash
# Download complete FIT dataset

# Create directory
mkdir -p FIT_data
cd FIT_data

# Download from Figshare
echo "Downloading February 2024 release..."
wget https://figshare.com/ndownloader/files/44580544 -O fitness_browser.tar.gz

# Extract
echo "Extracting..."
tar -xzf fitness_browser.tar.gz

# Decompress database
echo "Decompressing database..."
gunzip feba.db.gz

# Decompress sequences
gunzip aaseqs.gz

# Decompress all StrainFitness files
gunzip db.StrainFitness.*.gz

# Verify database
echo "Verifying database..."
sqlite3 feba.db "SELECT COUNT(*) FROM Organism;"

echo "Download complete!"
```

#### Per-Organism Download
```bash
#!/bin/bash
# Download data for specific organism

ORGID="Keio"  # Change as needed

# Create organism directory
mkdir -p ${ORGID}
cd ${ORGID}

# Download strain fitness
wget https://fit.genomics.lbl.gov/cgi_data/db.StrainFitness.${ORGID}

# If available, download from BigFit
if wget -q --spider https://genomics.lbl.gov/supplemental/bigfit/html/${ORGID}/fit_genes.tab; then
    wget https://genomics.lbl.gov/supplemental/bigfit/html/${ORGID}/fit_genes.tab
fi

echo "Downloaded data for ${ORGID}"
```

### 9. Data Extraction Workflow

**Step-by-Step Process**:

1. **Download Database**:
   ```bash
   wget https://figshare.com/ndownloader/files/44580544 -O fit_data.tar.gz
   tar -xzf fit_data.tar.gz
   gunzip feba.db.gz
   ```

2. **Explore Schema**:
   ```python
   import sqlite3
   conn = sqlite3.connect('feba.db')
   cursor = conn.cursor()

   # List tables
   cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
   tables = cursor.fetchall()

   # Get schema for key tables
   for table in ['Organism', 'Gene', 'GeneFitness', 'Experiment']:
       print(f"\n{table} schema:")
       cursor.execute(f"PRAGMA table_info({table})")
       print(cursor.fetchall())
   ```

3. **Extract Specific Data**:
   ```python
   # Extract all fitness data for one organism
   query = "SELECT * FROM GeneFitness WHERE orgId = 'Keio'"
   df = pd.read_sql_query(query, conn)
   df.to_csv('keio_all_fitness.csv', index=False)

   # Extract experiment metadata
   exps = pd.read_sql_query("SELECT * FROM Experiment WHERE orgId = 'Keio'", conn)
   exps.to_csv('keio_experiments.csv', index=False)
   ```

4. **Join and Reorganize**:
   ```python
   # Create gene × experiment matrix
   pivot_query = """
   SELECT
       g.locusId,
       g.sysName,
       g.desc,
       gf.expName,
       gf.fit,
       gf.t
   FROM GeneFitness gf
   JOIN Gene g ON gf.orgId = g.orgId AND gf.locusId = gf.locusId
   WHERE gf.orgId = 'Keio'
   """
   df = pd.read_sql_query(pivot_query, conn)

   # Pivot to wide format
   fit_matrix = df.pivot(index='locusId', columns='expName', values='fit')
   t_matrix = df.pivot(index='locusId', columns='expName', values='t')

   # Save
   fit_matrix.to_csv('keio_fitness_matrix.csv')
   t_matrix.to_csv('keio_tscores_matrix.csv')
   ```

### 10. Performance Considerations

**Database Size**: ~5 GB
**RAM Required**: 8-16 GB recommended for large queries
**Query Speed**: Indexed queries are fast; full table scans slow

**Optimization Tips**:
1. Always filter by `orgId` first
2. Use `LIMIT` for exploratory queries
3. Create temp tables for complex multi-step analyses
4. Index custom columns if doing repeated queries
5. Use pandas chunking for very large result sets

**Example Chunked Read**:
```python
# Read large table in chunks
chunks = []
for chunk in pd.read_sql_query(query, conn, chunksize=10000):
    # Process chunk
    filtered = chunk[chunk['t'].abs() > 4]
    chunks.append(filtered)

result = pd.concat(chunks)
```

## Related Research

- Part 1: Database schema and structure
- Part 3: Phenotype classification and confusion matrix
- Part 4: Practical extraction plan with code examples

## Open Questions

1. Exact file sizes for February 2024 release individual files
2. Complete list of organism IDs (orgId) for all 48 organisms in database
3. Google Drive link for 84 GB complete BigFit dataset
4. Whether organism page downloads require authentication
