import os
import sqlite3
import pandas as pd

def aggregateDataset(range_school_year=[2023], db_path='enrollment_csv_file\preprocessed_data\cleaned_enrollment_data.db'):
    conn = sqlite3.connect(db_path)
    database = []
    metadata_rows = []
    enrollment_summary = []

    for year in range_school_year:
        try:
            df = pd.read_sql_query(f"SELECT * FROM `{year}`", conn)
            df['school_year'] = year  # Track year in dataframe
            database.append(df)

            metadata_rows.append({'table_name': str(year), 'school_year': year})

            # Sum enrollment columns
            numeric_cols = df.select_dtypes(include='number').columns
            enrollment_cols = [col for col in numeric_cols if '_male' in col or '_female' in col]
            total_enrollment = df[enrollment_cols].sum(numeric_only=True).sum()
            enrollment_summary.append({'school_year': year, 'total_enrollment': int(total_enrollment)})

        except Exception as e:
            raise ValueError(f"Error reading table `{year}`: {e}")

    merged_df = pd.concat(database, ignore_index=True)

    columns_to_sum = [
        'k_male', 'k_female', 'g1_male', 'g1_female', 'g2_male', 'g2_female',
        'g3_male', 'g3_female', 'g4_male', 'g4_female', 'g5_male', 'g5_female',
        'g6_male', 'g6_female', 'elem_ng_male', 'elem_ng_female', 'g7_male', 'g7_female',
        'g8_male', 'g8_female', 'g9_male', 'g9_female', 'g10_male', 'g10_female',
        'jhs_ng_male', 'jhs_ng_female', 'g11_acad_-_abm_male', 'g11_acad_-_abm_female',
        'g11_acad_-_humss_male', 'g11_acad_-_humss_female', 'g11_acad_stem_male',
        'g11_acad_stem_female', 'g11_acad_gas_male', 'g11_acad_gas_female',
        'g11_acad_pbm_male', 'g11_acad_pbm_female', 'g11_tvl_male', 'g11_tvl_female',
        'g11_sports_male', 'g11_sports_female', 'g11_arts_male', 'g11_arts_female',
        'g12_acad_-_abm_male', 'g12_acad_-_abm_female', 'g12_acad_-_humss_male',
        'g12_acad_-_humss_female', 'g12_acad_stem_male', 'g12_acad_stem_female',
        'g12_acad_gas_male', 'g12_acad_gas_female', 'g12_acad_pbm_male',
        'g12_acad_pbm_female', 'g12_tvl_male', 'g12_tvl_female', 'g12_sports_male',
        'g12_sports_female', 'g12_arts_male', 'g12_arts_female'
    ]

    columns_to_last = [
        'region', 'division', 'district', 'school_name', 'street_address',
        'province', 'municipality', 'legislative_district', 'barangay', 'sector',
        'school_subclassification', 'school_type', 'modified_coc'
    ]

    agg_dict = {col: 'last' for col in columns_to_last}
    agg_dict.update({col: 'mean' for col in columns_to_sum})
    agg_dict['school_year'] = 'last'

    aggregated_df = merged_df.groupby('beis_school_id', as_index=False).agg(agg_dict)

    # Save main aggregated data
    aggregated_df.to_sql('aggregated_enrollment', conn, if_exists='replace', index=False)
    print("Aggregated data saved to 'aggregated_enrollment' in cleaned_enrollment_data.db")

    # Save table metadata
    metadata_df = pd.DataFrame(metadata_rows)
    metadata_df.to_sql('table_metadata', conn, if_exists='replace', index=False)
    print("Table metadata saved to 'table_metadata'")

    # Save total enrollment summary
    enrollment_summary_df = pd.DataFrame(enrollment_summary)
    enrollment_summary_df.to_sql('total_enrollment_by_year', conn, if_exists='replace', index=False)
    print("Total enrollment summary saved to 'total_enrollment_by_year'")

    conn.close()
    return aggregated_df

# Example call
# aggregateDataset(range_school_year=[2015, 2023])
