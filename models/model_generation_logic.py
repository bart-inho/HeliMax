from services.file_service import FileService
from models.simulation_model import SimulationModel
from models.material import Material

class ModelGenerationLogic:
    def model_generation_logic(idx, 
                    model_name, 
                    x_m, y_m, z_m, dis, 
                    antenna_spacing, 
                    rope_length, 
                    path_to_files, 
                    antenna_x, antenna_y, antenna_z,
                    measurement_step,
                    args):

        # Initialize Materials
        # Change the material names in the "Material" class 
        freespace = Material(1. , 0.   , 1., 0., 'freespace') # Free space
        glacier   = Material(3.2, 5.e-8, 1., 0., 'glacier'  ) # Glacier
        bedrock   = Material(5. , 1.e-2, 1., 0., 'bedrock'  ) # Bedrock
        metal     = Material(1. , 'inf', 1., 0., 'metal'    ) # Helico
        shield    = Material(6. , 1.e-2, 1., 0, 'shield'    ) # Shield

        # Initialize SimulationModel
        if idx == 0:
            model_name_it = model_name
        elif idx > 0:
            model_name_it = model_name + str(idx)

        # Generate model
        model = SimulationModel(model_name_it, 
                                x_m, y_m, z_m, 
                                [dis, dis, dis], # Change discretisation if needed here
                                [freespace, glacier, bedrock, metal, shield], # Change name of materials here
                                path_to_files)
        
        # Generate base model
        model.generate_base_glacier()
        model.generate_curved_bedrock_glacier([-10, 5, -200], # center of the curvature [m]
                                            100,            # radius of the curvature [m]
                                            args.rough)
        
        model.add_shield(antenna_x, antenna_y, antenna_z, dis, antenna_spacing, dis)

        # model.add_3D_oval_shape([antenna_x , antenna_y, antenna_z - rope_length], # center of the curvature [m]
        #                         [10, .5, .5],            # radius of the curvature [m]])
        #                         dis*20)
        # model.add_3D_oval_shape([antenna_x + 3.5, antenna_y, antenna_z - rope_length - 1.5], # center of the curvature [m]
        #                         [20, .1, .1],            # radius of the curvature [m]])
        #                         dis*100)
        # model.add_3D_oval_shape([antenna_x + antenna_spacing - 1, antenna_y, antenna_z - rope_length], # center of the curvature [m]
        #                         [5, 2, 2],            # radius of the curvature [m]])
        #                         dis*3)
        
        transceiver1 = [antenna_x, # 25 cells of buffer (20 minimum)    
                        antenna_y,
                        antenna_z]
        
        receiver1    = [antenna_x + antenna_spacing, # 25 cells of buffer (20 minimum)
                        antenna_y,
                        antenna_z]
            
        #Plot initial model
        model.plot_initial_model(transceiver1, receiver1)

        # Call FileService to write files
        FileService.write_materials_file(model.path + model.name + '_materials', 
                                        model.materials)
        
        FileService.write_h5_file(model.path + model.name + '_h5', 
                                model)

        FileService.write_input_file(model, 
                                    path_to_files+model_name_it, 
                                    path_to_files+model_name_it + '_materials', 
                                    path_to_files+model_name_it + '_h5', 
                                    25e6,   # Change frequency in Hz here
                                    transceiver1, receiver1, 
                                    measurement_step, 
                                    1000e-9) # Change time window in s here