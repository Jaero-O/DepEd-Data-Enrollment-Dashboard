import pandas as pd
import os
import shutil

def clean_dataset(csv_path):
    filename_no_ext = os.path.splitext(os.path.basename(csv_path))[0]
    print(csv_path)
    df = pd.read_csv(csv_path, skiprows=4, dtype={'BEIS School ID': 'object'})
    df_dropped = df.dropna(how='all').drop_duplicates()

    valid_format = df_dropped['BEIS School ID'].str.match(r'^\d{6}$')
    print(f"Valid BEIS School IDs: {valid_format.sum()}")
    print(f"Invalid BEIS School IDs: {(~valid_format).sum()}")

    df = df_dropped.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    if "beis_school" in df.columns:
        df = df.drop(columns=["beis_school"])

    df.loc[df['region'] == 'PSO', ['province', 'municipality', 'legislative_district', 'barangay']] = 'Others'

    cleaned_dir = "enrollment_csv_file\\cleaned_separate_datasets"
    data_type_dir = os.path.join(cleaned_dir, "data_types")
    os.makedirs(cleaned_dir, exist_ok=True)
    os.makedirs(data_type_dir, exist_ok=True)

    df.dtypes.to_csv(os.path.join(data_type_dir, f"{filename_no_ext}_data_types.csv"))
    df.to_csv(os.path.join(cleaned_dir, f"{filename_no_ext}.csv"), index=False)

    print(df.columns)

base_dir = 'enrollment_database'
unconverted_dir = os.path.join(base_dir, 'unconverted_xlsx_files')
os.makedirs(unconverted_dir, exist_ok=True)

files = [f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f))]

expected_csvs = set()

for file_name in files:
    file_path = os.path.join(base_dir, file_name)

    if not file_name.endswith(('.csv', '.xlsx')):
        continue

    base_name = ''.join(os.path.basename(file_name).strip().split())[:-5]
    csv_name = f"{base_name}.csv"
    csv_path = os.path.join(base_dir, csv_name)

    counter = 1
    while os.path.exists(csv_path):
        csv_name = f"{base_name}_{counter}.csv"
        csv_path = os.path.join(base_dir, csv_name)
        counter += 1

    if file_name.endswith('.xlsx'):
        temp = pd.read_excel(file_path)
        temp.to_csv(csv_path, index=None, header=True)
        shutil.move(file_path, os.path.join(unconverted_dir, os.path.basename(file_name)))
    else:
        csv_path = file_path

    print("Using file:", csv_path)
    clean_dataset(csv_path)

    cleaned_name = os.path.splitext(os.path.basename(csv_path))[0] + ".csv"
    expected_csvs.add(cleaned_name)

cleaned_dir = 'enrollment_csv_file\\cleaned_separate_datasets'
data_type_dir = os.path.join(cleaned_dir, 'data_types')
cleaned_csvs = set(f for f in os.listdir(cleaned_dir) if f.endswith('.csv'))

for csv_file in cleaned_csvs:
    if csv_file not in expected_csvs:
        file_path = os.path.join(cleaned_dir, csv_file)
        print(f"Deleting outdated file: {file_path}")
        os.remove(file_path)

        # Delete corresponding data type file
        data_type_file = os.path.join(data_type_dir, csv_file.replace('.csv', '_data_types.csv'))
        if os.path.exists(data_type_file):
            print(f"Deleting associated data type file: {data_type_file}")
            os.remove(data_type_file)
