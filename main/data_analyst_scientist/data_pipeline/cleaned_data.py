import os
import shutil
import pandas as pd
import sqlite3

def clean_data(base_dir='enrollment_database'):
    def clean_dataset(csv_path):
        filename_no_ext = os.path.splitext(os.path.basename(csv_path))[0]
        print(f"Processing file: {csv_path}")
        
        df = pd.read_csv(csv_path, skiprows=4, dtype={'BEIS School ID': 'object'})

        df = df.dropna(how='all')
        df = df.dropna(axis=1, how='all')

        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

        if "beis_school" in df.columns:
            df = df.drop(columns=["beis_school"])

        df.loc[df['region'] == 'PSO', ['province', 'municipality', 'legislative_district', 'barangay']] = 'Others'
        df = df.drop_duplicates()

        if 'beis_school_id' in df.columns:
            valid_format = df['beis_school_id'].str.match(r'^\d{6}$')
            print(f"Valid BEIS School IDs: {valid_format.sum()}")
            print(f"Invalid BEIS School IDs: {(~valid_format).sum()}")
        else:
            print("Column 'beis_school_id' not found after cleaning.")

        print(f"Cleaned columns: {df.columns.tolist()}")

        # Save to cleaned_enrollment_data.db
        if filename_no_ext.isdigit():
            df['school_year'] = int(filename_no_ext)

        shared_db_path = 'enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.db'
        table_name = filename_no_ext

        with sqlite3.connect(shared_db_path) as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"Saved table '{table_name}' to {shared_db_path}")

    # File processing
    unconverted_dir = os.path.join(base_dir, 'unconverted_xlsx_files')
    os.makedirs(unconverted_dir, exist_ok=True)

    files = [f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f))]

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

    return None

clean_data()
