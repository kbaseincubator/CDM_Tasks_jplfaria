#!/usr/bin/env python3
"""
Optimized script to add missing exchanges to models.
Uses direct JSON manipulation instead of COBRA save (which is very slow).
"""

import pandas as pd
import cobra
import json
from pathlib import Path
import time

print("="*80)
print("OPTIMIZED EXCHANGE ADDITION")
print("="*80)

# Load missing exchanges
missing_exchanges = pd.read_csv('results/missing_exchanges_details.csv')
organisms_to_correct = missing_exchanges['orgId'].unique()

print(f"\nProcessing {len(organisms_to_correct)} organisms...")
print()

# Define exchange reactions
exchange_reaction_ids = {
    'cpd10515': 'EX_cpd10515_e0',  # Fe2+
    'cpd00244': 'EX_cpd00244_e0',  # Ni2+
    'cpd11574': 'EX_cpd11574_e0',  # Molybdate
}

compound_names = {
    'cpd10515': 'Fe2+',
    'cpd00244': 'Ni2+',
    'cpd11574': 'Molybdate',
}

# Create output directory
models_dir = Path('models_missing_exchanges')
models_dir.mkdir(exist_ok=True)

# Track corrections
correction_log = []
start_time = time.time()

for i, org_id in enumerate(organisms_to_correct, 1):
    print(f"[{i}/{len(organisms_to_correct)}] Processing {org_id}...")

    # Find model file
    model_path = Path(f"../CDMSCI-198-build-models/models/{org_id}_gapfilled.json")

    if not model_path.exists():
        print(f"  WARNING: Model not found: {model_path}")
        continue

    # Load model JSON directly (faster than COBRA)
    with open(model_path, 'r') as f:
        model_json = json.load(f)

    original_num_reactions = len(model_json['reactions'])

    # Get missing compounds for this organism
    missing_for_org = missing_exchanges[missing_exchanges['orgId'] == org_id]

    exchanges_added = []

    # Check which exchanges to add
    for idx, row in missing_for_org.iterrows():
        cpd_id = row['compound_id']
        cpd_name = row['compound_name']
        exchange_rxn_id = exchange_reaction_ids[cpd_id]

        # Check if exchange already exists
        if any(rxn['id'] == exchange_rxn_id for rxn in model_json['reactions']):
            print(f"  - Already exists: {exchange_rxn_id} ({cpd_name})")
            continue

        # Create metabolite ID
        metabolite_id = f"{cpd_id}_e0"

        # Check if metabolite exists
        met_exists = any(met['id'] == metabolite_id for met in model_json['metabolites'])

        if not met_exists:
            # Add metabolite
            new_met = {
                "id": metabolite_id,
                "name": cpd_name,
                "compartment": "e0",
                "charge": 0,
                "formula": "",
                "annotation": {}
            }
            model_json['metabolites'].append(new_met)

        # Add exchange reaction
        new_rxn = {
            "id": exchange_rxn_id,
            "name": f"{cpd_name} exchange",
            "metabolites": {
                metabolite_id: -1.0
            },
            "lower_bound": -100.0,
            "upper_bound": 100.0,
            "gene_reaction_rule": "",
            "subsystem": "",
            "annotation": {}
        }

        model_json['reactions'].append(new_rxn)
        exchanges_added.append(cpd_name)
        print(f"  + Added: {exchange_rxn_id} ({cpd_name})")

    # Save modified model (direct JSON write - much faster than COBRA)
    output_path = models_dir / f"{org_id}_gapfilled_corrected.json"
    with open(output_path, 'w') as f:
        json.dump(model_json, f, indent=1)

    new_num_reactions = len(model_json['reactions'])

    print(f"  Reactions: {original_num_reactions} → {new_num_reactions} (+{new_num_reactions - original_num_reactions})")
    print(f"  Saved to: {output_path.name}")
    print()

    # Log
    correction_log.append({
        'orgId': org_id,
        'genome_id': org_id,
        'exchanges_added': ', '.join(exchanges_added),
        'num_exchanges_added': len(exchanges_added),
        'original_reactions': original_num_reactions,
        'corrected_reactions': new_num_reactions,
    })

elapsed = time.time() - start_time

print("="*80)
print(f"COMPLETED in {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
print(f"  Models corrected: {len(correction_log)}")
print(f"  Total exchanges added: {sum(c['num_exchanges_added'] for c in correction_log)}")
print()

# Save log
correction_df = pd.DataFrame(correction_log)
correction_df.to_csv('results/model_corrections_log.csv', index=False)

print("Correction log:")
print(correction_df.to_string(index=False))
print()
print(f"Saved to: results/model_corrections_log.csv")
print()
print("You can now continue with cell 17 in Notebook 04 (Re-run FBA Simulations)")
