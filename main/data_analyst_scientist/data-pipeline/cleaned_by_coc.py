import pandas as pd

# Load the dataset
data_file = "enrollment_csv_file/preprocessed_data/total_enrollment.csv"
df = pd.read_csv(data_file)

# Strip extra spaces from column names
df.columns = df.columns.str.strip()

# Define grade group columns
kinder_cols = ["K Male", "K Female"]
g1_g6_cols = [f"G{i} Male" for i in range(1, 7)] + [f"G{i} Female" for i in range(1, 7)]
jhs_cols = [f"G{i} Male" for i in range(7, 11)] + [f"G{i} Female" for i in range(7, 11)]
shs_cols = [col for col in df.columns if col.startswith("G11 ") or col.startswith("G12 ")]

# Other metadata columns
other_needed_cols = ["Region","Division","District","BEIS School ID","School Name","Street Address","Province","Municipality","Legislative District","Barangay","Sector","School Subclassification","School Type","Modified COC"]



# Function to filter based on Modified COC, keep relevant columns, and save to CSV
def save_data(coc_value, columns_to_keep, output_file):
    # Filter rows based on COC value
    df_filtered = df[df["Modified COC"].str.strip() == coc_value]
    
    # If no data found, skip and return
    if df_filtered.empty:
        print(f"No data found for COC: {coc_value}")
        return
    
    # Get final list of columns to retain
    cols_to_keep = (
        [col for col in other_needed_cols if col in df_filtered.columns] +
        [col for col in columns_to_keep if col in df_filtered.columns] +
        (["Total Enrollment"] if "Total Enrollment" in df_filtered.columns else [])
    )

    # Keep only the relevant columns
    df_filtered_cleaned = df_filtered[cols_to_keep]
    
    # Save to CSV
    df_filtered_cleaned.to_csv(output_file, index=False)
    print(f"Data for {coc_value} has been saved to {output_file}")


# Purely ES (only Grades 1-6)
save_data("Purely ES", g1_g6_cols, "enrollment_csv_file/preprocessed_data/data_by_coc/purely_es_data.csv")

# Purely JHS (only Grades 7-10)
save_data("Purely JHS", jhs_cols, "enrollment_csv_file/preprocessed_data/data_by_coc/purely_jhs_data.csv")

# Purely SHS (only Grades 11-12)
save_data("Purely SHS", shs_cols, "enrollment_csv_file/preprocessed_data/data_by_coc/purely_shs_data.csv")

# ES and JHS (Grades 1-10)
save_data("ES and JHS", g1_g6_cols + jhs_cols, "enrollment_csv_file/preprocessed_data/data_by_coc/es_and_jhs_data.csv")

# JHS and SHS (Grades 7-12)
save_data("JHS with SHS", jhs_cols + shs_cols, "enrollment_csv_file/preprocessed_data/data_by_coc/jhs_and_shs_data.csv")

# All Offering (Kinder, Grades 1-12)
save_data("All Offering", kinder_cols + g1_g6_cols + jhs_cols + shs_cols, "enrollment_csv_file/preprocessed_data/data_by_coc/all_offering_data.csv")

