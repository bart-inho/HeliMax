# This program is used to run the gprMax simulation applied to glaciology.
from services.folder_init import InitializeFolders
from models.model_generation_logic import ModelGenerationLogic
from simulations.simulation_runner import SimulationRunner
from simulations.simulation_plot_profile import PlotProfile
import argparse
from tqdm import tqdm  # Import tqdm
from concurrent.futures import ThreadPoolExecutor
import threading

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', action='store_true', help='run the simulation')
    parser.add_argument('--model', action='store_true', help='create the model')
    parser.add_argument('--merge', action='store_true', help='merge the simulation files')
    parser.add_argument('--plot', action='store_true', help='plot the simulation')
    parser.add_argument('--rough', action='store_true', help='rough bedrock')
    args = parser.parse_args()

    # Initialize folders
    model_name    = 'model'
    path_to_files = 'inout_files_noshield/'
    InitializeFolders.check_and_create_directories(path_to_files)
    
    antenna_spacing = 4  # Change antenna spacing in [m] here

    dis = 0.06
    measurement_number = 1 # number of traces
    measurement_step = (45-7.5) / measurement_number
    print(measurement_step)

    x_m = 45
    y_m = 10
    z_m = 100

    antenna_x = round(30 * dis) # 30 cells of buffer (20 minimum
    antenna_y = round(y_m/2)
    antenna_z = round(20)

    rope_length = 15 # length of the rope in [m]

    if args.model:
        with ThreadPoolExecutor(max_workers=24) as executor:
            import concurrent.futures
            futures = [executor.submit(ModelGenerationLogic.model_generation_logic, idx, 
                                        model_name, 
                                        x_m, y_m, z_m, 
                                        dis, antenna_spacing, 
                                        rope_length, 
                                        path_to_files, 
                                        antenna_x, antenna_y, antenna_z,
                                        measurement_step,
                                        args) for idx in range(measurement_number)]
            
            # Process the futures as they complete (to maintain order, if necessary)
            for future in tqdm(concurrent.futures.as_completed(futures), total=measurement_number, desc='Creating Models'):
                result = future.result()  # result returned from create_model
                
    if args.run:
        # Create a queue to manage GPU availability
        gpu_queue = SimulationRunner.create_gpu_queue(1)  # Assuming you have 8 GPUs
        
        threads = []
        for idx in range(measurement_number):
            if idx == 0:
                idx = ''
            # Wait for a GPU to become available
            t = threading.Thread(target=SimulationRunner.run_simulation, args=(path_to_files, model_name, idx, gpu_queue))
            t.start()
            threads.append(t)
        
        # Wait for all threads to complete
        for t in threads:
            t.join()

        print("All simulations completed.")

    if args.merge:
        # Merge the files
        SimulationRunner.merge_files(True, path_to_files, model_name)

    if args.plot:
        # Plot the simulation
        plot_profile = PlotProfile(path_to_files + '_merged.out', 'Ey')
        plot_profile.get_output_data()
        plot_profile.plot()
        
if __name__ == "__main__":
    main()