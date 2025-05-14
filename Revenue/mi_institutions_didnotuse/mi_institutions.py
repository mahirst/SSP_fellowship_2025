import os
import pandas as pd
from zipfile import ZipFile

# specify years range and forms to check
years = range(2012, 2024)
finance_forms = ['F1A', 'F1B', 'F2', 'F3']
finance_dir = "IPEDS_Finance"

# define the institutions and unitids based on ipeds
target_colleges = pd.DataFrame({
    'Institution_Name': [
        "Wayne State University",
        "Andrews University",
        "Pensole Lewis College of Business and Design",
        "Saginaw Chippewa Tribal College"
    ],
    'UNITID': [172644, 169706, 495973, 437933] #there are only 4 so I just looked these up. Also turns out Pensole Lewis is new (2022) so won't get much from that
})

unitids = target_colleges['UNITID'].tolist()
financial_data = pd.DataFrame()

for year in years:
    fy = str(year)[-2:] + str(year + 1)[-2:]
    for form in finance_forms:
        zip_path = os.path.join(finance_dir, f"F{fy}_{form}.zip")
        if not os.path.exists(zip_path):
            print(f"Missing: {zip_path}")
            continue

        try:
            with ZipFile(zip_path) as z:
                for csv_file in [f for f in z.namelist() if f.lower().endswith('.csv')]:
                    with z.open(csv_file) as f:
                        df = pd.read_csv(f, encoding='latin1', low_memory=False)
                        if 'UNITID' in df.columns:
                            df = df[df['UNITID'].isin(unitids)]
                            df['Year'] = year
                            df['Form'] = form
                            financial_data = pd.concat([financial_data, df], ignore_index=True)
        except Exception as e:
            print(f"Failed to read {zip_path}: {e}")

# merge with institition names
df = financial_data.merge(target_colleges, on='UNITID', how='left')

# get total revenue for these four instituions
revenue_cols = ['F1A01', 'F1B01', 'F2A01', 'F3A01']
df['TotalRevenue'] = df[revenue_cols].sum(axis=1, skipna=True)
df = df.dropna(subset=['TotalRevenue'])

# summarize per institution per year
summary = df.groupby(['Institution_Name', 'Year'])['TotalRevenue'].sum().reset_index()

# pivot one row per college, one column per year
pivot = summary.pivot(index='Institution_Name', columns='Year', values='TotalRevenue').reset_index()

# check all 4 colleges are included
final = target_colleges[['Institution_Name']].drop_duplicates().merge(pivot, on='Institution_Name', how='left')

# export in csv format
output_path = "mi_summary.csv"
final.to_csv(output_path, index=False)
print(f" saved to {output_path}")
