import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.stats import chi2_contingency

ATN_colors = {
    'A-T-N-': '#e9d8a6',
    'A-T-N+': '#d9a453',
    'A-T+N-': '#c68639',
    'A-T+N+': '#ca6702',
    'A+T-N-': '#9d4edd',
    'A+T-N+': '#3b248f' ,
    'A+T+N-': '#2c397e',
    'A+T+N+':'#073b4c'
             }

order = ['A-T-N-','A-T-N+', 'A-T+N-','A-T+N+','A+T+N+','A+T+N-','A+T-N+','A+T-N-']

path = "/Users/gregorylepeu/Documents/Research/Projects/EPI_ND/"
file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df = pd.read_csv(path+'/data/'+file_name, encoding='ISO-8859-1')

# Remove all cases of epilpesy not ND
df = df[df['Epi_not_ND']<1]
df = df[df['ND']==1]

# Keep only the one with ab42/ab40 ratio
#df = df[df['ratio_abeta42_40']>0]


# Replace all 'syndrome' values ending with 'PPA' with 'Language'
df['Syndrome'] = df['Syndrome'].replace(to_replace=r'.*PPA$', value='Language', regex=True)
# Keep only with typical AD phenotype
desired_syndromes = ['Executive']
df  = df[df['Syndrome'].isin(desired_syndromes)]

# Step 1: Group the data by 'group' and 'ATN status' and count occurrences
group_ATN_counts = df.groupby(['Epi_ND', 'ATN status']).size().reset_index(name='counts')


# Step 3: Create a contingency table
contingency_table = group_ATN_counts.pivot(index='ATN status', columns='Epi_ND', values='counts').fillna(0)

# Step 4: Perform Chi-squared test
chi2, p, dof, expected = chi2_contingency(contingency_table)
print("Chi-squared Test Results:")
print(f"Chi-squared Statistic: {chi2:.4f}")
print(f"P-value: {p:.4f}")
print(f"Degrees of Freedom: {dof}")
print("Expected Frequencies:")
print(expected)

# Step 5: Plot a pie chart for each group
title = 'ATN status by group'
unique_groups = df['Epi_ND'].unique()
fig, axes = plt.subplots(1, len(unique_groups), figsize=(12, 6))

for i, group in enumerate(unique_groups):
    # Filter data for the specific group
    filtered_data = group_ATN_counts[group_ATN_counts['Epi_ND'] == group]
    n =  len(df[df['Epi_ND'] == group])

    # Sort the data based on the predefined order
    filtered_data['ATN status'] = pd.Categorical(filtered_data['ATN status'], categories=order, ordered=True)
    filtered_data = filtered_data.sort_values('ATN status')

    # Pie chart labels and sizes
    labels = filtered_data['ATN status']
    sizes = filtered_data['counts']
    colors = [ATN_colors[label] for label in labels]

    # Plot the pie chart in the respective subplot
    axes[i].pie(sizes, labels=labels,colors=colors, autopct='%1.1f%%', startangle=140)
    axes[i].axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    fig.text(0.1 + i * 0.5, 0.01, f'n = {n}', ha='center', fontsize=12)

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
