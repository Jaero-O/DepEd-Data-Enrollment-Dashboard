import pandas as pd

file_path = "enrollment_csv_file\\raw_data\SY 2023-2024 School Level Data on Official Enrollment 13.xlsx - DB.csv"
df = pd.read_csv(file_path, skiprows=4, dtype={'BEIS School': 'Int64'})

df_dropped = df.dropna().drop_duplicates()

data_info = (df_dropped.shape, df_dropped.size)

df_dropped['BEIS School'] = df_dropped['BEIS School ID'].astype(str)

valid_format = df_dropped['BEIS School'].str.match(r'^\d{6}$')

valid_count = valid_format.sum()
invalid_count = (~valid_format).sum()

print(f"Valid BEIS School IDs: {valid_count}")
print(f"Invalid BEIS School IDs: {invalid_count}")

df_dropped.dtypes.to_csv("enrollment_csv_file\preprocessed_data\data_types.csv")

df_dropped.to_csv("enrollment_csv_file\preprocessed_data\cleaned_enrollment_data.csv", index=False)

print(data_info)