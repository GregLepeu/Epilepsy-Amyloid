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
order = ['A-T-N-','A-T-N+', 'A-T+N-','A-T+N+', 'A+T-N-','A+T-N+', 'A+T+N-', 'A+T+N+']

# Remove all cases of epilpesy not ND
df = df[df['Epi_not_ND']<1]
df = df[df['ND']==1]

# Keep only the one with ab42/ab40 ratio
#df = df[df['ratio_abeta42_40']>0]

# Keep only with typical AD phenotype
# desired_syndromes = ['Language', 'Amnestic', 'Visual-Spatial']
# df  = df[df['Syndrome'].isin(desired_syndromes)]


# Barplot for all patients
title = 'ATN status across the cohort'
fig = plt.figure(title, figsize=(8, 8)).suptitle(title)
gridspec.GridSpec(12, 12)
ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
sns.countplot(ax=ax1,data=df, x='ATN status', order=order)


# Barplot for ND-epi patients
df_ND_epi = df[df['Epi_ND']==1]
title = 'ATN status for neurodegenrative epilepsy patients'
fig = plt.figure(title, figsize=(8, 8)).suptitle(title)
gridspec.GridSpec(12, 12)
ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
sns.countplot(ax=ax1,data=df_ND_epi, x='ATN status', order=order)


# Calculate the proportion of 'Epi' column for each possible 'AT status'
proportions_epiND = df[df['Epi_ND'] == 1].groupby('ATN status').size() / df.groupby('ATN status').size()
# Reorder the series based on the defined order
proportions_epiND = proportions_epiND.reindex(order)

# Plot the proportions using seaborn
title = 'Prevalence of neurodegenerative epilepsy across ATN status'
fig = plt.figure(title, figsize=(8, 8)).suptitle(title)
gridspec.GridSpec(12, 12)
sns.barplot(x=proportions_epiND.index, y=proportions_epiND.values)
# Create a contingency table and perform the Chi-Square test
contingency_table_nd = pd.crosstab(df['ATN status'], df['Epi_ND'])
chi2, p, dof, ex = chi2_contingency(contingency_table_nd)
print(f'Chi2 epi_ND: {chi2}, p-value: {p}')

# Calculate the proportion of 'Epi' column for each possible 'SNAP/AD'
proportions_SNAP = df[df['Epi_ND'] == 1].groupby('SNAP/AD').size() / df.groupby('SNAP/AD').size()
proportions_NonAD = df[df['Epi_ND'] == 1].groupby('AD/Non-AD').size() / df.groupby('AD/Non-AD').size()

# Plot the proportions using seaborn
title = 'Prevalence of neurodegenerative epilepsy across SNAP/AD'
fig = plt.figure(title, figsize=(8, 8)).suptitle(title)
gridspec.GridSpec(12, 12)
sns.barplot(x=proportions_SNAP.index, y=proportions_SNAP.values*100)
# Create a contingency table and perform the Chi-Square test
contingency_table_SNAP = pd.crosstab(df['SNAP/AD'], df['Epi_ND'])
chi2, p, dof, ex = chi2_contingency(contingency_table_SNAP)
print(f'Chi2 epi_ND: {chi2}, p-value: {p}')

# Plot the proportions using seaborn
title = 'Prevalence of neurodegenerative epilepsy across AD/Non-AD'
fig = plt.figure(title, figsize=(8, 8)).suptitle(title)
gridspec.GridSpec(12, 12)
sns.barplot(x=proportions_NonAD.index, y=proportions_NonAD.values*100)
# Create a contingency table and perform the Chi-Square test
proportions_NonAD = pd.crosstab(df['AD/Non-AD'], df['Epi_ND'])
chi2, p, dof, ex = chi2_contingency(proportions_NonAD)
print(f'Chi2 epi_ND: {chi2}, p-value: {p}')



plt.show()