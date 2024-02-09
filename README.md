# HeliMax

This repository contains a Python program designed to run gprMax simulations specifically tailored for glaciology research. It utilizes ground-penetrating radar (GPR) simulation to understand and analyze sub-glacial features, including bedrock roughness and ice thickness. The program supports model creation, simulation execution, file merging, and result plotting, with the capability to specify GPU usage for computational efficiency.

## Features

- **Model Generation**: Dynamically generates simulation models based on user-defined parameters.
- **Simulation Execution**: Runs simulations using specified GPUs to leverage computational resources effectively.
- **File Merging**: Merges simulation output files for consolidated analysis.
- **Result Plotting**: Plots the simulation results for visual analysis.

## Requirements

- Python 3.x
- gprMax
- tqdm
- multiprocessing

Please ensure you have gprMax installed and configured correctly on your system. You can find installation instructions for gprMax at [gprMax's GitHub page](https://github.com/gprMax/gprMax).

## Installation

Clone this repository to your local machine, make sure that it's in you folder `gprMax`:

```bash
git clone https://github.com/bart-inho/helimax.git
cd helimax
```

Ensure you have the necessary Python dependencies installed:

```bash
pip install -r requirements.txt
```

## Usage

The program is executed via the command line, offering several options to control its operation:

- `--run`: Execute the simulation.
- `--model`: Generate the simulation model.
- `--merge`: Merge simulation output files.
- `--plot`: Plot the simulation results.
- `--name`: Specify the path for input and output files. This argument is required.
- `--gpus`: Specify comma-separated GPU IDs to use for the simulation (e.g., `0,1,2,3`).

### Examples

Generate a model:

```bash
python main.py --model --name path/to/files
```

Run simulations using GPUs 0 and 1:

```bash
python main.py --run --name path/to/files --gpus 0,1
```

Merge simulation files and plot results:

```bash
python main.py --merge --plot --name path/to/files
```

## Customization

You can customize the simulation parameters such as antenna spacing, measurement number, and dimensions directly within the script. For more advanced configurations, edit the model generation logic as needed.

## Contributing

Contributions to improve the program or address issues are welcome. Please feel free to submit a pull request or open an issue.

## Acknowledgments

This project utilizes [gprMax](https://github.com/gprMax/gprMax), an open-source project for simulating GPR. We acknowledge the developers and contributors of gprMax for their valuable work.