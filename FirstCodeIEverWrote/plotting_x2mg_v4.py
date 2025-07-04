#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 13:22:36 2017

@author: 
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 20:48:25 2017

@author: andy
"""

import numpy as np
from matplotlib import pyplot as plt
import plottingRoutines as pR




#import all the stuff you need:
fl_v = np.load('/Users//Desktop/pythonstuff/mgfl_v.npy')
f_vdist = np.load('/Users//Desktop/pythonstuff/mgf_vdist.npy')
path = '/Users//Desktop/pythonstuff/'
abundn = np.load(path + 'abund_struct.npy')
regime = np.load(path + 'regime_struct.npy')



#plot the differential fluences for each regime,
#

jvel = np.arange(200,1825,25)  #Define jvel because it is convenient to do so here.

'''    
def histWRanges(flagnum,fluence,dataLim,speed=np.arange(200,1825,25)):
    returns the minimum, average, and maximum variances of fluence ratios
    per speed bin (200km/s - 800km/s)
    
    INPUTS:
        speed   - wind speed array to select ranges of data against.
        flagnum - regime number for species (1:CME, 2:CH, 3:IS, 0:bulk)
        fluence - name of species
        dataLim - scalar limit for purity of data ranges to be analyzed
  
    lower = []
    upper = []
    ratiomean = []
    xspeed = []
    
    if fluence == 'mg2o':
        for i in range(1,len(speed)):
            ind = np.where((regime['v_p'] >= speed[i-1] - 12.5) & (regime['v_p'] <= speed[i]-12.5) & (regime['flag'] == flagnum)
            & (regime['v_p'] != np.inf))
            
            var = np.array(sorted(abundn[ind]['mg2o']))
            var = 1.0/var
            
            if (np.size(var) != 0) & (len(var) >= dataLim):
                xspeed.append(np.average(regime['v_p'][ind]))
                
                try:
                    upp = fracs([var[int(len(var)*0.90)]],name=None)
                    low = fracs([var[int(len(var)* 0.10)]],name=None)
                    med = np.mean(fracs(var,name=fluence))
                    lower.append(med-low)
                    upper.append(upp-med)
                    ratiomean.append(np.mean(fracs(var,name=fluence)))
                    # xspeed.append(np.average(regime['v_p'][np.where()]))
                except ValueError:
                    pass
                
    elif fluence == 'o76':
        
        for i in range(1,len(speed)):
            ind = np.where((regime['v_p'] >= speed[i-1]-12.5) & (regime['v_p'] <= speed[i]-12.5) & (regime['flag'] == flagnum))
            var = sorted(abundn[ind][fluence])
            #xspeed = sorted()
            if (np.size(var) != 0) & (len(var) >= dataLim):
                xspeed.append(np.average(regime['v_p'][ind]))
                
                try:
                    upp = fracs([var[int(len(var)*0.90)]],name=None)
                    low = fracs([var[int(len(var)* 0.10)]],name=None)
                    med = np.mean(fracs(var,name=fluence))
                    lower.append(med-low)
                    upper.append(upp-med)
                    ratiomean.append(np.mean(fracs(var,name=fluence)))
                    # xspeed.append(np.average(regime['v_p'][np.where()]))
                except ValueError:
                    pass
    
    else:
    
        for i in range(1,len(speed)):
            ind = np.where((regime['v_p'] >= speed[i-1]-12.5) & (regime['v_p'] <= speed[i]-12.5) & (regime['flag'] == flagnum))
            var = sorted(abundn[ind][fluence]/abundn[ind]['mg2o'])
            #xspeed = sorted()
            if (np.size(var) != 0) & (len(var) >= dataLim):
                xspeed.append(np.average(regime['v_p'][ind]))
                
                try:
                    upp = fracs([var[int(len(var)*0.90)]],name=None)
                    low = fracs([var[int(len(var)* 0.10)]],name=None)
                    med = np.mean(fracs(var,name=fluence))
                    lower.append(med-low)
                    upper.append(upp-med)
                    ratiomean.append(np.mean(fracs(var,name=fluence)))
                    # xspeed.append(np.average(regime['v_p'][np.where()]))
                except ValueError:
                    pass
    return lower,upper,ratiomean, np.array(xspeed)
'''
    

#assigns values to lists corresponding to speed bins before plotting.
dataLim = 8

he2olow2, he2oupp2, he2omed2,hespeed2 = pR.histWRanges(2,'he2o',dataLim)
c2olow2,c2oupp2,c2omed2,cspeed2=pR.histWRanges(2,'c2o',dataLim)
n2olow2,n2oupp2,n2omed2,nspeed2=pR.histWRanges(2,'n2o',dataLim)
ne2olow2,ne2oupp2,ne2omed2,nespeed2=pR.histWRanges(2,'ne2o',dataLim)
mg2olow2,mg2oupp2,mg2omed2,mgspeed2=pR.histWRanges(2,'mg2o',dataLim)
si2olow2,si2oupp2,si2omed2,sispeed2=pR.histWRanges(2,'si2o',dataLim)
s2olow2,s2oupp2,s2omed2,sspeed2=pR.histWRanges(2,'s2o',dataLim)
fe2olow2,fe2oupp2,fe2omed2,fespeed2=pR.histWRanges(2,'fe2o',dataLim)
o76low2, o76upp2, o76med2,o76speed2=pR.histWRanges(2,'o76',dataLim)

he2olow1, he2oupp1, he2omed1,hespeed1 = pR.histWRanges(1,'he2o',dataLim)
c2olow1,c2oupp1,c2omed1,cspeed1=pR.histWRanges(1,'c2o',dataLim)
n2olow1,n2oupp1,n2omed1,nspeed1=pR.histWRanges(1,'n2o',dataLim)
ne2olow1,ne2oupp1,ne2omed1,nespeed1=pR.histWRanges(1,'ne2o',dataLim)
mg2olow1,mg2oupp1,mg2omed1,mgspeed1=pR.histWRanges(1,'mg2o',dataLim)
si2olow1,si2oupp1,si2omed1,sispeed1=pR.histWRanges(1,'si2o',dataLim)
s2olow1,s2oupp1,s2omed1,sspeed1=pR.histWRanges(1,'s2o',dataLim)
fe2olow1,fe2oupp1,fe2omed1,fespeed1=pR.histWRanges(1,'fe2o',dataLim)
o76low1, o76upp1, o76med1,o76speed1=pR.histWRanges(1,'o76',dataLim)

he2olow3, he2oupp3, he2omed3,hespeed3 = pR.histWRanges(3,'he2o',dataLim)
c2olow3,c2oupp3,c2omed3,cspeed3=pR.histWRanges(3,'c2o',dataLim)
n2olow3,n2oupp3,n2omed3,nspeed3=pR.histWRanges(3,'n2o',dataLim)
ne2olow3,ne2oupp3,ne2omed3,nespeed3=pR.histWRanges(3,'ne2o',dataLim)
mg2olow3,mg2oupp3,mg2omed3,mgspeed3=pR.histWRanges(3,'mg2o',dataLim)
si2olow3,si2oupp3,si2omed3,sispeed3=pR.histWRanges(3,'si2o',dataLim)
s2olow3,s2oupp3,s2omed3,sspeed3=pR.histWRanges(3,'s2o',dataLim)
fe2olow3,fe2oupp3,fe2omed3,fespeed3=pR.histWRanges(3,'fe2o',dataLim)
o76low3,o76upp3,o76med3,o76speed3=pR.histWRanges(3,'o76',dataLim)

he2olow0, he2oupp0, he2omed0,hespeed0 = pR.histWRanges(0,'he2o',dataLim)
c2olow0,c2oupp0,c2omed0,cspeed0=pR.histWRanges(0,'c2o',dataLim)
n2olow0,n2oupp0,n2omed0,nspeed0=pR.histWRanges(0,'n2o',dataLim)
ne2olow0,ne2oupp0,ne2omed0,nespeed0=pR.histWRanges(0,'ne2o',dataLim)
mg2olow0,mg2oupp0,mg2omed0,mgspeed0=pR.histWRanges(0,'mg2o',dataLim)
si2olow0,si2oupp0,si2omed0,sispeed0=pR.histWRanges(0,'si2o',dataLim)
s2olow0,s2oupp0,s2omed0,sspeed0=pR.histWRanges(0,'s2o',dataLim)
fe2olow0,fe2oupp0,fe2omed0,fespeed0=pR.histWRanges(0,'fe2o',dataLim)
o76low0,o76upp0,o76med0,o76speed0=pR.histWRanges(0,'o76',dataLim)


#Plots abundance ratios and variances.

#############********************##############

names = ['he2o','c2o','n2o','ne2o','mg2o','si2o','s2o','fe2o']
ylblparams = [[1,3.1,101],[-1,2,101],[-1.5,1,101],[-1.5,1,101],[-1,2,101],[-.55,0.5,101],
              [-1.5,0.5,100], [-2,1,101]]
reglbls = ['IS+CH','CME','CH','IS']
flagNum = [0,1,2,3]
ymaxparams = [1100,10,2.1,1.5,20.,3.0,1.0,3.0]
yminparams = [180,1.0,0.25,0.2,2,0.3,0.1,0.3]
for nm in range(len( names)):
    fig, axs = plt.subplots(2,2)
    axes = np.ravel(axs)
    axind = 0
    for rel in reglbls:
           
        x,y = pR.findReg(rel,names[nm],abundn[names[nm]])
        x,y = pR.goodBins(x,y)
        
        xbins = np.linspace(0,851,75)
        ybins = np.logspace(ylblparams[nm][0],ylblparams[nm][1],ylblparams[nm][2])
        px,py = pR.meanOfLog(5,x,y,speed = jvel)
        print len(py)
        fit = np.polyfit(px,py,1,full=False,cov=True)
        slope = fit[0][0]
        intercept = fit[0][1]
        covariance = fit[1]
        bfline = 10**(slope * xbins + intercept)
        counts,_,_ = np.histogram2d(x,y,bins=(xbins,ybins))
        cl = axes[axind].pcolormesh(xbins,ybins,np.transpose(counts),cmap='jet')
        axes[axind].pcolormesh(xbins,ybins,np.transpose(counts),cmap = 'jet')
        axes[axind].set_ylim(yminparams[nm], ymaxparams[nm])
        axes[axind].set_title(rel,fontweight='bold')
        axes[axind].set_yscale('log')
        axes[axind].plot(xbins,bfline,'w-')
        axes[axind].text(0.01,0.01,'Slope = %f +/- %f'%(slope,np.sqrt(covariance[-1][-1]))
        ,verticalalignment='bottom',horizontalalignment='left',transform=axes[axind].transAxes,color='white')
        
        axind += 1
    if names[nm] == 'mg2o':
        fig.text(0.04,0.6,'%s/Mg Abndance Ratios'%('O'),rotation='vertical',fontsize='large')
    else:
        fig.text(0.04,0.6,'%s/Mg Abundance Ratios'%names[nm][:-2].upper(),rotation='vertical',fontsize='large')
    fig.text(0.5,0,'Solar Wind Speed (km/s)',ha='center',va='center',fontsize='large')
    cax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
    fig.colorbar(cl,cax=cax)

#################**************************########################

#Abundance ratios with 10-90% variances.


fig, ((ax0,ax1),(ax2,ax3),(ax4,ax5),(ax6,ax7)) = plt.subplots(nrows=4,ncols=2)
fig.suptitle('Elemental Abundance Ratios',fontsize='large')
fig.text(0.5,0,'Solar Wind Speed (km/s)',ha='center',va='center',fontsize='large')
ax0.errorbar(hespeed2 + 5, he2omed2, yerr=[he2olow2, he2oupp2], fmt='bo',label="Coronal Hole")
#ax0.errorbar(hespeed0 + 10,he2omed0[:20],yerr=[he2olow0[:20],he2oupp0[:20]], fmt='ro',label="Bulk")
ax0.errorbar(hespeed1 + 15,he2omed1,yerr=[he2olow1,he2oupp1],fmt='ro',label='CME')
ax0.errorbar(hespeed3 , he2omed3,yerr=[he2olow3,he2oupp3], fmt='go',label="Interstream")
ax0.set_ylabel('He/Mg',fontweight = 'bold')
ax0.set_yscale('log')
ax0.set_ylim(ymin=100,ymax=1000)

ax0.legend(numpoints=1,loc="lower right")



ax1.errorbar(cspeed2+5, c2omed2, yerr =[c2olow2, c2oupp2], fmt='bo' )
ax1.errorbar(cspeed1+10,c2omed1,yerr=[c2olow1,c2oupp1], fmt='ro')
ax1.errorbar(cspeed3,c2omed3,yerr=[c2olow3,c2oupp3], fmt='go')
#ax1.errorbar(jvel[:20],c2omed0[:25],yerr=[c2olow0[:25],c2oupp0[:25]],fmt='yo')
ax1.set_yscale('log')
ax1.yaxis.set_label_position('right')
ax1.set_ylabel('C/Mg',fontweight='bold')
ax1.set_ylim(ymin=0.95,ymax=8.5)



ax2.errorbar(nspeed2+5,n2omed2, yerr=[n2olow2,n2oupp2], fmt='bo')
ax2.errorbar(nspeed1+10,n2omed1,yerr=[n2olow1,n2oupp1], fmt='ro')
ax2.errorbar(nspeed3,n2omed3,yerr=[n2olow3,n2oupp3], fmt='go')
#ax2.errorbar(jvel[:20],n2omed0[:25],yerr=[n2olow0[:25],n2oupp0[:25]],fmt='yo')
ax2.set_yscale('log')
ax2.set_ylabel('N/Mg',fontweight='bold')
ax2.set_ylim(ymin=0.35,ymax=2.5)



ax3.errorbar(nespeed2+5,ne2omed2,yerr=[ne2olow2,ne2oupp2],fmt='bo')
ax3.errorbar(nespeed1+10,ne2omed1,yerr=[ne2olow1,ne2oupp1], fmt='ro')
ax3.errorbar(nespeed3,ne2omed3,yerr=[ne2olow3,ne2oupp3], fmt='go')
#ax3.errorbar(jvel[:20],ne2omed0[:25],yerr=[ne2olow0[:25],ne2oupp0[:25]],fmt='yo')
ax3.set_yscale('log')
ax3.yaxis.set_label_position('right')
ax3.set_ylabel('Ne/Mg',fontweight='bold')
ax3.set_ylim(ymin=0.2,ymax=2)



ax4.errorbar(mgspeed2+5,mg2omed2,yerr=[mg2olow2,mg2oupp2],fmt='bo')
ax4.errorbar(mgspeed1+10,mg2omed1,yerr=[mg2olow1,mg2oupp1], fmt='ro')
ax4.errorbar(mgspeed3,mg2omed3,yerr=[mg2olow3,mg2oupp3], fmt='go')
#ax4.errorbar(jvel[:20],mg2omed0[:25],yerr=[mg2olow0[:25],mg2oupp0[:25]],fmt='yo')
ax4.set_yscale('log')
ax4.set_ylabel('O/Mg',fontweight='bold')
ax4.set_ylim(ymin=2,ymax=12)



ax5.errorbar(sispeed2+5,si2omed2,yerr=[si2olow2,si2oupp2],fmt='bo')
ax5.errorbar(sispeed1+10,si2omed1,yerr=[si2olow1,si2oupp1], fmt='ro')
ax5.errorbar(sispeed3,si2omed3,yerr=[si2olow3,si2oupp3], fmt='go')
#ax5.errorbar(jvel[:20],si2omed0[:25],yerr=[si2olow0[:25],si2oupp0[:25]],fmt='yo')
ax5.set_yscale('log')
ax5.yaxis.set_label_position('right')
ax5.set_ylabel('Si/Mg',fontweight='bold')
ax5.set_ylim(ymin=0.5,ymax=5)



ax6.errorbar(sspeed2+5,s2omed2,yerr=[s2olow2,s2oupp2],fmt='bo')
ax6.errorbar(sspeed1+10,s2omed1,yerr=[s2olow1,s2oupp1], fmt='ro')
ax6.errorbar(sspeed3,s2omed3,yerr=[s2olow3,s2oupp3], fmt='go')
#ax6.errorbar(jvel[:20],s2omed0[:25],yerr=[s2olow0[:25],s2oupp0[:25]],fmt='yo')
ax6.set_yscale('log')
ax6.set_ylabel('S/Mg',fontweight='bold')
ax6.set_ylim(ymin=0.1,ymax=1.0)



ax7.errorbar(fespeed2+5,fe2omed2,yerr=[fe2olow2,fe2oupp2],fmt='bo')
ax7.errorbar(fespeed1+10,fe2omed1,yerr=[fe2olow1,fe2oupp1], fmt='ro')
ax7.errorbar(fespeed3,fe2omed3,yerr=[fe2olow3,fe2oupp3], fmt='go')
#ax7.errorbar(jvel[:20],fe2omed0[:25],yerr=[fe2olow0[:25],fe2oupp0[:25]],fmt='yo')
ax7.set_yscale('log')
ax7.yaxis.set_label_position('right')
ax7.set_ylabel('Fe/Mg',fontweight='bold')
ax7.set_ylim(ymin=0.3,ymax=2.5)


fig, (axo72mg) = plt.subplots(1,1)
axo72mg.errorbar(o76speed2+5,o76med2,yerr=[o76low2,o76upp2],fmt='bo',label = 'Fast wind')
axo72mg.errorbar(o76speed1+10,o76med1,yerr=[o76low1,o76upp1],fmt='ro',label = 'CME')
axo72mg.errorbar(o76speed3,o76med3,yerr=[o76low3,o76upp3],fmt='go',label = 'Slow Wind')
#axo76.errorbar(jvel[:20],o76med0[:25],yerr=[o76low0[:25],o76upp0[:25]],fmt='yo',label='other')
axo72mg.set_yscale('log')
axo72mg.set_xlabel(r'Solar Wind Speed (km/s)',fontweight = "bold")
axo72mg.set_ylabel(r'${\bf {O^{\bf 7+}/O^{\bf 6+}}}$ Abundance Ratio',fontweight = 'bold')
axo72mg.set_ylim(0.0175,1.75)
axo72mg.legend(numpoints = 1, loc = 'lower left')



plt.show()



