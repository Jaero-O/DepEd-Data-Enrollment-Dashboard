import pandas as pd

# Load CSV file
file_path = "SY 2023-2024 School Level Data on Official Enrollment 13.xlsx - DB.csv"  # Change this to your actual file path
df = pd.read_csv(file_path, skiprows=4)

# Function to filter Region with value "Region 1"
def filter_region(df, region_name="Region I"):
    """Filters the DataFrame for rows where the Region column matches the given region_name."""
    filtered_df = df[df["Region"] == region_name]  # Change "Region" to the actual column name in your dataset
    return filtered_df

# Call the function and store the filtered DataFrame
region_1_df = filter_region(df)

# Display the filtered data
print(region_1_df.head())
