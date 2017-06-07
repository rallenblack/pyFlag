#! /usr/bin/env python

# Simple functions to read covariance FITS files and do initial processing

import pyfits
import numpy as np
import os.path

# Arguments
data_dir = '/lustre/projects/flag'
proj_id = 'AGBT16B_400'
session = '01'
tstamp = '2017_05_25_01:53:00'

# Constants
BANKS = ['A', 'B', 'C', 'D', \
         'E', 'F', 'G', 'H', \
         'I', 'J', 'K', 'L', \
         'M', 'N', 'O', 'P', \
         'Q', 'R', 'S', 'T']
column = 'DATA'

# Create covariance slicing map
Nele = 64
Nbin = 25
Nsamp = 4000

Nbaselines_tot = (Nele/2 + 1)*Nele
RIdx = (Nbaselines_tot)*np.ones((Nele,Nele))
cnt = 0
for i in range(0,Nele-1,2):
    for j in range(0,i+1,2):
        for ii in range(0,2):
            for jj in range(0,2):
                if ii == 0 and jj == 1 and i == j:
                    RIdx[i+ii, j+jj] = Nbaselines_tot
                else:
                    RIdx[i+ii, j+jj] = cnt
                    
                cnt = cnt + 1

RIdx = RIdx.flatten(1)
RIdx = RIdx.astype(int)

# Read in data and restructure
for bank in BANKS:
    filename = "%s/%s_%s/BF/%s%s.fits" % (data_dir, proj_id, session, tstamp, bank)
    if os.path.isfile(filename):
        hdulist = pyfits.open(filename)
        bintable = hdulist[1]
        data = bintable.data.field(column)

        Ncov = bintable.header['naxis2']
        R = np.zeros((Nele, Nele, Nbin, Ncov), 'complex64')
        for t in range(0, Ncov):
            r = data[t]
            for b in range(0, Nbin):
                b_off = Nbaselines_tot*b
                slices = range(b_off, b_off + Nbaselines_tot)
                rb = np.hstack((r[slices], 0));
                Rb = rb.take(RIdx).reshape(Nele, Nele)
                tmp = Rb + (Rb.transpose() - np.diag(np.diag(Rb.conj())))
                tmp = tmp*(1/(Nsamp - 1));
                
                R[:,:,b,t] = tmp






