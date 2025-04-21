import pandas as pd
import os

# Load the CSV file
file_path = "enrollment_csv_file\\preprocessed_data\\total_enrollment_per_educational_level.csv"
df = pd.read_csv(file_path, dtype={'BEIS School': 'Int64'})

# Create hierarchical structure and prepare rows for CSV
hierarchy = {}
rows = []  # To store flattened rows

# Get unique regions
for region in df['Region'].unique():
    hierarchy[region] = {}
    
    # Filter provinces in region
    region_df = df[df['Region'] == region]
    for province in region_df['Province'].unique():
        hierarchy[region][province] = {}
        
        # Filter municipalities in province
        province_df = region_df[region_df['Province'] == province]
        for municipality in province_df['Municipality'].unique():
            hierarchy[region][province][municipality] = {}
            
            # Filter legislative districts in municipality
            municipality_df = province_df[province_df['Municipality'] == municipality]
            for district in municipality_df['District'].unique():
                barangays = list(municipality_df[municipality_df['District'] == district]['Barangay'].unique())
                hierarchy[region][province][municipality][district] = barangays
                
                # Add rows for CSV
                for barangay in barangays:
                    rows.append({
                        'Region': region,
                        'Province': province,
                        'Municipality': municipality,
                        'District': district,
                        'Barangay': barangay
                    })

# Create a DataFrame from the rows
csv_df = pd.DataFrame(rows)

# Ensure the output directory exists
output_dir = "enrollment_csv_file\\preprocessed_data"
os.makedirs(output_dir, exist_ok=True)

# Save to CSV in the specified folder
output_path = os.path.join(output_dir, "hierarchical_structure.csv")
csv_df.to_csv(output_path, index=False)
