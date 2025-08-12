import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.stats import chi2_contingency

syndrome_colors = {
    'Normal': '#e9d8a6',
    'Diffuse': '#9b2226',
    'Executive': '#bb3e03',
    'Attention': '#ca6702',
    'Visuo-spatial': '#ee9b00',
    'Language': '#94d2bd',
    'Amnestic':'#005f73'
    }

syndrome_order = ['Amnestic','Language','Normal', 'Visuo-spatial','Attention','Executive',  'Diffuse']


path = "/Users/gregorylepeu/Documents/Research/Projects/EPI_ND/"
file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df = pd.read_csv(path+'/data/'+file_name, encoding='ISO-8859-1')

# Keep only EPI ND
df = df[df['Epi_ND']==1]

# # Keep only AD/SNAP
# df = df[df['SNAP/AD'].isin(['AD', 'SNAP'])]
# # Create the 'AD' categorical variable column
# df['AD'] = df.apply(lambda row: 1 if row['SNAP/AD'] == 'AD' else 0, axis=1)

# # Same for AD / Non-AD
df = df[df['AD/Non-AD'].isin(['AD', 'Non-AD'])]
df['AD'] = df.apply(lambda row: 1 if row['AD/Non-AD'] == 'AD' else 0, axis=1)

# Remove all cases of not inteprtable BNP
df = df[df['Syndrome']!= 'Not interpretable']

# Replace all 'syndrome' values ending with 'PPA' with 'Language'
df['Syndrome'] = df['Syndrome'].replace(to_replace=r'.*PPA$', value='Language', regex=True)

# Create the 'AD' categorical variable column
df['Amnestic'] = df.apply(lambda row: 1 if row['Syndrome'] == 'Amnestic' else 0, axis=1)

# Step 1: Group the data by 'group' and 'syndrome' and count occurrences
group_syndrome_counts = df.groupby(['AD', 'Syndrome']).size().reset_index(name='counts')


# Step 3: Create a contingency table
contingency_table = group_syndrome_counts.pivot(index='Syndrome', columns='AD', values='counts').fillna(0)

# Step 4: Perform Chi-squared test
chi2, p, dof, expected = chi2_contingency(contingency_table)
print("Chi-squared Test Results:")
print(f"Chi-squared Statistic: {chi2:.4f}")
print(f"P-value: {p:.4f}")
print(f"Degrees of Freedom: {dof}")
print("Expected Frequencies:")
print(expected)

# Step 5: Plot a pie chart for each group
title = 'Syndrome by SNAP / AD'
unique_groups = df['AD'].unique()
ig, axes = plt.subplots(1, len(unique_groups), figsize=(12, 6))

for i, group in enumerate(unique_groups):
    # Filter data for the specific group
    filtered_data = group_syndrome_counts[group_syndrome_counts['AD'] == group]

    # Sort the data based on the predefined order
    filtered_data['Syndrome'] = pd.Categorical(filtered_data['Syndrome'], categories=syndrome_order, ordered=True)
    filtered_data = filtered_data.sort_values('Syndrome')

    # Pie chart labels and sizes
    labels = filtered_data['Syndrome']
    sizes = filtered_data['counts']
    colors = [syndrome_colors[label] for label in labels]

    # Plot the pie chart in the respective subplot
    axes[i].pie(sizes, labels=labels,colors=colors, autopct='%1.1f%%', startangle=140)
    axes[i].axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

    if group == 0:
        axes[i].set_title('Non-AD')
    else:
        axes[i].set_title('AD')


#  Add Chi-squared test results to the figure
result_text = (f"Chi-squared Statistic: {chi2:.4f}\n"
               f"P-value: {p:.4f}\n")
# Adjust the position for placing text (you can change the coordinates as needed)
plt.figtext(0.5, 0.01, result_text, wrap=False, horizontalalignment='center', fontsize=12)

# Chi2 test amnestic syndrome
list_variable = ['Amnestic']
# Create an empty DataFrame with the specified column names
results_df = pd.DataFrame(columns=['Variable', '% Non-AD', '% AD', 'Chi2 Statistic', 'p-value','Degrees of Freedom','Expected Frequencies'])

for i, variable in enumerate(list_variable):
    # Create a contingency table (cross-tabulation of 'group' and 'value_category')
    contingency_table = pd.crosstab(df['AD/Non-AD'], df[variable])

    # Perform the Chi-Squared test
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    # Calculate the percentage of 'low' category per group
    percentage_per_group = (contingency_table[1] / contingency_table.sum(axis=1)) * 100

    results_df.loc[i] = [variable, percentage_per_group[1],  percentage_per_group[0],
                         f"{chi2}", p, dof,expected]

print(results_df)


plt.tight_layout()
plt.show()
