# This program is used to run the gprMax simulation applied to glaciology.
from services.file_service import FileService
from services.folder_init import InitializeFolders
from models.simulation_model import SimulationModel
from models.material import Material
from simulations.simulation_runner import SimulationRunner
from simulations.simulation_plot_profile import PlotProfile  
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', action='store_true', help='run the simulation')
    parser.add_argument('--plot', action='store_true', help='plot the simulation')
    parser.add_argument('--rough', action='store_true', help='rough bedrock')
    args = parser.parse_args()

    # Initialize folders
    InitializeFolders.check_and_create_directories()

    # Initialize Materials
    # Change the material names in the "Material" class 
    freespace = Material(1. , 0.   , 1., 0., 'freespace') # Free space
    moraine   = Material(8., 1.e-3, 1., 0., 'moraine'   ) # Moraine
    molasse   = Material(5., 5.e-4, 1., 0., 'molasse'   ) # Molasse
    metal     = Material(1., 'inf', 1., 0., 'metal'     ) # Helico
    
    # Initialize SimulationModel
    model_name    = 'test_moraine'
    inout_files   = 'inout_files/'
    path_to_files = inout_files + model_name

    # Generate model
    model = SimulationModel(model_name, 
                            20, 5, 20, 
                            [0.025, 0.025, 0.025], # Change discretisation if needed here
                            [freespace, moraine, molasse, metal], # Change name of materials here
                            inout_files)
    
    # Generate base model
    model.generate_base_vignes()
    model.generate_curved_molasse([-10, round(model.y_size/2), -800], # center of the curvature [m]
                             35,                  # radius of the curvature [m]
                             args.rough)

    measurement_number = 30 # number of traces
    antenna_spacing    = 1  # Change antenna spacing in [m] here
    measurement_step   = model.calculate_measurment_step(measurement_number, 
                                                         antenna_spacing) # Change antenna spacing in m here
    
    # Add antenna positions
    transceiver1 = [25 * model.discrete[0], # 25 cells of buffer (20 minimum)    
                    model.y_size/2        ,
                    model.z_size/10-.5     ]
    
    receiver1    = [25 * model.discrete[0] + antenna_spacing, # 25 cells of buffer (20 minimum)
                    model.y_size/2                          ,
                    model.z_size/10-.5                       ]
        
    #Plot initial model
    model.plot_initial_model(transceiver1, receiver1)

    # Call FileService to write files
    FileService.write_materials_file(model.path + model.name + '_materials', 
                                     model.materials)
    
    FileService.write_h5_file(model.path + model.name + '_h5', 
                              model)

    FileService.write_input_file(model, 
                                path_to_files, 
                                path_to_files + '_materials', 
                                path_to_files + '_h5', 
                                250e6,   # Change frequency in Hz here
                                transceiver1, receiver1, 
                                measurement_step, 
                                400e-9) # Change time window in s here
        
    # Run simulation
    if args.run:
        simulation_runner = SimulationRunner(model)
        simulation_runner.run_simulation(measurement_number)
        simulation_runner.merge_files(True)
        
    # Plot profile
    if args.plot:
        plot_profile = PlotProfile(model.path + model.name + '_merged.out', 'Ey')
        plot_profile.get_output_data()
        plot_profile.plot()

if __name__ == "__main__":
    main()