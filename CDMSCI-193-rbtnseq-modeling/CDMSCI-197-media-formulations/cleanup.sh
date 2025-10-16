#!/bin/bash
# Cleanup script for CDMSCI-197
# Removes temporary/duplicate files, keeps only essentials

echo "========================================"
echo "CDMSCI-197 Cleanup Script"
echo "========================================"
echo ""
echo "This will delete 18 temporary/duplicate files"
echo "All functionality is preserved in the final notebook"
echo ""

# Array of files to delete
files_to_delete=(
    # Old/duplicate notebooks
    "01-map-carbon-sources-to-modelseed.ipynb"
    "01-map-carbon-sources-to-modelseed-with-validation.ipynb"
    "01-map-carbon-sources-to-modelseed-corrected.ipynb.backup"

    # Temporary scripts
    "add_round3_validation.py"
    "create_corrected_workflow.py"
    "apply_manual_corrections.py"
    "apply_remaining_corrections.py"
    "regenerate_media_files.py"
    "verify_final_mappings.py"
    "add_manual_corrections_to_notebook.py"

    # Internal documentation
    "ACTION_CHECKLIST.md"
    "BUG_FIX_2025-10-15.md"
    "CDMSCI-197_RESULTS_ANALYSIS.md"
    "NOTEBOOK_ADDITION_MANUAL_CORRECTIONS.md"
    "NOTEBOOK_UPDATE_SUMMARY.md"
    "WORKFLOW_IMPROVEMENTS.md"

    # Intermediate results
    "results/round1_unmapped.txt"
    "results/round2_still_unmapped.csv"

    # This cleanup proposal (delete after running)
    "CLEANUP_PROPOSAL.md"
)

echo "Files to be deleted:"
for file in "${files_to_delete[@]}"; do
    if [ -e "$file" ]; then
        echo "  - $file"
    fi
done

echo ""
read -p "Proceed with cleanup? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    deleted_count=0
    not_found_count=0

    for file in "${files_to_delete[@]}"; do
        if [ -e "$file" ]; then
            rm "$file"
            echo "✓ Deleted: $file"
            ((deleted_count++))
        else
            echo "⚠ Not found: $file"
            ((not_found_count++))
        fi
    done

    echo ""
    echo "========================================"
    echo "Cleanup Complete"
    echo "========================================"
    echo "Deleted: $deleted_count files"
    echo "Not found: $not_found_count files"
    echo ""
    echo "Remaining structure:"
    echo "  - 1 notebook (01-map-carbon-sources-to-modelseed-corrected.ipynb)"
    echo "  - 2 documentation files (README.md, MANUAL_CORRECTIONS_SUMMARY.md)"
    echo "  - 1 input file (Manual_review_media_cpds.csv)"
    echo "  - 5 results files (results/*.csv)"
    echo "  - 122 media files (media/*.json)"
    echo ""
    echo "Project is now clean and ready for CDMSCI-199!"
else
    echo "Cleanup cancelled"
fi
