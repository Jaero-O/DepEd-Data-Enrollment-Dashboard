import pandas as pd

# Load the cleaned enrollment data
data_file = "enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv"
df = pd.read_csv(data_file)

# Strip extra spaces from column names
df.columns = df.columns.str.strip()

# Define grade group columns
kinder_cols = ["K Male", "K Female"]
g1_g6_cols = [f"G{i} Male" for i in range(1, 7)] + [f"G{i} Female" for i in range(1, 7)]
jhs_cols = [f"G{i} Male" for i in range(7, 11)] + [f"G{i} Female" for i in range(7, 11)] + ["JHS NG Male", "JHS NG Female"]
g11_cols = [col for col in df.columns if col.startswith("G11 ")]
g12_cols = [col for col in df.columns if col.startswith("G12 ")]
shs_cols = g11_cols + g12_cols

# Helper function to insert a column after a reference column 
def insert_column_after(df, ref_col, new_col_name, new_col_values):
    ref_index = df.columns.get_loc(ref_col)
    new_df = df.copy()
    new_df.insert(ref_index + 1, new_col_name, new_col_values)
    return new_df

# Insert computed totals in appropriate positions
df = insert_column_after(df, "K Female", "Total Kinder Enrollment", df[kinder_cols].sum(axis=1))
df = insert_column_after(df, "G6 Female", "Total G1-G6 Enrollment", df[g1_g6_cols].sum(axis=1))
df = insert_column_after(df, "JHS NG Female", "Total JHS Enrollment", df[jhs_cols].sum(axis=1))
df = insert_column_after(df, g12_cols[-1], "Total SHS Enrollment", df[shs_cols].sum(axis=1))

# Compute total enrollment per gender
male_columns = [col for col in df.columns if "Male" in col]
female_columns = [col for col in df.columns if "Female" in col]

total_male = df[male_columns].sum(axis=1)
total_female = df[female_columns].sum(axis=1)

# Insert gender totals AFTER "Total SHS Enrollment"
df = insert_column_after(df, "Total SHS Enrollment", "Total Male Enrollment", total_male)
df = insert_column_after(df, "Total Male Enrollment", "Total Female Enrollment", total_female)

# Compute and insert final total
total_k_to_shs = df[
    ["Total Kinder Enrollment", "Total G1-G6 Enrollment", "Total JHS Enrollment", "Total SHS Enrollment"]
].sum(axis=1)
df = insert_column_after(df, "Total Female Enrollment", "Total Enrollment", total_k_to_shs)

# Remove 'BEIS School' before saving
df = df.drop(columns=["BEIS School"])

# Save the final dataset
output_file = "enrollment_csv_file/preprocessed_data/total_enrollment.csv"
df.to_csv(output_file, index=False)


# Display sample output
print(df.loc[:, [
    "School Name",
    "Total Kinder Enrollment", "Total G1-G6 Enrollment",
    "Total JHS Enrollment", "Total SHS Enrollment",
    "Total Male Enrollment", "Total Female Enrollment",
    "Total Enrollment"
]].head(10))
