#!/usr/bin/env python3
"""
Create organism × condition growth/no-growth matrix from Fitness Browser RBTnSeq data

Usage:
    python create_growth_matrix.py --db feba.db --output growth_matrix.csv

Output:
    - Binary matrix: 1 = organism has data for condition (growth), 0 = no data
    - Rows = organisms (orgId)
    - Columns = conditions (expGroup + condition_1)
"""

import sqlite3
import pandas as pd
import argparse
from pathlib import Path
import sys


def load_organism_condition_pairs(conn, quality_filter=True):
    """
    Load all organism-condition pairs that have fitness data

    Args:
        conn: SQLite connection to feba.db
        quality_filter: If True, only include high-quality experiments

    Returns:
        DataFrame with columns: orgId, expGroup, condition_1, n_experiments
    """
    print("Loading organism-condition pairs from database...")

    # Base query
    query = """
    SELECT DISTINCT
        gf.orgId,
        e.expGroup,
        e.condition_1,
        COUNT(DISTINCT gf.expName) as n_experiments,
        COUNT(DISTINCT e.expName) as n_experiments_total
    FROM GeneFitness gf
    JOIN Experiment e ON gf.orgId = e.orgId AND gf.expName = e.expName
    WHERE 1=1
    """

    # Add quality filters if requested
    if quality_filter:
        query += """
        AND e.num > 0  -- Has fitness data
        AND e.gMed >= 50  -- Sufficient read depth
        AND (e.mad12 IS NULL OR e.mad12 <= 0.5)  -- Good gene-half consistency
        """

    query += """
    GROUP BY gf.orgId, e.expGroup, e.condition_1
    ORDER BY gf.orgId, e.expGroup, e.condition_1
    """

    df = pd.read_sql_query(query, conn)

    print(f"Found {len(df)} organism-condition pairs")
    print(f"  Unique organisms: {df['orgId'].nunique()}")
    print(f"  Unique condition groups: {df['expGroup'].nunique()}")
    print(f"  Unique conditions: {df.groupby(['expGroup', 'condition_1']).ngroups}")

    return df


def create_binary_matrix(df, condition_col='condition_1'):
    """
    Create binary growth matrix from organism-condition pairs

    Args:
        df: DataFrame with orgId and condition columns
        condition_col: Name of condition column to use

    Returns:
        Binary DataFrame (1 = has data, 0 = no data)
    """
    print("\nCreating binary matrix...")

    # Create pivot table
    matrix = df.pivot_table(
        index='orgId',
        columns=condition_col,
        values='n_experiments',
        aggfunc='sum',
        fill_value=0
    )

    # Convert to binary
    binary_matrix = (matrix > 0).astype(int)

    print(f"Matrix shape: {binary_matrix.shape[0]} organisms × {binary_matrix.shape[1]} conditions")
    print(f"  Total cells: {binary_matrix.size:,}")
    print(f"  Cells with data: {binary_matrix.sum().sum():,}")
    print(f"  Coverage: {100 * binary_matrix.sum().sum() / binary_matrix.size:.2f}%")

    return binary_matrix


def create_hierarchical_matrix(df):
    """
    Create binary matrix with hierarchical columns (expGroup, condition_1)

    Args:
        df: DataFrame with orgId, expGroup, condition_1

    Returns:
        Binary DataFrame with MultiIndex columns
    """
    print("\nCreating hierarchical matrix (expGroup × condition_1)...")

    # Create pivot table with hierarchical columns
    matrix = df.pivot_table(
        index='orgId',
        columns=['expGroup', 'condition_1'],
        values='n_experiments',
        aggfunc='sum',
        fill_value=0
    )

    # Convert to binary
    binary_matrix = (matrix > 0).astype(int)

    print(f"Matrix shape: {binary_matrix.shape[0]} organisms × {binary_matrix.shape[1]} conditions")
    print(f"  Total cells: {binary_matrix.size:,}")
    print(f"  Cells with data: {binary_matrix.sum().sum():,}")
    print(f"  Coverage: {100 * binary_matrix.sum().sum() / binary_matrix.size:.2f}%")

    return binary_matrix


def get_matrix_statistics(matrix):
    """
    Calculate and display matrix statistics

    Args:
        matrix: Binary growth matrix

    Returns:
        dict with statistics
    """
    print("\n" + "="*70)
    print("MATRIX STATISTICS")
    print("="*70)

    stats = {}

    # Overall
    stats['n_organisms'] = len(matrix)
    stats['n_conditions'] = len(matrix.columns)
    stats['total_cells'] = matrix.size
    stats['cells_with_data'] = matrix.sum().sum()
    stats['coverage_pct'] = 100 * stats['cells_with_data'] / stats['total_cells']

    print(f"\nOverall:")
    print(f"  Organisms: {stats['n_organisms']}")
    print(f"  Conditions: {stats['n_conditions']}")
    print(f"  Total cells: {stats['total_cells']:,}")
    print(f"  Cells with data: {stats['cells_with_data']:,}")
    print(f"  Coverage: {stats['coverage_pct']:.2f}%")

    # Per organism
    per_org = matrix.sum(axis=1).sort_values(ascending=False)
    stats['max_conditions_per_org'] = per_org.max()
    stats['min_conditions_per_org'] = per_org.min()
    stats['median_conditions_per_org'] = per_org.median()
    stats['mean_conditions_per_org'] = per_org.mean()

    print(f"\nPer Organism:")
    print(f"  Most tested: {per_org.index[0]} ({per_org.iloc[0]} conditions)")
    print(f"  Least tested: {per_org.index[-1]} ({per_org.iloc[-1]} conditions)")
    print(f"  Median: {stats['median_conditions_per_org']:.1f} conditions")
    print(f"  Mean: {stats['mean_conditions_per_org']:.1f} conditions")

    # Per condition
    per_cond = matrix.sum(axis=0).sort_values(ascending=False)
    stats['max_organisms_per_cond'] = per_cond.max()
    stats['min_organisms_per_cond'] = per_cond.min()
    stats['median_organisms_per_cond'] = per_cond.median()
    stats['mean_organisms_per_cond'] = per_cond.mean()

    print(f"\nPer Condition:")
    print(f"  Most tested: {per_cond.index[0]} ({per_cond.iloc[0]} organisms)")
    print(f"  Least tested: {per_cond.index[-1]} ({per_cond.iloc[-1]} organisms)")
    print(f"  Median: {stats['median_organisms_per_cond']:.1f} organisms")
    print(f"  Mean: {stats['mean_organisms_per_cond']:.1f} organisms")

    return stats


def create_condition_group_matrices(df):
    """
    Create separate matrices for each condition group (carbon source, nitrogen source, etc.)

    Args:
        df: DataFrame with orgId, expGroup, condition_1

    Returns:
        dict of matrices by expGroup
    """
    print("\n" + "="*70)
    print("CREATING CONDITION-SPECIFIC MATRICES")
    print("="*70)

    matrices = {}

    for group in sorted(df['expGroup'].unique()):
        print(f"\n{group}:")
        group_df = df[df['expGroup'] == group]

        matrix = group_df.pivot_table(
            index='orgId',
            columns='condition_1',
            values='n_experiments',
            aggfunc='sum',
            fill_value=0
        )

        binary_matrix = (matrix > 0).astype(int)

        print(f"  Shape: {binary_matrix.shape[0]} organisms × {binary_matrix.shape[1]} conditions")
        print(f"  Coverage: {100 * binary_matrix.sum().sum() / binary_matrix.size:.2f}%")

        matrices[group] = binary_matrix

    return matrices


def main():
    parser = argparse.ArgumentParser(
        description='Create organism × condition growth/no-growth matrix from Fitness Browser data'
    )
    parser.add_argument(
        '--db',
        type=str,
        default='feba.db',
        help='Path to Fitness Browser database (feba.db)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='growth_matrix.csv',
        help='Output CSV file for full matrix'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='.',
        help='Output directory for condition-specific matrices'
    )
    parser.add_argument(
        '--no-quality-filter',
        action='store_true',
        help='Disable quality filtering (include all experiments)'
    )
    parser.add_argument(
        '--hierarchical',
        action='store_true',
        help='Create hierarchical matrix with expGroup × condition_1 columns'
    )
    parser.add_argument(
        '--by-group',
        action='store_true',
        help='Create separate matrices for each condition group'
    )

    args = parser.parse_args()

    # Check database exists
    db_path = Path(args.db)
    if not db_path.exists():
        print(f"Error: Database not found: {db_path}", file=sys.stderr)
        print(f"\nPlease download feba.db from:", file=sys.stderr)
        print(f"  https://figshare.com/articles/dataset/25236931", file=sys.stderr)
        sys.exit(1)

    # Connect to database
    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(str(db_path))

    try:
        # Load data
        quality_filter = not args.no_quality_filter
        if quality_filter:
            print("Using quality filters: gMed ≥ 50, mad12 ≤ 0.5, no error flags")
        else:
            print("No quality filters applied")

        df = load_organism_condition_pairs(conn, quality_filter=quality_filter)

        # Create main matrix
        if args.hierarchical:
            matrix = create_hierarchical_matrix(df)
        else:
            matrix = create_binary_matrix(df)

        # Get statistics
        stats = get_matrix_statistics(matrix)

        # Save main matrix
        output_path = Path(args.output)
        print(f"\nSaving matrix to: {output_path}")
        matrix.to_csv(output_path)
        print(f"Saved")

        # Create condition-specific matrices if requested
        if args.by_group:
            output_dir = Path(args.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            matrices = create_condition_group_matrices(df)

            for group, group_matrix in matrices.items():
                # Clean group name for filename
                safe_name = group.replace(' ', '_').replace('/', '_')
                output_file = output_dir / f"growth_matrix_{safe_name}.csv"

                print(f"\nSaving {group} matrix to: {output_file}")
                group_matrix.to_csv(output_file)
                print(f"Saved")

        # Save statistics
        stats_file = output_path.with_suffix('.stats.txt')
        print(f"\nSaving statistics to: {stats_file}")
        with open(stats_file, 'w') as f:
            f.write("Growth Matrix Statistics\n")
            f.write("="*70 + "\n\n")
            for key, value in stats.items():
                if isinstance(value, float):
                    f.write(f"{key}: {value:.2f}\n")
                else:
                    f.write(f"{key}: {value}\n")
        print(f"Saved")

        print("\n" + "="*70)
        print("COMPLETE")
        print("="*70)
        print(f"\nFiles created:")
        print(f"  {output_path}")
        print(f"  {stats_file}")
        if args.by_group:
            print(f"  {len(matrices)} condition-specific matrices in {output_dir}")

    finally:
        conn.close()


if __name__ == '__main__':
    main()
