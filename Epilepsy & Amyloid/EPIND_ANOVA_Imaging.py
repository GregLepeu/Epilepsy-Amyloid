import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import chi2_contingency
from statsmodels.stats.multitest import multipletests

path = "/Users/gregorylepeu/Documents/Research/Projects/EPI_ND/"
file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df = pd.read_csv(path+'/data/'+file_name, encoding='ISO-8859-1')

# Remove all cases of epielpsy not ND
df = df[df['Epi_not_ND']<1]
df = df[df['ND']==1]

# Keep only with specific phenotype
desired_syndromes = ['Amnestic']
df  = df[df['Syndrome'].isin(desired_syndromes)]

column_labels = df.columns
list_region = [col for col in column_labels if col.startswith('mri_zscore')]

# Create an empty DataFrame with the specified column names
results_df = pd.DataFrame(columns=['Region', 'Mean Epi', 'Mean not Epi','SD Epi', 'SD not Epi', 'F', 'p-value'])

for i, region in enumerate(list_region):
    df_anova = pd.DataFrame({'group':df['Epi_ND'],'value':df[region]})

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

results_df.to_csv(path+'/data/ANOVA_morphometry_ND_amnestic.csv')