# File Naming Convention Summary

**Date**: 2025-10-06
**Updated after**: Naming consistency review

---

## File-by-File Naming Conventions

### CSV Data Files

1. **organism_metadata.csv**
   - Organism column: `Species_Name` (simple format)
   - Example: `Escherichia coli BW25113`
   - Also includes: `orgId`, `Full_Species_Name`, `NCBI_TaxID`
   - Status: Updated to use simple names

2. **supplementary_table_s2_clean.csv**
   - Column headers: Species names (simple format)
   - Example: `Escherichia coli BW25113`
   - Rows: Carbon sources
   - Status: Updated to use simple names

3. **supplementary_table_s2_carbon.csv**
   - Column headers: Species names (simple format)
   - Example: `Burkholderia phytofirmans PsJN`
   - Rows: Carbon sources
   - Status: Updated to use simple names

4. **combined_growth_matrix.csv**
   - Column headers: Species names (simple format)
   - Example: `Burkholderia phytofirmans PsJN`
   - Rows: Carbon sources
   - Status: Updated to use simple names

5. **data_source_discrepancies.csv**
   - Organism_Name column: Species names (simple format)
   - Example: `Kangiella aquimarina DSM 16071`
   - Also includes: `Organism_ID` (orgId)
   - Status: Updated to use simple names

6. **carbon_source_growth_matrix.csv**
   - Row labels: `orgId` (short identifiers)
   - Example: `Keio`, `Cola`, `Burk376`
   - Column headers: Carbon source names
   - Status: Original format (uses orgId, not species names)
   - Note: This file uses orgId by design for compactness

7. **organism_name_mapping_supplementary_to_FIT.csv**
   - Column 1: Supplementary Table names (no division prefix)
   - Column 2: Fitness Browser orgId
   - Example: `Escherichia coli BW25113,Keio`
   - Status: Simple names

---

## Naming Format Standards

### Simple Species Name Format
**Format**: `Genus species strain`  
**Examples**:
- `Escherichia coli BW25113`
- `Burkholderia phytofirmans PsJN`
- `Echinicola vietnamensis KMM 6221, DSM 17526`

### Full Species Name Format (metadata only)
**Format**: `Division: Genus species strain`  
**Examples**:
- `Gammaproteobacteria: Escherichia coli BW25113`
- `Betaproteobacteria: Burkholderia phytofirmans PsJN`

**Usage**: Only in `organism_metadata.csv` `Full_Species_Name` column

### orgId Format
**Format**: Short identifier (varies by organism)  
**Examples**:
- `Keio` (E. coli BW25113)
- `Cola` (Echinicola vietnamensis)
- `Burk376` (Paraburkholderia bryophila 376MFSha3.1)

**Usage**: 
- `organism_metadata.csv` `orgId` column
- `carbon_source_growth_matrix.csv` row labels
- `data_source_discrepancies.csv` `Organism_ID` column

---

## Cross-Referencing Between Files

To map between naming conventions:

1. **Species Name → orgId**: Use `organism_metadata.csv`
   ```
   Species_Name: "Escherichia coli BW25113" → orgId: "Keio"
   ```

2. **orgId → Species Name**: Use `organism_metadata.csv`
   ```
   orgId: "Cola" → Species_Name: "Echinicola vietnamensis KMM 6221, DSM 17526"
   ```

3. **Supplementary Table Name → orgId**: Use `organism_name_mapping_supplementary_to_FIT.csv`
   ```
   "Escherichia coli BW25113" → "Keio"
   ```

---

## Files NOT Updated (and why)

- **carbon_source_growth_matrix.csv**: Uses orgId by design (original extracted data)
- **carbon_source_growth_heatmap.png**: Visualization, no text changes needed
- **carbon_source_growth_matrix_stats.txt**: Stats file, references orgId

These files maintain their original format for reference and backward compatibility.

---

## Consistency Check Results

✅ All primary data files use consistent **simple species names**  
✅ All cross-reference files updated  
✅ Metadata file includes all naming formats for easy lookup  
✅ Discrepancy file updated with simple names  
✅ Documentation (DATA_STRATEGY.md, DATA_INTEGRATION_REPORT.md) uses simple names  

**No inconsistencies remaining!**
