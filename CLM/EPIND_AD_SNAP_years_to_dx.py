import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

path = "/Users/gregorylepeu/Documents/Research/Projects/EPI_ND"
file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df = pd.read_csv(path+'/data/'+file_name, encoding='ISO-8859-1')

# Keep only EPI ND
df = df[df['Epi_ND']==1]

# # Keep only with typical AD phenotype
# desired_syndromes = ['Amnestic']
# df  = df[df['Syndrome'].isin(desired_syndromes)]

## Keep only AD/SNAP
#df = df[df['SNAP/AD'].isin(['AD', 'SNAP'])]
## Create the 'AP' categorical variable column
#df['AP'] = df.apply(lambda row: 1 if row['SNAP/AD'] == 'AD' else 0, axis=1)

# Same for AD / Non-AD
df = df[df['AD/Non-AD'].isin(['AD', 'Non-AD'])]
df['AP'] = df.apply(lambda row: 1 if row['AD/Non-AD'] == 'AD' else 0, axis=1)

# Round 'DIFFERENCE_YEARS' for better binning
df['Year to Dx of ND'] = df['Year to Dx of ND'].round()
df['group'] = df['Year to Dx of ND']


# Perform the 1-way ANOVA
model = ols('group ~ C(AP)', data=df).fit()  # Fit the model
anova_table = sm.stats.anova_lm(model)  # Perform ANOVA
f_stat = anova_table['F'][0]
p_value = anova_table['PR(>F)'][0]

# Calculate the median for both groups
#medians = df.groupby('SNAP/AD')['Year to Dx of ND'].median()
medians = df.groupby('AD/Non-AD')['Year to Dx of ND'].median()
means = df.groupby('AD/Non-AD')['Year to Dx of ND'].mean()

# Plot histogram with bin width of ... year
title = 'Year Relative to Diagnosis of Neurodegenerative Disease'
fig = plt.figure(title, figsize=(8, 4)).suptitle(title)
gridspec.GridSpec(12, 12)
sns.histplot(data=df, x='Year to Dx of ND', hue='AD/Non-AD', binwidth=2.5, kde=True, multiple="dodge",palette='coolwarm')
plt.xlabel('Years from Epilepsy Diagnosis to Memory Clinic')
plt.ylabel('Count')

# Annotate the plot with the ANOVA results
anova_text = f"ANOVA F-statistic: {f_stat:.2f}\np-value: {p_value:.3f}"
plt.text(x=-5, y=2.5, s=anova_text, fontsize=8, ha='center', va='center')

plt.show()

print(medians)
