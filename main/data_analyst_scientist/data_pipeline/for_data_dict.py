import pandas as pd
import os

# Load the structured data from the CSV file
file_path = 'enrollment_csv_file\\preprocessed_data\\hierarchical_structure.csv'
df = pd.read_csv(file_path)

# Create a dictionary to hold the structured data
structured_data = {}

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    region = row['Region']
    province = row['Province']
    municipality = row['Municipality']
    district = row['District']
    barangay = row['Barangay']
    
    # Handle missing or NaN values for barangay
    if pd.isna(barangay):  # Skip rows with missing barangay values
        continue
    
    province = str(province).title()
    municipality = str(municipality).title()  # Convert municipality to string and apply title casing
    barangay = str(barangay).title()  # Convert barangay to string and apply title casing
    
    # Add region if it doesn't exist
    if region not in structured_data:
        structured_data[region] = {}
    
    # Add province if it doesn't exist
    if province not in structured_data[region]:
        structured_data[region][province] = {}
    
    # Add municipality if it doesn't exist
    if municipality not in structured_data[region][province]:
        structured_data[region][province][municipality] = {}
    
    # Add district if it doesn't exist
    if district not in structured_data[region][province][municipality]:
        structured_data[region][province][municipality][district] = []
    
    # Add barangay to the district
    if barangay not in structured_data[region][province][municipality][district]:
        structured_data[region][province][municipality][district].append(barangay)

# Prepare data for the structured TXT output with indentation
output_lines = []

for region, provinces in structured_data.items():
    output_lines.append(f"Region: {region}")
    
    for province, municipalities in provinces.items():
        output_lines.append(f"  Province: {province}")
        
        for municipality, districts in municipalities.items():
            output_lines.append(f"    Municipality: {municipality}")
            
            for district, barangays in districts.items():
                output_lines.append(f"      District: {district}")
                output_lines.append(f"        Barangays:")
                
                for barangay in barangays:
                    output_lines.append(f"          {barangay}")

# Make sure the output directory exists
output_dir = 'enrollment_csv_file\\preprocessed_data'
os.makedirs(output_dir, exist_ok=True)

# Save structured data to a TXT file in the specified folder
output_txt_path = os.path.join(output_dir, 'structured_data.txt')
with open(output_txt_path, 'w', encoding='utf-8') as file:
    for line in output_lines:
        file.write(line + '\n')

print(f"Structured data saved to {output_txt_path}")
