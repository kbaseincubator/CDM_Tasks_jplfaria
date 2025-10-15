#!/usr/bin/env python3
"""
Search for compounds in ModelSEED database

This script provides tools to search for compounds using:
1. Local template file (GramNegModelTemplateV6.json) - fast, offline
2. ModelSEED Solr API - comprehensive, online

Usage:
    python search_compounds.py glucose
    python search_compounds.py "citric acid"
    python search_compounds.py --id cpd00027
"""

import json
import sys
from pathlib import Path
from urllib.request import urlopen, URLError
from urllib.parse import quote

# Configuration
TEMPLATE_PATH = Path(__file__).parent / 'GramNegModelTemplateV6.json'
SOLR_URL = 'https://modelseed.org/solr/compounds/select'


def search_template_by_name(compound_name, template_path=TEMPLATE_PATH):
    """Search for compound by name in local template file"""
    if not template_path.exists():
        print(f"Error: Template file not found at {template_path}")
        return []

    with open(template_path) as f:
        template = json.load(f)

    matches = []
    search_lower = compound_name.lower()

    for compound in template['compounds']:
        # Search in name
        if search_lower in compound['name'].lower():
            matches.append(compound)
            continue

        # Search in abbreviation
        abbr = compound.get('abbreviation', '')
        if abbr and search_lower in abbr.lower():
            matches.append(compound)
            continue

        # Search in aliases
        for alias in compound.get('aliases', []):
            if search_lower in alias.lower():
                matches.append(compound)
                break

    return matches


def search_template_by_id(compound_id, template_path=TEMPLATE_PATH):
    """Search for compound by ID in local template file"""
    if not template_path.exists():
        print(f"Error: Template file not found at {template_path}")
        return None

    with open(template_path) as f:
        template = json.load(f)

    for compound in template['compounds']:
        if compound['id'] == compound_id:
            return compound

    return None


def search_solr(compound_name, fields='name,id,formula,charge,mass,aliases'):
    """Search ModelSEED Solr API for compounds"""
    query = f"{SOLR_URL}?wt=json&q=aliases:{quote(compound_name)}&fl={fields}"

    try:
        connection = urlopen(query, timeout=10)
        response = json.load(connection)
        return response['response']['docs']
    except URLError as e:
        print(f"Error connecting to ModelSEED: {e}")
        return []
    except Exception as e:
        print(f"Error searching Solr: {e}")
        return []


def search_solr_by_id(compound_id, fields='name,id,formula,charge,mass,aliases,deltaG'):
    """Search ModelSEED Solr API by compound ID"""
    query = f"{SOLR_URL}?wt=json&q=id:{compound_id}&fl={fields}"

    try:
        connection = urlopen(query, timeout=10)
        response = json.load(connection)
        docs = response['response']['docs']
        return docs[0] if docs else None
    except URLError as e:
        print(f"Error connecting to ModelSEED: {e}")
        return None
    except Exception as e:
        print(f"Error searching Solr: {e}")
        return None


def format_compound_output(compound, source='template'):
    """Format compound information for display"""
    lines = []
    lines.append(f"ID: {compound.get('id', 'N/A')}")
    lines.append(f"Name: {compound.get('name', 'N/A')}")

    abbr = compound.get('abbreviation')
    if abbr:
        lines.append(f"Abbreviation: {abbr}")

    formula = compound.get('formula')
    if formula:
        lines.append(f"Formula: {formula}")

    mass = compound.get('mass')
    if mass:
        lines.append(f"Mass: {mass}")

    charge = compound.get('charge') or compound.get('defaultCharge')
    if charge is not None:
        lines.append(f"Charge: {charge}")

    deltag = compound.get('deltaG')
    if deltag is not None:
        lines.append(f"ΔG: {deltag}")

    # Show aliases (truncate if too many)
    aliases = compound.get('aliases', [])
    if aliases:
        if isinstance(aliases, str):
            aliases = [aliases]
        if len(aliases) > 5:
            aliases_str = ', '.join(aliases[:5]) + f' ... ({len(aliases)} total)'
        else:
            aliases_str = ', '.join(aliases)
        lines.append(f"Aliases: {aliases_str}")

    lines.append(f"Source: {source}")

    return '\n'.join(lines)


def main():
    """Main search function"""
    if len(sys.argv) < 2:
        print("Usage: python search_compounds.py <compound_name>")
        print("       python search_compounds.py --id <compound_id>")
        print("\nExamples:")
        print("  python search_compounds.py glucose")
        print("  python search_compounds.py 'citric acid'")
        print("  python search_compounds.py --id cpd00027")
        sys.exit(1)

    # Check if searching by ID
    search_by_id = False
    if sys.argv[1] == '--id':
        if len(sys.argv) < 3:
            print("Error: --id requires compound ID")
            sys.exit(1)
        search_term = sys.argv[2]
        search_by_id = True
    else:
        search_term = ' '.join(sys.argv[1:])

    print(f"Searching for: {search_term}")
    print("=" * 70)

    if search_by_id:
        # Search by ID
        print("\n1. Searching local template...")
        compound = search_template_by_id(search_term)
        if compound:
            print(f"\nFound in template:")
            print(format_compound_output(compound, 'local template'))
        else:
            print("Not found in local template")

        print("\n2. Searching ModelSEED online database...")
        compound = search_solr_by_id(search_term)
        if compound:
            print(f"\nFound in ModelSEED:")
            print(format_compound_output(compound, 'ModelSEED Solr'))
        else:
            print("Not found in ModelSEED database")

    else:
        # Search by name
        print("\n1. Searching local template...")
        template_matches = search_template_by_name(search_term)

        if template_matches:
            print(f"\nFound {len(template_matches)} match(es) in template:")
            for i, compound in enumerate(template_matches[:5], 1):
                print(f"\n--- Match {i} ---")
                print(format_compound_output(compound, 'local template'))

            if len(template_matches) > 5:
                print(f"\n... and {len(template_matches) - 5} more matches")
        else:
            print("No matches in local template")

        print("\n" + "=" * 70)
        print("\n2. Searching ModelSEED online database...")
        solr_matches = search_solr(search_term)

        if solr_matches:
            print(f"\nFound {len(solr_matches)} match(es) in ModelSEED:")
            for i, compound in enumerate(solr_matches[:5], 1):
                print(f"\n--- Match {i} ---")
                print(format_compound_output(compound, 'ModelSEED Solr'))

            if len(solr_matches) > 5:
                print(f"\n... and {len(solr_matches) - 5} more matches")
        else:
            print("No matches in ModelSEED database")

    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
