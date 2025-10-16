#!/usr/bin/env python3
"""
Extract actual gap-filled reaction IDs by comparing draft vs gapfilled models
"""

import json
from pathlib import Path
from collections import Counter
import pandas as pd

models_dir = Path('models')
output_file = Path('results/gapfilled_reactions_detailed.csv')

results = []
all_reactions = Counter()

# Get all organism IDs from model files
organism_ids = set()
for draft_file in models_dir.glob('*_draft.json'):
    org_id = draft_file.stem.replace('_draft', '')
    organism_ids.add(org_id)

print(f"Found {len(organism_ids)} organisms")

# For each organism, compare draft vs gapfilled
for org_id in sorted(organism_ids):
    draft_file = models_dir / f'{org_id}_draft.json'
    gapfilled_file = models_dir / f'{org_id}_gapfilled.json'

    if not gapfilled_file.exists():
        print(f"  {org_id}: No gapfilled model found")
        continue

    # Load models
    with open(draft_file, 'r') as f:
        draft_model = json.load(f)

    with open(gapfilled_file, 'r') as f:
        gapfilled_model = json.load(f)

    # Get reaction IDs
    draft_rxns = set(rxn['id'] for rxn in draft_model['reactions'])
    gapfilled_rxns = set(rxn['id'] for rxn in gapfilled_model['reactions'])

    # Find added reactions
    added_rxns = gapfilled_rxns - draft_rxns

    if added_rxns:
        print(f"  {org_id}: {len(added_rxns)} reactions added")
        for rxn_id in added_rxns:
            results.append({
                'Organism_ID': org_id,
                'Reaction_ID': rxn_id
            })
            all_reactions[rxn_id] += 1
    else:
        print(f"  {org_id}: No reactions added (draft already growing)")

# Save detailed results
df = pd.DataFrame(results)
df.to_csv(output_file, index=False)
print(f"\nSaved {len(df)} gap-filled reactions to {output_file}")

# Save top reactions summary
top_reactions = all_reactions.most_common(20)
print(f"\nTop 20 most frequently gap-filled reactions:")
for rxn_id, count in top_reactions:
    print(f"  {rxn_id}: {count} models ({100*count/len(organism_ids):.1f}%)")

# Save top reactions to CSV
top_df = pd.DataFrame(top_reactions, columns=['Reaction_ID', 'Model_Count'])
top_df.to_csv('results/top_gapfilled_reactions.csv', index=False)
print(f"\nSaved top reactions to results/top_gapfilled_reactions.csv")
