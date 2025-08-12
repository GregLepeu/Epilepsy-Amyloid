import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import chi2_contingency
from statsmodels.stats.multitest import multipletests

# In the Epi-ND patients, compared the SNAP and AD group

path = "/Users/gregorylepeu/Documents/Research/Projects/EPI_ND"
file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df = pd.read_csv(path+'/data/'+file_name, encoding='ISO-8859-1')

# Keep only EPI ND
df = df[df['Epi_ND']==1]

# # Keep only AD/SNAP
# df = df[df['SNAP/AD'].isin(['AD', 'SNAP'])]
# # Create the 'AT status' column based on the A and T status
# df['AP'] = df.apply(lambda row: 1 if row['SNAP/AD'] == 'AD' else 0, axis=1)

# Same for AD / Non-AD
df = df[df['AD/Non-AD'].isin(['AD', 'Non-AD'])]
df['AP'] = df.apply(lambda row: 1 if row['AD/Non-AD'] == 'AD' else 0, axis=1)


# Keep only columns that contain 'left' or 'right' in their name
df_filtered = df.loc[:, df.columns.str.contains('AP|left|right', case=False, regex=True)]
# Ensure filtering is applied only to column names
right_epi_cols = df_filtered.columns[df_filtered.columns.str.contains('right|AP', case=False, regex=True)]
left_cols = df_filtered.columns[df_filtered.columns.str.contains('left|AP', case=False, regex=True)]
# Create separate DataFrames
df_right = df_filtered[right_epi_cols].copy()
df_left = df_filtered[left_cols].copy()
# Remove 'right' and 'left' from column names
df_right = df_right.rename(columns=lambda x: x.replace('Right', '').strip())
df_left = df_left.rename(columns=lambda x: x.replace('Left', '').strip())
# Concatenate both together to "double" the amount of structure
df = pd.concat([df_right, df_left], axis=0, ignore_index=True)

# Remove rows with any NaN values
df = df.dropna().reset_index(drop=True)

column_labels = df.columns
list_region = [col for col in column_labels if col.startswith('mri_zscore')]

# Create an empty DataFrame with the specified column names
results_df = pd.DataFrame(columns=['Region', 'Mean AD', 'Mean Non-AD','SD AD', 'SD Non-AD', 'F', 'p-value'])

for i, region in enumerate(list_region):
    df_anova = pd.DataFrame({'group':df['AP'],'value':df[region]})

    # Perform ANOVA using statsmodels
    model = ols('value ~ C(group)', data=df_anova).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    # Calculate the mean and standard deviation for each group in 'Epi_ND'
    group_stats = df_anova.groupby('group')['value'].agg(['mean', 'std'])
    a = group_stats.loc[1,'mean']
    results_df.loc[i] = [region, group_stats.loc[1,'mean'], group_stats.loc[0,'mean'],
                         group_stats.loc[1,'std'], group_stats.loc[0,'std'], anova_table.loc['C(group)','F'],anova_table.loc['C(group)','PR(>F)']]


# Apply Benjamini-Hochberg correction to p-values
rejected, p_corrected, _, _ = multipletests(results_df['p-value'], alpha=0.05, method='fdr_bh')
results_df['FDR-corrected p-value'] = p_corrected

print(results_df)

results_df.to_csv(path+'/data/ANOVA_EPI_morpho_AD_NonAD_Combined_LR.csv')