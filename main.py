# This program is used to run the gprMax simulation applied to glaciology.
from services.file_service import FileService
from models.simulation_model import SimulationModel
from models.material import Material
from simulations.simulation_runner import SimulationRunner

def main():
    # Initialize Materials
    freespace = Material(1., 0., 1., 0, 'freespace')
    glacier = Material(3.2, 5.e-8, 1., 0, 'glacier')
    bedrock = Material(5., 0.01, 1, 0, 'bedrock')
    helico = Material(1., 'inf', 1., 0, 'helico')

    
    # Initialize SimulationModel
    model_name = 'OOP_tests'
    inout_files = 'inout_files/'
    path_to_files = inout_files + model_name

    # Generate model
    model = SimulationModel(model_name, 
                            50, 10, 40, 
                            [0.2, 0.2, 0.2], 
                            [freespace, glacier, bedrock, helico],
                            inout_files)

    # Generate base model
    model.generate_base()
    measurement_number = 5
    measurement_step = model.calculate_measurment_step(measurement_number)

    # Add curved bedrock feature
    center = [25, 5, 20] # assuming the center is at the middle of the model
    r = 35 # radius of the curvature
    model.generate_curved_bedrock(center, r)

    # Update model matrix orientation and shape if necessary
    model.flip_matrix()

    transceiver1 = [round(model.x_size/10),     
                    round(model.y_size/2), 
                    round(model.z_size/3-.5)]
    
    receiver1    = [round(model.x_size/10 + 4), 
                    round(model.y_size/2), 
                    round(model.z_size/3-.5)]

    #Plot initial model
    model.plot_initial_model(transceiver1, receiver1)

    # Reshape model for gprMax format
    model.reshape_model()

    # Call FileService to write files
    FileService.write_materials_file(model.path + model.name + '_materials', 
                                     model.materials)
    
    FileService.write_h5_file(model.path + model.name + '_h5', 
                              model)

    FileService.write_input_file(model, 
                                path_to_files, 
                                path_to_files + '_materials', 
                                path_to_files + '_h5', 
                                25e6, transceiver1, receiver1, 
                                measurement_step, 4e-6)
    
    simulation_runner = SimulationRunner(model)

    # simulation_runner.run_simulation(measurement_number)
    simulation_runner.merge_files(True)

if __name__ == "__main__":
    main()