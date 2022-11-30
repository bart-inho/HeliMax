gprMax=~/scratch/gprMax# PATH to gprMax env
helico=${gprMax}/helico-gprMax/inout_files# PATH to helico-gprMax
in:
	python ${gprMax}/helico-gprMax/GenerateModels.py
run: 
	python -m gprMax inout_files/bedrock_model.in -n 40 -gpu
merge:
	python -m tools.outputfiles_merge ${helico}/bedrock_model --remove-files
plot:
	python -m tools.plot_Bscan ${helico}/bedrock_model_merged.out Ez