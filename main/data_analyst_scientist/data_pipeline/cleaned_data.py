import os
import shutil
import pandas as pd
import sqlite3
import hashlib

def dataframe_hash(df: pd.DataFrame) -> str:
    """Returns a hash string of a DataFrame's contents."""
    return hashlib.sha256(
        pd.util.hash_pandas_object(df.sort_index(axis=1).reset_index(drop=True), index=False).values
    ).hexdigest()

def table_exists_and_equal(conn, table_name, new_df):
    try:
        old_df = pd.read_sql_query(f"SELECT * FROM `{table_name}`", conn)
        return dataframe_hash(old_df) == dataframe_hash(new_df)
    except Exception:
        return False

def clean_data(base_dir='enrollment_database'):
    def preprocess_file(file_path):
        df = pd.read_csv(file_path, skiprows=4, dtype={'BEIS School ID': 'object'})
        df = df.dropna(how='all').dropna(axis=1, how='all')
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

        if "beis_school" in df.columns:
            df = df.drop(columns=["beis_school"])

        df.loc[df['region'] == 'PSO', ['province', 'municipality', 'legislative_district', 'barangay']] = 'Others'
        df = df.drop_duplicates()

        filename_no_ext = os.path.splitext(os.path.basename(file_path))[0]
        if filename_no_ext.isdigit():
            df['school_year'] = int(filename_no_ext)

        return filename_no_ext, df

    shared_db_path = 'enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.db'
    unconverted_dir = os.path.join(base_dir, 'unconverted_xlsx_files')
    os.makedirs(unconverted_dir, exist_ok=True)

    files = [f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f))]
    cleaned_datasets = []

    # Step 1: Identify and convert files
    for file_name in files:
        file_path = os.path.join(base_dir, file_name)

        if not file_name.endswith(('.csv', '.xlsx')):
            continue

        if file_name.endswith('.xlsx'):
            base_name = ''.join(os.path.basename(file_name).strip().split())[:-5]
            csv_name = f"{base_name}.csv"
            csv_path = os.path.join(base_dir, csv_name)
            counter = 1
            while os.path.exists(csv_path):
                csv_name = f"{base_name}_{counter}.csv"
                csv_path = os.path.join(base_dir, csv_name)
                counter += 1
            pd.read_excel(file_path).to_csv(csv_path, index=None, header=True)
            shutil.move(file_path, os.path.join(unconverted_dir, os.path.basename(file_name)))
        else:
            csv_path = file_path

        cleaned_datasets.append(csv_path)

    # Step 2: Check if everything already exists and is equal
    all_tables_unchanged = True
    with sqlite3.connect(shared_db_path) as conn:
        for csv_path in cleaned_datasets:
            table_name, cleaned_df = preprocess_file(csv_path)
            if not table_exists_and_equal(conn, table_name, cleaned_df):
                all_tables_unchanged = False
                break

    if all_tables_unchanged:
        print("All cleaned tables already exist and are unchanged. Skipping processing.")
        return None

    # Step 3: Save updated versions
    print("⚙️ Some cleaned tables have changed. Reprocessing...")
    with sqlite3.connect(shared_db_path) as conn:
        for csv_path in cleaned_datasets:
            table_name, cleaned_df = preprocess_file(csv_path)
            if table_exists_and_equal(conn, table_name, cleaned_df):
                print(f"Skipped saving table '{table_name}' (no changes)")
            else:
                cleaned_df.to_sql(table_name, conn, if_exists='replace', index=False)
                print(f"Saved table '{table_name}' to {shared_db_path}")

    return None
