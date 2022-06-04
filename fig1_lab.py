#!/usr/bin/env python3.9

import sys
sys.path.append('/usr/local/lib/python3.9/site-packages')
import pickle 
from neuron import h

import matplotlib as mpl
mpl.use('Agg')
import pylab as pl
from fig1_core import *
from params.fig1_params_ori import *


def fig1_make(cell_path, st_amp, label, spines=True):

    soma, dendrite, axon = load_3dcell(cell_path, spines)

    # --- stimulation ---

    st = h.IClamp(soma(0.5))
    st.dur = st_dur
    st.delay = st_del
    st.amp = st_amp


    t = h.Vector()        
    v_soma = h.Vector()   
    t.record(h._ref_t)
    v_soma.record(soma(0.5)._ref_v)
 
    h.dt = dt

    def initialize():
        h.finitialize(v_init)
        h.fcurrent()

    def integrate():
        while h.t<tstop:
            h.fadvance()

    def run():
        initialize()
        integrate()

    run()


    # --- data saving --- 

    with open('data/%s_python.p' % label, 'wb') as f:
        pickle.dump((list(t),list(v_soma)), f)

    # --- plotting ---

    pl.plot(t,v_soma)
    pl.savefig('data/img/%s_python.png' % label)


if __name__=='__main__':
    fig1_make(sys.argv[1], float(sys.argv[2]), sys.argv[3], spines=bool(int(sys.argv[4])))