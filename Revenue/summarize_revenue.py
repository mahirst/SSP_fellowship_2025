import pandas as pd

# load files
revenue_data = pd.read_csv("college_financial_data_out.csv")
college_info = pd.read_csv("colleges_matched_fresh_with_fuzzy.csv")

# merge to get names
df = revenue_data.merge(college_info[['UNITID', 'college_name']], on='UNITID', how='left')

# total revenue from any finance form downloaded from IPEDS
revenue_columns = ['F1A01', 'F1B01', 'F2A01', 'F3A01']
df['TotalRevenue'] = df[revenue_columns].sum(axis=1, skipna=True)

# drop empty values
df = df.dropna(subset=['TotalRevenue'])

# summary
summary = df.groupby(['college_name', 'Year'])['TotalRevenue'].sum().reset_index()

# pivot to wide format
pivot = summary.pivot(index='college_name', columns='Year', values='TotalRevenue').reset_index()

# check all 199 colleges are present
all_colleges = college_info[['college_name']].drop_duplicates()
final = all_colleges.merge(pivot, on='college_name', how='left')

# save
final.to_csv("college_total_revenue_summary.csv", index=False)
print("Saved as college_total_revenue_summary.csv")
