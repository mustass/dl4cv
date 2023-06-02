# Deep Learning for Computer Vision

## Repo structure
This repo takes advantage of two frameworks: (1) Hydra for configs management and (2) Pytorch Lightning for improving our lives when colaborating and running experiments on different hardware. 

The particular approach of this repo is heavily inspired by [https://youtu.be/w10WrRA-6uI].

## Getting started 

1. Create a virtual environment the way you are used to (conda, venv, pyenv, whatever). 

*On HPC:*

It's very important that you load a new-ish python version before running the getting started script. Do this by: 
```
module load python3/3.10
module load cuda/11.7
```

2. Set environment variables (!!):
```{bash}
export PATH_TO_VENV=#path to your venv
```

3. Run the bash script from the root folder:
```{bash}
./get_started.sh
```

This will:
1. Create a virtual environment with the name `venv` in the parent folder. *If you want the name or location to be different, it's up to you. Just remember that the path to the environment is used in the `train_dtu_hpc.sh` script. So adjust accordingly.*
2. Install the package in editable mode with all requirements
3. Download the dataset and extract it

You can further install the requirements for developing the package:
```{bash}
pip install -r requirements-dev.txt
```

## Contribution guide

This repo has protection on the ``main`` branch. Therefore any contribution has to go through a Pull Request. 

Make sure to run ``make`` in the root directory and push changes before creating a Pull Request. This will require you to have the packages in `requriements-dev.txt` installed.

## Running things and stuffs

### Preprocessing of the LJ dataset

To run conditional training or/and evaluation we need to create spectrograms.
```{bash}
python3 scripts/preprocess.py
```