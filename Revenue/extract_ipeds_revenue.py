# script to obtain 'total institutional revenue' data for ~200 US colleges
# SSP early-career fellowship program project title: "Revenue, Region, and Racial demographics: A study of university publishing programs and presses over time"
# note to self, if you're on your work laptop you might need to create a VE
  
import os
import pandas as pd
from zipfile import ZipFile

# years and finance forms to extract; note these are fiscal years, so 2012 is technically 2011-2012
years = range(2012, 2025)
finance_forms = ['F1A', 'F1B', 'F2', 'F3']
finance_dir = "IPEDS_Finance"

# load colleges (with UNITID)
colleges_df = pd.read_csv("colleges_matched_fresh_with_fuzzy.csv")
unitids = colleges_df['UNITID'].dropna().astype(int).tolist()

# collector for financial data
financial_data = pd.DataFrame()

for year in years:
    fy = str(year)[-2:] + str(year + 1)[-2:]  # e.g., '1213' for 2013
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

# save the extracted data
financial_data.to_csv("college_financial_data_out.csv", index=False)
print("Saved as college_financial_data_out.csv")
