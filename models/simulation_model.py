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
        
        self.model = np.zeros((nx, ny, nz)) # Free space = 0
        self.model[round(nx/2):nx,:,:] = 1 # Glacier = 1
        self.model[0:round(nx/20),:,:] = 3 # Helico = 3

    def calculate_measurment_step(self, number_of_measurements):
        return (self.z_size - 30)/number_of_measurements

    def generate_curved_bedrock(self, center, r):
        nx = self.model.shape[0]
        nz = self.model.shape[2]

        for i in range(0, nx):
            for j in range(0, nz):
                rij = np.sqrt(((j - center[2])*self.discrete[2])**2 + 
                              ((i - center[0])*self.discrete[0])**2) # Calculate distance
                if rij < r and i >= round(nx/2):
                    self.model[i, :, j] = 2 # Bedrock = 2
                    
    def flip_matrix(self):
        self.model = self.model.T

    def reshape_model(self):
        nx = int(self.x_size / self.discrete[0])
        ny = int(self.y_size / self.discrete[1])
        nz = int(self.z_size / self.discrete[2])
        
        self.model = np.reshape(self.model, (nx, ny, nz))

    def plot_initial_model(self, transceiver, receiver):
        nx = int(self.x_size / self.discrete[0])
        ny = int(self.y_size / self.discrete[1])
        nz = int(self.z_size / self.discrete[2])

        model_plot = self.model.T
        plt.imshow(model_plot[:, round(transceiver[1]/self.y_size*ny), :]) 
        plt.scatter(transceiver[0]/self.x_size*nx, transceiver[2]/self.z_size*nz)
        plt.scatter(receiver[0]/self.x_size*nx, receiver[2]/self.z_size*nz)
        plt.title(self.name)
        plt.savefig(self.path+'/figures/'+self.name+'.png')
        # plt.show()
        plt.close()