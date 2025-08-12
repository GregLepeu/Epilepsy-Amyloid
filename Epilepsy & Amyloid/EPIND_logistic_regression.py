# Import necessary libraries
import pandas as pd
import statsmodels.api as sm

# Load your data (assuming your dataframe is named df)
path = "/Users/gregorylepeu/Documents/Research/Projects/CLM/"
file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'
df = pd.read_csv(path+'/data/'+file_name, encoding='ISO-8859-1')

dependent_variable = 'Irritative activity'# 'Irritative activity' 'Slowing'

# Remove all cases of epilpesy not ND
df = df[df['Epi_not_ND']<1]
df = df[df['ND']==1]
df = df[df['EEG dans NLG']==1]


df['Y'] = df.apply(lambda row: 1 if row[dependent_variable] == 'Focal' else 0, axis=1)



# Define the dependent variable (y) and independent variables (X)
y = df['Y']  # Dependent variable, categorical (1 or 0)
X = df[['csf_abeta42', 'csf_tTau', 'csf_phTau']]  # Independent variables

# Add a constant to the independent variables matrix for the intercept
X = sm.add_constant(X)

# Fit the logistic regression model
logit_model = sm.Logit(y, X)
result = logit_model.fit()

# Print the model summary
print(result.summary())