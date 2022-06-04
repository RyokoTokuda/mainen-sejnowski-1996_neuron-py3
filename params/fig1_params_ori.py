#!/usr/bin/env python3.9

"""
original: https://github.com/felix11h/mainen-sejnowski-1996_neuron-python
some values of parameters are changed referencing 
"Signal integration on the dendrites of a pyramidal neuron model", 
L.Xiumin, (2014), cognitive neurodynamics, 8(1), 81-85
"""
ra        = 150.
global_ra = ra
rm        = 30000.
c_m       = 0.75
cm_myelin = 0.04
g_pas_node = 0.02

v_init    = -70.
temp = 37.

Ek = -90.
Ena = 60.

# conductance (pS/um^2)
gna_dend = 20. 
gna_node = 30000. # nodes of Ranvier
gna_soma = gna_dend

gkv_axon = 2000.
gkv_soma = 200.
gkv_hillock = 3000 # axon hillock and initial segment
gkv_node = 0 # nodes of Ranvier

gca = 0.3
gkm = 0.1
gkca = 3.

gca_soma = gca
gkm_soma = gkm
gkca_soma = gkca

# ---- spine params ----

spine_dens = 1.
spine_area = 0.83 # um


# ---- axon params ----

n_axon_seg = 5

iseg_L = 15.
iseg_nseg = 5

hill_L = 10.
hill_nseg = 5

myelin_nseg = 5
myelin_L = 100.

node_nseg = 1
node_L = 1.

# ---- stim ----

st_dur = 900.
st_del = 5.


# ---- simulation ----

tstop = 1000
dt = 0.025