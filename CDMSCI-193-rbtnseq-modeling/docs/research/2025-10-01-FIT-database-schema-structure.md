---
date: 2025-10-01
researcher: Jose P. Faria
topic: "FIT Fitness Browser - Database Schema and Structure"
tags: [research, fitness-browser, database-schema, sqlite, genomics]
status: complete
last_updated: 2025-10-01
last_updated_by: Jose P. Faria
---

# Research: FIT Fitness Browser Database Schema and Structure

**Date**: 2025-10-01
**Researcher**: Jose P. Faria
**Resource**: https://fit.genomics.lbl.gov/cgi-bin/myFrontPage.cgi

## Research Question

Document the complete database schema and structure of the FIT Fitness Browser SQLite database (feba.db) to enable data extraction and reorganization for custom analyses.

## Summary

The FIT Fitness Browser uses a SQLite3 database (feba.db, ~5 GB) with 39 tables storing genome-wide mutant fitness data for 48 organisms (46 bacteria + 2 archaea). The schema is defined in `lib/db_setup_tables.sql` from the source code repository at https://bitbucket.org/berkeleylab/feba. Core tables include Organism, Gene, GeneFitness, and Experiment, with fitness values stored as log2 ratios and t-statistics.

## Detailed Findings

### 1. Database Overview

**File**: feba.db
**Format**: SQLite3
**Size**: ~5 GB (as of 2017 release, likely larger in 2024)
**Schema Location**: `lib/db_setup_tables.sql` in source code
**Download**: https://figshare.com/articles/dataset/25236931

### 2. Complete Table List (39 Tables)

#### Core Data Tables:
1. **Organism** - Organism metadata
2. **Gene** - Gene annotations for all organisms
3. **GeneFitness** - Per-gene fitness values across experiments
4. **Experiment** - Experiment metadata and conditions
5. **Ortholog** - Ortholog relationships between genes

#### Analysis Tables:
6. **Cofit** - Cofitness relationships (genes with similar fitness patterns)
7. **ConservedCofit** - Conserved cofitness across species
8. **SpecificPhenotype** - Genes with strong condition-specific phenotypes
9. **SpecOG** - Ortholog groups with conserved specific phenotypes

#### Annotation Tables:
10. **GeneDomain** - Protein domain annotations
11. **GeneFeature** - Gene features (transmembrane, signal peptide, etc.)
12. **LocusXref** - Cross-references to external databases
13. **BestHitKEGG** - Best KEGG ortholog hits
14. **BestHitSwissProt** - Best SwissProt hits
15. **BestHitMetacyc** - Best MetaCyc hits
16. **SEEDAnnotation** - SEED subsystem annotations
17. **SEEDClass** - SEED EC/TC numbers
18. **Reannotation** - Curated reannotations
19. **ReannotationEC** - EC numbers from reannotations

#### Pathway/Metabolic Tables:
20. **MetacycPathway** - MetaCyc pathway definitions
21. **MetacycPathwayReaction** - Reactions in pathways
22. **MetacycPathwayReactionPredecessor** - Reaction dependencies
23. **MetacycPathwayPrimaryCompound** - Primary compounds in pathways
24. **MetacycPathwayCoverage** - Pathway coverage per organism
25. **MetacycReaction** - Reaction definitions
26. **MetacycReactionCompound** - Compounds in reactions
27. **MetacycReactionEC** - EC numbers for reactions
28. **MetacycCompound** - Compound definitions

#### KEGG Integration:
29. **KEGGMember** - KEGG orthology group membership
30. **KgroupDesc** - KEGG orthology group descriptions
31. **KgroupEC** - EC numbers for KEGG groups
32. **KEGGCompound** - KEGG compound information
33. **KEGGConf** - KEGG map coordinates
34. **KEGGMap** - KEGG pathway maps
35. **ECInfo** - EC number descriptions

#### SEED Integration:
36. **SEEDRoles** - SEED subsystem roles
37. **SEEDAnnotationToRoles** - Mapping annotations to roles
38. **SEEDRoleReaction** - Reactions for SEED roles
39. **SEEDReaction** - SEED reaction definitions

#### Support Tables:
40. **Compounds** - Media compound information
41. **MediaComponents** - Components of media and mixes
42. **StrainDataSeek** - Seek positions for strain fitness files
43. **Publication** - Publication references
44. **ScaffoldSeq** - Genome scaffold sequences

### 3. Critical Table Schemas

#### Organism Table
```sql
CREATE TABLE Organism(
   orgId            TEXT     NOT NULL,
   division         TEXT     NOT NULL,
   genus            TEXT     NOT NULL,
   species          TEXT     NOT NULL,
   strain           TEXT     NOT NULL,
   taxonomyId       INT,     /* NCBI taxonomyId */
   PRIMARY KEY (orgId)
);
```

**Key Points**:
- `orgId` is the primary organism identifier (e.g., "Keio", "WCS417")
- Used throughout database to link data to organisms

#### Gene Table
```sql
CREATE TABLE Gene(
   orgId            TEXT     NOT NULL,
   locusId          TEXT     NOT NULL,
   sysName          TEXT,    /* locus tag like SO_1446 or b2338 */
   scaffoldId       TEXT     NOT NULL,
   begin            INT      NOT NULL,
   end              INT      NOT NULL,
   type             INT      NOT NULL,  /* 1=protein, 2=rRNA, 5=tRNA, etc. */
   strand           TEXT     NOT NULL,
   gene             TEXT,    /* gene name like recA */
   desc             TEXT,
   GC               REAL,    /* %GC of gene sequence */
   PRIMARY KEY (orgId, locusId)
);
CREATE INDEX 'locusOrg' on Gene ('locusId' ASC, 'orgId' ASC);
CREATE INDEX 'sysNameOrg' on Gene ('sysName' ASC, 'orgId' ASC);
CREATE INDEX 'geneOrg' on Gene ('gene' ASC, 'orgId' ASC);
```

**Key Points**:
- Composite primary key: (orgId, locusId)
- `type`: 1=protein-coding, 2=rRNA, 5=tRNA, 6=ncRNA, 7=pseudogene
- `gene`: Common gene name (may be NULL for unknown genes)
- `desc`: Functional description
- Indexed for fast lookups by locusId, sysName, and gene name

#### GeneFitness Table (CRITICAL)
```sql
CREATE TABLE GeneFitness(
   orgId            TEXT     NOT NULL,
   locusId          TEXT     NOT NULL,
   expName          TEXT     NOT NULL,
   fit              REAL     NOT NULL,
   t                REAL     NOT NULL,
   PRIMARY KEY (orgId,locusId,expName)
);
```

**Key Points**:
- **THIS IS THE MAIN FITNESS DATA TABLE**
- Composite primary key: (orgId, locusId, expName)
- `fit`: Fitness value (log2 ratio of abundance end/beginning)
- `t`: t-like test statistic for significance
- **No standard error column** - must calculate from source or use t-statistic
- Estimated **500,000 to 1,000,000 rows** across all organisms/experiments

**Fitness Value Interpretation**:
- `fit = 0`: Gene not important; mutants grew normally
- `fit < 0`: Gene important for fitness; mutants less abundant
- `fit > 0`: Gene detrimental; mutants have growth advantage
- Typical significant range: |fit| > 2 with |t| > 4

#### Experiment Table
```sql
CREATE TABLE Experiment(
   orgId         TEXT       NOT NULL,
   expName       TEXT       NOT NULL,
   expDesc       TEXT       NOT NULL,  /* short form */
   timeZeroSet   TEXT       NOT NULL,
   num           INT        NOT NULL,
   nMapped       INT        NOT NULL,
   nPastEnd      INT        NOT NULL,
   nGenic        INT        NOT NULL,
   nUsed         INT        NOT NULL,
   gMed          INT        NOT NULL,
   gMedt0        INT        NOT NULL,
   gMean         REAL       NOT NULL,
   cor12         REAL       NOT NULL,
   mad12         REAL       NOT NULL,
   mad12c        REAL       NOT NULL,
   mad12c_t0     REAL       NOT NULL,
   opcor         REAL       NOT NULL,
   adjcor        REAL       NOT NULL,
   gccor         REAL       NOT NULL,
   maxFit        REAL       NOT NULL,
   expGroup      TEXT       NOT NULL,
   expDescLong   TEXT       NOT NULL,
   mutantLibrary TEXT       NOT NULL,
   person        TEXT       NOT NULL,
   dateStarted   TEXT       NOT NULL,
   setName       TEXT       NOT NULL,
   seqindex      TEXT       NOT NULL,
   media         TEXT       NOT NULL,
   mediaStrength REAL       NOT NULL,
   temperature   TEXT       NOT NULL,
   pH            TEXT       NOT NULL,
   vessel        TEXT       NOT NULL,
   aerobic       TEXT       NOT NULL,
   liquid        TEXT       NOT NULL,
   shaking       TEXT       NOT NULL,
   condition_1   TEXT       NOT NULL,
   units_1       TEXT       NOT NULL,
   concentration_1 TEXT     NOT NULL,
   condition_2   TEXT       NOT NULL,
   units_2       TEXT       NOT NULL,
   concentration_2 TEXT     NOT NULL,
   condition_3   TEXT       NOT NULL,
   units_3       TEXT       NOT NULL,
   concentration_3 TEXT     NOT NULL,
   condition_4   TEXT       NOT NULL,
   units_4       TEXT       NOT NULL,
   concentration_4 TEXT     NOT NULL,
   growthPlate TEXT NOT NULL,
   growthWells TEXT NOT NULL,
   nGenerations REAL NOT NULL,
   pubId TEXT NOT NULL,
   PRIMARY KEY (orgId, expName)
);
```

**Key Points**:
- Composite primary key: (orgId, expName)
- **Quality Metrics** (first 18 columns): nMapped, cor12, mad12, etc.
- **Experimental Conditions**: Up to 4 conditions with concentrations and units
- **Growth Conditions**: media, temperature, pH, vessel, aerobic, liquid, shaking
- **Metadata**: person, dateStarted, mutantLibrary, pubId

**Critical Quality Metrics**:
- `mad12`: Median absolute difference between gene halves (should be ≤ 0.5)
- `cor12`: Correlation between gene halves
- `gccor`: Correlation with GC content (should be ≤ 0.2)
- `nGenerations`: Total generations of growth

#### FitByExp_[orgId] Tables (Per-Organism)
```sql
-- Example for E. coli Keio collection
CREATE TABLE FitByExp_Keio(
  expName TEXT NOT NULL,
  locusId TEXT NOT NULL,
  fit REAL NOT NULL,
  t REAL NOT NULL,
  PRIMARY KEY (expName,locusId)
);
```

**Key Points**:
- **One table per organism** (not in main schema, dynamically created)
- Stored by experiment for fast lookup of all genes in an experiment
- Same data as GeneFitness but organized differently
- Primary key: (expName, locusId) - reverse of GeneFitness

### 4. Key Relationships

```
Organism (orgId)
    ↓
Gene (orgId, locusId)
    ↓
GeneFitness (orgId, locusId, expName)
    ↑
Experiment (orgId, expName)
```

**Join Pattern for Complete Data**:
```sql
SELECT
    o.genus, o.species, o.strain,
    g.locusId, g.sysName, g.gene, g.desc,
    e.expName, e.expDesc, e.media, e.condition_1, e.concentration_1,
    gf.fit, gf.t
FROM Organism o
JOIN Gene g ON o.orgId = g.orgId
JOIN GeneFitness gf ON g.orgId = gf.orgId AND g.locusId = gf.locusId
JOIN Experiment e ON gf.orgId = e.orgId AND gf.expName = e.expName
WHERE o.orgId = 'Keio' AND ABS(gf.t) > 4;
```

### 5. Identifier Format

**orgId:locusId Pattern**:
- Format used throughout database: "orgId:locusId"
- Example: "Keio:b0001", "WCS417:PP_0001"
- Ensures unique identification across all organisms

**Stable Identifiers**:
- Most use NCBI locus tags (e.g., b0001, SO_1446)
- Some use MicrobesOnline numeric IDs
- Identifiers preserved over time for stable URLs

### 6. External Data Files

**db.StrainFitness.[orgId]** files:
- **NOT in SQLite database**
- Separate tab-delimited files (one per organism)
- Contains per-strain (not per-gene) fitness values
- Must download separately from Figshare
- Seek positions stored in StrainDataSeek table

**Format**:
```
barcode | rcbarcode | scaffold | strand | pos | locusId | n | construct | locusStrand | [exp1] | [exp2] | ...
```

### 7. Data Organization Strategy

**By Organism**:
- Each organism has unique orgId
- All data linked via orgId foreign key
- Allows per-organism queries and downloads

**By Experiment**:
- Each experiment unique within organism
- expName not globally unique (only within orgId)
- FitByExp tables optimize experiment-based queries

**By Gene**:
- Genes unique within organism (orgId + locusId)
- Multiple experiments per gene
- Cofitness calculated across experiments

## Code References

- Database schema: `lib/db_setup_tables.sql:1-540`
- Source repository: https://bitbucket.org/berkeleylab/feba

## Practical Usage Examples

### Query All Organisms
```python
import sqlite3
conn = sqlite3.connect('feba.db')
cursor = conn.cursor()
cursor.execute("SELECT orgId, genus, species, strain FROM Organism")
for row in cursor:
    print(row)
```

### Get Gene Count Per Organism
```sql
SELECT orgId, COUNT(*) as gene_count
FROM Gene
WHERE type = 1  -- protein-coding only
GROUP BY orgId
ORDER BY gene_count DESC;
```

### Find Strong Phenotypes
```sql
SELECT g.orgId, g.locusId, g.sysName, g.gene, g.desc,
       e.expDesc, gf.fit, gf.t
FROM GeneFitness gf
JOIN Gene g ON gf.orgId = g.orgId AND gf.locusId = g.locusId
JOIN Experiment e ON gf.orgId = e.orgId AND gf.expName = e.expName
WHERE ABS(gf.fit) > 2 AND ABS(gf.t) > 4
LIMIT 100;
```

### Get Experiments for Carbon Sources
```sql
SELECT orgId, expName, expDesc, condition_1, concentration_1
FROM Experiment
WHERE expGroup = 'carbon source'
ORDER BY orgId, condition_1;
```

## Related Research

- Part 2: Data extraction and download mechanisms
- Part 3: Phenotype classification and statistical methods
- Part 4: Practical extraction plan with code examples

## Open Questions

1. Exact size of feba.db in February 2024 release (only 2017 size of 5 GB confirmed)
2. Complete list of orgId values for all 48 organisms
3. Whether StrainDataSeek table is populated in downloadable database
