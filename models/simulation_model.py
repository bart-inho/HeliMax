import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

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
        self.model[:, :, round(35/self.discrete[2]):nz] = 1 # Glacier = 1

    def add_rectangle(self, antenna_x, antenna_y, antenna_z, thick, antenna_spacing, dis):
        
        right_corner = round((antenna_x - 2)/dis)
        left_corner = round((antenna_x + antenna_spacing + 2)/dis)
        height = round((antenna_z-2)/dis)
        thickness = round(thick/dis)
        front = round((antenna_y - 2)/dis)
        back = round((antenna_y + 2)/dis)

        self.model[right_corner:left_corner, front:back, height-thickness:height] = 3

    def add_3D_oval_shape(self, center, radii, thickness):
        nx, ny, nz = self.model.shape
        center = np.array(center) / self.discrete
        radii = np.array(radii) / self.discrete / 2
        thickness = thickness / self.discrete[0]

        # Create index arrays for i, j, k
        i, j, k = np.mgrid[:nx, :ny, :nz]

        # Calculate the squared distances from the center divided by the radii squared
        # to create an ellipsoid equation of the form (x^2/a^2 + y^2/b^2 + z^2/c^2 = 1)
        ellipsoid = (((i - center[0]) / radii[0])**2 +
                     ((j - center[1]) / radii[1])**2 +
                     ((k - center[2]) / radii[2])**2  )

        # Define the outer and inner surfaces of the shell
        outer_surface = ellipsoid <= 1
        inner_surface = ellipsoid <= (1 - thickness/radii[0])**2

        # Create shell between the inner and outer surfaces
        shell_mask = outer_surface & ~inner_surface

        # Update the model with the new values where the shell should be
        self.model[shell_mask] = 3  # Assign a value for the shell material


    def generate_curved_bedrock_glacier(self, center, r, arg_rough):
        nx, ny, nz = self.model.shape

        r_bedrock = r
        r_ice = r + .5
        roughness = 1.5e-2

        # Create index arrays for i, j, k
        i, j, k = np.mgrid[:nx, :ny, :nz]

        # Calculate distances considering roughness
        if arg_rough:
            # Create a different roughness factor for each y-slice
            roughness_factor = np.random.normal(loc=1, scale=roughness, size=(nx, ny, nz))
        else:
            roughness_factor = 1

        rij = roughness_factor * np.sqrt(((k - center[2]) * self.discrete[2])**2 +
                                        ((i - center[0]) * self.discrete[0])**2)

        # Create bedrock, ice, water, and free-air layers based on the radial distances
        bedrock_mask = (k >= round(nz/3)) & (rij > r_bedrock)
        ice_mask = (k >= round(nz/3)) & (rij < r_ice)

        self.model[bedrock_mask] = 2  # Bedrock = 2
        self.model[ice_mask] = 1  # Ice = 1

    def plot_initial_model(self, transceiver, receiver):
        """
        Plot the initial model

        Parameters:
        self (SimulationModel): the model to plot
        transceiver (np.array): the transceiver position
        receiver (np.array): the receiver position

        Returns:
        None
        """

        nx = self.model.shape[0]
        nz = self.model.shape[2]

        model = self.model[:, round(self.y_size/self.discrete[1]/2), :].T

        X, Y = np.meshgrid(np.linspace(0, self.x_size + self.discrete[0], nx+1), 
                        np.linspace(0, self.z_size + self.discrete[2], nz +1))
        
        # Plot parameters
        colors = ['white', 'blue', 'gray', 'black']  # Define colors for each category

        # Create a colormap from the list of colors
        cmap = mcolors.ListedColormap(colors)

        # Create a boundary norm with the categories as boundaries
        bounds = [0, 1, 2, 3, 4]  # Set boundaries including the right edge for the last category
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        plt.pcolormesh(X, Y, model, cmap=cmap, norm=norm, shading='auto')
        cbar = plt.colorbar(ticks=[0.5, 1.5, 2.5, 3.5], boundaries=bounds, orientation='horizontal', pad=0.11, aspect=50)  # Set tick positions at the center of each category
        cbar.set_ticklabels(['Free Space', 'Glacier Ice', 'Bedrock', 'Metal'])  # Label each tick with text
        plt.scatter(transceiver[0], transceiver[2], .5, color='red', label='Transceiver')  # Mark transceiver
        plt.scatter(receiver[0], receiver[2], .5, color='green', label='Receiver')  # Mark receiver
        # plt.legend(loc='upper right')
        plt.gca().invert_yaxis()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.ylabel('depth [m]')
        plt.xlabel('distance [m]')
        plt.title('Moon Lava Tube GPR Test')
        plt.tight_layout()
        plt.savefig(self.path+'/figures/'+self.name+'.png', format='png')  # Use efficient format
        plt.close()