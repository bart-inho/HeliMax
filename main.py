# This program is used to run the gprMax simulation applied to glaciology.
from services.folder_init import InitializeFolders
from models.model_generation_logic import ModelGenerationLogic
from simulations.simulation_runner import SimulationRunner
from simulations.simulation_plot_profile import PlotProfile
import argparse
from tqdm import tqdm  # Import tqdm
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count, current_process

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', action='store_true', help='run the simulation')
    parser.add_argument('--model', action='store_true', help='create the model')
    parser.add_argument('--merge', action='store_true', help='merge the simulation files')
    parser.add_argument('--plot', action='store_true', help='plot the simulation')
    parser.add_argument('--rough', action='store_true', help='rough bedrock')
    parser.add_argument('--name', type=str, help='Path to input and output files', required=True)
    parser.add_argument('--gpus', type=str, help='Comma-separated list of GPU IDs to use', default='0')

    args = parser.parse_args()

    # Initialize folders
    model_name    = 'model'
    path_to_files = args.name
    InitializeFolders.check_and_create_directories(path_to_files)
    
    antenna_spacing = 4  # Change antenna spacing in [m] here

    dis = 0.06
    measurement_number = 200 # number of traces

    x_m = 60
    y_m = 10
    z_m = 100

    measurement_step = (x_m-7.5) / measurement_number
    print(measurement_step)

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
                                        antenna_x+(idx*measurement_step), antenna_y, antenna_z,
                                        measurement_step,
                                        args) for idx in range(measurement_number)]
            
            # Process the futures as they complete (to maintain order, if necessary)
            for future in tqdm(concurrent.futures.as_completed(futures), total=measurement_number, desc='Creating Models'):
                result = future.result()  # result returned from create_model
                
    if args.run:
        gpu_ids = [int(gpu) for gpu in args.gpus.split(',')]

        # Prepare arguments for each simulation
        total_gpus = len(gpu_ids)
        simulation_args = [(args.name, 'model', idx, gpu_ids[idx % total_gpus]) for idx in range(200)]

        # Use multiprocessing Pool to run simulations in parallel
        with Pool(processes=total_gpus) as pool:
            list(tqdm(pool.imap(SimulationRunner.run_simulation, simulation_args), total=len(simulation_args)))

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