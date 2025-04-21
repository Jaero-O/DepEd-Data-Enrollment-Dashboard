import pandas as pd
import sqlite3
import os

df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

# ===========
regions_df = df[['region']].drop_duplicates().reset_index(drop=True)
regions_df['region_id'] = regions_df.index + 1
region_map = dict(zip(regions_df['region'], regions_df['region_id']))

# ===========
divisions_df = df[['division', 'region']].drop_duplicates().reset_index(drop=True)
divisions_df['region_id'] = divisions_df['region'].map(region_map)
divisions_df['division_id'] = divisions_df.index + 1
division_map = dict(zip(divisions_df['division'], divisions_df['division_id']))

# ===========
district_df = df[['district', 'division']].drop_duplicates().reset_index(drop=True)
district_df['division_id'] = district_df['division'].map(division_map)
district_df['district_id'] = district_df.index + 1
district_map = dict(zip(district_df['district'], district_df['district_id']))

# ===========
district_df = df[['district', 'division']].drop_duplicates().reset_index(drop=True)
district_df['division_id'] = district_df['division'].map(division_map)
district_df['district_id'] = district_df.index + 1
district_map = dict(zip(district_df['district'], district_df['district_id']))

# ===========
legislative_district_df = df[['legislative_district', 'district']].drop_duplicates().reset_index(drop=True)
legislative_district_df['district_id'] = legislative_district_df['district'].map(district_map)
legislative_district_df['Legislative district_id'] = legislative_district_df.index + 1
legislative_district_map = dict(zip(legislative_district_df['legislative_district'], legislative_district_df['Legislative district_id']))


# ===========
province_df = df[['province', 'region']].drop_duplicates().reset_index(drop=True)
province_df['region_id'] = province_df['region'].map(region_map)
province_df['province_id'] = province_df.index + 1
province_map = dict(zip(province_df['province'], province_df['province_id']))

# ===========
municipality_df = df[['municipality', 'province']].drop_duplicates().reset_index(drop=True)
municipality_df['province_id'] = municipality_df['province'].map(province_map)
municipality_df['municipality_id'] = municipality_df.index + 1
municipality_map = dict(zip(municipality_df['municipality'], municipality_df['municipality_id']))

# ===========
barangay_df = df[['barangay', 'municipality']].drop_duplicates().reset_index(drop=True)
barangay_df['municipality_id'] = barangay_df['municipality'].map(municipality_map)
barangay_df['barangay_id'] = barangay_df.index + 1
barangay_map = dict(zip(barangay_df['barangay'], barangay_df['barangay_id']))

# ===========
school_loc_df = df[['school_name', 'barangay']].drop_duplicates().reset_index(drop=True)
school_loc_df['barangay_id'] = school_loc_df['barangay'].map(barangay_map)
school_loc_df['School ID'] = df['beis_school_id']
school_loc_map = dict(zip(school_loc_df['school_name'], school_loc_df['School ID']))

# ===========
schools_df = df[['beis_school_id', 'school_name', 'school_type', 'division', 'modified_coc', 'school_subclassification', 'sector']].copy()

schools_df['division_id'] = schools_df['division'].map(division_map)
schools_df = schools_df[['beis_school_id', 'school_name', 'school_type', 'modified_coc', 'school_subclassification', 'sector']]

# ======
enrollment_columns = df.columns[14:]  # enrollment starts at column 14
enrollments_df = df.melt(
    id_vars=['beis_school_id'],
    value_vars=enrollment_columns,
    var_name='Grade_Gender',
    value_name='enrollment_count'
)

# Extract grade level and gender
enrollments_df[['grade_level', 'gender']] = enrollments_df['Grade_Gender'].str.extract(r'(.*)\s+(Male|Female)', expand=True)

# Clean up
enrollments_df['enrollment_count'] = pd.to_numeric(enrollments_df['enrollment_count'], errors='coerce')
enrollments_df = enrollments_df.dropna(subset=['enrollment_count'])
enrollments_df = enrollments_df[['beis_school_id', 'grade_level', 'gender', 'enrollment_count']]

# ======
os.makedirs("enrollment_csv_file/normalized_dataset/norm_csv/", exist_ok=True)

regions_df.to_csv("enrollment_csv_file/normalized_dataset/norm_csv/regions.csv", index=False)
divisions_df.to_csv("enrollment_csv_file/normalized_dataset/norm_csv/divisions.csv", index=False)
district_df.to_csv("enrollment_csv_file/normalized_dataset/norm_csv/districts.csv", index=False)
legislative_district_df.to_csv("enrollment_csv_file/normalized_dataset/norm_csv/legislative_districts.csv", index=False)

province_df.to_csv("enrollment_csv_file/normalized_dataset/norm_csv/provinces.csv", index=False)
municipality_df.to_csv("enrollment_csv_file/normalized_dataset/norm_csv/municipalities.csv", index=False)
barangay_df.to_csv("enrollment_csv_file/normalized_dataset/norm_csv/barangays.csv", index=False)

schools_df.to_csv("enrollment_csv_file/normalized_dataset/norm_csv/schools.csv", index=False)
enrollments_df.to_csv("enrollment_csv_file/normalized_dataset/norm_csv/enrollments.csv.gzip", compression="gzip", index=False)

print("All CSV files have been saved successfully in 'enrollment_csv_file/normalized_dataset/norm_csv/'")

def create_and_load_tables_from_csv(db_name, csv_dir):

    table_files = {
        "regions": "regions.csv",
        "divisions": "divisions.csv",
        "districts": "districts.csv",
        "legislative_districts": "legislative_districts.csv",
        "provinces": "provinces.csv",
        "municipalities": "municipalities.csv",
        "barangays": "barangays.csv",
        "schools": "schools.csv",
        "enrollments": "enrollments.csv.gzip"
    }

    conn = sqlite3.connect(db_name)
    print(f"Connected to database: {db_name}")

    try:
        for table_name, file_name in table_files.items():
            file_path = os.path.join(csv_dir, file_name)
            
            if file_name.endswith(".gzip"):
                df = pd.read_csv(file_path, compression='gzip')
            else:
                df = pd.read_csv(file_path)

            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"Table '{table_name}' created and loaded from '{file_name}'")
    except Exception as e:
        print("Error processing files:", e)
    finally:
        conn.close()
        print("Connection closed.")

create_and_load_tables_from_csv("enrollment_csv_file/normalized_dataset/normalized_data.db", "enrollment_csv_file/normalized_dataset/norm_csv")