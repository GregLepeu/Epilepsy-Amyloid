import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import dabest
from scipy.stats import chi2_contingency

path = "/Users/gregorylepeu/Documents/Research/Projects/EPI_ND/"
file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df = pd.read_csv(path+'/data/'+file_name, encoding='ISO-8859-1')
order = ['A-T-', 'A-T+', 'A+T-', 'A+T+']

# Calculate the proportion of 'Epi' column for each possilbe 'AT status'
proportions_epi = df[df['Epi Soarian'] == 1].groupby('AT status').size() / df.groupby('AT status').size()
# Reorder the series based on the defined order
proportions_epi = proportions_epi.reindex(order)

# Plot the proportions using seaborn
title = 'Prevalence of epilepsy'
fig = plt.figure(title, figsize=(8, 8)).suptitle(title)
gridspec.GridSpec(12, 12)
sns.barplot(x=proportions_epi.index, y=proportions_epi.values)
# Create a contingency table and perform the Chi-Square test
contingency_table = pd.crosstab(df['AT status'], df['Epi Soarian'])
chi2, p, dof, ex = chi2_contingency(contingency_table)
print(f'Chi2 epi: {chi2}, p-value: {p}')



# Calculate the proportion of 'Epi' column for each possible 'AT status'
proportions_epiND = df[df['Epi_ND'] == 1].groupby('AT status').size() / df.groupby('AT status').size()
# Reorder the series based on the defined order
proportions_epiND = proportions_epiND.reindex(order)

# Plot the proportions using seaborn
title = 'Prevalence of neurodegenerative epilepsy'
fig = plt.figure(title, figsize=(8, 8)).suptitle(title)
gridspec.GridSpec(12, 12)
sns.barplot(x=proportions_epiND.index, y=proportions_epiND.values)
# Create a contingency table and perform the Chi-Square test
contingency_table_nd = pd.crosstab(df['AT status'], df['Epi_ND'])
chi2, p, dof, ex = chi2_contingency(contingency_table_nd)
print(f'Chi2 epi ND: {chi2}, p-value: {p}')


plt.show()