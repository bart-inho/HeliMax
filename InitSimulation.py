import numpy as np
import matplotlib.pyplot as plt
import h5py
from os.path import exists
import os
from FunctionRep import *

# Model size and discretization -----------------------------------
xsize = 100 # x-size of the model [m]
ysize = 100 # y-size of the model [m]

dx = .1 # z cell size [m]
dy = .1 # y cell size [m]
dz = .1 # z cell size [m]

discrete = [dx, dy, dz]

nx = int(xsize / dx) # x-number of cell
ny = int(ysize / dy) # y-number of cell

# Frequency and time window ---------------------------------------
freq = 25e6 # [MHz]
time_window = 1.5e-6 # [s]
measurment_number = 20 # number of gprMax simulations
measurment_step = round((ysize - 10)/measurment_number) # number of step minus a margin

# Folder, files name and path -------------------------------------
ModelName = 'off_centered_bedrock_air_helico'

folder_inout = 'inout_files/'
filename_input = ModelName # .in file
filename_materials = ModelName+'_materials' # material file
path_to_h5 = folder_inout+ModelName # path

# Create path to file ---------------------------------------------
path_to_input = folder_inout + filename_input
path_to_materials = folder_inout+filename_materials

# Define materials [eps_r ; sigma ; mu_r ; vel] -------------------
mat_freespace = [1., 0., 1., 0] # gprMax build in 
mat_glacier = [3.2, 5.e-8, 1., 0]  # Church et al., 2020
mat_bedrock = [5., 0.01, 1, 0] # granite Annan (1999)
mat_helico = [1., 'inf', 1., 0] # metal gprMax build in

# Create material file --------------------------------------------
WriteMaterialsFile(path_to_materials, mat_freespace, mat_bedrock, mat_glacier, mat_helico)

# Generate base of the model --------------------------------------
model = np.zeros((ny, nx)) # Free space = 1
model[round(ny/2):ny,:] = 2 # Granite = 2
model[0:round(ny/20), :] = 3 # Helico = 3

# Generate a curved bedrock ---------------------------------------
center = [0, nx]
r = 100 # Define center of the circle
CreateCircleShape(model, r, center, dx, dy)

# Flip matrix ------------------------------------------------------
model = model.T # taking the transverse of the matrix is necessary for the gprMax format

# Define x and y position for the transiever and the receiver ------
trans = [round(xsize/10), round(ysize/3-.5)]
recei = [round(xsize/10 + 3), round(ysize/3-.5)]

# Plot model -------------------------------------------------------
PlotInitialModel(ModelName, model, trans, recei, xsize, ysize)

# Rehape the model for gprMax compulsory third dimension -----------
model = np.reshape(model, (nx, ny, 1))

# generate h5 file -------------------------------------------------
Writeh5File(path_to_h5, model, discrete)

# Generate .in file ------------------------------------------------
WriteInputFile(ModelName, path_to_input, path_to_materials, path_to_h5, xsize, ysize, discrete, freq, trans, recei, measurment_step, time_window)