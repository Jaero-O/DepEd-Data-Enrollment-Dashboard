from pathlib import Path

folder_path = Path('enrollment_database')
filenames = [f.name for f in folder_path.iterdir() if f.is_file()]
years = [int(f.replace('.csv', '')) for f in filenames]
print(filenames)
print(years)