gprMax=C:\Users\bart\Documents\prog\Python\gprMax# PATH to gprMax env
helico=${gprMax}\helico-gprMax\inout_files
in:
	python ${gprMax}\helico-gprMax\GenerateModels.py
run: 
	python -m gprMax ${helico}\bedrock_model.in -n 30 -gpu