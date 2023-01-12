import numpy as np
import matplotlib.pyplot as plt
from os.path import exists
import h5py as h5py
import os
from random import randrange

# This function repository regroups every repetitive or space consuming task. 

# Write materials and input files --------------------------
def WriteMaterialsFile(path_to_materials, mat_freespace, mat_bedrock, 
    mat_glacier, mat_helico, mat_shield):
    infilename_materials = open(path_to_materials+'.txt', 'w') # create materials file
    infilename_materials.write('#material: '+str(mat_freespace[0])+' '+str(mat_freespace[1])+' '+str(mat_freespace[2])+' '+str(mat_freespace[3])+' freespace\n')
    infilename_materials.write('#material: '+str(mat_glacier[0])+' '+str(mat_glacier[1])+' '+str(mat_glacier[2])+' '+str(mat_glacier[3])+' glacier\n')
    infilename_materials.write('#material: '+str(mat_bedrock[0])+' '+str(mat_bedrock[1])+' '+str(mat_bedrock[2])+' '+str(mat_bedrock[3])+' bedrock\n')
    infilename_materials.write('#material: '+str(mat_helico[0])+' '+str(mat_helico[1])+' '+str(mat_helico[2])+' '+str(mat_helico[3])+' helicopter\n')
    infilename_materials.write('#material: '+str(mat_shield[0])+' '+str(mat_shield[1])+' '+str(mat_shield[2])+' '+str(mat_shield[3])+' shield\n')

def WriteInputFile(ModelName, path_to_input, path_to_materials, path_to_h5, xsize, ysize, 
    discrete, freq, trans, recei, time_window, trace):
    infilename = open(path_to_input+str(trace)+'.in', 'w') # create .in file
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
    # infilename.write('#src_steps: '+str(mstep)+' 0 0\n')
    # infilename.write('#rx_steps: '+str(mstep)+' 0 0\n')
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

def GeneratePaths(ModelName, folder_inout):
    filename_input = ModelName # .in file
    filename_materials = ModelName+'_materials' # material file
    path_to_h5 = folder_inout+ModelName # path

    # Create path to file ---------------------------------------------
    path_to_input = folder_inout + filename_input
    path_to_materials = folder_inout+filename_materials

    return path_to_h5, path_to_input, path_to_materials

def Homogenization():

    epsilon_0 = 8.8541878128e-12
    mu_0 = 1.25663706212e-6
    # Define the properties of the wire and air
    permittivity_air = 1.0 # F/m
    permeability_air = 1.0 # H/m
    
    permittivity_wire = 1e-10 # F/m (very small value for a perfect conductor)
    permeability_wire = 1e-10 # H/m (very small value for a perfect conductor)

    # Define the volume fraction of the wire in the wire mesh shield
    f = 0.2 # 10% wire, 90% air

    # Calculate the effective permittivity and permeability of the wire mesh shield
    permittivity_eff = permittivity_air*(1-f) + permittivity_wire*f
    permeability_eff = permeability_air*(1-f) + permeability_wire*f

    #print out the result
    wire_permittivity = permittivity_eff/epsilon_0
    wire_permeability = permeability_eff/mu_0

    print('Relative permittivity:', wire_permittivity, 'F/m')
    print('Relative permeability:', wire_permeability, 'H/m')

    return wire_permittivity, wire_permeability

def GenerateMaterials():
    mat_freespace = [1., 0., 1., 0] # gprMax build in 
    mat_glacier = [3.2, 5.e-8, 1., 0]  # Church et al., 2020
    mat_bedrock = [5., 0.01, 1, 0] # granite Annan (1999)
    mat_helico = [1., 'inf', 1., 0] # metal gprMax build in

    wire_permittivity, wire_permeability = Homogenization()
    mat_shield = [wire_permittivity, 'inf', wire_permeability, 0] # metal gprmax build in

    return mat_freespace, mat_glacier, mat_bedrock, mat_helico, mat_shield

def CurvedBedrockModel(dx, dy, nx, ny):
    model = np.zeros((ny, nx)) # Free space = 0
    model[round(45.0/dy):ny,:] = 1 # Glacier = 1, 15.0 = distance from top of the model
    # Generate a curved bedrock
    center = [0, nx]
    r = 100 # Define center of the circle
    CreateCircleShape('smooth', 'bedrock', model, r, center, dx, dy) #generate circle shape
    return model

def HelicoShape(model, delta, antenna_start, antenna_height, dx, dy):
    model[round((antenna_height - 20)/dx):round((antenna_height - 16.5)/dy),
        round((antenna_start+delta-4)/dx): round((antenna_start+delta+9)/dy)] = 3
    return model

def ShieldShape(model, delta, antenna_start, antenna_height, dx, dy):
    model[round((antenna_height - 0.75)/dx):round((antenna_height - 0.5)/dy),
        round((antenna_start+delta-2)/dx): round((antenna_start+delta+4)/dy)] = 4
    return model

# Generate circle shape depending on reius
def CreateCircleShape(type, material, model, r, center, dx, dy):
    if material == 'bedrock':
        mat = 2
    elif material == 'helico':
        mat = 3
    elif material == 'glacier':
        mat = 1
    elif material == 'freespace':
        mat = 0
    elif material == 'shield':
        mat = 4

    nx = model.shape[0]
    ny = model.shape[1]
    N = nx * ny
    N_loop = N-N/2
    for i in range(0, nx): # start loop on x
        for j in range(0, ny): # start loop on y
            if type == 'smooth':
                rij = np.sqrt(((j - center[1])*dx)**2 + ((i - center[0])*dy)**2) # Calculate distance
            # elif type == 'rough':
            #     rij = (np.sqrt(((j - center[1])*dx)**2 + ((i - center[0])*dy)**2))+np.sin(N_loop/25000) # Calculate distance
            else:
                print('Please enter correct string input : either smooth or rough')
            if rij > r and i > round(ny/2):# condition
                model[i, j] = mat
            N_loop += 1

def MoveHelico(ModelName, path_to_input, path_to_materials,
    path_to_h5, xsize, ysize, discrete, freq, trans, recei, trace, time_window, nx, ny, dx, dy, delta, antenna_start, antenna_height):
    
    # Generate base of the model --------------------------------------
    model = CurvedBedrockModel(dx, dy, nx, ny)

    # Define helico shape
    model = HelicoShape(model, delta, antenna_start, antenna_height, dx, dy)
    model = ShieldShape(model, delta, antenna_start, antenna_height, dx, dy)

    model = model.T

    # Rehape the model for gprMax compulsory third dimension and print h5 file
    Writeh5File(path_to_h5, np.reshape(model, (nx, ny, 1)), discrete)

    # Generate .in file ------------------------------------------------
    WriteInputFile(ModelName, path_to_input, path_to_materials,
    path_to_h5, xsize, ysize, discrete, freq, trans, recei, time_window, trace)
    return model

# Plot initial model
def PlotInitialModel(ModelName, model, trans, recei, xsize, ysize, dx, dy):
    nx = model.shape[0]
    ny = model.shape[1]
    # Plot the model ---------------------------------------------------
    plt.imshow(model.T) # plotting the transverse
    plt.scatter(trans[0]/xsize*nx, trans[1]/ysize*ny)
    plt.scatter(recei[0]/xsize*nx, recei[1]/ysize*ny)
    plt.title(ModelName)
    plt.savefig('figures/'+ModelName+'.png')
    plt.close()

