import pandas as pd

fimo_output_path = 'fimo.tsv'  # Raw FIMO output
jaspar_file_path = 'JASPAR2024_CORE_non-redundant_pfms_transfac.txt'  # JASPAR file
regen_output_path = 'regen_family_exclusive.tsv'  # Output for regenerative species
nonregen_output_path = 'nonregen_family_exclusive.tsv'  # Output for non-regenerative species

#loads fimo output
fimo_df = pd.read_csv(fimo_output_path, sep='\t')

#define species categories
regenerative_species = ['japonicus', 'macularius']
nonregenerative_species = ['ciliatus']

#filter based on 'sequence_name'
regenerative_df = fimo_df[fimo_df['sequence_name'].isin(regenerative_species)]
nonregenerative_df = fimo_df[fimo_df['sequence_name'].isin(nonregenerative_species)]

#parse JASPAR file for motif family names 
motif_family_mappings = {}
with open(jaspar_file_path, 'r') as jaspar_file:
    for line in jaspar_file:
        if line.startswith('AC'):
            current_motif_id = line.split()[1]
        elif line.startswith('CC tf_family:'):
            current_family = line.split(':')[1].strip()
            motif_family_mappings[current_motif_id] = current_family

#maps motifs to family name
def map_family(motif_id):
    return motif_family_mappings.get(motif_id, 'Unknown')

regenerative_df['family'] = regenerative_df['motif_id'].apply(map_family)
nonregenerative_df['family'] = nonregenerative_df['motif_id'].apply(map_family)

#identify unique families
regen_families = set(regenerative_df['family']) - set(nonregenerative_df['family'])
nonregen_unique_families = set(nonregenerative_df['family']) - set(regenerative_df['family'])

#filter df for unique families
regen_unique_filtered_df = regenerative_df[regenerative_df['family'].isin(regen_families)]
nonregen_unique_filtered_df = nonregenerative_df[nonregenerative_df['family'].isin(nonregen_unique_families)]

#save outputs
regen_unique_filtered_df.to_csv(regen_output_path, sep='\t', index=False)
nonregen_unique_filtered_df.to_csv(nonregen_output_path, sep='\t', index=False)
