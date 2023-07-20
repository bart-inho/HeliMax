import numpy as np
import matplotlib.pyplot as plt

class SimulationModel:
    # This class is used to store the model information and generate the base model.

    def __init__(self, name, x_size, y_size, z_size, 
                 discrete, materials, path):
        self.name = name
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size
        self.discrete = discrete
        self.materials = materials
        self.path = path

    def generate_base(self):
        nx = int(self.x_size / self.discrete[0])
        ny = int(self.y_size / self.discrete[1])
        nz = int(self.z_size / self.discrete[2])
        
        self.model = np.zeros((nz, ny, nx)) # Free space = 0
        self.model[round(nz/3):nz, :, :] = 1 # Glacier = 1
        # self.model[0:round(nx/20),:,:] = 4 # Helico = 4

    def calculate_measurment_step(self, number_of_measurements):
        return (self.z_size - 50)/number_of_measurements

    def generate_curved_bedrock(self, center, r):
        nx = self.model.shape[0]
        nz = self.model.shape[2]

        r_bedrock=r
        r_ice=r+.25
        r_air=r+.5 
        r_water = r+.75
        roughness=1.5e-2

        for i in range(0, nx):
            for j in range(0, nz):
                # Add some roughness to the radial distance.
                roughness_factor = np.random.normal(loc=1, scale=roughness)
                rij = roughness_factor * np.sqrt(((j - center[2])*self.discrete[2])**2 + 
                                                ((i - center[0])*self.discrete[0])**2) # Calculate distance

                # Create bedrock, ice, water, and free-air layers based on the radial distances
                if i >= round(nx/3):
                    if rij < r_bedrock:
                        self.model[i, :, j] = 2 # Bedrock = 2
                    elif rij < r_ice:
                        self.model[i, :, j] = 1 # Ice = 1
                    elif rij < r_air:
                        self.model[i, :, j] = 0 # Free-air = 0
                    elif rij < r_water:
                        self.model[i, :, j] = 3 # water = 3
                            
        if np.any(self.model == 3):
            print('Water layer added to the model.')
        else:
            print('No water layer added to the model.')
                        
    def flip_matrix(self):
        self.model = self.model.T

    def reshape_model(self):
        nx = int(self.x_size / self.discrete[0])
        ny = int(self.y_size / self.discrete[1])
        nz = int(self.z_size / self.discrete[2])
        
        self.model = np.reshape(self.model, (nx, ny, nz))

    def plot_initial_model(self, transceiver, receiver):
        ny = int(self.y_size / self.discrete[1])

        model_plot = self.model.T
        plt.pcolormesh(np.arange(0, self.x_size, self.discrete[0]), 
                       np.arange(0, self.z_size, self.discrete[2]), 
                       model_plot[:, round(transceiver[1]/self.y_size*ny), :])
        
        plt.scatter(transceiver[0], transceiver[2])
        plt.scatter(receiver[0], receiver[2])
        plt.gca().invert_yaxis()
        plt.gca().set_aspect('equal')
        plt.ylabel('depth [m]')
        plt.xlabel('distance [m]')
        plt.title(self.name)
        plt.savefig(self.path+'/figures/'+self.name+'.png')
        # plt.show()
        plt.close()