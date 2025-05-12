import pandas as pd

# Load the dataset
data_file = "enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv"
df = pd.read_csv(data_file)

# Clean column names: strip, lowercase, and replace spaces with underscores
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Define grade group columns (with updated naming)
kinder_cols = ["k_male", "k_female"]

# Elementary including Non-Graded
g1_g6_cols = (
    [f"g{i}_male" for i in range(1, 7)] +
    [f"g{i}_female" for i in range(1, 7)] +
    ["elem_ng_male", "elem_ng_female"]
)

# JHS including Non-Graded
jhs_cols = (
    [f"g{i}_male" for i in range(7, 11)] +
    [f"g{i}_female" for i in range(7, 11)] +
    ["jhs_ng_male", "jhs_ng_female"]
)

# SHS columns (starts with g11_ or g12_)
shs_cols = [col for col in df.columns if col.startswith("g11_") or col.startswith("g12_")]

# Identify all Non-Graded columns (for total NG computation)
ng_cols = [col for col in df.columns if "ng_male" in col or "ng_female" in col]

# Other metadata columns (updated names)
other_needed_cols = [
    "region", "division", "district", "beis_school_id", "school_name", "street_address",
    "province", "municipality", "legislative_district", "barangay", "sector",
    "school_subclassification", "school_type", "modified_coc"
]

# Compute gender-specific totals, including Non-Graded columns
male_cols = [col for col in df.columns if col.endswith("_male")]
female_cols = [col for col in df.columns if col.endswith("_female")]

# Total male enrollment: Sum only the male-related columns (including non-graded male columns)
df["total_male_enrollment"] = df[male_cols].sum(axis=1)

# Total female enrollment: Sum only the female-related columns (including non-graded female columns)
df["total_female_enrollment"] = df[female_cols].sum(axis=1)

# Total non-graded enrollment (NG Male and NG Female)
df["total_non_graded_enrollment"] = df[ng_cols].sum(axis=1)

# Total enrollment: Sum of male and female enrollment (including non-graded)
df["total_enrollment"] = df["total_male_enrollment"] + df["total_female_enrollment"]

# Function to filter based on Modified COC, keep relevant columns, and save to CSV
def save_data(coc_value, columns_to_keep, output_file):
    # Filter rows based on COC value
    df_filtered = df[df["modified_coc"].str.strip() == coc_value]
    
    # If no data found, skip and return
    if df_filtered.empty:
        print(f"No data found for COC: {coc_value}")
        return

    # Get final list of columns to retain
    cols_to_keep = (
        [col for col in other_needed_cols if col in df_filtered.columns] +
        [col for col in columns_to_keep if col in df_filtered.columns] +
        [col for col in ["total_non_graded_enrollment", "total_male_enrollment", "total_female_enrollment", "total_enrollment"] if col in df_filtered.columns]
    )

    # Keep only the relevant columns
    df_filtered_cleaned = df_filtered[cols_to_keep]
    
    # Save to CSV
    df_filtered_cleaned.to_csv(output_file, index=False)
    print(f"Data for {coc_value} has been saved to {output_file}")

# Save data by school type
save_data("Purely ES", kinder_cols + g1_g6_cols, "enrollment_csv_file/preprocessed_data/data_by_coc/purely_es_data.csv")
save_data("Purely JHS", jhs_cols, "enrollment_csv_file/preprocessed_data/data_by_coc/purely_jhs_data.csv")
save_data("Purely SHS", shs_cols, "enrollment_csv_file/preprocessed_data/data_by_coc/purely_shs_data.csv")
save_data("ES and JHS", kinder_cols + g1_g6_cols + jhs_cols, "enrollment_csv_file/preprocessed_data/data_by_coc/es_and_jhs_data.csv")
save_data("JHS with SHS", jhs_cols + shs_cols, "enrollment_csv_file/preprocessed_data/data_by_coc/jhs_and_shs_data.csv")
save_data("All Offering", kinder_cols + g1_g6_cols + jhs_cols + shs_cols, "enrollment_csv_file/preprocessed_data/data_by_coc/all_offering_data.csv")

print("Data processing complete.")
