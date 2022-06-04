# mainen-sejnowski-1996_neuron-py3

## About this project
Original publication: Z. F. Mainen and T. J. Sejnowski (1996) Influence of dendritic structure on firing pattern in model neocortical neurons. Nature 382: 363-366.

Original project: https://github.com/felix11h/mainen-sejnowski-1996_neuron-python.git , which was adapted from the implementation found on [ModelDB](https://senselab.med.yale.edu/modeldb/showModel.cshtml?model=2488).

This project is mainly for running the above original program with python3.  
I modified the scripts written by python2 for python3.

## Environment
- Python 3.9
- NEURON 8.0.0

## How to run
1. Run this code to compile .mod files.
```
nrnivmodl
```

2. Execute `run_ori.sh`. 
   It will 
   - run a simulation with hoc main script
   - make a plot from the result of hoc program
   - run a simulation with python3 main script
   - execute a test to check whether the result from hoc project and that from python3 corresponds to each other
