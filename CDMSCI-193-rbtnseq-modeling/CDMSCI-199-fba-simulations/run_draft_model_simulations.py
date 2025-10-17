#!/usr/bin/env python3
"""
Run FBA simulations on DRAFT models (pre-gap-filling) to compare vs gap-filled

This helps answer: Does pyruvate gap-filling improve predictions even for other carbon sources?
"""

import cobra
import pandas as pd
import json
from pathlib import Path
from tqdm import tqdm

# Paths
models_dir = Path('../CDMSCI-198-build-models/models')
media_dir = Path('../CDMSCI-197-media-formulations/media')
simulatable_file = Path('results/simulatable_carbon_sources.csv')
organism_metadata_file = Path('results/organism_metadata.csv')
output_file = Path('results/draft_model_fba_results.csv')

# Load inputs
simulatable = pd.read_csv(simulatable_file)
organism_metadata = pd.read_csv(organism_metadata_file)

print(f"Carbon sources to simulate: {len(simulatable)}")
print(f"Organisms to simulate: {len(organism_metadata)}")
print(f"Total simulations: {len(simulatable) * len(organism_metadata):,}")
print()

# Growth threshold
GROWTH_THRESHOLD = 0.001  # h^-1

# Run simulations
results = []
errors = []

total_sims = len(simulatable) * len(organism_metadata)

with tqdm(total=total_sims, desc="Running draft model FBA") as pbar:
    for _, org_row in organism_metadata.iterrows():
        org_id = org_row['orgId']
        organism = org_row['organism']

        # Load DRAFT model
        draft_model_path = models_dir / f'{org_id}_draft.json'

        if not draft_model_path.exists():
            print(f"  WARNING: Draft model not found for {org_id}")
            pbar.update(len(simulatable))
            continue

        try:
            model = cobra.io.load_json_model(str(draft_model_path))
        except Exception as e:
            print(f"  ERROR loading draft model {org_id}: {e}")
            pbar.update(len(simulatable))
            continue

        # Simulate each carbon source
        for _, cs_row in simulatable.iterrows():
            carbon_source = cs_row['experimental_name']
            media_filename = cs_row['media_filename']
            media_path = media_dir / media_filename

            if not media_path.exists():
                errors.append({
                    'organism': organism,
                    'orgId': org_id,
                    'carbon_source': carbon_source,
                    'error': 'Media file not found'
                })
                pbar.update(1)
                continue

            # Load media
            try:
                with open(media_path, 'r') as f:
                    media_dict = json.load(f)
            except Exception as e:
                errors.append({
                    'organism': organism,
                    'orgId': org_id,
                    'carbon_source': carbon_source,
                    'error': f'Media load error: {e}'
                })
                pbar.update(1)
                continue

            # Apply media and run FBA
            try:
                model.medium = media_dict
                solution = model.optimize()

                biomass_flux = solution.objective_value
                status = solution.status
                prediction = 1 if biomass_flux > GROWTH_THRESHOLD else 0

                results.append({
                    'organism': organism,
                    'orgId': org_id,
                    'carbon_source': carbon_source,
                    'media_filename': media_filename,
                    'biomass_flux': biomass_flux,
                    'status': status,
                    'prediction': prediction
                })

            except Exception as e:
                errors.append({
                    'organism': organism,
                    'orgId': org_id,
                    'carbon_source': carbon_source,
                    'error': f'FBA error: {e}'
                })

            pbar.update(1)

# Save results
df = pd.DataFrame(results)
df.to_csv(output_file, index=False)

print(f"\nCompleted: {len(results):,} simulations")
print(f"Errors: {len(errors)}")
print(f"Saved to: {output_file}")

if errors:
    error_df = pd.DataFrame(errors)
    error_df.to_csv('results/draft_model_fba_errors.csv', index=False)
    print(f"Error log: results/draft_model_fba_errors.csv")

# Quick summary
print(f"\nPrediction summary:")
print(df['prediction'].value_counts().sort_index())
print(f"\nMean biomass flux: {df['biomass_flux'].mean():.4f}")
print(f"Median biomass flux: {df['biomass_flux'].median():.4f}")
