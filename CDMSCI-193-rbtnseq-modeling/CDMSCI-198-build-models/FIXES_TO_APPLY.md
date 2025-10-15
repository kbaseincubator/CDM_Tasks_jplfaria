# Fixes to Apply to RAST Annotation Notebook

## Add FASTA Output Functionality

Currently the notebook only saves pickle files. You want RAST-annotated FASTA files too.

### Step 1: Update Configuration Cell

Add FASTA output directory:

```python
# Paths
FASTA_DIR = Path('../data/raw/protein_sequences')
OUTPUT_DIR = Path('results/genomes')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Add this line:
FASTA_OUTPUT_DIR = Path('results/fasta_annotated')
FASTA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = Path('results/rast_annotation_log.txt')

print(f"Configuration set")
print(f"  Input directory: {FASTA_DIR}")
print(f"  Output directory: {OUTPUT_DIR}")
print(f"  FASTA output directory: {FASTA_OUTPUT_DIR}")  # Add this line
print(f"  Log file: {LOG_FILE}")
```

### Step 2: Add FASTA Save Function

Add this function to the "Helper Functions" cell (after `save_genome`):

```python
def save_genome_as_fasta(genome, organism_id):
    """Save annotated genome as FASTA file with functional annotations"""
    output_file = FASTA_OUTPUT_DIR / f"{organism_id}_RAST.fasta"

    with open(output_file, 'w') as f:
        for feature in genome.features:
            # Create FASTA header with annotations
            header = f">{feature.id}"

            # Add functional roles if annotated
            if feature.ontology_terms:
                roles = "; ".join(feature.ontology_terms[:3])  # First 3 roles
                header += f" | {roles}"
            else:
                header += " | Hypothetical protein"

            # Write header and sequence
            f.write(header + '\n')
            f.write(feature.seq + '\n')

    return output_file
```

Also add function to check if FASTA already exists:

```python
def fasta_already_exists(organism_id):
    """Check if FASTA output already exists"""
    output_file = FASTA_OUTPUT_DIR / f"{organism_id}_RAST.fasta"
    return output_file.exists()
```

### Step 3: Update Annotation Loop

In the "Annotate Genomes" cell, replace the section after annotation completes:

Replace this:
```python
        # Count annotations
        annotated_features = sum(1 for f in genome.features if f.ontology_terms)
        log_message(f"  Annotated features: {annotated_features}/{len(genome.features)}")

        # Save genome
        output_file = save_genome(genome, organism_id)
        log_message(f"  ✓ Saved to: {output_file.name}")
```

With this:
```python
        # Count annotations
        annotated_features = sum(1 for f in genome.features if f.ontology_terms)
        log_message(f"  Annotated features: {annotated_features}/{len(genome.features)}")

        # Save genome as pickle
        output_file = save_genome(genome, organism_id)
        log_message(f"  ✓ Saved pickle: {output_file.name}")

        # Save genome as annotated FASTA
        fasta_file = save_genome_as_fasta(genome, organism_id)
        log_message(f"  ✓ Saved FASTA: {fasta_file.name}")
```

### Step 4: Update Skip Check

In the "Annotate Genomes" cell, update the already annotated check:

Replace this:
```python
    # Check if already annotated
    if genome_already_annotated(organism_id):
        log_message(f"  ✓ Already annotated - skipping")
        skipped += 1
        continue
```

With this:
```python
    # Check if already annotated (both pickle and FASTA exist)
    if genome_already_annotated(organism_id) and fasta_already_exists(organism_id):
        log_message(f"  ✓ Already annotated - skipping")
        skipped += 1
        continue
```

### Step 5: Update Summary Cell

Update the summary to mention both outputs:

Replace:
```python
**Files Created**:
- `results/genomes/{organism_id}_genome.pkl` - Annotated genome objects (57 files)
- `results/rast_annotation_log.txt` - Annotation log with timestamps
```

With:
```python
**Files Created**:
- `results/genomes/{organism_id}_genome.pkl` - Annotated genome objects (57 files)
- `results/fasta_annotated/{organism_id}_RAST.fasta` - Annotated FASTA files (57 files)
- `results/rast_annotation_log.txt` - Annotation log with timestamps
```

## FASTA File Format

The annotated FASTA files will look like:

```
>protein001 | Glyceraldehyde-3-phosphate dehydrogenase; Gluconeogenesis; Glycolysis
MKVAIINGFGRIGRLVTRAAFNSGKVDVVAINDPFIDLNYMVYMFQYDSTHGKFHGTVKAENGKLVINGNPITIFQERDPSKIKWGDAGAAEYVVESTGVFTTMEKAGAHLKGGAKRVIISAPAKDIEDKGVGHSGGILSMANAGPNTNGSQFFICTAGGKALELGERLMVQNIFGEKGYKPDKTTYKNKASGQRVGDLLVVYDLGGGTF...
>protein002 | Phosphoglycerate kinase; Glycolysis
MSKIGTIQGIVSSGRKGQALEALAPYAKDVAVLELDTPNEISAALEELGVPVTVASSHIKSEVVAEIAAANPFVQPLFGDEILAVGGAAYNKEIADAMKQRGIELPGVINAIANVPRKLKLDIIPDGDMSHDDPETMNEALKAAALGPLVFGYQAGAIEQGVGRIAGDYQAKLRQTGGGLRVPAVGVPGILLPGLVGYLTELQGLDLQTAIGL...
>protein003 | Hypothetical protein
MKLVAFGQSPLVRVLHPDFLSRFGFKAGVVVGLTDSGTSHQFADLLQQLKQRGVQPLDRLRELFADGAVLPQVYGEQGKPVLNATRHDAQPQGGLVGVGTGQWQVLEGVAPQAPALVLDFKRLVGSAALIGGGSLVGQQRTALEQVAFPVVGQFPPLSIPEKPVVVQVLGGLGQNPRAAEPQVPVLGEALRSKIAQVQQTEPAQVGGVL...
```

## Benefits

1. **Portable format** - FASTA files can be used with other tools
2. **Human readable** - Easy to inspect annotations
3. **Standard format** - Compatible with BLAST, alignment tools, etc.
4. **Backup** - Pickle files can break between Python versions, FASTA is stable

## Notes

- Each protein header includes functional roles from RAST annotation
- Hypothetical proteins (no annotation) are labeled clearly
- Only first 3 roles included in header (to keep it readable)
- Full annotations still available in pickle file if needed
