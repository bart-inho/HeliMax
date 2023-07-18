import numpy as np
import matplotlib.pyplot as plt
from os.path import exists
import h5py as h5py
import os
from random import randrange

# This function repository regroups every repetitive or space consuming task. 
def WriteMaterialsFile(path_to_materials, mat_freespace, mat_bedrock, mat_glacier, mat_helico):
    infilename_materials = open(path_to_materials+'.txt', 'w') # create materials file
    infilename_materials.write('#material: '+str(mat_freespace[0])+' '+str(mat_freespace[1])+' '+str(mat_freespace[2])+' '+str(mat_freespace[3])+' freespace\n')
    infilename_materials.write('#material: '+str(mat_glacier[0])+' '+str(mat_glacier[1])+' '+str(mat_glacier[2])+' '+str(mat_glacier[3])+' glacier\n')
    infilename_materials.write('#material: '+str(mat_bedrock[0])+' '+str(mat_bedrock[1])+' '+str(mat_bedrock[2])+' '+str(mat_bedrock[3])+' bedrock\n')
    infilename_materials.write('#material: '+str(mat_helico[0])+' '+str(mat_helico[1])+' '+str(mat_helico[2])+' '+str(mat_helico[3])+' helicopter\n')
    
def WriteInputFile(ModelName, path_to_input, path_to_materials, path_to_h5, 
                   xsize, ysize, zsize, discrete, freq, transiever1, reciever1, mstep, time_window):
    infilename = open(path_to_input+'.in', 'w') # create .in file
    dx = discrete[0]
    dy = discrete[1]
    dz = discrete[2]
    infilename.write('#title: '+ModelName+'\n')
    # Set domain size, don't forget z = dz for 2D
    infilename.write('#domain: '+str(xsize)+' '+str(ysize)+' '+str(zsize)+' \n')
    infilename.write('#dx_dy_dz: '+str(dx)+' '+str(dy)+' '+str(dz)+' \n')
    # Time window
    infilename.write('#time_window: '+ str(time_window)+'\n')
    # Frequency and antenna geometry
    infilename.write('#waveform: ricker 1 '+ str(freq)+ ' my_ricker\n')
    infilename.write('#hertzian_dipole: z '+str(transiever1[0])+' '+str(transiever1[1])+' '+str(transiever1[2])+' my_ricker\n')
    infilename.write('#rx: '+str(reciever1[0])+' '+str(reciever1[1])+' '+str(reciever1[2])+'\n')
    # Movement of the right
    infilename.write('#src_steps: '+str(mstep)+' 0 0\n')
    infilename.write('#rx_steps: '+str(mstep)+' 0 0\n')
    # Include external files
    infilename.write('#geometry_objects_read: 0 0 0 '+path_to_h5+'.h5 '+path_to_materials+'.txt')

def Writeh5File(path_to_h5, model, discrete):
    dx = discrete[0]
    dy = discrete[1]
    dz = discrete[2]
    if exists(path_to_h5) == True: # condition to delete old h5 file
        os.remove(path_to_h5) # delete old h5 file
    hdf = h5py.File(path_to_h5+'.h5', 'w') # create a new h5 file
    modelh5 = hdf.create_dataset(name = 'data', data = model) # create a new dataset
    hdf.attrs['dx_dy_dz'] = [dx, dy, dz] # create an attribute that containes dx, dy and dz
    # -> more info : https://docs.h5py.org/en/stable/high/dataset.html?highlight=attrs#h5py.Dataset.attrs

def GenerateGlacierShape(model, r, center, dx, dz):
    nx = model.shape[0]
    nz = model.shape[2]

    for i in range(0, nx):
        for j in range(0, nz):
            rij = np.sqrt(((j - center[2])*dz)**2 + ((i - center[0])*dx)**2) # Calculate distance
            if rij < r and i >= round(nx/2):
                model[i, :, j] = 2 # Bedrock = 2

def PlotInitialModel(ModelName, model, transiever1, reciever1, xsize, ysize, zsize):
    nx = model.shape[0]
    ny = model.shape[1]
    nz = model.shape[2]
    model_plot = model.T
    # Plot the model ---------------------------------------------------
    plt.imshow(model_plot[:, round(transiever1[1]/ysize*ny), :]) # plotting the transverse
    plt.scatter(transiever1[0]/xsize*nx, transiever1[2]/zsize*nz)
    plt.scatter(reciever1[0]/xsize*nx, reciever1[2]/zsize*nz)
    plt.title(ModelName)
    plt.savefig('figures/'+ModelName+'.png')
    plt.close()