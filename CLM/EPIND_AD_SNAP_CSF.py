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
df = df[df['AD/Non-AD'].isin(['AD', 'Non-AD'])]

# Create the 'AT status' column based on the A and T status
df['AP'] = df.apply(lambda row: 1 if row['AD/Non-AD'] == 'AD' else 0, axis=1)

column_labels = df.columns
list_CSF = ['csf_abeta42','csf_abeta40','ratio_abeta42_40','csf_phTau','csf_tTau']

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

results_df.to_csv(path+'/data/ANOVA_EPI_AD_Non_AD_CSF.csv')
