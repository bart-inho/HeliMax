import numpy as np
import matplotlib.pyplot as plt
import h5py
from os.path import exists
import os
from FunctionRep import *

# Model size and discretization -----------------------------------
xsize = 60 # x-size of the model [m]
ysize = 120 # y-size of the model [m]

dx = .1 # z cell size [m]
dy = .1 # y cell size [m]
dz = .1 # z cell size [m]

discrete = [dx, dy, dz]

nx = int(xsize / dx) # x-number of cell
ny = int(ysize / dy) # y-number of cell

# Frequency and time window ---------------------------------------
freq = 25e6 # [MHz]
time_window = 0.75e-6 # [s]
measurment_number = 30 # number of gprMax simulations
measurment_step = (xsize - 10)/measurment_number # number of step minus a margin
print('Measurment step = ', measurment_step, '[m]')
print('Measurment number = ', measurment_number)

# Folder, files name and path -------------------------------------
ModelName = 'test_moving'
folder_inout = 'inout_files/'

path_to_h5, path_to_input, path_to_materials = GeneratePaths(ModelName, folder_inout)

# Define materials [eps_r ; sigma ; mu_r ; vel] -------------------
mat_freespace, mat_glacier, mat_bedrock, mat_helico = GenerateMaterials()

# Create material file --------------------------------------------
WriteMaterialsFile(path_to_materials, mat_freespace, mat_bedrock, mat_glacier, mat_helico)

# Generate base of the model --------------------------------------
model = CurvedBedrockModel(dx, dy, nx, ny)

# Define x and y position for the transiever and the receiver ------
antenna_heigh = 30.0 # [m] from the top of the model (sky)
antenna_start = 6.0  # [m] from the right of the model
trans = [round(antenna_start),     round(antenna_heigh)]
recei = [round(antenna_start + 2.0), round(antenna_heigh)]

# Define helico shape
model = HelicoShape(model, 'helico', antenna_start, antenna_heigh, dx, dy)

model = model.T
# Plot model -------------------------------------------------------
PlotInitialModel(ModelName, model, trans, recei, xsize, ysize, dx, dy)

# Rehape the model for gprMax compulsory third dimension -----------
model = np.reshape(model, (nx, ny, 1))

# generate h5 file -------------------------------------------------
Writeh5File(path_to_h5, model, discrete)

# Generate .in file ------------------------------------------------
WriteInputFile(ModelName, path_to_input, path_to_materials, path_to_h5, xsize, ysize, discrete, freq, trans, recei, measurment_step, time_window)