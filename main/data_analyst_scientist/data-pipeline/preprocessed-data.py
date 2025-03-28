import pandas as pd

file_path = "SY 2023-2024 School Level Data on Official Enrollment 13.xlsx - DB.csv"
df = pd.read_csv(file_path)

def filter_region(df, region_name="Region 1"):
    """Filters the DataFrame for rows where the Region column matches the given region_name."""
    filtered_df = df[df["Region"] == region_name]
    return filtered_df

region_1_df = filter_region(df)

print(region_1_df.head())
