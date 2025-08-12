import os
import random
import string
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta

path = "/Users/gregorylepeu/Documents/Research/Projects/EPI_ND/"
file_name = 'CLMPACSMOLIS_486subjects_EPi.csv'

# Load CSV files into a pandas DataFrame
df_epi = pd.read_csv(path+'/data/'+file_name, encoding='ISO-8859-1')

# Remove all cases of epilepsy not ND
df_epi = df_epi[df_epi['Epi_not_ND']<1]
df_epi = df_epi[df_epi['ND']==1]
# df_epi = df_epi[df_epi['Epi_ND']==0]
#df_epi = df_epi[df_epi['SNAP/AD']=='SNAP']
#df_epi = df_epi[df_epi['AD/Non-AD']=='Non-AD']


# # Keep only the one with ab42/ab40 ratio
# df_epi = df_epi[df_epi['ratio_abeta42_40']>0]
#
# # Keep only with specific phenotype
#desired_syndromes = ['Amnestic']
#df_epi  = df_epi[df_epi['Syndrome'].isin(desired_syndromes)]


# Count the number of 1's in the column
count_Epi = df_epi['Epi Soarian'].sum()
count_Epi_ND = df_epi['Epi_ND'].sum()
count_EEG = df_epi['EEG dans NLG'].sum()
count_BNP = df_epi['NPSY'].sum()
count_MoCA = df_epi['moca_score_01'].count()
count_MoCA_2 = df_epi['moca_score_02'].count()
count_CDR = df_epi['cdr_age_01'].count()
count_CDR_2 = df_epi['cdr_age_02'].count()
count_MRI = df_epi['mri_tiv'].count()
count_ratio = df_epi['ratio_abeta42_40'].count()
count_subject = len(df_epi)
count_female = df_epi['sex'].eq(1).sum()
mean_age = df_epi['csf_age'].mean()
std_age = df_epi['csf_age'].std()
count_educ = df_epi['education_level'].count()


print('There is '+str(count_female)+ ' females of of '+str(count_subject))
print('There is '+str(count_BNP)+ ' patient with NPSY evaluation out of '+str(count_subject))
print('There is '+str(count_MoCA)+ ' patient with MoCA evaluation out of '+str(count_subject))
print('There is '+str(count_MoCA_2)+ ' patient with several MoCA evaluation out of '+str(count_subject))
print('There is '+str(count_CDR)+ ' patient with CDR evaluation out of '+str(count_subject))
print('There is '+str(count_CDR_2)+ ' patient with several CDR evaluation out of '+str(count_subject))
print('There is '+str(count_MRI)+ ' patient with morpho evaluation out of '+str(count_subject))
print('There is '+str(count_EEG)+ ' patient with EEG out of '+str(count_subject))
print('There is '+str(count_Epi)+ ' patient with epilepsy out of '+str(count_subject))
print('There is '+str(count_Epi_ND)+ ' patient with neurodegenerative epilepsy out of '+str(count_subject))
print('There is '+str(count_ratio)+ ' patient with abeta42/40 ratio out of '+str(count_subject))
print('There is '+str(count_educ)+ ' patient with education evaluation out of '+str(count_subject))
print('Mean age: ' + str(mean_age))
print('SD age: ' + str(std_age))