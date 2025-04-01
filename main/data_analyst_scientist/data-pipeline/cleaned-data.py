import pandas as pd

# Load CSV file
file_path = "SY 2023-2024 School Level Data on Official Enrollment 13.xlsx - DB.csv"
df = pd.read_csv(file_path, skiprows=4, dtype={'BEIS School': 'Int64'})

# Drop null and duplicate values
df_dropped = df.dropna().drop_duplicates()

data_info = (df_dropped.shape, df_dropped.size)

#Convert School ID to string to check if 
df_dropped['BEIS School'] = df_dropped['BEIS School ID'].astype(str)

# Check if BEIS School ID matches exactly six digits (NNNNNN)
valid_format = df_dropped['BEIS School'].str.match(r'^\d{6}$')

# Count valid and invalid entries
valid_count = valid_format.sum()
invalid_count = (~valid_format).sum()

# Print results
print(f"Valid BEIS School IDs: {valid_count}")
print(f"Invalid BEIS School IDs: {invalid_count}")

df_dropped.dtypes.to_csv("data_types.csv")

print(data_info)