import pandas as pd

# Load CSV file
file_path = "SY 2023-2024 School Level Data on Official Enrollment 13.xlsx - DB.csv"
df = pd.read_csv(file_path, skiprows=4)

# Strip spaces from column names (in case of extra spaces)
df.columns = df.columns.str.strip()

# List of all regions
regions = [
    "Region I", "Region II", "Region III", "Region IV-A", "Region V", "Region VI",
    "Region VII", "Region VIII", "Region IX", "Region X", "Region XI", "Region XII",
    "BARMM", "CAR", "CARAGA", "MIMAROPA", "NCR", "PSO"
]

# List of all divisions
divisions = [
    "Abra", "Agusan del Norte", "Agusan del Sur", "Aklan", "Alaminos City", "Albay",
    "Angeles City", "Antipolo City", "Antique", "Apayao", "Aurora", "Bacoor City",
    "Bacolod City", "Bago City", "Baguio City", "Bais City", "Balanga City", "Basilan",
    "Batac City", "Bataan", "Batangas", "Batangas City", "Bayawan City", "Baybay City",
    "Bayugan City", "Benguet", "Biliran", "Binan City", "Bislig City", "Bogo City",
    "Borongan City", "Bulacan", "Butuan City", "Cabadbaran City", "Cabanatuan City",
    "Cagayan", "Cagayan de Oro City", "Calamba City", "Calapan City", "Calbayog City",
    "Caloocan City", "Camarines Norte", "Camarines Sur", "Camiguin", "Canlaon City",
    "Candon City", "Capiz", "Carcar City", "Catanduanes", "Catbalogan City",
    "Cauayan City", "Cebu", "Cebu City", "City of Ilagan", "City of Naga, Cebu",
    "City of San Jose Del Monte", "City of San Juan", "Cotabato City", "Dagupan City",
    "Danao City", "Dasmarinas City", "Dapitan City", "Davao City", "Davao De Oro",
    "Davao Occidental", "Davao Oriental", "Davao del Norte", "Davao del Sur",
    "Dinagat Island", "Digos City", "Dipolog City", "Dumaguete City", "Eastern Samar",
    "El Salvador", "Escalante City", "General Santos City", "General Trias City",
    "Gingoog City", "Gapan City", "Greece", "Guimaras", "Guihulngan City",
    "Himamaylan City", "Ifugao", "Iligan City", "Ilocos Norte", "Ilocos Sur",
    "Iloilo", "Iloilo City", "Imus City", "Iriga City", "Island Garden City of Samal",
    "Isabela", "Isabela City", "Italy", "Kidapawan City", "Kalinga",
    "Kingdom of Bahrain", "Kingdom of Saudi Arabia", "Koronadal City",
    "La Carlota City", "La Union", "Lanao del Norte", "Lanao del Sur - I",
    "Lanao del Sur - II", "Laoag City", "Lapu-Lapu City", "Las Piñas City",
    "Legaspi City", "Leyte", "Ligao City", "Lipa City", "Lucena City", "MIMAROPA",
    "Mabalacat City", "Maguindanao I", "Maguindanao II", "Makati City",
    "Malabon City", "Malaybalay City", "Malolos City", "Mandaluyong City",
    "Mandaue City", "Manila", "Marawi City", "Marikina City", "Marinduque", "Masbate",
    "Masbate City", "Mati City", "Maasin City", "Meycauayan City",
    "Misamis Occidental", "Misamis Oriental", "Mountain Province", "Muntinlupa City",
    "NCR", "Naga City", "Navotas", "Negros Occidental", "Negros Oriental",
    "Northern Samar", "Nueva Ecija", "Nueva Vizcaya", "Occidental Mindoro",
    "Olongapo City", "Oriental Mindoro", "Ormoc City", "Oroquieta City",
    "Ozamis City", "Palawan", "Pampanga", "Panabo City", "Pangasinan I, Lingayen",
    "Pangasinan II, Binalonan", "Paranaque City", "Pasay City", "Pasig City",
    "Passi City", "Puerto Princesa City", "Quezon", "Quezon City", "Quirino",
    "Qatar", "Rizal", "Roxas City", "Sagay City", "Samar (Western Samar)",
    "San Carlos City", "San Fernando City", "San Jose City", "San Pablo City",
    "San Pedro City", "Santiago City", "Sarangani", "Science City of Muñoz",
    "Silay City", "Siquijor", "Sipalay City", "South Cotabato", "Southern Leyte",
    "Special Geographic Area Division", "Sorsogon", "Sorsogon City",
    "State of Kuwait", "Sto. Tomas City", "Sorsogon City", "Sultan Kudarat",
    "Sultanate of Oman", "Surigao City", "Surigao del Norte", "Surigao del Sur",
    "Tabaco City", "Tabuk City", "Tacloban City", "Tacurong City", "Tagbilaran City",
    "Taguig City and Pateros", "Tagum City", "Talisay City", "Talisay City",
    "Tandag City", "Tanauan City", "Tanjay City", "Tarlac", "Tarlac City",
    "Tawi-Tawi", "Toledo City", "Tuguegarao City", "Urdaneta City",
    "United Arab Emirates", "Valencia City", "Valenzuela City", "Victorias City",
    "Vigan City", "Zambales", "Zamboanga City", "Zamboanga Sibugay",
    "Zamboanga del Norte", "Zamboanga del Sur"
]
# Note: huhu hanggang page 15/57 pa lang 'tong list ng districts, ang dami hindi ko na alam gagawin HAHAHAHHAHAHA
districts = [
  "Bacarra I", "Bacarra II", "Badoc", "Bangui", "Banna (Espiritu)", "Burgos", "Currimao", "Dingras I", "Dingras II",
  "Marcos-Nueva Era", "Adams-Pagudpud", "Paoay", "Pasuquin", "Piddig", "Pinili", "San Nicolas", "Sarrat", "Solsona",
  "Vintar I", "Vintar II", "Alilem-Sugpon", "Banayoyo-Lidlidda-San Emilio", "Bantay", "Burgos-San Esteban", "Cabugao",
  "Caoayan", "Cervantes-Quirino", "Magsingal", "Narvacan North", "Narvacan South-Nagbukel",
  "Salcedo-Galimuyod-Sigay-Del Pilar", "San Juan", "San Vicente", "Santa", "Santiago", "Sinait", "Sta. Catalina",
  "Sta. Cruz", "Sta. Lucia", "Sta. Maria", "Sto. Domingo-San Ildefonso", "Suyo", "Tagudin", "Agoo East", "Agoo West",
  "Aringay", "Bacnotan", "Bagulin", "Balaoan", "Bangar", "Bauang North", "Bauang South", "Caba", "Luna I", "Luna II",
  "Naguilian", "Pugo", "Rosario", "San Gabriel", "Santol", "Sto. Tomas", "Sudipen", "Tubao", "Agno", "Aguilar", "Anda",
  "Bani", "Basista", "Bayambang I", "Bayambang II", "Binmaley I", "Binmaley II", "Bolinao", "Bugallon I", "Bugallon II",
  "Calasiao I", "Calasiao II", "Dasol", "Infanta", "Labrador", "Lingayen I", "Lingayen II", "Lingayen III", "Mabini",
  "Malasiqui I", "Malasiqui II", "Mangatarem I", "Mangatarem II", "Mapandan", "Sta. Barbara I", "Sta. Barbara II",
  "Sual", "Urbiztondo", "Alcala", "Asingan I", "Asingan II", "Balungao", "Bautista", "Binalonan I", "Binalonan II",
  "Laoac", "Manaoag", "Mangaldan I", "Mangaldan II", "Natividad", "Pozorrubio I", "Pozorrubio II", "Rosales I",
  "Rosales II", "San Fabian I", "San Fabian II", "San Jacinto", "San Manuel", "San Nicolas I", "San Nicolas II",
  "San Quintin", "Sison", "Tayug I", "Tayug II", "Umingan I", "Umingan II", "Villasis I", "Villasis II",
  "Dagupan City District I", "Dagupan City District II", "Dagupan City District III", "Dagupan City District IV",
  "Laoag City District I", "Laoag City District II", "Laoag City District III", "San Carlos City District I",
  "San Carlos City District II", "San Carlos City District III", "San Carlos City District IV",
  "Urdaneta City District I", "Urdaneta City District II", "District I", "District II", "District III",
  "San Fernando I", "San Fernando II", "Batac I", "Batac II", "Basco", "Itbayat", "Ivana-Uyugan", "Mahatao",
  "Sabtang", "Abulug", "Alcala East", "Allacapan North", "Amulung East", "Amulung West", "Aparri East", "Aparri West",
  "Baggao North", "Baggao West", "Ballesteros", "Buguey North", "Calayan West", "Camalaniugan", "Claveria East",
  "Enrile East", "Enrile West", "Gattaran East", "Gattaran West", "Gonzaga West", "Iguig", "Lal-lo North",
  "Lal-lo South", "Lasam East", "Pamplona", "Penablanca East", "Penablanca West", "Piat", "Rizal", "Sanchez Mira",
  "Solana North", "Solana South", "Sta. Ana", "Sta. Praxedes", "Sta. Teresita", "Sto. Nino", "Tuao East", "Tuao West",
  "Baggao East", "Gattaran Central", "Solana West Educational Zone", "Alcala West", "Aparri South Educational Zone",
  "Buguey South", "Gonzaga East", "Lal-lo Central", "Allacapan South", "Lasam West", "Calayan East", "Baggao South",
  "Alicia North", "Alicia South", "Angadanan East", "Angadanan West", "Aurora", "Benito Soliven", "Cabagan",
  "Cordon North", "Delfin Albano", "Echague East", "Echague South", "Echague West", "Gamu", "Jones East", "Jones West",
  "Luna", "Mallig", "Palanan", "Quezon", "Quirino", "Ramon", "Reina Mercedes", "Roxas East", "Roxas West",
  "San Agustin", "San Guillermo", "San Isidro", "San Mariano I", "San Mariano II", "San Mateo North",
  "San Mateo South", "San Pablo", "Tumauini North", "Tumauini South", "Cabatuan East", "Cabatuan West", "Alicia East",
  "Cordon South", "Aritao East", "Bagabag I", "Bambang I", "Bambang II", "Bayombong I", "Bayombong II", "Diadi",
  "Dupax del Norte I", "Dupax del Sur", "Kasibu East", "Eastern Kayapa", "Solano I", "Solano II", "Sta. Fe",
  "Villaverde", "Ambaguio", "Alfonso Castañeda", "Kasibu West", "Western Kayapa", "Aritao West", "Bagabag II",
  "Dupax del Norte II", "Aglipay", "Cabarroguis", "Diffun I", "Diffun II", "Maddela Zone I", "Nagtipunan", "Saguday",
  "Maddela Zone II", "Tuguegarao East Educational Zone", "Tuguegarao North Educational Zone",
  "Tuguegarao West Educational Zone", "Tuguegarao Northeast Educational Zone", "Cauayan East District",
  "Cauayan North District", "Cauayan South District", "Cauayan West District", "Cauayan Northeast District",
  "Santiago East", "Santiago North", "Santiago South", "Santiago West", "East", "South", "West", "North",
  "Northwest", "San Antonio", "San Jose City East", "San Jose City West", "Baler", "Casiguran", "Dilasag",
  "Dinalungan", "Dingalan", "Dipaculao", "Ma. Aurora", "San Luis", "Abucay", "Bagac", "Dinalupihan East", "Hermosa",
  "Limay", "Mariveles", "Morong", "Orani", "Orion", "Pilar", "Samal", "Dinalupihan West",
  "San Jose Del Monte East", "San Jose Del Monte West", "San Fernando East", "San Fernando North", "San Fernando West", "Gapan North", "Gapan South",
  "Tarlac Central District", "Tarlac East District", "Tarlac North District A", "Tarlac South District A", "Tarlac West District A",
  "Tarlac North District B", "Tarlac South District B", "Tarlac West District B", "Tarlac West District C", "Munoz", "Balanga City East",
  "Balanga City West", "Meycauayan East", "Meycauayan West", "Mabalacat North", "Mabalacat South", "Mabalacat East", "Dasmariñas I",
  "Dasmariñas II", "Agoncillo", "Alitagtag", "Balayan East", "Balete", "Bauan", "Calaca", "Calatagan", "Cuenca", "Ibaan", "Laurel",
  "Lemery", "Lian", "Lobo", "Malvar", "Mataas Na Kahoy", "Nasugbu East", "Padre Garcia", "Rosario East", "San Juan East", "San Pascual",
  "Taal", "Talisay", "Taysan", "Tingloy", "Tuy", "Balayan West", "San Juan West", "Nasugbu West", "Rosario West", "Nasugbu North",
  "Alfonso", "Amadeo", "Carmona", "General E. Aguinaldo", "General Mariano Alvarez", "Indang I", "Indang II", "Kawit", "Magallanes",
  "Maragondon", "Mendez", "Naic I", "Naic II", "Noveleta", "Silang I", "Silang II", "Tagaytay City", "Tanza", "Ternate",
  "Trece Martirez City", "Alaminos", "Bay", "Calauan", "Cavinti", "Famy-Mabitac", "Liliw", "Los Baños", "Luisiana", "Lumban-Kalayaan",
  "Magdalena", "Majayjay", "Nagcarlan-Rizal", "Paete", "Pagsanjan", "Pangil-Pakil", "Pila", "Santa Cruz", "Santa Maria", "Siniloan",
  "Victoria", "Alabat", "Atimonan", "Buenavista", "Burdeos", "Calauag East", "Calauag West", "Candelaria East", "Candelaria West",
  "Catanauan", "Dolores", "Gen. Luna", "Gen. Nakar", "Guinayangan", "Gumaca East", "Gumaca West", "Lopez East", "Lopez West",
  "Lucban", "Macalelon", "Mauban North", "Mauban South", "Mulanay", "Padre Burgos-Agdangan", "Pagbilao", "Patnanungan-Jomalig",
  "Perez", "Pitogo", "Polillo", "Real", "Sampaloc", "San Andres", "San Francisco", "Sariaya East", "Sariaya West", "Tagkawayan",
  "Tiaong", "Unisan", "Panukulan", "Angono", "Teresa", "Binangonan I", "Binangonan II", "Cainta I (Cainta)", "Cardona", "Pililla",
  "Rodriguez I (Rodriguez)", "San Mateo", "Tanay I", "Taytay I", "Taytay II", "Cainta II", "Rodriguez II", "Binangonan III", "Baras",
  "Jalajala", "Tanay II", "Batangas City East District", "Batangas City New District", "Batangas City North District",
  "Batangas City South District", "Batangas City West District", "Batangas City Coastal District", "Batangas City Verde Island District",
  "Cavite City I District", "Cavite City II District", "Cavite City III District", "Lipa City East District", "Lipa City North District",
  "Lipa City South District", "Lipa City West District", "Lucena East District", "Lucena North District", "Lucena South District",
  "Lucena West District", "Ambray", "Dapdapan", "Del Remedio", "Fule Almeda", "Lakeside", "Sto. Angel", "Calamba City East I",
  "Calamba City East II", "Calamba City West", "District I-A", "District II-A", "District II-B", "District II-C", "District I-B",
  "District I-C", "District II-D", "Tanauan City East I", "Tanauan City North I", "Tanauan City South I", "Tanauan City West I",
  "Tanauan City East II", "Tanauan City East III", "Tanauan City North II", "Tanauan City North III", "Tanauan City South II",
  "Tanauan City West II", "City of Sta. Rosa District I", "City of Sta. Rosa District II", "City of Sta. Rosa District III",
  "Tayabas East", "Tayabas West", "Bacoor I", "Bacoor II", "Imus I", "Imus II", "Binan", "District IV", "District V", "General Trias I",
  "General Trias II", "San Pedro", "Sto. Tomas North", "Sto. Tomas South", "Boac North", "Boac South", "Gasan", "Mogpog",
  "Santa Cruz East", "Santa Cruz North", "Santa Cruz South", "Torrijos"
]

# Function to filter DataFrame based on a given region
def filter_region(df, region_name):
    """Filters the DataFrame for rows where the Region column matches the given region_name."""
    if "Region" in df.columns:
        if region_name in regions:
            return pd.DataFrame(df[df["Region"] == region_name])
        else:
            print(f"Error: '{region_name}' is not in the defined regions list.")
            return pd.DataFrame()
    else:
        print("Error: 'Region' column not found in DataFrame.")
        return pd.DataFrame()

# Function to filter DataFrame based on a given division
def filter_division(df, division_name):
    """Filters the DataFrame for rows where the Division column matches the given division_name."""
    if "Division" in df.columns:
        if division_name in divisions:
            return pd.DataFrame(df[df["Division"] == division_name])
        else:
            print(f"Error: '{division_name}' is not in the defined divisions list.")
            return pd.DataFrame()
    else:
        print("Error: 'Division' column not found in DataFrame.")
        return pd.DataFrame()
    
# Function to filter DataFrame based on a given district
def filter_district(df, district_name):
    """Filters the DataFrame for rows where the District column matches the given district_name."""
    if "District" in df.columns:
        if district_name in districts:
            return pd.DataFrame(df[df["District"] == district_name])
        else:
            print(f"Error: '{district_name}' is not in the defined districts list.")
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
