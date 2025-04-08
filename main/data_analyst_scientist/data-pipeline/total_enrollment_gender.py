import pandas as pd

# Load the cleaned enrollment data CSV file
data_file = "enrollment_csv_file\preprocessed_data\cleaned_enrollment_data.csv"
df = pd.read_csv(data_file)

# Strip spaces from column names
df.columns = df.columns.str.strip()

# Define male and female column lists
male_columns = [col for col in df.columns if "Male" in col]
female_columns = [col for col in df.columns if "Female" in col]

# Compute total enrollment per grade level
for male_col, female_col in zip(male_columns, female_columns):
    grade = male_col.replace(" Male", "")  # Extract grade level name
    df[f"Total {grade}"] = df[male_col] + df[female_col]  # Sum male & female for each grade

# Compute total enrollment per gender
df["Total Male Enrollment"] = df[male_columns].sum(axis=1)
df["Total Female Enrollment"] = df[female_columns].sum(axis=1)

# Compute overall total enrollment
df["Total Enrollment"] = df["Total Male Enrollment"] + df["Total Female Enrollment"]

# Save the updated dataset
df.to_csv("enrollment_csv_file/preprocessed_data/total_enrollment_gender.csv", index=False)

# Display the first few rows
print(df.head(20))