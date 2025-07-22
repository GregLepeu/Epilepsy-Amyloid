import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import dabest
from scipy.stats import chi2_contingency

path = "/Users/gregorylepeu/Documents/Research/Projects/CLM/"
file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df = pd.read_csv(path+'/data/'+file_name, encoding='ISO-8859-1')

# Remove all cases of epilpesy not ND
df = df[df['Epi_not_ND']<1]

df['Epi_ND'] = df['Epi_ND'].astype(str)

title = 'CSF ab42'
fig = plt.figure(title, figsize=(8, 8)).suptitle(title)
gridspec.GridSpec(12, 12)
ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
two_groups_unpaired = dabest.load(df, x='Epi_ND', y='csf_abeta42', idx=('0','1'))
two_groups_unpaired.mean_diff.plot(ax=ax1,raw_marker_size=3)

title = 'CSF ab42_40 ratio'
fig = plt.figure(title, figsize=(8, 8)).suptitle(title)
gridspec.GridSpec(12, 12)
ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
two_groups_unpaired = dabest.load(df, x='Epi_ND', y='ratio_abeta42_40', idx=('0','1'))
two_groups_unpaired.mean_diff.plot(ax=ax1,raw_marker_size=3)

title = 'CSF phopho Tau'
fig = plt.figure(title, figsize=(8, 8)).suptitle(title)
gridspec.GridSpec(12, 12)
ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
two_groups_unpaired = dabest.load(df, x='Epi_ND', y='csf_phTau', idx=('0','1'))
two_groups_unpaired.mean_diff.plot(ax=ax1,raw_marker_size=3)

title = 'CSF tTau'
fig = plt.figure(title, figsize=(8, 8)).suptitle(title)
gridspec.GridSpec(12, 12)
ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
two_groups_unpaired = dabest.load(df, x='Epi_ND', y='csf_tTau', idx=('0','1'))
two_groups_unpaired.mean_diff.plot(ax=ax1,raw_marker_size=3)

plt.show()