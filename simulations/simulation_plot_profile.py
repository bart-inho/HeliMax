import os

import h5py
import numpy as np
import matplotlib.pyplot as plt

from gprMax.exceptions import CmdInputError
from tools.outputfiles_merge import get_output_data

class PlotProfile:
    def __init__(self, outputfile, rx_component):
        self.outputfile = outputfile
        self.rx_component = rx_component

    def get_output_data(self):
        # Open output file and read number of outputs (receivers)
        f = h5py.File(self.outputfile, 'r')
        nrx = f.attrs['nrx']
        f.close()

        # Check there are any receivers
        if nrx == 0:
            raise CmdInputError('No receivers found in {}'.format(self.outputfile))

        for rx in range(1, nrx + 1):
            self.outputdata, self.dt = get_output_data(self.outputfile, rx, self.rx_component)

    def plot(self):
        plthandle = self.mpl_plot()
        plthandle.show()

    def mpl_plot(self):
        (path, filename) = os.path.split(self.outputfile)

        fig = plt.figure(num=filename + ' - rx' + str(1),  # Adjust this as needed
                         figsize=(20, 10), facecolor='w', edgecolor='w')
        plt.imshow(self.outputdata,
                   extent=[0, self.outputdata.shape[1], self.outputdata.shape[0] * self.dt, 0],
                   interpolation='nearest', aspect='auto', cmap='seismic',
                   vmin=-np.amax(np.abs(self.outputdata)), vmax=np.amax(np.abs(self.outputdata)))
        # set z-axis limits
        plt.xlabel('Trace number')
        plt.ylabel('Time [s]')
        plt.title('{}'.format(filename))

        # Grid properties
        ax = fig.gca()
        ax.grid(which='both', axis='both', linestyle='-.')

        cb = plt.colorbar()
        # Add colorbar limits
        plt.clim(-1e-2, 1e-2)
        if 'E' in self.rx_component:
            cb.set_label('Field strength [V/m]')
        elif 'H' in self.rx_component:
            cb.set_label('Field strength [A/m]')
        elif 'I' in self.rx_component:
            cb.set_label('Current [A]')

        # Save a PDF/PNG of the figure
        savefile = os.path.splitext(filename)[0]
        fig.savefig(path + os.sep + savefile + '.pdf', dpi=None, format='pdf',
                    bbox_inches='tight', pad_inches=0.1)

        return plt