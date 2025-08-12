import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import chi2_contingency

path = "/Users/gregorylepeu/Documents/Research/Projects/CLM/"
file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df = pd.read_csv(path+'/data/'+file_name, encoding='ISO-8859-1')

# Number of MoCA assessments
n_assessments = 8

# Initialize a new DataFrame to store the MoCA score differences per year
mean_diff_per_year = []
first_last_diff_per_year = []

# Loop over each subject
for idx, row in df.iterrows():
    # Get MoCA scores and ages for the subject
    scores = row[[f'moca_score_{i:02d}' for i in range(1, n_assessments + 1)]].values.astype('float64')
    ages = row[[f'moca_age_{i:02d}' for i in range(1, n_assessments + 1)]].values.astype('float64')

    # Remove NaN values for valid score and age pairs
    valid_idx = ~np.isnan(scores) & ~np.isnan(ages)
    valid_scores = scores[valid_idx]
    valid_ages = ages[valid_idx]

    # Calculate consecutive differences if there are at least two valid assessments
    if len(valid_scores) >= 2:
        # Consecutive score and age differences
        score_diffs = np.diff(valid_scores)
        age_diffs = np.diff(valid_ages)

        # Mean difference per year
        diff_per_year = score_diffs / age_diffs
        mean_diff_per_year.append(np.mean(diff_per_year))

        # First and last score difference per year
        first_last_diff = (valid_scores[-1] - valid_scores[0]) / (valid_ages[-1] - valid_ages[0])
        first_last_diff_per_year.append(first_last_diff)
    else:
        # If fewer than two assessments, set values to NaN
        mean_diff_per_year.append(np.nan)
        first_last_diff_per_year.append(np.nan)

# Create the result DataFrame
moca_diff_per_year = pd.DataFrame({
    'Moca_mean_diff_per_year': mean_diff_per_year,
    'Moca_first_last_diff_per_year': first_last_diff_per_year
})

df['Moca_mean_diff_per_year'] = mean_diff_per_year
df ['Moca_first_last_diff_per_year'] = first_last_diff_per_year

df.to_csv(path+'/data/'+file_name)


