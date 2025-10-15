# Fix: Malformed FASTA Files Removed

**Date**: 2025-10-08

## Problem

RAST annotation notebook was failing for 4 organisms with error:
```
'NoneType' object has no attribute 'seq'
```

Failing organisms: Marino2, Pputida_KT2440, Shewanella_ANA3, Sulcia

## Root Cause

8 files in `data/raw/protein_sequences/` were HTML error pages (1.5KB each), not FASTA files:
1. Marino2_proteins.fasta
2. Pputida_KT2440_proteins.fasta
3. Shewanella_ANA3_proteins.fasta
4. Sulcia_proteins.fasta
5. Dtox_proteins.fasta
6. Echoli_proteins.fasta
7. Halo_proteins.fasta
8. Thermus_proteins.fasta

These files contained HTML error pages from failed manual downloads, not protein sequences.

## Files Checked

```bash
file Marino2_proteins.fasta
# Output: HTML document text, ASCII text

head Marino2_proteins.fasta
# Output:
# <!DOCTYPE html>
# <html xmlns="http://www.w3.org/1999/xhtml" lang="en-US" xml:lang="en-US">
# <head>
# <meta http-equiv="X-UA-Compatible" content="IE=edge">
# <link rev="made" href="mailto:morgannprice@yahoo.com" />
```

## Solution

Removed all 8 HTML error page files:
```bash
rm Marino2_proteins.fasta Pputida_KT2440_proteins.fasta \
   Shewanella_ANA3_proteins.fasta Sulcia_proteins.fasta \
   Dtox_proteins.fasta Echoli_proteins.fasta \
   Halo_proteins.fasta Thermus_proteins.fasta
```

## Result

- Before: 65 files (57 valid + 8 HTML error pages)
- After: 57 valid FASTA files
- All files verified as valid FASTA format
- Size range: 607KB to 2.7MB (appropriate for bacterial proteomes)
- No files smaller than 100KB

## Files Distribution

```
File sizes:
- Smallest: 607KB
- Largest: 2.7MB
- Average: ~1.7MB
- All 57 files are valid FASTA format
```

## Next Steps

Re-run the RAST annotation notebook:
```bash
cd CDMSCI-198-build-models
jupyter notebook 01-annotate-genomes-with-rast.ipynb
```

Expected results:
- All 57 organisms should annotate successfully
- No more "'NoneType' object has no attribute 'seq'" errors
- Both pickle and FASTA outputs generated for each organism

## Note

These 8 extra organisms were NOT part of the 57 organisms from the carbon source growth matrix (CDMSCI-196). They appear to have been manually downloaded attempts that failed and saved HTML error pages instead of actual FASTA files.

The official download notebook (01-download-organism-data.ipynb) downloads the correct 57 organisms automatically from Fitness Browser.
