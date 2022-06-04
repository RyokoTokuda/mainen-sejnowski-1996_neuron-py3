#!/usr/bin/env python3.9

from ast import Try
import sys

from yaml import load
sys.path.append('/usr/local/lib/python3.9/site-packages')
from neuron import h

import numpy as np
# from itertools import izip # this is for python2x, and izip is replaced to zip in python3
from params.fig1_params_ori import *

def taper_diam(sec,zero_bound,one_bound):
    ''' 
    mctavish 2010 
    http://www.neuron.yale.edu/phpbb/viewtopic.php?f=2&t=2131
    '''
    dx = 1./sec.nseg
    for (seg, x) in zip(sec, np.arange(dx/2, 1, dx)):
        seg.diam=(one_bound-zero_bound)*x+zero_bound

"""
call_path: .hoc file
"""

def create_axon(soma):

    soma_compl_area = 0
    for seg in soma:
        soma_compl_area += seg.area() # equal to A in .hoc file
    
    equiv_diam = np.sqrt(soma_compl_area/(4.*np.pi))

    # initial segment between hillock + myelin
    iseg = h.Section(name='iseg')
    iseg.L = iseg_L
    iseg.nseg = iseg_nseg
    iseg.diam = equiv_diam/10. # see Sloper and Powell 1982, Fig.71

    # axon hillock
    hill = h.Section(name='hill')
    hill.L = hill_L
    hill.nseg = hill_nseg
    taper_diam(hill, 4*iseg.diam, iseg.diam)


    # construct myelinated axon with nodes of ranvier
    myelin = [h.Section(name="myelin %d" % i) for i 
              in range(n_axon_seg)]
    for myelin_sec in myelin:
        myelin_sec.nseg = myelin_nseg # each of the 5 sections has 5 segments
        myelin_sec.L = myelin_L
        myelin_sec.diam = iseg.diam

    node = [h.Section(name="node %d" % i) for i 
            in range(n_axon_seg)]
    for node_sec in node:
        node_sec.nseg = node_nseg
        node_sec.L = node_L
        node_sec.diam = iseg.diam*0.75


    # syntax: childsec.connect(parentsec, parentx, childx)
    hill.connect(soma, 0.5, 0)
    iseg.connect(hill, 1 , 0)
    myelin[0].connect(iseg, 1, 0)
    node[0].connect(myelin[0], 1, 0)

    for i in range(n_axon_seg-1):
         myelin[i+1].connect(node[i], 1, 0)
         node[i+1].connect(myelin[i+1], 1 ,0)

    # visualize the topology
    sl = h.SectionList()
    for sec in h.allsec():
        sl.append(sec)

    return myelin, node, hill, iseg


def create_spine(spines, dendritic_only):
    '''
    --- spines: bool (1 or 0)
    '''

    '''
    Based on the "Folding factor" described in
    Jack et al (1989), Major et al (1994)
    note: this assumes active channels are present in spines
    at same density as dendrites 
    '''
    if spines:
        for sec in dendritic_only:
            a = 0.
            for seg in sec.allseg():
                a += seg.area()

            F = (sec.L*spine_area*spine_dens + a)/a

            sec.L = sec.L*F**(2/3.)

            for seg in sec.allseg():
                seg.diam = seg.diam * F**(1/3.)

def init_cell(soma, dendritic, myelin, node, hill, iseg):
    # ---- mechanisms ----

    # passive
    for sec in h.allsec():
        sec.insert('pas')
        sec.Ra = ra
        sec.cm = c_m
        sec.g_pas = 1./rm
        sec.e_pas = v_init

    # exceptions along the axon
    for myelin_sec in myelin:
        myelin_sec.cm = cm_myelin
    
    for node_sec in node:
        node_sec.g_pas = g_pas_node

    # na+ channels
    for sec in h.allsec():
        sec.insert('na')
    for sec in dendritic:
        sec.gbar_na = gna_dend
    for myelin_sec in myelin:
        myelin_sec.gbar_na = gna_dend

    hill.gbar_na = gna_node
    iseg.gbar_na = gna_node

    for node_sec in node:
        node_sec.gbar_na = gna_node

    # kv delayed rectifier channels
    iseg.insert('kv')
    iseg.gbar_kv = gkv_axon

    hill.insert('kv') 
    hill.gbar_kv = gkv_axon

    soma.insert('kv')
    soma.gbar_kv = gkv_soma
    
    # dendritic channels
    for sec in dendritic:
        sec.insert('km')
        sec.gbar_km = gkm

        sec.insert('kca')
        sec.gbar_kca = gkca

        sec.insert('ca')
        sec.gbar_ca = gca

        sec.insert('cad')
    
    soma.gbar_na = gna_soma

    #soma.insert('km')
    soma.gbar_km = gkm_soma

    #soma.insert('kca')
    soma.gbar_kca = gkca_soma

    #soma.insert('ca')
    soma.gbar_ca = gca_soma

    for sec in h.allsec():
        if h.ismembrane('k_ion', sec = sec):
            sec.ek = Ek
        
    for sec in h.allsec():
        if h.ismembrane('na_ion', sec = sec):
            sec.ena = Ena
            h.vshift_na = -5 # seems to be necessary for 3d cells to shift Na kinetics -5 mV
    
    for sec in h.allsec():
        if h.ismembrane('ca_ion', sec = sec):
            sec.eca = 140
            h.ion_style("ca_ion",0,1,0,0,0, sec = sec) # need "sec=sec"
            h.vshift_ca = 0


def load_3dcell(cell_path, spines):
    h('forall delete_section()')

    # ---- conditions ----

    h.celsius = temp

    # ---- soma & dendrite ----

    h.xopen(cell_path)

    soma = h.soma
    dendritic = [] # section list

    # segment lengths should be not longer than 50um
    # contains soma!
    for sec in h.allsec():
        diam = sec.diam
        n = sec.L/50.+1
        sec.nseg = int(n) # needed in Python, automatic in hoc
        if h.n3d(sec=sec) == 0:
            sec.diam = diam
        dendritic.append(sec)


    dendritic_only = [] # exclude the soma
    for sec in dendritic:
        if sec != h.soma:
            dendritic_only.append(sec)

    # make sure to exclude the soma
    assert len(dendritic)-1 == len(dendritic_only)

    create_spine(spines, dendritic_only)

    myelin, node, hill, iseg = create_axon(soma)

    init_cell(soma, dendritic, myelin, node, hill, iseg)

    axon = [iseg, hill, myelin, node]


    return soma, dendritic_only, axon


if __name__=='__main__':
    cellpath = sys.argv[1]
    spines = bool(int(sys.argv[2]))
    load_3dcell(cellpath,spines)
