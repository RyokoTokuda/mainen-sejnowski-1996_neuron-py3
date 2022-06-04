#!/bin/bash

x86_64/special demofig1_rec_ori.hoc

python3 plot_from_hoc_data.py data/fig1_L5_pyramid_hoc.dat

python3 fig1_lab.py "cells/j4a.hoc" 0.2 "fig1_L5_pyramid" 1

python3 test_data.py data/fig1_L5_pyramid_hoc.dat data/fig1_L5_pyramid_python.p