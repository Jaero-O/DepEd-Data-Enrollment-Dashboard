import pandas as pd

# Load CSV file
file_path = "SY 2023-2024 School Level Data on Official Enrollment 13.xlsx - DB.csv"
df = pd.read_csv(file_path, skiprows=4, dtype={'BEIS School': 'Int64'})

# Strip spaces from column names (in case of extra spaces)
df.columns = df.columns.str.strip()

# Extract unique values dynamically from relevant columns
regions = df['Region'].dropna().unique().tolist() if 'Region' in df.columns else []
divisions = df['Division'].dropna().unique().tolist() if 'Division' in df.columns else []
districts = df['District'].dropna().unique().tolist() if 'District' in df.columns else []
beis_school_ids = df['BEIS School ID'].dropna().unique().tolist() if 'BEIS School ID' in df.columns else []
school_names = df['School Name'].dropna().unique().tolist() if 'School Name' in df.columns else []
provinces = df['Province'].dropna().unique().tolist() if 'Province' in df.columns else []
municipalities = df['Municipality'].dropna().unique().tolist() if 'Municipality' in df.columns else []
legislative_districts = df['Legislative District'].dropna().unique().tolist() if 'Legislative District' in df.columns else []
sectors = df['Sector'].dropna().unique().tolist() if 'Sector' in df.columns else []
school_subclassifications = df['School Subclassification'].dropna().unique().tolist() if 'School Subclassification' in df.columns else []
school_types = df['School Type'].dropna().unique().tolist() if 'School Type' in df.columns else []
modified_cocs = df['Modified COC'].dropna().unique().tolist() if 'Modified COC' in df.columns else []

# Function to filter based on a given column and value
def filter_dataframe(df, column_name, value, unique_values):
    """Filters the DataFrame for rows where the given column matches the value."""
    if column_name in df.columns:
        if value in unique_values:
            return df[df[column_name] == value]
        else:
            print(f"Error: '{value}' is not in the available {column_name} list.")
            return pd.DataFrame()
    else:
        print(f"Error: '{column_name}' column not found in DataFrame.")
        return pd.DataFrame()

# Individual functions for each filter
def filter_region(df, region_name):
    return filter_dataframe(df, "Region", region_name, regions)

def filter_division(df, division_name):
    return filter_dataframe(df, "Division", division_name, divisions)

def filter_district(df, district_name):
    return filter_dataframe(df, "District", district_name, districts)

def filter_beis_school_id(df, beis_school_id):
    """Ensures filtering works correctly for integer-based BEIS School ID."""
    if isinstance(beis_school_id, int):
        return filter_dataframe(df, "BEIS School ID", beis_school_id, beis_school_ids)
    else:
        print("Error: BEIS School ID should be an integer.")
        return pd.DataFrame()

def filter_school_name(df, school_name):
    return filter_dataframe(df, "School Name", school_name, school_names)

def filter_province(df, province_name):
    return filter_dataframe(df, "Province", province_name, provinces)

def filter_municipality(df, municipality_name):
    return filter_dataframe(df, "Municipality", municipality_name, municipalities)

def filter_legislative_district(df, legislative_district_name):
    return filter_dataframe(df, "Legislative District", legislative_district_name, legislative_districts)

def filter_sector(df, sector_name):
    return filter_dataframe(df, "Sector", sector_name, sectors)

def filter_school_subclassification(df, subclassification_name):
    return filter_dataframe(df, "School Subclassification", subclassification_name, school_subclassifications)

def filter_school_type(df, school_type_name):
    return filter_dataframe(df, "School Type", school_type_name, school_types)

def filter_modified_coc(df, modified_coc_name):
    return filter_dataframe(df, "Modified COC", modified_coc_name, modified_cocs)

# Example usage: Store filtered data in a new DataFrame
#region_a_df = filter_region(df, "CARAGA")
#division_b_df = filter_division(df, "Cebu")
#district_c_df = filter_district(df, "Badoc")
#beis_school_id_d_df = filter_beis_school_id(df, 105098)
#school_name_e_df = filter_school_name(df, "San Miguel National High School")
#province_f_df = filter_province(df, "ILOCOS NORTE")
#municipality_g_df = filter_municipality(df, "BACARRA")
#legislative_district_h_df = filter_legislative_district(df, "1st District")
#sector_i_df = filter_sector(df, "Public")
#school_subclassification_j_df = filter_school_subclassification(df, "LUC")
#school_type_k_df = filter_school_type(df, "School with no Annexes")
#modified_coc_l_df = filter_modified_coc(df, "Purely ES")

# Display filtered data
#print(region_a_df)
#print(division_b_df)
#print(district_c_df)
#print(beis_school_id_d_df)
#print(school_name_e_df)
#print(province_f_df)
#print(municipality_g_df)
#print(legislative_district_h_df)
#print(sector_i_df)
#print(school_subclassification_j_df)
#print(school_type_k_df)
#print(modified_coc_l_df)
