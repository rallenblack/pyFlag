import pyfits
import numpy as np
import os.path

# Should eventually be a function
# def get_antenna_positions(self, fits_file, use_radec)

data_dir = '/lustre/projects/flag'
proj_id = 'AGBT16B_400'
session = '01'
tstamp = '2017_05_25_01:53:00'

bank = 'A'

filename = "%s/%s_%s/BF/%s%s.fits" % (data_dir, proj_id, session, tstamp, bank)

hdulist  = pyfits.open(filename)
bintable = hdulist[1]
tbdata     = bintable.data.field('DMJD') # Or the 0th field (field(0))

dmjd_idx = 1
ra_idx   = 2
dec_idx  = 3
mnt_az_idx  = 4
mnt_el_idx  = 5
obsc_az_idx = 9
obsc_el_idx = 10

dmjd = tbdata[ra_idx]

# ra and dec
ra  = tbdata[ra_idx]
dec = tbdata[dec_idx]

use_radec = 1

if use_radec:
    az_off = ra
    el_off = dec
else: 
    mnt_az = tbdata[mnt_az_idx]
    mnt_el = tbdata[mnt_el_idx]

    obsc_az = tbdata[obsc_az_idx]
    obsc_el = tbdata[obsc_el_idx]

    az_off = mnt_az - obsc_az
    el_off = mnt_el - obsc_el
