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


path = "/Users/gregorylepeu/Documents/Research/Projects/CLM/"
file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df = pd.read_csv(path+'/data/'+file_name, encoding='ISO-8859-1')

# Remove all cases of epilpesy not ND
df = df[df['Epi_not_ND']<1]
df = df[df['ND']==1]

# Remove all cases of not inteprtable BNP
df = df[df['Syndrome']!= 'Not interpretable']

# Replace all 'syndrome' values ending with 'PPA' with 'Language'
df['Syndrome'] = df['Syndrome'].replace(to_replace=r'.*PPA$', value='Language', regex=True)

# Step 1: Group the data by 'group' and 'syndrome' and count occurrences
group_syndrome_counts = df.groupby(['Epi_ND', 'Syndrome']).size().reset_index(name='counts')


# Step 3: Create a contingency table
contingency_table = group_syndrome_counts.pivot(index='Syndrome', columns='Epi_ND', values='counts').fillna(0)

# Step 4: Perform Chi-squared test
chi2, p, dof, expected = chi2_contingency(contingency_table)
print("Chi-squared Test Results:")
print(f"Chi-squared Statistic: {chi2:.4f}")
print(f"P-value: {p:.4f}")
print(f"Degrees of Freedom: {dof}")
print("Expected Frequencies:")
print(expected)

# Step 5: Plot a pie chart for each group
title = 'Syndrome by group'
unique_groups = df['Epi_ND'].unique()
ig, axes = plt.subplots(1, len(unique_groups), figsize=(12, 6))

for i, group in enumerate(unique_groups):
    # Filter data for the specific group
    filtered_data = group_syndrome_counts[group_syndrome_counts['Epi_ND'] == group]

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
        axes[i].set_title('Without Epilepsy')
    else:
        axes[i].set_title('With Epilepsy')


#  Add Chi-squared test results to the figure
result_text = (f"Chi-squared Statistic: {chi2:.4f}\n"
               f"P-value: {p:.4f}\n")
# Adjust the position for placing text (you can change the coordinates as needed)
plt.figtext(0.5, 0.01, result_text, wrap=False, horizontalalignment='center', fontsize=12)


plt.tight_layout()
plt.show()

