import os, h5py
import numpy as np

from track import Track

DATA_DIR = './data/example_tracks'
FILENAMES = os.listdir(DATA_DIR)
HDFPATH = 'data/example_grid.h5'

COLUMNS = ['EEP', 'M/Msun', 'Age(Gyr)', '[Fe/H]', 'fk', 'Rocrit', 
           'Prot(days)', 'log(Teff)(K)', 'R/Rsun', 'Z/X(surface)']

data = []

# Loop through track data files and calculate EEPs and then append to data
for i, fn in enumerate(FILENAMES):
    track = Track(os.path.join(DATA_DIR, fn))
    track.df['EEP'] = track.calculate_eep()
    data.append(track.df.loc[track.eep_index['ZAMS']:track.eep_index['TAMS'], COLUMNS].to_numpy())

data = np.concatenate(data)

h5f = h5py.File(HDFPATH, 'w')

dset = h5f.create_dataset('data', data=data)
dset.attrs.create('columns', COLUMNS)

h5f.close()
