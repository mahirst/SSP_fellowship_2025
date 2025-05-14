import pandas as pd

# load institution list (must include 'UNITID' and 'college_name')
colleges = pd.read_csv("colleges_matched_incluMissing.csv")

# load IPEDS 2022 or 2012 enrollment file (just uncomment)
#df = pd.read_csv("ef2022a_rv.csv", encoding='latin1', low_memory=False)
df = pd.read_csv("ef2012a_rv.csv", encoding='latin1', low_memory=False)

# filter institutions
df = df[df['UNITID'].isin(colleges['UNITID'])]

# aggregate demog-based totals per UNITID
race_columns = {
    'EFNRALT': "Nonresident Alien",
    'EFHISPT': "Hispanic/Latino",
    'EFAIANT': "American Indian or Alaska Native",
    'EFASIAT': "Asian",
    'EFBKAAT': "Black or African American",
    'EFNHPIT': "Native Hawaiian or Other Pacific Islander",
    'EFWHITT': "White",
    'EF2MORT': "Two or More Races",
    'EFUNKNT': "Race/Ethnicity Unknown"
}

# select & sum only these columns
demo_data = df[['UNITID'] + list(race_columns.keys())].groupby('UNITID').sum().reset_index()

# calc total enrollment and top 3 groups
def summarize_row(row):
    race_counts = row[race_columns.keys()]
    total = race_counts.sum()
    top3 = race_counts.sort_values(ascending=False).head(3).index
    top3_labels = [race_columns.get(col) for col in top3]
    return pd.Series([total] + top3_labels)

summary = demo_data.apply(summarize_row, axis=1)
summary.columns = ['Total Students', 'Top Group 1', 'Top Group 2', 'Top Group 3']
summary['UNITID'] = demo_data['UNITID']

# merges with institution names
final = colleges.merge(summary, on='UNITID')[['college_name', 'Total Students', 'Top Group 1', 'Top Group 2', 'Top Group 3']]

# save (make sure this matches the date you are looking at lol)
#final.to_csv("institution_top_demographics_2022.csv", index=False)
#print("Saved as institution_top_demographics_2022.csv")

final.to_csv("institution_top_demographics_2012.csv", index=False)
print("Saved as institution_top_demographics_2012.csv")
