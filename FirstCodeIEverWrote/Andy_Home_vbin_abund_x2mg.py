# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 12:40:36 2017

@author: andy
"""

import numpy as np
import matplotlib.pyplot as plt
#import aswics2python_unknown2dnum2_mod7 as apu

path = '/home/andy/Desktop/pythonstuff/'
abundn = np.load(path + 'abund_struct.npy')
regime = np.load(path + 'regime_struct.npy')

v_start = 187.5
v_end = 1812.5
v_step = 6.25

sdnum = 699
ednum = 1552

nv = int((v_end - v_start)/v_step)

ivel = [(n*v_step) + v_start for n in range(nv)]

nregime = 3
nspecies = range(30)

specnm = ['he2o','c2o','n2o','ne2o','mg2o','si2o','s2o','fe2o','nhe']
vthernm = ['vthhe','vthc5','vthn5','vthne8','vthmg10','vthsi8','vths8','vthfe10','vtho6']
vnm = ['vhe','vc5','vn5','vne8','vmg10','vsi8','vs8','vfe10','vo6']
vth_id = ['vthhe','vthc5','vtho6','vtho6','vtho6','vtho6','vtho6','vthfe10','vtho6']

fip = [3,4,5,6,7,8,9,10]


nfrac = len(fip)

f_vdist = np.zeros((nv,nfrac+1,nregime+1))
n_samp_v = np.zeros((nv,nfrac+1,nregime+1))
n_samp = np.zeros((nfrac+1,nregime+1))
mean_vth = np.zeros((nv,nfrac+1,nregime+1))
voa = np.zeros((nv,nregime+1))
vfea = np.zeros((nv,nfrac+1,nregime+1))

for reg in range(4):
    
    for spec,vthnm,v,vnum in zip(specnm,vthernm,vnm,range(len(vnm))):
    
        for iv in range(1,nv):
            
            
                
            if reg != 3:
                    
                
                abund = abundn[np.where((abundn[v] >= ivel[iv-1]) & (abundn[v] < ivel[iv]) & (abundn[v] > 0.0)
                & (abundn['he2o'] > 0.0) & (abundn[vthnm] > 0.0) & (regime['flag'] == reg + 1) & (abundn['dnum']
                >= sdnum) & (abundn['dnum'] <= ednum) & (abundn['nhe'] > 0.0) & (abundn['mg2o'] > 0.0))]
                
                abund_oxy = abundn[np.where((abundn['vo6'] >= ivel[iv-1]) & (abundn['vo6'] < ivel[iv]) & (abundn['nhe'] > 0.0) & 
                (abundn['he2o'] > 0.0 ) & (regime['flag'] == reg+1) & (abundn['dnum'] >= sdnum) & (abundn['dnum'] <= ednum)
                & (abundn['vtho6'] > 0.0) & (abundn['mg2o'] > 0.0))]
                
                
            if reg == 3:
                
                abund = abundn[np.where((abundn[v] >= ivel[iv-1]) & (abundn[v] < ivel[iv]) & (abundn[v] > 0.) & 
                (abundn['he2o'] > 0.) & (abundn[vthnm] > 0.) & (abundn['dnum'] >= sdnum) & (abundn['dnum'] <= ednum)\
                & (abundn['nhe'] > 0.0) & (abundn['mg2o'] > 0.0))]
                
                abund_oxy = abundn[np.where((abundn['vo6'] >= ivel[iv-1]) & (abundn['vo6'] < ivel[iv]) & (abundn['nhe'] > 0.0) & 
                (abundn['he2o'] > 0.0 ) & (abundn['dnum'] >= sdnum) & (abundn['dnum'] <= ednum)& (abundn['vtho6'] > 0.0) & (abundn['mg2o'] > 0.0))]
                

            if (np.size(abund) > 0) & (np.size(abund_oxy) > 0):
                
                if vnum < 8:

                    n_samp[vnum,reg] += len(abund)
                    n_samp_v[iv,vnum,reg] += len(abund)
    
                    nvx = np.array([np.sum(((((abund[spec]/abund['mg2o']) * n * abund['nhe'])/(abund['he2o'])) * ((1.0/(abund[vthnm]*np.sqrt(2.0*np.pi))))) * 
                        np.exp(-((n - abund[v])**2.)/(2.0*(abund[vthnm]**2.)))*v_step) for n in ivel])
                    
                    f_vdist[:,vnum,reg] += (nvx) * (2. * 3600. * 1e5)  
                    
                else:
                    
                    n_samp[8,reg] += len(abund_oxy)
                    
                    nvox = np.array([np.sum(((abund_oxy['nhe'] * n)/abund_oxy['he2o']) * ((1./(abund_oxy['vtho6'] * np.sqrt(2.*np.pi)))) * 
                        np.exp(-((n - abund_oxy['vo6'])**2.)/(2. * (abund_oxy['vtho6'])**2.)) * v_step) for n in ivel])
                   
                    f_vdist[:,vnum,reg] += (nvox) * (2. * 3600. * 1e5)
                
                
          

for iv in range(nv):
    f_vdist[iv,:,nregime] = f_vdist[iv,:,nregime]*(852.83/(n_samp[:,nregime]/12.0))
    
    #Low Speed:

    f_vdist[iv,:,2] = f_vdist[iv,:,2]*(333.67/(n_samp[:,2]/12.0))
    
    #High Speed:
    
    f_vdist[iv,:,1] = f_vdist[iv,:,1]*(313.01/(n_samp[:,1]/12.0))
    
        #cme:
    f_vdist[iv,:,0] = f_vdist[iv,:,0]*(193.25/(n_samp[:,0]/12.0))
         
fl_v = np.zeros(((nv/4)+1,nfrac+1,nregime+1))
jvel = np.zeros((nv/4))

for iv in range(0,nv,4):
    jv = int(iv)/4
    jvel[jv] = ivel[iv+2]
    fl_v[jv,:,:]=sum(f_vdist[iv:iv+4,:,:],0)
        
for ireg in range(nregime+1):
    for ifrac in range(nfrac+1):
        fl_v[int(nv/4),ifrac,ireg] = sum(fl_v[0:int(nv/4),ifrac,ireg])

#template for a tidy way to print fluences as a table (this one is for the bulk fluences)
np.save('/home/andy/Desktop/pythonstuff/mgf_vdist',f_vdist)
np.save('/home/andy/Desktop/pythonstuff/mgfl_v',fl_v)
np.set_printoptions(linewidth = 120, formatter={'float': '{:10.2e}'.format})    
for i in range(int(nv/4)):
    print '{:6d}'.format(int(jvel[i])),fl_v[i,:,3]#/fl_v[int(nv/4),:,3]

#plot the differential fluences for each regime
plt.figure(1)
plt.plot(jvel,fl_v[0:65,0,0],'r')
plt.plot(jvel,fl_v[0:65,0,1],'b')
plt.plot(jvel,fl_v[0:65,0,2],'g')
plt.plot(jvel,fl_v[0:65,0,3],color='orange')


#plot the o7+/o6+ abundance ratios

plt.figure(2)
plt.plot(jvel,fl_v[0:65,:,0],'r')
plt.yscale('log')
plt.plot(jvel,fl_v[0:65,:,1],'b')
plt.yscale('log')
plt.plot(jvel,fl_v[0:65,:,2],'g')
plt.yscale('log')
plt.plot(jvel,fl_v[0:65,:,3],color='orange')
plt.yscale('log')                 
              
                


