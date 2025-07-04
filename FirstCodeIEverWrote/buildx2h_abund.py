#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 22 11:59:13 2018

@author: ''
"""

#Author AndrewAmmons

#Normalize GIM data to ACE/SWICS 2 hour time bins.

import numpy as np
import aswics2python_unknown2dnum as apu 

gim_mom = np.load('/Users/''/Desktop/pythonstuff/gim_mom_sav.npy')
aswix = np.load('/Users/''/Desktop/pythonstuff/aswics_sav.npy')
swepam = np.load('/Users/''/Desktop/pythonstuff/swepam_sav.npy')

#Define Genesis start and end times (day number 699 to dnum 1552).
d_start = round(min(gim_mom['dnum']))
d_end = round(max(gim_mom['dnum']))

#Select ACE data for Genesis period.
abundn = aswix[np.where((aswix['dnum'] >= d_start) & (aswix['dnum'] <= d_end))]
swep = swepam[np.where((swepam['dnum'] >= d_start) & (swepam['dnum'] <= d_end))]

lngth = len(abundn) #Assign array length.
regime = np.zeros((lngth,),dtype=[('dnum','d'),('v_p','d'),('n_p','d'),('t_p','d'),('he2p','d'),('flag', 'i2')])

#Average GIM data to two hour values and store in regime struct.

for i in range(len(abundn)-1):
    #find the GIM data >= the current abundn time and
    #< the next one:
    drp = np.where((swep['dnum'] >= abundn['dnum'][i]) & (swep['dnum'] < abundn['dnum'][i+1]) & (swep['prot_spd'] > 0.0) 
                    & (swep['prot_den'] > 0.0) & (swep['prot_temp'] > 0.0))
    if np.size(drp) > 0:
        regime['dnum'][i] = abundn['dnum'][i]
        regime['v_p'][i] = (np.average(swep['prot_spd'][drp]))
        regime['n_p'][i] = (np.average(swep['prot_den'][drp]))
        regime['t_p'][i] = (np.average(swep['prot_temp'][drp]))
        regime['he2p'][i] = (np.average(swep['he42p'][drp]))
        regime['dnum'][i+1] = abundn['dnum'][i+1]

# open regime time files: 
c_h = np.loadtxt('/Users/''/Desktop/pythonstuff/GNS_CH.txt',skiprows=2)
cme = np.loadtxt('/Users/''/Desktop/pythonstuff/GNS_CME.txt',skiprows=2)
i_s = np.loadtxt('/Users/''/Desktop/pythonstuff/GNS_IS.txt',skiprows=2)

#Fit regime numbers to data and add flag to regime struct array: 

for i in range(len(c_h)):
    ig = ((regime['dnum'] >= apu.unknown2dnum(c_h[i][:2])+(2./24)) & (regime['dnum'] <= apu.unknown2dnum(c_h[i][2:4])))
    regime['flag'][ig] = 2 
for i in range(len(cme)):
    ig = ((regime['dnum'] >= apu.unknown2dnum(cme[i][:2])+(2./24)) & (regime['dnum'] <= apu.unknown2dnum(cme[i][2:4])))
    regime['flag'][ig] = 1
for i in range(len(i_s)):
    ig = ((regime['dnum'] >= apu.unknown2dnum(i_s[i][:2])+(2./24)) & (regime['dnum'] <= apu.unknown2dnum(i_s[i][2:4])))
    regime['flag'][ig] = 3
    
############################################################################################################
#normalize abundn data to hydrogen:

    
o2h = regime['he2p'][np.where(regime['he2p'] > 0.0)]/abundn['he2o'][np.where(regime['he2p'] > 0.0)]
abundn = abundn[np.where(o2h)] #only get abundn data where value is a number (not divided by zero or null)
names = ['he2o','c2o','n2o','ne2o','mg2o','si2o','s2o','fe2o']

for name in names:
    abundn[name] = abundn[name]*o2h
    print abundn[name]
    
    
regime = regime[np.where(regime['he2p'] > 0.0)] #only get regime data where regime has helium to proton data.

#Note that abundn_struct and regime_struct have been renamed here:
np.save('/Users/''/Desktop/pythonstuff/abund2h_struct',abundn)
np.save('/Users/''/Desktop/pythonstuff/regime2h_struct',regime)
