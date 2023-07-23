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

    def calculate_measurment_step(self, number_of_measurements, antenna_spacing):
        nx = self.model.shape[0]
        nx_buffered = nx - 50 # buffer of 20 cell on each side
        return round((nx_buffered * self.discrete[0] - antenna_spacing) / number_of_measurements, 2)

    def generate_base_glacier(self):
        nx = int(self.x_size / self.discrete[0])
        ny = int(self.y_size / self.discrete[1])
        nz = int(self.z_size / self.discrete[2])
        
        self.model = np.zeros((nx, ny, nz)) # Free space = 0
        self.model[:, :, round(nz/3):nz] = 1 # Glacier = 1
        # self.model[:, :, 0:10] = 3 # Metal = 3

    def generate_curved_bedrock_glacier(self, center, r, arg_rough):
        nx = self.model.shape[0]
        nz = self.model.shape[2]

        r_bedrock=r
        r_ice=r+.5
        roughness=1.5e-2

        for i in range(0, nx):
            for j in range(0, nz):
                # Add some roughness to the radial distance.
                if arg_rough:
                    roughness_factor = np.random.normal(loc=1, scale=roughness)
                else:
                    roughness_factor = 1

                rij = roughness_factor * np.sqrt(((j - center[2])*self.discrete[2])**2 + 
                                                ((i - center[0])*self.discrete[0])**2) # Calculate distance

                # Create bedrock, ice, water, and free-air layers based on the radial distances
                if j >= round(nz/3):
                    if rij > r_bedrock:
                        self.model[i, :, j] = 2 # Bedrock = 2
                    elif rij < r_ice:
                        self.model[i, :, j] = 1 # Ice = 1

    def plot_initial_model(self, transceiver, receiver):

        X, Y = np.meshgrid(np.arange(0, self.x_size, self.discrete[0]), 
                        np.arange(0, self.z_size, self.discrete[2]))
        
        plt.pcolormesh(X, Y, self.model[:, round(transceiver[1]*self.discrete[1]), :].T)
        plt.scatter(transceiver[0], transceiver[2])
        plt.scatter(receiver[0], receiver[2])
        plt.gca().invert_yaxis()
        plt.gca().set_aspect('equal')
        plt.colorbar()
        plt.clim(0, 3)
        plt.ylabel('depth [m]')
        plt.xlabel('distance [m]')
        plt.title(self.name)
        plt.savefig(self.path+'/figures/'+self.name+'.png')
        plt.close()        