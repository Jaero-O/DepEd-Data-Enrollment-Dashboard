import pandas as pd

# Load the cleaned enrollment data
data_file = "enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv"
df = pd.read_csv(data_file)

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

# Insert computed totals in appropriate positions
df = insert_column_after(df, "k_female", "total_kinder_enrollment", df[kinder_cols].sum(axis=1))
df = insert_column_after(df, "elem_ng_female", "total_elem_enrollment", df[g1_g6_cols].sum(axis=1))
df = insert_column_after(df, "jhs_ng_female", "total_jhs_enrollment", df[jhs_cols].sum(axis=1))
df = insert_column_after(df, g12_cols[-1], "total_shs_enrollment", df[shs_cols].sum(axis=1))

# Insert Total Non-Graded Enrollment after SHS
df = insert_column_after(df, "total_shs_enrollment", "total_non_graded_enrollment", df[ng_cols].sum(axis=1))

# Compute total enrollment per gender
male_columns = [col for col in df.columns if "male" in col]
female_columns = [col for col in df.columns if "female" in col]

total_male = df[male_columns].sum(axis=1)
total_female = df[female_columns].sum(axis=1)

# Insert gender totals AFTER "Total Non-Graded Enrollment"
df = insert_column_after(df, "total_non_graded_enrollment", "total_male_enrollment", total_male)
df = insert_column_after(df, "total_male_enrollment", "total_female_enrollment", total_female)

# Compute and insert final total
total_k_to_shs = df[
    ["total_kinder_enrollment", "total_elem_enrollment", "total_jhs_enrollment", "total_shs_enrollment"]
].sum(axis=1)
df = insert_column_after(df, "total_female_enrollment", "total_enrollment", total_k_to_shs)

# Remove 'beis_school' before saving, if it exists
if "beis_school" in df.columns:
    df = df.drop(columns=["beis_school"])

# Save the final dataset
output_file = "enrollment_csv_file/preprocessed_data/total_enrollment.csv"
df.to_csv(output_file, index=False)

# Display sample output
print(df.loc[:, [
    "school_name",
    "total_kinder_enrollment", "total_elem_enrollment",
    "total_jhs_enrollment", "total_shs_enrollment",
    "total_non_graded_enrollment",
    "total_male_enrollment", "total_female_enrollment",
    "total_enrollment"
]].head(10))
