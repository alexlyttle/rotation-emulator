import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SOLAR_LOGG = 4.4384
SOLAR_TEFF = 5776.0
SOLAR_ZX = 0.023

class Track:
    def __init__(self, path):
        df = pd.read_csv(path)
        df['log(L/Lsun)'] = np.log10(df['L/Lsun'])
        df['log(R/Rsun)'] = np.log10(df['R/Rsun'])
        df['log(Z/X)(surface)'] = np.log10(df['Z/X(surface)'])
        df['log(g)'] = SOLAR_LOGG + np.log10(df['M/Msun']) - 2 * df['log(R/Rsun)']

        self.eep_index = {
            'preMS': df.index[0],
            'ZAMS': df.loc[df['Lnuc/Lsun'] / df['L/Lsun'] > 1-1e-6].index[0],
            'IAMS': df.loc[df['Xcore'] < 0.3].index[0],
            'TAMS': df.loc[df['Xcore'] < 1e-6].index[0],
            'RGBtip': df.index[-1],
        }
        assert np.all(df.index.to_numpy() - np.arange(len(df)) == 0)
        self.df = df
        
    def calculate_eep(self):
        xs = self.df[['log(Teff)(K)', 'log(g)']].to_numpy()

        d = np.zeros(xs.shape[0])
        delta_d = np.sqrt(np.sum((xs[1:] - xs[:-1])**2, axis=1))
        d[1:] += np.cumsum(delta_d)

        indices = list(self.eep_index.values())
        eep = np.zeros(xs.shape[0])

        for i, (index0, index1) in enumerate(zip(indices[:-1], indices[1:])):
            eep[index0:index1] = i + (d[index0:index1] - d[index0]) / (d[index1] - d[index0])
    
        eep[-1] = i + 1

        return eep

    def plot(self, x, y, **kwargs):
        if 'ax' in kwargs.keys():
            ax = kwargs.pop('ax')
        else:
            fig, ax = plt.subplots()
        
        self.df.loc[self.eep_index['preMS']:self.eep_index['ZAMS']].plot(x=x, y=y, c='C0', label=r'$\rm preMS - ZAMS$', ax=ax, **kwargs)
        self.df.loc[self.eep_index['ZAMS']:self.eep_index['IAMS']].plot(x=x, y=y, c='C1', label=r'$\rm ZAMS - IAMS$', ax=ax, **kwargs)
        self.df.loc[self.eep_index['IAMS']:self.eep_index['TAMS']].plot(x=x, y=y, c='C2', label=r'$\rm IAMS - TAMS$', ax=ax, **kwargs)
        self.df.loc[self.eep_index['TAMS']:self.eep_index['RGBtip']].plot(x=x, y=y, c='C3', label=r'$\rm TAMS - RGBtip$', ax=ax, **kwargs)

        return ax
