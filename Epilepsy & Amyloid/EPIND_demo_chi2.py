import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import chi2_contingency

path = "/Users/gregorylepeu/Documents/Research/Projects/EPI_ND/"
file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df = pd.read_csv(path+'/data/'+file_name, encoding='ISO-8859-1')

# Remove all cases of epilpesy not ND
df = df[df['Epi_not_ND']<1]
df = df[df['ND']==1]

# # Keep only with typical AD phenotype
# desired_syndromes = ['Amnestic']
# df  = df[df['Syndrome'].isin(desired_syndromes)]

list_variable = ['sex']

# Create an empty DataFrame with the specified column names
results_df = pd.DataFrame(columns=['Variable', '% Epi', '% not Epi', 'Chi2 Statistic', 'p-value','Degrees of Freedom','Expected Frequencies'])

for i, variable in enumerate(list_variable):
    # Create a contingency table (cross-tabulation of 'group' and 'value_category')
    contingency_table = pd.crosstab(df['Epi_ND'], df[variable])

    # Perform the Chi-Squared test
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    # Calculate the percentage of 'low' category per group
    percentage_per_group = (contingency_table[1] / contingency_table.sum(axis=1)) * 100

    results_df.loc[i] = [variable, percentage_per_group[1],  percentage_per_group[0],
                         f"{chi2}", p, dof,expected]

print(results_df)

#results_df.to_csv(path+'/data/demo_Chi2_ND.csv')