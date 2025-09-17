import pandas as pd
from scipy.stats import chi2_contingency

path = "/Users/gregorylepeu/Documents/Research/Projects/EPI-ND/"
file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df = pd.read_csv(path+'/data/'+file_name, encoding='ISO-8859-1')

# Remove all cases of epilpesy not ND
df = df[df['Epi_not_ND']<1]
df = df[df['ND']==1]

# Remove all the ones without ratio
#df = df[df['ratio_abeta42_40']>0]

# Keep only the ones with eeg
#df = df[df['EEG dans NLG']>0]

# Create a categorical variable column
df['Focal Slowing'] = df.apply(lambda row: 1 if row['Slowing'] == 'Focal' else 0, axis=1)

# Create a contingency table (cross-tabulation of 'group' and 'value_category')
contingency_table = pd.crosstab(df['Epi_ND'], df['sex'])

# Perform the Chi-Squared test
chi2, p, dof, expected = chi2_contingency(contingency_table)

# Print results
print(f"Chi2 Statistic: {chi2}")
print("P-value: {:.10f}".format(p))
print(f"Degrees of Freedom: {dof}")
print("Expected Frequencies:")
print(expected)

# Calculate the percentage of 'low' category per group
percentage_per_group = (contingency_table[1] / contingency_table.sum(axis=1)) * 100
print(percentage_per_group)