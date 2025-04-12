import pandas as pd

df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

# ===========
regions_df = df[['Region']].drop_duplicates().reset_index(drop=True)
regions_df['Region ID'] = regions_df.index + 1
region_map = dict(zip(regions_df['Region'], regions_df['Region ID']))

# ===========
divisions_df = df[['Division', 'Region']].drop_duplicates().reset_index(drop=True)
divisions_df['Region ID'] = divisions_df['Region'].map(region_map)
divisions_df['Division ID'] = divisions_df.index + 1
division_map = dict(zip(divisions_df['Division'], divisions_df['Division ID']))

# ===========
district_df = df[['District', 'Division']].drop_duplicates().reset_index(drop=True)
district_df['Division ID'] = district_df['Division'].map(division_map)
district_df['District ID'] = district_df.index + 1
district_map = dict(zip(district_df['District'], district_df['District ID']))

# ===========
district_df = df[['District', 'Division']].drop_duplicates().reset_index(drop=True)
district_df['Division ID'] = district_df['Division'].map(division_map)
district_df['District ID'] = district_df.index + 1
district_map = dict(zip(district_df['District'], district_df['District ID']))

# ===========
legislative_district_df = df[['Legislative District', 'District']].drop_duplicates().reset_index(drop=True)
legislative_district_df['District ID'] = legislative_district_df['District'].map(district_map)
legislative_district_df['Legislative District ID'] = legislative_district_df.index + 1
legislative_district_map = dict(zip(legislative_district_df['Legislative District'], legislative_district_df['Legislative District ID']))


# ===========
province_df = df[['Province', 'Region']].drop_duplicates().reset_index(drop=True)
province_df['Region ID'] = province_df['Region'].map(region_map)
province_df['Province ID'] = province_df.index + 1
province_map = dict(zip(province_df['Province'], province_df['Province ID']))

# ===========
municipality_df = df[['Municipality', 'Province']].drop_duplicates().reset_index(drop=True)
municipality_df['Province ID'] = municipality_df['Province'].map(province_map)
municipality_df['Municipality ID'] = municipality_df.index + 1
municipality_map = dict(zip(municipality_df['Municipality'], municipality_df['Municipality ID']))

# ===========
barangay_df = df[['Barangay', 'Municipality']].drop_duplicates().reset_index(drop=True)
barangay_df['Municipality ID'] = barangay_df['Municipality'].map(municipality_map)
barangay_df['Barangay ID'] = barangay_df.index + 1
barangay_map = dict(zip(barangay_df['Barangay'], barangay_df['Barangay ID']))

# ===========
school_loc_df = df[['School Name', 'Barangay']].drop_duplicates().reset_index(drop=True)
school_loc_df['Barangay ID'] = school_loc_df['Barangay'].map(barangay_map)
school_loc_df['School ID'] = df['BEIS School ID']
school_loc_map = dict(zip(school_loc_df['School Name'], school_loc_df['School ID']))

# ===========
schools_df = df[['BEIS School ID', 'School Name', 'School Type', 'Division', 'Modified COC', 'School Subclassification', 'Sector']].copy()

schools_df['Division ID'] = schools_df['Division'].map(division_map)
schools_df = schools_df[['BEIS School ID', 'School Name', 'School Type', 'Modified COC', 'School Subclassification', 'Sector']]

# ======
enrollment_columns = df.columns[14:]  # enrollment starts at column 14
enrollments_df = df.melt(
    id_vars=['BEIS School ID'],
    value_vars=enrollment_columns,
    var_name='Grade_Gender',
    value_name='Enrollment Count'
)

# Extract grade level and gender
enrollments_df[['Grade Level', 'Gender']] = enrollments_df['Grade_Gender'].str.extract(r'(.*)\s+(Male|Female)', expand=True)

# Clean up
enrollments_df['Enrollment Count'] = pd.to_numeric(enrollments_df['Enrollment Count'], errors='coerce')
enrollments_df = enrollments_df.dropna(subset=['Enrollment Count'])
enrollments_df = enrollments_df[['BEIS School ID', 'Grade Level', 'Gender', 'Enrollment Count']]

# ======
regions_df.to_csv("enrollment_csv_file/normalized_dataset/regions.csv", index=False)
divisions_df.to_csv("enrollment_csv_file/normalized_dataset/divisions.csv", index=False)
district_df.to_csv("enrollment_csv_file/normalized_dataset/districts.csv", index=False)
legislative_district_df.to_csv("enrollment_csv_file/normalized_dataset/legislative_districts.csv", index=False)

province_df.to_csv("enrollment_csv_file/normalized_dataset/provinces.csv", index=False)
municipality_df.to_csv("enrollment_csv_file/normalized_dataset/municipalities.csv", index=False)
barangay_df.to_csv("enrollment_csv_file/normalized_dataset/barangays.csv", index=False)

schools_df.to_csv("enrollment_csv_file/normalized_dataset/schools.csv", index=False)
enrollments_df.to_csv("enrollment_csv_file/normalized_dataset/enrollments.csv", index=False)
