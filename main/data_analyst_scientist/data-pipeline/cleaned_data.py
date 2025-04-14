import pandas as pd

file_path = "enrollment_csv_file\\raw_data\SY 2023-2024 School Level Data on Official Enrollment 13.xlsx - DB.csv"
df = pd.read_csv(file_path, skiprows=4, dtype={'BEIS School ID': 'object'})

df_dropped = df.dropna(how='all').drop_duplicates()

data_info = (df_dropped.shape, df_dropped.size)

valid_format = df_dropped['BEIS School ID'].str.match(r'^\d{6}$')

valid_count = valid_format.sum()
invalid_count = (~valid_format).sum()

print(f"Valid BEIS School IDs: {valid_count}")
print(f"Invalid BEIS School IDs: {invalid_count}")

df = df_dropped.copy()
# Clean column names: strip, lowercase, and replace spaces with underscores
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Define grade group columns with lowercase names
kinder_cols = ["k_male", "k_female"]
g1_g6_cols = (
    [f"g{i}_male" for i in range(1, 7)] +
    [f"g{i}_female" for i in range(1, 7)] +
    ["elem_ng_male", "elem_ng_female"]
)
jhs_cols = (
    [f"g{i}_male" for i in range(7, 11)] +
    [f"g{i}_female" for i in range(7, 11)] +
    ["jhs_ng_male", "jhs_ng_female"]
)
g11_cols = [col for col in df.columns if col.startswith("g11_")]
g12_cols = [col for col in df.columns if col.startswith("g12_")]
shs_cols = g11_cols + g12_cols
ng_cols = [col for col in df.columns if "ng_male" in col or "ng_female" in col]

# Helper function to insert a column after a reference column 
def insert_column_after(df, ref_col, new_col_name, new_col_values):
    ref_index = df.columns.get_loc(ref_col)
    new_df = df.copy()
    new_df.insert(ref_index + 1, new_col_name, new_col_values)
    return new_df

# Remove 'beis_school' before saving, if it exists
if "beis_school" in df.columns:
    df = df.drop(columns=["beis_school"])


df.dtypes.to_csv("enrollment_csv_file\preprocessed_data\data_types.csv")

df.to_csv("enrollment_csv_file\preprocessed_data\cleaned_enrollment_data.csv", index=False)

print(df.columns)