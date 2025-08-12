import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import chi2_contingency

path = "/Users/gregorylepeu/Documents/Research/Projects/EPI_ND"
file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df = pd.read_csv(path+'/data/'+file_name, encoding='ISO-8859-1')

# Keep only EPI ND
df = df[df['Epi_ND']==1]

# Keep only AD/SNAP
#df = df[df['SNAP/AD'].isin(['AD', 'SNAP'])]
# Create the 'AP' categorical variable column
#df['AP'] = df.apply(lambda row: 1 if row['SNAP/AD'] == 'AD' else 0, axis=1)

# # Same for AD / Non-AD
df = df[df['AD/Non-AD'].isin(['AD', 'Non-AD'])]
df['AP'] = df.apply(lambda row: 1 if row['AD/Non-AD'] == 'AD' else 0, axis=1)

column_labels = df.columns
list_CSF = ['mri_age','education_level', 'moca_score_01', 'cdr_score_01', 'mri_tiv']

# Create an empty DataFrame with the specified column names
results_df = pd.DataFrame(columns=['Region', 'Mean AD', 'Mean Non-AD','SD AD', 'SD Non-AD', 'F', 'p-value'])

for i, region in enumerate(list_CSF):
    df_anova = pd.DataFrame({'group':df['AP'],'value':df[region]})

    # Perform ANOVA using statsmodels
    model = ols('value ~ C(group)', data=df_anova).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    # Calculate the mean and standard deviation for each group in 'Epi_ND'
    group_stats = df_anova.groupby('group')['value'].agg(['mean', 'std'])
    a = group_stats.loc[1,'mean']
    results_df.loc[i] = [region, group_stats.loc[1,'mean'], group_stats.loc[0,'mean'],
                         group_stats.loc[1,'std'], group_stats.loc[0,'std'], anova_table.loc['C(group)','F'],anova_table.loc['C(group)','PR(>F)']]

print(results_df)

results_df.to_csv(path+'/data/ANOVA_Epi_demo_NonAD.csv')
