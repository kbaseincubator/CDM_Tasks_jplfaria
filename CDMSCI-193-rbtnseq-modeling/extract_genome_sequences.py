#!/usr/bin/env python3
"""
Extract genome sequences from feba.db ScaffoldSeq table to FASTA files.

Creates one .fna file per organism in data/raw/nucleotide_sequences/
"""

import sqlite3
from pathlib import Path

# Paths
DB_PATH = "data/source/feba.db"
OUTPUT_DIR = Path("data/raw/nucleotide_sequences")

def extract_genome_sequences():
    """Extract all genome sequences from feba.db to FASTA files."""

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get list of all organisms
    cursor.execute("SELECT DISTINCT orgId FROM ScaffoldSeq ORDER BY orgId")
    organisms = [row[0] for row in cursor.fetchall()]

    print(f"Extracting genome sequences for {len(organisms)} organisms from feba.db\n")

    for i, org_id in enumerate(organisms, 1):
        # Get all scaffolds for this organism
        cursor.execute("""
            SELECT scaffoldId, sequence
            FROM ScaffoldSeq
            WHERE orgId = ?
            ORDER BY scaffoldId
        """, (org_id,))

        scaffolds = cursor.fetchall()

        # Create FASTA file
        output_file = OUTPUT_DIR / f"{org_id}_genome.fna"

        with open(output_file, 'w') as f:
            for scaffold_id, sequence in scaffolds:
                # Write FASTA header
                f.write(f">{org_id}|{scaffold_id}\n")

                # Write sequence in 80-character lines (FASTA format standard)
                for j in range(0, len(sequence), 80):
                    f.write(sequence[j:j+80] + '\n')

        total_bp = sum(len(seq) for _, seq in scaffolds)
        file_size = output_file.stat().st_size

        print(f"[{i}/{len(organisms)}] {org_id}: {len(scaffolds)} scaffolds, {total_bp:,} bp ({file_size:,} bytes)")

    conn.close()
    print(f"\nCompleted! Extracted {len(organisms)} genome sequences to {OUTPUT_DIR}/")

if __name__ == "__main__":
    extract_genome_sequences()
