gprMax=~/scratch/gprMax# PATH to gprMax env
helico=${gprMax}/helico-gprMax/inout_files# PATH to helico-gprMax
in:
	python ${gprMax}/helico-gprMax/InitSimulation.py
run: 
	python RunSimulation.py
plot:
	python PlotSimulation.py