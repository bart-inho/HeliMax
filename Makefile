gprMax=~/scratch/gprMax# PATH to gprMax env
helico=${gprMax}/helico-gprMax/inout_files# PATH to helico-gprMax
init:
	python ${gprMax}/helico-gprMax/InitSimulation.py
run: 
	python RunSimulation.py
plot:
	python PlotSimulation.py
clean:
	rm inout_files/*.h5 inout_files/*.txt inout_files/*.in inout_files/*.out