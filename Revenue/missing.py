import os
import pandas as pd
from zipfile import ZipFile

# setup fun!
years = range(2012, 2024)  # 2023 data = 2022–2023
finance_forms = ['F1A', 'F1B', 'F2', 'F3']
finance_dir = "IPEDS_Finance"

# load missing colleges file
colleges_df = pd.read_csv("missing_colleges_with_verified_metadata.csv")
unitids = colleges_df['UNITID'].dropna().astype(int).tolist()

# collector for financial data
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

# merge with college names
df = financial_data.merge(colleges_df[['UNITID', 'Institution_Name']], on='UNITID', how='left')

# identify total revenue columns and combine into one
revenue_cols = ['F1A01', 'F1B01', 'F2A01', 'F3A01']
df['TotalRevenue'] = df[revenue_cols].sum(axis=1, skipna=True)
df = df.dropna(subset=['TotalRevenue'])

# sum revenue per institution and year
summary = df.groupby(['Institution_Name', 'Year'])['TotalRevenue'].sum().reset_index()

# pivot to wide format
pivot = summary.pivot(index='Institution_Name', columns='Year', values='TotalRevenue').reset_index()

# double check all colleges are included
full_list = colleges_df[['Institution_Name']].drop_duplicates()
final = full_list.merge(pivot, on='Institution_Name', how='left')

# save to file
final.to_csv("missing_colleges_revenue_summary.csv", index=False)
print("Saved as missing_colleges_revenue_summary.csv")
