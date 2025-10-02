# COMPREHENSIVE REVIEW: Fitness Browser (FIT) Resource at fit.genomics.lbl.gov

**Date:** 2025-09-30
**Resource URL:** http://fit.genomics.lbl.gov/cgi-bin/myFrontPage.cgi

## EXECUTIVE SUMMARY

The Fitness Browser (FIT) is a comprehensive web-based resource developed by the Arkin lab, Deutschbauer lab, and collaborators at Lawrence Berkeley National Laboratory. It provides access to thousands of genome-wide fitness experiments for diverse bacteria, archaea, and fungi, utilizing Random Barcode Transposon-Site Sequencing (RB-TnSeq) technology. The resource is freely available and serves as a powerful tool for functional genomics research.

**Main URL:** http://fit.genomics.lbl.gov/cgi-bin/myFrontPage.cgi
**Access:** Free and freely available
**Current Status:** 403 error on direct page access (access restrictions in place)

---

## 1. OVERVIEW OF THE FITNESS BROWSER RESOURCE

### 1.1 Purpose and Scope

The Fitness Browser is designed to:
- Display genome-wide mutant fitness data from bacterial, archaeal, and fungal organisms
- Enable researchers to identify gene functions through phenotypic analysis
- Provide interactive tools for comparative genomics and functional annotation
- Support hypothesis generation about poorly-annotated genes

### 1.2 Current Data Coverage (February 2024 Release)

- **7,552 genome-wide fitness experiments**
- **46 bacterial species**
- **2 archaeal species**
- **Identified mutant phenotypes for 11,779 protein-coding genes** that had not been annotated with a specific function
- **2,316 poorly-annotated genes** had high-confidence associations conserved in other bacteria

### 1.3 Technology: RB-TnSeq (Random Barcode Transposon-Site Sequencing)

**Methodology:**
- Every mutant strain has a transposon inserted at a random location in the genome
- Each transposon includes a random barcode for tracking
- Strain abundance is tracked using PCR followed by DNA sequencing ("BarSeq")
- Each fitness experiment uses pools of 30,000 to 500,000 mutant strains
- Fitness = log2 ratio of abundance at experiment end vs. beginning

**Advantages:**
- High-throughput phenotyping
- TnSeq performed once per organism instead of once per sample
- Simple PCR for each BarSeq assay
- 48-96 samples can be sequenced on one Illumina HiSeq lane

---

## 2. COMPLETE LIST OF PAGES AND SECTIONS

### 2.1 Main Navigation Pages

#### A. Front Page (myFrontPage.cgi)
- Main entry point to the Fitness Browser
- Provides overview and access to all features
- Search functionality by gene, sequence, and condition

#### B. Help Page (help.cgi)
- Comprehensive documentation about the Fitness Browser
- Explains methodology, data interpretation, and features
- Tutorial information for using the tools

### 2.2 Search and Query Interfaces

#### A. Search By Gene
- Search for specific genes using locus tags or gene names
- Most genomes use NCBI locus tags and GenBank accessions
- Some use MicrobesOnline numeric identifiers
- Stable identifiers ensure URLs continue to work over time

#### B. Search By Sequence (Fitness BLAST)
**URL:** Integrated into main browser
**Example Page:** https://fit.genomics.lbl.gov/images/fitblast_example.html

**Features:**
- Link from any protein sequence to homologs with fitness data
- Powered by usearch (not traditional BLAST)
- Shows homologs identified by LASTAL
- Displays short results (top hit) and table results (up to 50 homologs)
- Highlights significant phenotypes and strong cofitness

**Fitness BLAST for Genomes:**
- Identify orthologs in the dataset for an entire genome at once
- Batch processing capability

#### C. Search By Condition
- Browse experiments by growth conditions
- Categories include:
  - Carbon sources
  - Nitrogen sources
  - Stress conditions
  - Other experimental conditions

### 2.3 Organism Pages (org.cgi)

**URL Pattern:** `fit.genomics.lbl.gov/cgi-bin/org.cgi?orgId=[ORGANISM_ID]`
**Example:** https://fit.genomics.lbl.gov/cgi-bin/org.cgi?orgId=WCS417

**Features:**
- Complete information about each organism
- List of all experiments for that organism
- Downloadable tables at bottom of page
- Links to genome sequences and gene models
- Metadata about the bacteria
- Additional experiments beyond main publications (for some organisms)

### 2.4 Gene Pages (singleFit.cgi)

**URL Pattern:** `fit.genomics.lbl.gov/cgi-bin/singleFit.cgi?orgId=[ORG]&locusId=[LOCUS]&showAll=[0/1]`

**Features:**
- Gene fitness values across all experiments
- Visualization options (scatterplots, heatmaps)
- **Protein Tab:** Links to other analysis tools
- **Homologs Tab:** Top homologs with fitness data (via protein BLAST)
- Cofitness analysis showing genes with similar fitness patterns
- Links to external databases (RefSeq, UniProt)

**Quality Metrics:**
- T-like test statistic for reliability
- Recommendation: ignore fitness effects with |t| < 4
- For strong positive selection: fitness > 2, t > 5, standard error < 1

### 2.5 Experiment Pages

**Features:**
- Details about specific experimental conditions
- All genes with strong positive or negative fitness effects
- Quality metrics for the experiment
- Tables include experiments that didn't meet quality thresholds due to strong positive selection
- Replicate information when available

### 2.6 Comparative Analysis Pages

#### A. Compare Genes
- Side-by-side comparison of fitness patterns
- Cofitness calculation (Pearson correlation)
- Visual comparison tools

#### B. Compare Experiments
- Compare similar experimental conditions
- Different concentrations of same compound
- Replicate experiments

#### C. Multi-Organism Overview of a Condition (orthCond.cgi)
**URL Pattern:** `fit.genomics.lbl.gov/cgi-bin/orthCond.cgi?expGroup=[GROUP]&condition1=[CONDITION]`

**Examples:**
- Stress experiments in gentamicin sulfate salt
- Nitrogen source experiments in sodium nitrite

**Features:**
- View genes with specific phenotypes across organisms
- Identify conserved functional relationships
- Comparative fitness analysis

### 2.7 Specialized Analysis Pages

#### A. Top Phenotypes
- Genes with strongest fitness effects
- Ranked by significance
- Filter by positive or negative selection

#### B. Top Cofitness
- Gene pairs with highest cofitness scores
- Evidence for functional relationships
- Pathway predictions

**Cofitness Thresholds:**
- Cofitness > 0.75 + rank 1 or 2 = likely same pathway
- Conserved cofitness: both gene pairs and orthologs > 0.6 = strong functional relationship evidence

#### C. Specific Phenotypes
- Browse genes by specific experimental conditions
- Filter by fitness value thresholds
- Condition-specific gene lists

#### D. Outliers
- Genes with unusual fitness patterns
- Quality control features
- Identification of experimental artifacts

#### E. Examples
- Curated examples demonstrating tool usage
- Case studies of functional annotation
- Best practices for data interpretation

### 2.8 Data Download Pages

**Available Downloads:**
- **feba.db** - Complete SQLite3 database (approximately 5 GB as of July 2017)
- **aaseqs** - All protein sequences in FASTA format
- **db.StrainFitness files** - Tab-delimited tables of per-strain fitness values (one per organism)
- **Individual organism tables** - From links at bottom of organism pages
- **BLAST database** - aaseq database for local searches
- **Source code** - code.tar snapshot

**Database Schema:** Available at feba/lib/db_setup_tables.sql in source code

**Direct Database URL:** http://fit.genomics.lbl.gov/cgi_data/feba.db

---

## 3. INTEGRATED TOOLS AND RELATED RESOURCES

### 3.1 PaperBLAST
**URL:** http://papers.genomics.lbl.gov/cgi-bin/litSearch.cgi

**Purpose:** Text mining papers for information about protein homologs

**Features:**
- Links 801,007 protein sequences to 1,268,048 scientific articles
- Updated every 2 months
- Searches 14 curated databases
- Shows similarities to Fitness Browser proteins with mutant phenotypes
- Highlights strong phenotypes (fitness under -2)
- Displays cofitness information
- Integrates Swiss-Prot, GeneRIF, BioLiP, EcoCyc updates

### 3.2 Curated BLAST for Genomes
**URL:** http://papers.genomics.lbl.gov/cgi-bin/genomeSearch.cgi

**Purpose:** Find candidate genes for specific processes or enzymatic activities

**Features:**
- Searches curated descriptions of 100,000+ characterized proteins
- Works with genomes from multiple sources:
  - NCBI assembly database
  - JGI Integrated Microbial Genomes
  - MicrobesOnline
  - Fitness Browser
- Searches six-frame genome translations to find missed proteins
- Incorporates data from BRENDA, CAZy, CharProtDB, MetaCyc, REBASE, Fitness Browser

### 3.3 GapMind
**URL:** http://papers.genomics.lbl.gov/gaps

**Purpose:** Automated annotation of metabolic pathways

**Features:**
- Annotates amino acid biosynthesis in bacteria and archaea
- Covers carbon catabolism pathways
- Describes utilization of 62 carbon sources:
  - 19 amino acids
  - 19 simple sugars or sugar acids
  - 5 disaccharides
  - 11 organic acids
- Incorporates 130 different reactions
- Analyzes a genome in 10-40 seconds
- Color-codes pathway steps by confidence (high/medium/low)
- Identifies "known gaps" (missing enzymes in organisms that can grow)
- Avoids error-prone transitive annotations
- Relies on database of experimentally characterized proteins
- Uses ublast and HMMer with TIGRFam models
- Correctly handles fusion proteins and split proteins

**Typical Results:** 1-2 gaps in amino acid biosynthesis for bacteria that make all 20 amino acids

### 3.4 SitesBLAST
**URL:** http://papers.genomics.lbl.gov/cgi-bin/sites.cgi

**Purpose:** Compare functional residues between proteins

**Features:**
- Database of 170,045 proteins with known functional residues
- Includes ligand-binding and active-site residues from BioLiP crystal structures
- Swiss-Prot features with experimental evidence
- Shows whether functional residues are conserved
- Can identify potential functional residues ~50% of the time for random proteins
- Interactive analysis of functional residues in protein families

**Companion Tool:** Sites on a Tree (for phylogenetic context)

### 3.5 fast.genomics
**URL:** http://fast.genomics.lbl.gov

**Purpose:** Fast comparative genome browser for diverse bacteria and archaea

**Features:**
- Representative genomes for 7,312 genera (April 2025 GTDB update)
- Split database architecture for speed:
  - Main database: 1 representative per genus (6,377 genera)
  - Order-specific databases: up to 10 representatives per species
- View gene neighborhoods
- Taxonomic distribution of protein homologs
- Co-occurrence analysis (phylogenetic profiling)
- Compare prevalence of two different proteins
- Accelerated searches (usually seconds)
- GitHub repository: https://github.com/morgannprice/fast.genomics

**Publication:** Price & Arkin, PLOS ONE, April 2024

---

## 4. FUNGAL FITNESS BROWSER

**URL:** http://fungalfit.genomics.lbl.gov/cgi-bin/myFrontPage.cgi

**Purpose:** Parallel resource for fungal organisms

**Technology:** Same RB-TnSeq methodology as bacterial version

**Organisms Include:**
- Saccharomyces cerevisiae
- Rhodosporidium toruloides
- Other fungal species

**Related Resource:** Supplementary Data for Functional Profiling of Saccharomyces cerevisiae genome at https://genomics.lbl.gov/YeastFitnessData/

---

## 5. KEY FEATURES AND CAPABILITIES

### 5.1 Data Visualization

**Available Visualizations:**
- Scatterplots of fitness values
- Heatmaps for experiment comparison
- Gene neighborhood views
- Taxonomic distribution charts
- Cofitness correlation plots

### 5.2 Quality Control and Metrics

**Fitness Value Quality:**
- T-like test statistic for significance
- Standard error calculations
- Read count requirements (mean ≥ 10 for strong positive effects)
- Replicate experiment validation

**Experiment Quality:**
- Quality thresholds for experiments
- Identification of outliers
- Strong positive selection criteria

### 5.3 Functional Annotation Capabilities

**Direct Evidence:**
- Mutant phenotypes in specific conditions
- Gene essentiality determination
- Growth requirement identification

**Comparative Evidence:**
- Cofitness analysis (genes with similar fitness patterns)
- Conserved cofitness across species
- Ortholog comparisons

**Integration with Literature:**
- PaperBLAST connections
- Links to characterized homologs
- Curated database integration

### 5.4 Programmatic Access

**URL-based Queries:**
- Direct linking to genes, organisms, experiments
- Stable identifiers over time
- URL parameters for automated queries

**Data Downloads:**
- Complete SQLite database
- Per-organism fitness tables
- Protein sequence databases
- Source code availability

**Example URL Structure:**
```
Gene: fit.genomics.lbl.gov/cgi-bin/singleFit.cgi?orgId=[ORG]&locusId=[LOCUS]
Organism: fit.genomics.lbl.gov/cgi-bin/org.cgi?orgId=[ORG_ID]
Condition: fit.genomics.lbl.gov/cgi-bin/orthCond.cgi?expGroup=[GROUP]&condition1=[CONDITION]
```

### 5.5 Integration Features

**Embed in Web Pages:**
- Can incorporate into websites with just a few lines of code
- Stable URLs for citation
- Direct linking capabilities

**Cross-tool Integration:**
- Seamless connection with PaperBLAST
- Integration with GapMind pathway analysis
- Links to Curated BLAST results
- Connection to fast.genomics browser

---

## 6. HOW SECTIONS CONNECT TOGETHER

### 6.1 Workflow: From Sequence to Function

1. **Entry Point:** Search by gene name, sequence, or condition
2. **Gene Page:** View fitness data, find homologs
3. **Protein Tab:** Access PaperBLAST, Curated BLAST, other tools
4. **Homologs Tab:** Identify related genes with fitness data
5. **Cofitness Analysis:** Find functionally related genes
6. **Literature Integration:** Connect to scientific articles via PaperBLAST
7. **Pathway Context:** Use GapMind for metabolic pathway placement
8. **Functional Residues:** Verify with SitesBLAST
9. **Comparative Genomics:** Check distribution with fast.genomics

### 6.2 Data Flow Architecture

```
Primary Data Sources:
    ↓
RB-TnSeq Experiments → BarSeq Analysis → Fitness Values
    ↓                                           ↓
SQLite Database (feba.db) ← Quality Control ← Statistical Analysis
    ↓                            ↓
Web Interface (CGI scripts)    Data Downloads
    ↓
Integration Layer:
- PaperBLAST (literature)
- Curated BLAST (characterized proteins)
- GapMind (pathways)
- SitesBLAST (functional sites)
- fast.genomics (comparative)
```

### 6.3 Cross-Reference System

**Internal Links:**
- Gene pages ↔ Organism pages
- Experiment pages ↔ Gene pages
- Cofitness pairs ↔ Gene comparisons
- Homolog tabs ↔ Fitness BLAST

**External Links:**
- RefSeq and UniProt identifiers
- NCBI locus tags
- MicrobesOnline integration
- Literature citations

---

## 7. SUPPLEMENTAL DATA REPOSITORIES

### 7.1 Main Supplemental Sites

#### A. Mutant Phenotypes for Bacterial Genes
**URL:** https://genomics.lbl.gov/supplemental/bigfit/

**Content:**
- Complete dataset for 32 bacterial species
- Genome sequences and gene models
- Supplementary tables from Nature publication
- Mapping to RefSeq and UniProt
- R images with complete dataset
- TnSeq read mapping information
- Complete dataset tarball (84 GB)

**Important Note:** Authors disclosed issues with original sucrose and D-mannitol stock solutions - recommend disregarding those specific experiments

#### B. Validating Regulatory Predictions
**URL:** https://genomics.lbl.gov/supplemental/cofittf/

**Purpose:** Uses mutant fitness data to validate regulatory predictions from RegPrecise

#### C. Strong Selection Study
**URL:** https://genomics.lbl.gov/supplemental/strongselection/

**Content:** Comparison of costs and benefits of 86% of proteins in E. coli K-12 during growth in minimal glucose medium using ribosomal profiling and transposon mutant assays

#### D. Source Data Repository
**URL:** https://genomics.lbl.gov/supplemental/fitness-bioinf/

**Content:** Additional fitness bioinformatics resources and data

---

## 8. SCIENTIFIC PUBLICATIONS

### 8.1 Major Nature Publication

**Title:** "Mutant phenotypes for thousands of bacterial genes of unknown function"

**Citation:** Price MN, Wetmore KM, Waters RJ, et al. Nature. 2018 May;557(7706):503-509. doi: 10.1038/s41586-018-0124-0

**Free Author Version:** Available at https://escholarship.org/uc/item/7c96t04w

**Key Findings:**
- Genome-wide mutant fitness data from 32 diverse bacteria
- Identified phenotypes for 11,779 previously uncharacterized genes
- Proposed specific functions for unknown proteins
- 2,316 high-confidence associations conserved across bacteria

### 8.2 Key mBio Publications

**RB-TnSeq Methodology:**
- Wetmore KM, Price MN, Waters RJ, et al. (2015) "Rapid quantification of mutant fitness in diverse bacteria by sequencing randomly barcoded transposons" mBio 6(3):e00306-15

**Selection on Bacterial Genomes:**
- Price MN, et al. (2015) "Weakly deleterious mutations and low rates of recombination limit the impact of natural selection on bacterial genomes" mBio 6(5):e01302-15

**Desulfovibrio Study:**
- Kuehl JV, Price MN, et al. (2014) "Functional genomics with a comprehensive library of transposon mutants for the sulfate-reducing bacterium Desulfovibrio alaskensis G20" mBio 5:e01041-14

**Transcription Start Sites:**
- Shao W, Price MN, Deutschbauer AM, et al. (2014) "Conservation of transcription start sites within genes across a bacterial genus" mBio 5:e01398-14

### 8.3 Interactive Tools Publication

**Title:** "Interactive tools for functional annotation of bacterial genomes"

**Citation:** Database, February 2024. doi: 10.1093/database/baae089

**Available at:** https://pmc.ncbi.nlm.nih.gov/articles/PMC11378808/

**Content:** Comprehensive guide to using all tools together for functional annotation

---

## 9. DATA RELEASES AND ARCHIVES

### 9.1 Figshare Releases

**February 2024 Release:**
- URL: https://figshare.com/articles/dataset/25236931
- 7,552 experiments, 46 bacteria, 2 archaea
- Files: feba.db, aaseqs, db.StrainFitness.*, code.tar
- License: Creative Commons Attribution 4.0

**November 2021 Release:**
- URL: https://figshare.com/articles/dataset/16913530

**November 2020 Release:**
- URL: https://figshare.com/articles/dataset/13172087

**June 2017 Release:**
- URL: https://figshare.com/articles/dataset/5134840

### 9.2 fast.genomics Release

**2023 Release:**
- URL: https://figshare.com/articles/dataset/24010353
- Fast comparative genome browser data

---

## 10. SOURCE CODE AND DEVELOPMENT

### 10.1 Code Repository

**Main Repository:** https://bitbucket.org/berkeleylab/feba
**Git URL:** https://bitbucket.org/berkeleylab/feba.git

**Code Structure:**
- Perl CGI scripts for web interface
- SQLite database schema (lib/db_setup_tables.sql)
- Analysis pipeline for RB-TnSeq data
- Visualization tools

### 10.2 Related GitHub Repositories

**Morgan Price's Repositories:**
- **fast.genomics:** https://github.com/morgannprice/fast.genomics - Genome browser for bacteria and archaea
- **PaperBLAST:** https://github.com/morgannprice/PaperBLAST - Find papers about proteins
- **BobaseqFitness:** https://github.com/morgannprice/BobaseqFitness - R scripts for Boba-seq analysis

**Community Repositories:**
- **RB-TnSeq:** https://github.com/beckham-lab/RB-TnSeq - Scripts for estimating mutant fitness

### 10.3 Development Team

**Primary Developers:**
- Morgan Price (computational tools, analysis)
- Victoria Lo
- Wenjun Shao

**Principal Investigators:**
- Adam P. Arkin (Arkin lab)
- Adam M. Deutschbauer (Deutschbauer lab)

**Funding:** Office of Science, US Department of Energy

---

## 11. TECHNICAL SPECIFICATIONS

### 11.1 Database Structure

**Format:** SQLite3 (version 3)
**Size:** Approximately 5 GB (July 2017); grows with updates
**Identifier Format:** "orgId:locusId"

**Main Tables (from schema):**
- Organism information
- Gene annotations
- Experiment metadata
- Fitness values
- Cofitness calculations
- Strain-level fitness data (external files)

### 11.2 Search Technology

**Protein Similarity:**
- LASTAL for Fitness BLAST
- usearch for Fitness BLAST for genomes
- Traditional BLAST for single sequence and homologs page
- HMMer for enzyme models (GapMind)
- ublast for fast searches (GapMind)

### 11.3 Statistical Methods

**Fitness Calculation:**
- Log2 ratio of end vs. beginning abundance
- Reads per barcode as abundance proxy
- Normalization for experimental noise

**Significance Testing:**
- T-like test statistic
- Standard error estimation
- Recommended threshold: |t| ≥ 4
- Strong positive selection: fitness > 2, t > 5, SE < 1, mean reads ≥ 10

**Cofitness:**
- Pearson correlation of fitness patterns
- Threshold: > 0.75 for functional relationship
- Conserved cofitness: > 0.6 in both species

---

## 12. USE CASES AND APPLICATIONS

### 12.1 Gene Function Prediction

**Scenario:** Unknown protein needs functional annotation

**Workflow:**
1. Search gene in Fitness Browser
2. Examine fitness phenotypes across conditions
3. Check cofitness with characterized genes
4. Use PaperBLAST to find literature on homologs
5. Verify with Curated BLAST for characterized proteins
6. Check functional residues with SitesBLAST
7. Place in pathway context with GapMind

### 12.2 Pathway Analysis

**Scenario:** Investigating metabolic pathway

**Workflow:**
1. Use GapMind to identify pathway genes
2. Check fitness data for pathway genes
3. Examine cofitness within pathway
4. Identify missing steps ("gaps")
5. Use Curated BLAST to find candidates for gaps
6. Validate with experimental fitness data

### 12.3 Comparative Genomics

**Scenario:** Understanding gene distribution across taxa

**Workflow:**
1. Search gene in fast.genomics
2. View taxonomic distribution
3. Check gene neighborhoods
4. Compare with orthologs in Fitness Browser
5. Examine conserved cofitness
6. Identify functional conservation patterns

### 12.4 Transporter Identification

**Example from Publications:**
- Identify genes with fitness defects in specific nutrient conditions
- Check cofitness with known transporters
- Verify substrate specificity through condition-specific phenotypes
- Validate with gene neighborhood analysis
- Confirm with literature via PaperBLAST

---

## 13. LIMITATIONS AND CONSIDERATIONS

### 13.1 Technical Limitations

**Transposon Insertion Bias:**
- Insertions near gene start/end less likely to cause knockout
- Site-specific nucleotide biases affect insertion frequencies
- Some genomic regions difficult to disrupt

**Essential Genes:**
- Cannot obtain fitness data for absolutely essential genes
- "Likely essential" designation based on lack of insertions
- May miss conditional essentiality

**Quality Thresholds:**
- Some experiments don't meet quality standards
- Strong positive selection can complicate analysis
- Experimental noise in some conditions

### 13.2 Biological Limitations

**Known Gaps:**
- Some pathways have missing enzymes (unknown mechanisms)
- Organisms can grow despite apparent pathway gaps
- Alternative pathways not always identified

**Condition Coverage:**
- Cannot test all possible growth conditions
- Some phenotypes only visible in specific contexts
- Gene redundancy can mask phenotypes

**Annotation Challenges:**
- Transitive annotation errors common
- Protein function context-dependent
- Multiple functions for some proteins

### 13.3 Data Considerations

**Strain-Specific Issues:**
- Sucrose and D-mannitol data in original publication unreliable
- Stock solution contamination disclosed
- Check organism-specific notes

**Database Updates:**
- Cofitness values may not match between releases
- Additional experiments added over time
- Version-specific data important for reproducibility

---

## 14. BEST PRACTICES FOR USING THE RESOURCE

### 14.1 Data Interpretation

**Confidence Building:**
1. Check multiple lines of evidence (not single fitness value)
2. Compare replicate experiments
3. Look at similar conditions (dose-response)
4. Examine ortholog phenotypes
5. Verify cofitness relationships
6. Consult literature via PaperBLAST

**Quality Assessment:**
1. Check t-statistic (|t| ≥ 4 recommended)
2. Verify standard error
3. Look at read counts
4. Consider experiment quality metrics
5. Check for outliers

### 14.2 Integration Strategy

**Multi-Tool Approach:**
1. Start with Fitness Browser phenotypes
2. Add PaperBLAST literature context
3. Use GapMind for pathway placement
4. Verify with Curated BLAST
5. Check conserved residues with SitesBLAST
6. Examine distribution with fast.genomics

### 14.3 Citation and Data Usage

**Citing the Resource:**
- Primary citation: Price et al., Nature 2018
- Methodology: Wetmore et al., mBio 2015
- Specific releases: Use Figshare DOIs
- Interactive tools: Database 2024 publication

**Data Download:**
- Use official Figshare releases for reproducibility
- Note version/date in methods
- Check for organism-specific caveats
- Preserve metadata with downloaded data

---

## 15. FUTURE DIRECTIONS AND UPDATES

### 15.1 Database Growth

**Ongoing Additions:**
- New organisms continuously added
- Additional experiments for existing organisms
- Updated annotations and reannotations
- Integration of new experimental data

### 15.2 Tool Development

**Recent Updates:**
- February 2024: Latest database release
- April 2025: fast.genomics GTDB update
- Ongoing: PaperBLAST database updates (every 2 months)

### 15.3 Community Contributions

**Open Source:**
- Code available on Bitbucket
- Community can adapt and extend
- RB-TnSeq methodology adopted by other labs
- Independent implementations (e.g., beckham-lab)

---

## 16. CONTACT AND SUPPORT

### 16.1 Primary Resources

**Main Site:** http://fit.genomics.lbl.gov
**Help Page:** http://fit.genomics.lbl.gov/cgi-bin/help.cgi
**Developer:** Morgan Price (morgannprice.org)

### 16.2 Related Resources

**ENIGMA Project:** https://enigma.lbl.gov/resources/
**Lawrence Berkeley Lab:** https://genomics.lbl.gov

### 16.3 Scientific Community

**Publications:** Morgan Price's publication list at morgannprice.org/publicat.htm
**Google Scholar:** Search for "Adam Deutschbauer" and "Morgan Price"

---

## 17. CONCLUSION

The Fitness Browser represents a comprehensive, well-integrated ecosystem for functional genomics research in bacteria, archaea, and fungi. With over 7,500 genome-wide experiments, integration with multiple analytical tools (PaperBLAST, GapMind, SitesBLAST, Curated BLAST, fast.genomics), and extensive documentation, it provides researchers with unprecedented access to mutant phenotype data.

### Key Strengths:

1. **Scale:** Largest collection of bacterial fitness data
2. **Quality:** Rigorous statistical methods and quality control
3. **Integration:** Seamless connection with complementary tools
4. **Accessibility:** Free, web-based, with downloadable data
5. **Documentation:** Extensive help and publication support
6. **Openness:** Open source code and Creative Commons data
7. **Maintenance:** Regular updates and improvements
8. **Innovation:** RB-TnSeq methodology enables high-throughput analysis

### Impact:

The resource has enabled functional annotation of thousands of previously uncharacterized genes, proposed specific functions for unknown proteins, and provided a model for high-throughput functional genomics. It continues to serve as a critical resource for the microbiology and genomics communities.

---

## APPENDIX: URL REFERENCE GUIDE

### Main Pages
- Front Page: `http://fit.genomics.lbl.gov/cgi-bin/myFrontPage.cgi`
- Help: `http://fit.genomics.lbl.gov/cgi-bin/help.cgi`

### Query Pages
- Gene: `http://fit.genomics.lbl.gov/cgi-bin/singleFit.cgi?orgId=[ORG]&locusId=[LOCUS]&showAll=[0/1]`
- Organism: `http://fit.genomics.lbl.gov/cgi-bin/org.cgi?orgId=[ORG_ID]`
- Cross-organism condition: `http://fit.genomics.lbl.gov/cgi-bin/orthCond.cgi?expGroup=[GROUP]&condition1=[CONDITION]`

### Data Downloads
- Database: `http://fit.genomics.lbl.gov/cgi_data/feba.db`
- Protein sequences: `http://fit.genomics.lbl.gov/cgi_data/aaseqs`

### Integrated Tools
- PaperBLAST: `http://papers.genomics.lbl.gov/cgi-bin/litSearch.cgi`
- Curated BLAST: `http://papers.genomics.lbl.gov/cgi-bin/genomeSearch.cgi`
- GapMind: `http://papers.genomics.lbl.gov/gaps`
- SitesBLAST: `http://papers.genomics.lbl.gov/cgi-bin/sites.cgi`
- fast.genomics: `http://fast.genomics.lbl.gov`

### Related Resources
- Fungal FIT: `http://fungalfit.genomics.lbl.gov/cgi-bin/myFrontPage.cgi`
- BigFit supplement: `https://genomics.lbl.gov/supplemental/bigfit/`
- Source code: `https://bitbucket.org/berkeleylab/feba`

---

**Report Generated:** Based on comprehensive web research conducted on 2025-09-30
**Note:** Some pages returned 403 errors during direct access attempts, but comprehensive information was gathered through documentation, publications, and related resources.
