import numpy as np
import mne
import os as os
from mne import io
import scipy.io
import matplotlib.pyplot as plt
from scipy import signal
import time
from scipy.fftpack import fft, fftfreq

animal =  "Ent_CamK2_54"
session ='S01'

os.chdir('/Users/gregorylepeu/Documents/Research/Projects/Post-Ictal/Data/'+animal+'/Pre-processed_No_rescale_fif/')

filename = animal +'_' + session
raw = io.read_raw_fif(filename+'_filtered_No_rescale_raw.fif')


# ***Visualisation***
color = {"eeg": "r", "emg": "k"}
scale = {"eeg": 600, "emg": 100}
raw.plot(remove_dc=True, duration=10, n_channels=16, scalings=scale, color=color, title=str(filename), show=True, block=True, show_options=True, show_first_samp=True)
