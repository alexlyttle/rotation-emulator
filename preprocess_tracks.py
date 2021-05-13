import os, h5py, timeit
import numpy as np

from track import Track

DATA_DIR = '/rds/projects/d/daviesgr-alex-phd/rotation_grid/rot_evolved'
FILENAMES = [fn for fn in os.listdir(DATA_DIR) if fn.startswith('m') and fn.endswith('.csv')]
HDFPATH = '/rds/projects/d/daviesgr-alex-phd/repos/alexlyttle/rotation-emulator/data/yrec_grid.h5'

COLUMNS = ['EEP', 'M/Msun', 'Age(Gyr)', '[Fe/H]', 'fk', 'Rocrit', 
           'Prot(days)', 'log(Teff)(K)', 'R/Rsun', 'log(Z/X)(surface)']

data = []

# Loop through track data files and calculate EEPs and then append to data
for i, fn in enumerate(FILENAMES):
    print(fn)
    try:
        track = Track(os.path.join(DATA_DIR, fn))
        track.df['EEP'] = track.calculate_eep()
        data.append(track.df.loc[track.eep_index['ZAMS']:track.eep_index['TAMS'], COLUMNS].to_numpy())
    except Exception as err:
        print(err)
data = np.concatenate(data)

h5f = h5py.File(HDFPATH, 'w')

dset = h5f.create_dataset('data', data=data)
dset.attrs.create('columns', COLUMNS)

h5f.close()
