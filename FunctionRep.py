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
    
def WriteInputFile(ModelName, path_to_input, path_to_materials, path_to_h5, xsize, ysize, discrete, freq, trans, recei, mstep, time_window):
    infilename = open(path_to_input+'.in', 'w') # create .in file
    dx = discrete[0]
    dy = discrete[1]
    dz = discrete[2]
    infilename.write('#title: '+ModelName+'\n')
    # Set domain size, don't forget z = dz for 2D
    infilename.write('#domain: '+str(xsize)+' '+str(ysize)+' '+str(dz)+' \n')
    infilename.write('#dx_dy_dz: '+str(dx)+' '+str(dy)+' '+str(dz)+' \n')
    # Time window
    infilename.write('#time_window: '+ str(time_window)+'\n')
    # Frequency and antenna geometry
    infilename.write('#waveform: ricker 1 '+ str(freq)+ ' my_ricker\n')
    infilename.write('#hertzian_dipole: z '+str(trans[0])+' '+str(trans[1])+' 0 my_ricker\n')
    infilename.write('#rx: '+str(recei[0])+' '+str(recei[1])+' 0\n')
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

def CreateCircleShape(type, model, r, center, dx, dy):
    nx = model.shape[0]
    ny = model.shape[1]
    N = nx * ny
    N_loop = N-N/2
    for i in range(0, nx): # start loop on x
        for j in range(0, ny): # start loop on y
            if type == 'smooth':
                rij = np.sqrt(((j - center[1])*dx)**2 + ((i - center[0])*dy)**2) # Calculate distance
            elif type == 'rough':
                rij = (np.sqrt(((j - center[1])*dx)**2 + ((i - center[0])*dy)**2))+np.sin(N_loop/25000) # Calculate distance
            else:
                print('Please enter correct string input : either smooth or rough')

            if rij > r and i > round(ny/2):# condition
                model[i, j] = 2 # Bedrock = 2
            N_loop += 1
                
def PlotInitialModel(ModelName, model, trans, recei, xsize, ysize):
    nx = model.shape[0]
    ny = model.shape[1]
    # Plot the model ---------------------------------------------------
    plt.imshow(model.T) # plotting the transverse
    plt.scatter(trans[0]/xsize*nx, trans[1]/ysize*ny)
    plt.scatter(recei[0]/xsize*nx, recei[1]/ysize*ny)
    plt.title(ModelName)
    plt.savefig('figures/'+ModelName+'.png')
    plt.close()

def MoveHelico(model, nx, ny, dx, dy, step):
    model[300:400, step:200+step] = 3