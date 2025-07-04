# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 20:48:25 2017

@author: andy
"""

import numpy as np
from matplotlib import pyplot as plt





#import all the stuff you need:
fl_v = np.load('/Users//Desktop/pythonstuff/hfl_v.npy')
f_vdist = np.load('/Users//Desktop/pythonstuff/hf_vdist.npy')
path = '/Users//Desktop/pythonstuff/'
abundn = np.load(path + 'abund_struct.npy')
regime = np.load(path + 'regime_struct.npy')
#aswix1d = np.load(path + 'aswix_1d.npy')


#plot the differential fluences for each regime,
#

jvel = np.arange(200,1825,25)  #Define jvel because it is convenient to do so here.
'''
fig, (pr_fl) = plt.subplots()
line1 = pr_fl.plot(jvel,fl_v[:65,0,0],'r',label= "CME")
line2 = pr_fl.plot(jvel,fl_v[:65,0,1],'b',label="CH")
line3 = pr_fl.plot(jvel,fl_v[:65,0,2],'g',label="IS")
line4 = pr_fl.plot(jvel,fl_v[:65,0,3],color='black',label="Bulk")
pr_fl.set_ylabel(r"Proton Fluence ${ cm^{-2}}$",fontsize='large')
pr_fl.set_xlabel(r"Proton Speed (${ km s^{-1}}$)",fontsize='large')
pr_fl.legend(loc="upper right")
'''

#plot the o7+/o6+ abundance ratios

for i in range(4):
    fig, (snax) = plt.subplots()
    aline1 = snax.plot(np.arange(200,1825,25),fl_v[0:65,0,i],'r',label = 'He')
    aline2 = snax.plot(np.arange(200,1825,25),fl_v[:65,1,i],'b-',label = 'C')
    aline3 = snax.plot(np.arange(200,1825,25),fl_v[:65,2,i],color='gold',label = '')
    aline4 = snax.plot(np.arange(200,1825,25),fl_v[:65,3,i],color='skyblue',label = 'N')
    aline5 = snax.plot(np.arange(200,1825,25),fl_v[:65,4,i],color='green',label='O')
    aline6 = snax.plot(np.arange(200,1825,25),fl_v[:65,5,i],color='purple',label='He')
    aline7 = snax.plot(np.arange(200,1825,25),fl_v[:65,6,i],color='lawngreen',label='Mg')
    aline8 = snax.plot(np.arange(200,1825,25),fl_v[:65,7,i],color='pink',label='S')
    snax.set_yscale('log')
    snax.set_ylabel('Normalized Fluence (arbitrary units)',fontsize='large')
    snax.set_xlabel(r'Solar Wind Proton Speed (km${ s^{ -1}}$)',fontsize = 'large')
    
    snax.legend()
    print fig    
    
#Sorting routines and things.

def findReg(speedArray,regimeNum,array,oneDay=0):
    
    if oneDay == 1:
        flagArr = aswix1d['flag']
        speedArr = speedArray
    else:
        flagArr = regime['flag']
        speedArr = speedArray
    if regimeNum == 'IS+CH':
        ind = np.where((flagArr != 1) & (flagArr != 0))
        lst1 = array[ind]
        lst2 = speedArr[ind]
    elif regimeNum == 'all':
        ind = np.where((flagArr[:]))
        lst1 = array[np.where(flagArr[:])]
        lst2 = speedArr[ind]
    elif regimeNum == 'CME':
        ind = np.where((flagArr == 1))
        lst1 = array[np.where(flagArr == 1)]
        lst2 = speedArr[ind]
    elif regimeNum == 'CH':
        ind = np.where((flagArr == 2))
        lst1 = array[np.where(flagArr == 2)]
        lst2 = speedArr[ind]
    elif regimeNum == 'IS':
        ind = np.where((flagArr == 3))
        lst1 = array[np.where(flagArr == 3)]
        lst2 = speedArr[ind]
    else:
        lst1 = []
        lst2 = []
    return lst2,lst1
    

def fracs(arr1,name=None):
    lst = []
    if (name != None):
        for i in arr1:
            
            if i > 0.0:
                lst.append(i)
    if (name == None):
        for i in arr1:
            if i > 0.0:
                lst.append(i)
    return lst



def meanOfLog(dataLim,xdata,ydata,speed=np.arange(200,1825,25)):
    '''
    INPUTS: 
        speed    - array of speeds in range low -> high with steps, user defined.
        dataLim  - scalar limit to which taking the mean of the log(data) applies.
        xdata    - wind speed data to check against speed input.
        ydata    - data to be weighted.
    '''
    dBins = []
    vBins = []
    #bBins = []
    
    for i in range(1,len(speed)):
        yvals = ydata[np.where((xdata >= speed[i-1]) & (xdata <= speed[i]))]
        xvals = xdata[np.where((xdata >= speed[i-1]) & (xdata <= speed[i]))]
        
        if (len(yvals) >= dataLim) & (np.nan not in yvals):
            dBins.append(np.mean(np.log10(yvals)))
            vBins.append(np.mean(xvals))
            
     #       bBins.append(np.log10(var))
    return vBins,dBins
            
    
def goodBins(lst1,lst2):
    '''return properly aligned data arrays.'''
    arr1 = lst1[np.where((lst1 > 0.0) & (lst2 > 0.0) & (lst1 != np.nan) & (lst2 != np.nan))]
    arr2 = lst2[np.where((lst1 > 0.0) & (lst2 > 0.0) & (lst2 != np.nan) & (lst2 != np.nan))]
    
    return arr1, arr2
    
def histWRanges(flagnum,fluence,dataLim,speed=np.arange(200,1825,25)):
    '''returns the minimum, average, and maximum variances of fluence ratios
    per speed bin (200km/s - 800km/s)
    
    INPUTS:
        speed   - wind speed array to select ranges of data against.
        flagnum - regime number for species (1:CME, 2:CH, 3:IS, 0:bulk)
        fluence - name of species
        dataLim - scalar limit for purity of data ranges to be analyzed
    '''    
    lower = []
    upper = []
    ratiomean = []
    xspeed = []
    '''
    if fluence == 'n2o' or fluence == 's2o':
        
        for i in range(1,len(speed)):
            ind = np.where((aswix1d['speed'] >= speed[i-1]-12.5) & (aswix1d['speed'] <= speed[i]-12.5) & (aswix1d['flag'] == flagnum))
            var = sorted(aswix1d[ind][fluence])
            
            if (np.size(var) != 0) & (len(var) >= dataLim):
                xspeed.append(np.average(aswix1d['speed'][ind]))
                
                try:
                    upp = fracs([var[int(len(var)*0.90)]],name=None)
                    low = fracs([var[int(len(var)*0.90)]],name=None)
                    mean = np.mean(fracs(var,name=None))
                    lower.append(low-mean)
                    upper.append(upp-mean)
                    ratiomean.append(np.mean(fracs(var)))
                except ValueError:
                    pass
            else:
                pass
    else:
        '''
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
    return lower,upper,ratiomean, np.array(xspeed)

    

#assigns values to lists corresponding to speed bins before plotting.
dlimit = 8

he2olow2, he2oupp2, he2omed2,hespeed2 = histWRanges(2,'he2o',dlimit)
c2olow2,c2oupp2,c2omed2,cspeed2=histWRanges(2,'c2o',dlimit)
n2olow2,n2oupp2,n2omed2,nspeed2=histWRanges(2,'n2o',dlimit)
ne2olow2,ne2oupp2,ne2omed2,nespeed2=histWRanges(2,'ne2o',dlimit)
mg2olow2,mg2oupp2,mg2omed2,mgspeed2=histWRanges(2,'mg2o',dlimit)
si2olow2,si2oupp2,si2omed2,sispeed2=histWRanges(2,'si2o',dlimit)
s2olow2,s2oupp2,s2omed2,sspeed2=histWRanges(2,'s2o',dlimit)
fe2olow2,fe2oupp2,fe2omed2,fespeed2=histWRanges(2,'fe2o',dlimit)
o76low2, o76upp2, o76med2,o76speed2=histWRanges(2,'o76',dlimit)

he2olow1, he2oupp1, he2omed1,hespeed1 = histWRanges(1,'he2o',dlimit)
c2olow1,c2oupp1,c2omed1,cspeed1=histWRanges(1,'c2o',dlimit)
n2olow1,n2oupp1,n2omed1,nspeed1=histWRanges(1,'n2o',dlimit)
ne2olow1,ne2oupp1,ne2omed1,nespeed1=histWRanges(1,'ne2o',dlimit)
mg2olow1,mg2oupp1,mg2omed1,mgspeed1=histWRanges(1,'mg2o',dlimit)
si2olow1,si2oupp1,si2omed1,sispeed1=histWRanges(1,'si2o',dlimit)
s2olow1,s2oupp1,s2omed1,sspeed1=histWRanges(1,'s2o',dlimit)
fe2olow1,fe2oupp1,fe2omed1,fespeed1=histWRanges(1,'fe2o',dlimit)
o76low1, o76upp1, o76med1,o76speed1=histWRanges(1,'o76',dlimit)

he2olow3, he2oupp3, he2omed3,hespeed3 = histWRanges(3,'he2o',dlimit)
c2olow3,c2oupp3,c2omed3,cspeed3=histWRanges(3,'c2o',dlimit)
n2olow3,n2oupp3,n2omed3,nspeed3=histWRanges(3,'n2o',dlimit)
ne2olow3,ne2oupp3,ne2omed3,nespeed3=histWRanges(3,'ne2o',dlimit)
mg2olow3,mg2oupp3,mg2omed3,mgspeed3=histWRanges(3,'mg2o',dlimit)
si2olow3,si2oupp3,si2omed3,sispeed3=histWRanges(3,'si2o',dlimit)
s2olow3,s2oupp3,s2omed3,sspeed3=histWRanges(3,'s2o',dlimit)
fe2olow3,fe2oupp3,fe2omed3,fespeed3=histWRanges(3,'fe2o',dlimit)
o76low3,o76upp3,o76med3,o76speed3=histWRanges(3,'o76',dlimit)

he2olow0, he2oupp0, he2omed0,hespeed0 = histWRanges(0,'he2o',dlimit)
c2olow0,c2oupp0,c2omed0,cspeed0=histWRanges(0,'c2o',dlimit)
n2olow0,n2oupp0,n2omed0,nspeed0=histWRanges(0,'n2o',dlimit)
ne2olow0,ne2oupp0,ne2omed0,nespeed0=histWRanges(0,'ne2o',dlimit)
mg2olow0,mg2oupp0,mg2omed0,mgspeed0=histWRanges(0,'mg2o',dlimit)
si2olow0,si2oupp0,si2omed0,sispeed0=histWRanges(0,'si2o',dlimit)
s2olow0,s2oupp0,s2omed0,sspeed0=histWRanges(0,'s2o',dlimit)
fe2olow0,fe2oupp0,fe2omed0,fespeed0=histWRanges(0,'fe2o',dlimit)
o76low0,o76upp0,o76med0,o76speed0=histWRanges(0,'o76',dlimit)

#Plots abundance ratios and variances.

#############********************##############

names = ['he2o','c2o','n2o','ne2o','mg2o','si2o','s2o','fe2o']
speeds = ['vhe','vc5','vn5','vne8','vmg10','vsi8','vs8','vfe10']
ylblparams = [[1,3,101],[-1,0.3,101],[-1.5,0,101],[-1.5,0,101],[-1.5,0,101],[-1.5,-0.5,101],
              [-1.5,0.5,100], [-2,1,101]]
reglbls = ['IS+CH','CME','CH','IS']
flagNum = [0,1,2,3]
ymaxparams = [200,1,0.25,0.25,0.5,0.5,0.125,0.5]
yminparams = [20,0.1,0.03,0.03,0.055,0.05,0.02,0.05]
for nm in range(len(names)):#len( names)):
    fig, axs = plt.subplots(2,2,figsize=(15,10))
    axes = np.ravel(axs)
    axind = 0
    for rel in reglbls:
        '''
        if names[nm] == 'n2o' or names[nm] == 's2o':
            x,y = findReg(rel,aswix1d[names[nm]],oneDay = 1)
            x,y = goodBins(x,y)
        
        else:
            '''
        x,y = findReg(abundn[speeds[nm]],rel,abundn[names[nm]])
        x,y = goodBins(x,y)
        
        xbins = np.linspace(0,851,75)
        ybins = np.logspace(ylblparams[nm][0],ylblparams[nm][1],ylblparams[nm][2])
        px,py = meanOfLog(5,x,y,speed = abundn[speeds[nm]])

        fit = np.polyfit(px,py,1,full=False,cov=True)
        slope = fit[0][0]
        intercept = fit[0][1]
        covariance = fit[1]
        bfline = 10**(slope * xbins + intercept)
        counts,_,_ = np.histogram2d(x,y,bins=(xbins,ybins))
        cl = axes[axind].pcolormesh(xbins,ybins,np.transpose(counts),cmap='jet')
        axes[axind].pcolormesh(xbins,ybins,np.transpose(counts),cmap = 'jet')
        axes[axind].set_ylim(ymin=yminparams[nm], ymax=ymaxparams[nm])
        axes[axind].set_title(rel,fontweight='bold')
        axes[axind].set_yscale('log')
        axes[axind].plot(xbins,bfline,'w-')
        axes[axind].text(0.01,0.01,'Slope = %f +/- %f'%(slope,np.sqrt(covariance[-1][-1]))
        ,verticalalignment='bottom',horizontalalignment='left',transform=axes[axind].transAxes,color='white')
        
        axind += 1
    
    fig.text(0.04,0.6,'%s Abundance Ratios'%names[nm].upper(),rotation='vertical',fontsize='large')
    fig.text(0.5,0,'Solar Wind Speed (km/s)',ha='center',va='center',fontsize='large')
    cax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
    fig.colorbar(cl,cax=cax)

#################**************************########################


#Abundance ratios with 10-90% variances.


fig, ((ax0,ax1),(ax2,ax3),(ax4,ax5),(ax6,ax7)) = plt.subplots(nrows=4,ncols=2,figsize=(15,10))
fig.suptitle('Elemental Abundance Ratios',fontsize='large')
fig.text(0.5,0,'Solar Wind Speed (km/s)',ha='center',va='center',fontsize='large')
ax0.errorbar(hespeed2 + 5, he2omed2, yerr=[he2olow2, he2oupp2], fmt='bo',label="Coronal Hole")
#ax0.errorbar(hespeed0 + 10,he2omed0[:20],yerr=[he2olow0[:20],he2oupp0[:20]], fmt='ro',label="Bulk")
ax0.errorbar(hespeed1 + 15,he2omed1,yerr=[he2olow1,he2oupp1],fmt='ro',label='CME')
ax0.errorbar(hespeed3 , he2omed3,yerr=[he2olow3,he2oupp3], fmt='go',label="Interstream")
ax0.set_ylabel('He/O',fontweight = 'bold')
ax0.set_yscale('log')
ax0.set_ylim(ymin=30,ymax=300)

ax0.legend(numpoints=1,loc="lower right")



ax1.errorbar(cspeed2+5, c2omed2, yerr =[c2olow2, c2oupp2], fmt='bo' )
ax1.errorbar(cspeed1+10,c2omed1,yerr=[c2olow1,c2oupp1], fmt='ro')
ax1.errorbar(cspeed3,c2omed3,yerr=[c2olow3,c2oupp3], fmt='go')
#ax1.errorbar(jvel[:20],c2omed0[:25],yerr=[c2olow0[:25],c2oupp0[:25]],fmt='yo')
ax1.set_yscale('log')
ax1.yaxis.set_label_position('right')
ax1.set_ylabel('C/O',fontweight='bold')
ax1.set_ylim(ymin=0.25,ymax=2.)



ax2.errorbar(nspeed2+5,n2omed2, yerr=[n2olow2,n2oupp2], fmt='bo')
ax2.errorbar(nspeed1+10,n2omed1,yerr=[n2olow1,n2oupp1], fmt='ro')
ax2.errorbar(nspeed3,n2omed3,yerr=[n2olow3,n2oupp3], fmt='go')
#ax2.errorbar(jvel[:20],n2omed0[:25],yerr=[n2olow0[:25],n2oupp0[:25]],fmt='yo')
ax2.set_yscale('log')
ax2.set_ylabel('N/O',fontweight='bold')
ax2.set_ylim(ymin=0.075,ymax=0.7)



ax3.errorbar(nespeed2+5,ne2omed2,yerr=[ne2olow2,ne2oupp2],fmt='bo')
ax3.errorbar(nespeed1+10,ne2omed1,yerr=[ne2olow1,ne2oupp1], fmt='ro')
ax3.errorbar(nespeed3,ne2omed3,yerr=[ne2olow3,ne2oupp3], fmt='go')
#ax3.errorbar(jvel[:20],ne2omed0[:25],yerr=[ne2olow0[:25],ne2oupp0[:25]],fmt='yo')
ax3.set_yscale('log')
ax3.yaxis.set_label_position('right')
ax3.set_ylabel('Ne/O',fontweight='bold')
ax3.set_ylim(ymin=0.06,ymax=0.6)



ax4.errorbar(mgspeed2+5,mg2omed2,yerr=[mg2olow2,mg2oupp2],fmt='bo')
ax4.errorbar(mgspeed1+10,mg2omed1,yerr=[mg2olow1,mg2oupp1], fmt='ro')
ax4.errorbar(mgspeed3,mg2omed3,yerr=[mg2olow3,mg2oupp3], fmt='go')
#ax4.errorbar(jvel[:20],mg2omed0[:25],yerr=[mg2olow0[:25],mg2oupp0[:25]],fmt='yo')
ax4.set_yscale('log')
ax4.set_ylabel('Mg/O',fontweight='bold')
ax4.set_ylim(ymin=0.05,ymax=0.5)



ax5.errorbar(sispeed2+5,si2omed2,yerr=[si2olow2,si2oupp2],fmt='bo')
ax5.errorbar(sispeed1+10,si2omed1,yerr=[si2olow1,si2oupp1], fmt='ro')
ax5.errorbar(sispeed3,si2omed3,yerr=[si2olow3,si2oupp3], fmt='go')
#ax5.errorbar(jvel[:20],si2omed0[:25],yerr=[si2olow0[:25],si2oupp0[:25]],fmt='yo')
ax5.set_yscale('log')
ax5.yaxis.set_label_position('right')
ax5.set_ylabel('Si/O',fontweight='bold')
ax5.set_ylim(ymin=0.05,ymax=0.5)



ax6.errorbar(sspeed2+5,s2omed2,yerr=[s2olow2,s2oupp2],fmt='bo')
ax6.errorbar(sspeed1+10,s2omed1,yerr=[s2olow1,s2oupp1], fmt='ro')
ax6.errorbar(sspeed3,s2omed3,yerr=[s2olow3,s2oupp3], fmt='go')
#ax6.errorbar(jvel[:20],s2omed0[:25],yerr=[s2olow0[:25],s2oupp0[:25]],fmt='yo')
ax6.set_yscale('log')
ax6.set_ylabel('S/O',fontweight='bold')
ax6.set_ylim(ymin=0.025)



ax7.errorbar(fespeed2+5,fe2omed2,yerr=[fe2olow2,fe2oupp2],fmt='bo')
ax7.errorbar(fespeed1+10,fe2omed1,yerr=[fe2olow1,fe2oupp1], fmt='ro')
ax7.errorbar(fespeed3,fe2omed3,yerr=[fe2olow3,fe2oupp3], fmt='go')
#ax7.errorbar(jvel[:20],fe2omed0[:25],yerr=[fe2olow0[:25],fe2oupp0[:25]],fmt='yo')
ax7.set_yscale('log')
ax7.yaxis.set_label_position('right')
ax7.set_ylabel('Fe/O',fontweight='bold')
ax7.set_ylim(ymin=0.07)



fig, (axo76) = plt.subplots(1,1)
axo76.errorbar(o76speed2+5,o76med2,yerr=[o76low2,o76upp2],fmt='bo',label = 'Fast wind')
axo76.errorbar(o76speed1+10,o76med1,yerr=[o76low1,o76upp1],fmt='ro',label = 'CME')
axo76.errorbar(o76speed3,o76med3,yerr=[o76low3,o76upp3],fmt='go',label = 'Slow Wind')
#axo76.errorbar(jvel[:20],o76med0[:25],yerr=[o76low0[:25],o76upp0[:25]],fmt='yo',label='other')
axo76.set_yscale('log')
axo76.set_xlabel(r'Solar Wind Speed (km/s)',fontweight = "bold")
axo76.set_ylabel(r'${\bf {O^{\bf 7+}/O^{\bf 6+}}}$ Abundance Ratio',fontweight = 'bold')
axo76.set_ylim(-3,1)
axo76.legend(numpoints = 1, loc = 'lower left')

plt.show()

