
    # # Run simulation
    # if args.run:
    #     simulation_runner.run_simulation(1)
    
    # # run a command line to delete files
    # os.system('rm -r inout_files_noshield/*.in inout_files_noshield/*.txt inout_files_noshield/*.h5 ')

    # antenna_x += measurement_step

    # # Plot profile
    # if args.plot:
    #         # Initialize SimulationModel

    #     simulation_runner = SimulationRunner(model)
    #     simulation_runner.merge_files(True)
    #     # Generate model
    #     model = SimulationModel(model_name, 
    #                             45, 10, 100, 
    #                             [dis, dis, dis], # Change discretisation if needed here
    #                             [freespace, glacier, bedrock, metal, shield], # Change name of materials here
    #                             inout_files)
    #     # simulation_runner.merge_files(True)
    #     plot_profile = PlotProfile(model.path + model.name + '_merged.out', 'Ey')
    #     plot_profile.get_output_data()
    #     plot_profile.plot()