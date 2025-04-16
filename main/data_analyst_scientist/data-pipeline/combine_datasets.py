import os
import pandas as pd

def aggregateDataset(range_school_year = [2023]):
    base_dir = 'enrollment_csv_file\\cleaned_separate_datasets'

    files = [f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f)) and f.endswith('.csv')]

    database = {}

    for file in files:
        file_path = os.path.join(base_dir, file)
        df_name = int(os.path.splitext(file)[0])
        database[df_name] = pd.read_csv(file_path)

    merged_df = pd.concat([database[key] for key in range_school_year], ignore_index=True)

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
    agg_dict.update({col: 'sum' for col in columns_to_sum})

    aggregated_df = merged_df.groupby('beis_school_id', as_index=False).agg(agg_dict)

    aggregated_df.to_csv('enrollment_csv_file/preprocessed_data/merged_aggregated_output.csv', index=False)
    # temporary csv file (sa cleaned_enrollment_data.csv na dapat toh)

aggregateDataset()
# sample use of function