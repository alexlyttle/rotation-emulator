import os, h5py, logging
import numpy as np

from track import Track

FORMAT = '%(asctime)-15s:%(levelname)-8s:%(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

DATA_DIR = '/rds/projects/d/daviesgr-alex-phd/rotation_grid/rot_evolved'
FILENAMES = [fn for fn in os.listdir(DATA_DIR) if fn.startswith('m') and fn.endswith('.csv')]
HDFPATH = '/rds/projects/d/daviesgr-alex-phd/repos/alexlyttle/rotation-emulator/data/yrec_grid.h5'

COLUMNS = ['EEP', 'M/Msun', 'Age(Gyr)', '[Fe/H]', 'fk', 'Rocrit', 
           'Prot(days)', 'log(Teff)(K)', 'R/Rsun', 'log(Z/X)(surface)']

data = []
n_tracks = len(FILENAMES)

logging.info('Looping through filenames')
# Loop through track data files and calculate EEPs and then append to data
for i, fn in enumerate(FILENAMES):
    try:
        track = Track(os.path.join(DATA_DIR, fn))
        track.df['EEP'] = track.calculate_eep()
        data.append(track.df.loc[track.eep_index['ZAMS']:track.eep_index['TAMS'], COLUMNS].to_numpy())
    except Exception as err:
        logging.warning(f'Error occured with file: {fn}')
        logging.error(err)
logging.info('Done')

logging.info('Concatenating')
data = np.concatenate(data)
logging.info('Done')

logging.info('Writing to file')
h5f = h5py.File(HDFPATH, 'w')

dset = h5f.create_dataset('data', data=data)
dset.attrs.create('columns', COLUMNS)

h5f.close()
logging.info('Done')
