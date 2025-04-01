import pandas as pd

# Load CSV file
file_path = "SY 2023-2024 School Level Data on Official Enrollment 13.xlsx - DB.csv"
df = pd.read_csv(file_path, skiprows=4)

# Strip spaces from column names (in case of extra spaces)
df.columns = df.columns.str.strip()

# Extract unique values dynamically from 'Region', 'Division', and 'District' columns
regions = df['Region'].dropna().unique().tolist() if 'Region' in df.columns else []
divisions = df['Division'].dropna().unique().tolist() if 'Division' in df.columns else []
districts = df['District'].dropna().unique().tolist() if 'District' in df.columns else []

# Function to filter DataFrame based on a given region
def filter_region(df, region_name):
    """Filters the DataFrame for rows where the Region column matches the given region_name."""
    if "Region" in df.columns:
        if region_name in regions:
            return df[df["Region"] == region_name]
        else:
            print(f"Error: '{region_name}' is not in the available regions list.")
            return pd.DataFrame()
    else:
        print("Error: 'Region' column not found in DataFrame.")
        return pd.DataFrame()

# Function to filter DataFrame based on a given division
def filter_division(df, division_name):
    """Filters the DataFrame for rows where the Division column matches the given division_name."""
    if "Division" in df.columns:
        if division_name in divisions:
            return df[df["Division"] == division_name]
        else:
            print(f"Error: '{division_name}' is not in the available divisions list.")
            return pd.DataFrame()
    else:
        print("Error: 'Division' column not found in DataFrame.")
        return pd.DataFrame()
    
# Function to filter DataFrame based on a given district
def filter_district(df, district_name):
    """Filters the DataFrame for rows where the District column matches the given district_name."""
    if "District" in df.columns:
        if district_name in districts:
            return df[df["District"] == district_name]
        else:
            print(f"Error: '{district_name}' is not in the available districts list.")
            return pd.DataFrame()
    else:
        print("Error: 'District' column not found in DataFrame.")
        return pd.DataFrame()

# Example usage: Store filtered data in a new DataFrame
region_caraga_df = filter_region(df, "CARAGA")
division_cebu_df = filter_division(df, "Cebu")
district_badoc_df = filter_district(df, "Badoc")

# Display filtered data
print(region_caraga_df)
print(division_cebu_df)
print(district_badoc_df)