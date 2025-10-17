#!/usr/bin/env python3
"""
Condition-specific gap-filling for all 571 false negatives

For each organism × carbon source where:
  - Experimental growth = 1
  - Model prediction = 0

Run gap-filling specifically for that carbon source media and track:
  - Did gap-filling succeed?
  - How many reactions were added?
  - Which specific reactions were added?
  - What is the biomass flux after gap-filling?
  - How does this compare to pyruvate gap-filling?

This generates comprehensive data to answer:
  "Which FNs are fixable via gap-filling vs fundamentally missing pathways?"
  "Is condition-specific gap-filling adding meaningful biology or just overfitting?"
"""

import cobra
from cobra.flux_analysis import gapfill
import pandas as pd
import json
from pathlib import Path
from tqdm import tqdm
import time

# Paths
models_dir = Path('../CDMSCI-198-build-models/models')
media_dir = Path('../CDMSCI-197-media-formulations/media')
false_negatives_file = Path('results/false_negatives.csv')
universal_model_path = Path('../CDMSCI-198-build-models/GramNegModelTemplateV6.json')
output_file = Path('results/condition_specific_gapfilling_results.csv')
detailed_reactions_file = Path('results/condition_specific_gapfilling_reactions.csv')

# Load inputs
fn_df = pd.read_csv(false_negatives_file)
print(f"Loaded {len(fn_df)} false negatives to gap-fill")
print()

# Load universal model (for gap-filling reactions)
print("Loading universal model template...")
try:
    universal = cobra.io.load_json_model(str(universal_model_path))
    print(f"  Universal model loaded: {len(universal.reactions)} reactions")
except Exception as e:
    print(f"  ERROR: Could not load universal model: {e}")
    print(f"  Exiting...")
    exit(1)

# Growth threshold
GROWTH_THRESHOLD = 0.001  # h^-1

# Results storage
results = []
reaction_details = []
errors = []

# Track timing
start_time = time.time()

print(f"\nStarting {len(fn_df)} gap-filling experiments...")
print()

with tqdm(total=len(fn_df), desc="Gap-filling FNs") as pbar:
    for idx, row in fn_df.iterrows():
        org_id = row.get('orgId')
        if pd.isna(org_id):
            # Try to extract from organism name
            organism = row['organism']
            # This is fragile - ideally we'd have orgId in FN CSV
            # For now, skip if missing
            pbar.set_postfix_str(f"Skipping {organism} (no orgId)")
            pbar.update(1)
            continue

        organism = row['organism']
        carbon_source = row['carbon_source']
        media_filename = f"{carbon_source.replace(' ', '_').replace(',', '')}.json"

        # Construct paths
        draft_model_path = models_dir / f'{org_id}_draft.json'
        media_path = media_dir / carbon_source.replace(' ', '_') + '.json'

        # Check if files exist
        if not draft_model_path.exists():
            errors.append({
                'organism': organism,
                'orgId': org_id,
                'carbon_source': carbon_source,
                'error': 'Draft model file not found'
            })
            pbar.update(1)
            continue

        if not media_path.exists():
            errors.append({
                'organism': organism,
                'orgId': org_id,
                'carbon_source': carbon_source,
                'error': 'Media file not found'
            })
            pbar.update(1)
            continue

        # Load draft model
        try:
            model = cobra.io.load_json_model(str(draft_model_path))
        except Exception as e:
            errors.append({
                'organism': organism,
                'orgId': org_id,
                'carbon_source': carbon_source,
                'error': f'Model load error: {e}'
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

        # Apply media
        try:
            model.medium = media_dict
        except Exception as e:
            errors.append({
                'organism': organism,
                'orgId': org_id,
                'carbon_source': carbon_source,
                'error': f'Media application error: {e}'
            })
            pbar.update(1)
            continue

        # Test if model already grows (shouldn't happen for FNs, but check)
        try:
            pre_gapfill_solution = model.optimize()
            pre_gapfill_flux = pre_gapfill_solution.objective_value
        except:
            pre_gapfill_flux = 0.0

        if pre_gapfill_flux > GROWTH_THRESHOLD:
            # This shouldn't happen for a false negative!
            errors.append({
                'organism': organism,
                'orgId': org_id,
                'carbon_source': carbon_source,
                'error': f'Draft model already grows (flux={pre_gapfill_flux:.4f}) - not a true FN?'
            })
            pbar.update(1)
            continue

        # Run gap-filling
        try:
            # Get gap-filling solutions
            solutions = gapfill(model, universal, demand_reactions=False)

            # solutions is a list of sets of reactions
            # Take the first solution (minimal set)
            if len(solutions) > 0:
                gapfill_reactions = list(solutions[0])
                num_reactions_added = len(gapfill_reactions)

                # Add reactions to model
                for reaction in gapfill_reactions:
                    model.add_reactions([reaction.copy()])

                # Re-optimize
                post_gapfill_solution = model.optimize()
                post_gapfill_flux = post_gapfill_solution.objective_value
                gapfill_success = post_gapfill_flux > GROWTH_THRESHOLD

                # Record result
                results.append({
                    'organism': organism,
                    'orgId': org_id,
                    'carbon_source': carbon_source,
                    'media_filename': media_path.name,
                    'pre_gapfill_flux': pre_gapfill_flux,
                    'post_gapfill_flux': post_gapfill_flux,
                    'gapfill_success': gapfill_success,
                    'num_reactions_added': num_reactions_added,
                    'reactions_added': ';'.join([r.id for r in gapfill_reactions]),
                    'gapfill_solutions_count': len(solutions)
                })

                # Record detailed reactions
                for reaction in gapfill_reactions:
                    reaction_details.append({
                        'organism': organism,
                        'orgId': org_id,
                        'carbon_source': carbon_source,
                        'reaction_id': reaction.id,
                        'reaction_name': reaction.name,
                        'reaction_formula': reaction.build_reaction_string(),
                        'subsystem': reaction.subsystem
                    })

            else:
                # No gap-filling solution found
                results.append({
                    'organism': organism,
                    'orgId': org_id,
                    'carbon_source': carbon_source,
                    'media_filename': media_path.name,
                    'pre_gapfill_flux': pre_gapfill_flux,
                    'post_gapfill_flux': 0.0,
                    'gapfill_success': False,
                    'num_reactions_added': 0,
                    'reactions_added': '',
                    'gapfill_solutions_count': 0
                })

        except Exception as e:
            errors.append({
                'organism': organism,
                'orgId': org_id,
                'carbon_source': carbon_source,
                'error': f'Gap-filling error: {e}'
            })

        pbar.update(1)

# Save results
print(f"\nSaving results...")
results_df = pd.DataFrame(results)
results_df.to_csv(output_file, index=False)
print(f"  Main results: {output_file}")

reactions_df = pd.DataFrame(reaction_details)
reactions_df.to_csv(detailed_reactions_file, index=False)
print(f"  Detailed reactions: {detailed_reactions_file}")

if errors:
    errors_df = pd.DataFrame(errors)
    errors_df.to_csv('results/condition_specific_gapfilling_errors.csv', index=False)
    print(f"  Errors: results/condition_specific_gapfilling_errors.csv")

# Summary statistics
elapsed_time = time.time() - start_time
print(f"\nCompleted in {elapsed_time/60:.1f} minutes")
print(f"Total experiments: {len(results)}")
print(f"Successful gap-filling: {results_df['gapfill_success'].sum()} ({100*results_df['gapfill_success'].mean():.1f}%)")
print(f"Failed gap-filling: {(~results_df['gapfill_success']).sum()}")
print(f"Errors: {len(errors)}")
print()

if len(results) > 0:
    print("Reactions added statistics:")
    print(results_df['num_reactions_added'].describe())
    print()
    print(f"Mean reactions added: {results_df['num_reactions_added'].mean():.1f}")
    print(f"Median reactions added: {results_df['num_reactions_added'].median():.1f}")
    print(f"Max reactions added: {results_df['num_reactions_added'].max()}")
    print()

    # Most frequently added reactions
    if len(reactions_df) > 0:
        from collections import Counter
        rxn_counts = Counter(reactions_df['reaction_id'])
        print("Top 20 most frequently added reactions:")
        for rxn_id, count in rxn_counts.most_common(20):
            pct = 100 * count / len(results_df)
            print(f"  {rxn_id}: {count} times ({pct:.1f}%)")

print("\nGap-filling experiment complete!")
print("Next steps:")
print("  1. Analyze results/condition_specific_gapfilling_results.csv")
print("  2. Compare reactions added vs pyruvate gap-filling")
print("  3. Assess biological plausibility of added reactions")
