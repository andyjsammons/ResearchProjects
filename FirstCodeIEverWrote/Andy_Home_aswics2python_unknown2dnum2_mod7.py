import numpy as np
from scipy import io
#from matplotlib.cbook import flatten

def open_file(filename,delimiter):
    ''' open a file and return a list of everything after the delimiter.'''
    File = open(filename).readlines()
    
    if type(delimiter) == str:
        line = File[File.index(delimiter)+1:]
        
        return line
    elif type(delimiter) == list:
        line = File[File.index(File.startswith(delimiter[0])):]
        return line
        

def bin_count(dnum,lst):
    '''PURPOSE: return occurance of data entries per day number.
    
       INPUTS: 'dnum' - day number in question.
               'lst' - list from which to count dnum occurrences.
               '''
    daylist = list(np.floor(lst))
    dnum = np.floor(dnum)
    num = daylist.count(dnum)
    return num

def leapyear(y):
    '''
    PURPOSE: 
        Return 'True' or 'False' for status of given year as leap.
    INPUT: 
        'y' -Year to be tested, Should be full year (e.g.:1999).
    **Supports both multidimensional lists and arrays, but returns a 1D list**
    '''

    if y % 4 == 0 and y % 100 != 0 or y % 400 == 0:
        return True
    else:
        return False      
    
    
    
    
def dnum2yydoy(dnum):
    '''
    PURPOSE:
        return the year, and day of year value for dnum.
    INPUTS:
        'dnum' -days passed since January 1st 2000
    OUTPUTS: 
        'yy' -Year of given dnum value
        'doy' - day of year for given dnum value'''
    yy = np.floor(np.floor(dnum)/365.25)
    doy = dnum - np.floor(yy*365.25)
    
    yy = yy + 2000
    if np.ndim(yy) == 0:
        if leapyear(yy) == True:
            doy += 1
    return yy, doy




def days_in_month(m,y):
    '''
    PURPOSE: 
        Return an unsigned integer number of days in the month and year.
    INPUT: 'm' -An optional int value representing the month of year. If not
                provided, the current month and year are used.
           'y' -An optional int value representing the year. If not provided, 
                current year is used.
    **Compatible with multi-dimensional lists and arrays**            
    '''

    if leapyear(y) == True:
        dim = (31,29,31,30,31,30,31,31,30,31,30,31)
    else:
        dim = (31,28,31,30,31,30,31,31,30,31,30,31)
    mi = m - 1
    ndays = dim[mi]   
    return ndays
        
        

def ymd2doy(yy,mm,dd):
    '''
    PURPOSE: 
        Given a year/month/day, return the day of the year.
    ARGUMENTS: 
        'yy' - four-digit year
        'mm' - month (1-12)
        'dd' - day of month (1-31)      
    EXAMPLE: 
        >>> print ymd2doy(1998, 2, 1)
             '''
    doy = dd
    for m in range(1,mm):
        doy = doy + days_in_month(m,yy)
        m += 1
    return doy
    
def yydoy2dnum(yy,doy):
    ''' 
    PURPOSE: 
        Return the Day number since January 1, 2000
    INPUT:
        'yy' four-digit year
        'doy' Day of year
    '''

    doycopy = float(doy)
    float(yy)
    if (yy % 4) == 0:
        doycopy = doycopy - 1.0

    dnum = np.floor((int(yy) - 2000)*365.25) + doycopy
    return dnum

        
        
        
def doy2md(year,doy):
    ''' PURPOSE: Converts a day of year to month, and day of month
        INPUTS: 
           'year'  four-digit year
           'doy'   day of year (1-365, or 1-366)    
        OUTPUTS:
            'month'   month of year (1-12)
            'day'    day of year (1-31)
        SIDE EFFECTS:
            -Shortness of breath
            -Confusion
            -Loss of consciousness
        EXAMPLE:
            >>> doy2md(1998, 43)
            >>> 2, 12 '''
    monthdays = [31,28,31,30,31,30,31,31,30,31,30,31]
  
    if leapyear(year) == True:
        monthdays[1] += 1
    day = doy
    month = 0
    while int(day) > monthdays[month]:
        day -= monthdays[month]
        month += 1
    month += 1
    return month, day
    
    
def unknown2dnum(year,date):
    '''
    PURPOSE: 
        Given a date in unknown format, convert to Ed's dnum format.
    ARGUMENTS: 
        'date' - date in one of several possible formats.
    POST CONDITIONS: 
        Return a double precision day number thingy.
    INVARIANTS: 
        date with value < 0 return the dnum for today's date.
    EXAMPLE: 
        >>> dnum = unknown2dnum( [ 1998, 78 ] ) -- day 78, 1998, 00:00 UT
        >>> dnum = unknown2dnum( [1998, 78.5] ) -- day 78, 1998, 12:00 UT
        >>> dnum = unknown2dnum( [1998, 78, 12, 00] ) -- same  '''      
    if np.size(date) == 1:
        dnum = yydoy2dnum(float(year),float(date))
        return dnum
    else:
        dnum = []
        for i in date:
            dnum.append(yydoy2dnum(float(year),float(i)))
        return dnum
  

def idl2python(idlsavefile):
    '''
    PORPOISE :
        Read IDL save file and return a dictionary with stored values
    '''
    returndict = io.readsav(idlsavefile)
    return returndict

      
    
def aswics2python(): 
    '''
    PURPOSE: Parse aswics data into python record array, and save it to a binary file.
    '''      
    path = '/home/andy/Desktop/pythonstuff/'
    pathswics = '/home/andy/Desktop/pythonstuff/ACE_SWICS/'
    pathswep = '/home/andy/Desktop/SWEPAM_data/'
    pathwind = '/home/andy/Desktop/OMNI_data/'
    filename_swep = 'ACE_SW_Proton_Data_12min_200'
    filename_wind = 'wind_5min_b200'
    filename_ele = 'ACE_SWICS_2hr_1.1lv2_200'
    filename_q = 'ACE_qdist_2hr_1.1lv2_200'
    
    dnum = []; yist = []   #initiate empty data lists
    doy = []; he2o = []
    c2o = []; n2o = []
    ne2o = []; mg2o = []
    si2o = []; s2o = []
    fe2o = []; c56 = []
    o76 = []; avq_c = []
    avq_o = []; avq_fe = []
    nhe = []; vhe = []
    vc5 = []; vo6 = []
    vfe10 = []; vmg10 = []
    vn5 = []; vne8 = []
    vs8 = []; vsi8 = []
    c4 = []; c5 = []
    c6 = []; o5 = []
    o6 = []; o7 = []
    o8 = []; ne8 = []
    ne9 = []; mg6 = []
    mg7 = []; mg8 = []
    mg9 = []; mg10 = []
    mg11 = []; mg12 = []
    si6 = []; si7 = []
    si8 = []; si9 = []
    si10 = []; si11 = []
    si12 = []; fe6 = []
    fe7 = []; fe8 = []
    fe9 = []; fe10 = []
    fe11 = []; fe12 = []
    fe13 = []; fe14 = []
    fe15 = []; fe16 = []
    fe17 = []; fe18 = []
    fe19 = []; fe20 = []
    vthhe = []; vthc5 = []
    vtho6 = []; vthfe10 = []
    vthmg10 = []; vthn5 = []
    vthne8 = []; vtho6 = []
    vths8 = []; vthsi8 = []
    swtype = []

    iy = range(1,5)
    
    for i in iy:  #iterate through files by year
        
        year = 2000 + i

        file_e = open(pathswics + filename_ele + str(i) + '.txt')
        line_e = file_e.readline()
        while line_e:
            line_e += file_e.readline()
            if 'BEGIN DATA' in line_e:
                break
        line_e = file_e.readlines()
        e_len = len(line_e)
        file_e.close()
        
        file_q = open(pathswics + filename_q + str(i) + '.txt')
        line_q = file_q.readline()
        while line_q:
            line_q += file_q.readline()
            if 'BEGIN DATA' in line_q:
                break
        line_q = file_q.readlines()
        q_len = len(line_q)
        file_q.close()
        
        index = 0
        
        while index != max(e_len,q_len):   #while not EOF: 
            
            yist.append(year)
            
            if index >= e_len:
                ace_arr = np.zeros(70)
            else:
                ace_arr = np.array(line_e[index].split())    #create array of raw data Then append array elements to data lists
            dnum.append(unknown2dnum(year,float(ace_arr[6])))
            doy.append(ace_arr[6]),nhe.append(ace_arr[8]),vhe.append(ace_arr[10])
            vthhe.append(ace_arr[11]),vthc5.append(ace_arr[16])
            vtho6.append(ace_arr[21]),vthfe10.append(ace_arr[26]),c56.append(ace_arr[33]),o76.append(ace_arr[36])
            avq_c.append(ace_arr[39]),avq_o.append(ace_arr[42]),avq_fe.append(ace_arr[45]),he2o.append(ace_arr[58])
            c2o.append(ace_arr[61]),ne2o.append(ace_arr[64]),mg2o.append(ace_arr[67]),si2o.append(ace_arr[70])
            fe2o.append(ace_arr[55]),swtype.append(ace_arr[54])
            
            if index >= q_len:
                ace_arr = np.zeros(70)
            else:
                ace_arr = np.array(line_q[index].split())
            
            c4.append(ace_arr[8]),c5.append(ace_arr[9]),c6.append(ace_arr[10]),o5.append(ace_arr[11]),o6.append(ace_arr[12])
            o7.append(ace_arr[13]),o8.append(ace_arr[14]),ne8.append(ace_arr[15]),ne9.append(ace_arr[16])
            mg6.append(ace_arr[17]),mg7.append(ace_arr[18]),mg8.append(ace_arr[19]),mg9.append(ace_arr[20])
            mg10.append(ace_arr[21]),mg11.append(ace_arr[22]),mg12.append(ace_arr[23]),si6.append(ace_arr[24])
            si7.append(ace_arr[25]),si8.append(ace_arr[26]),si9.append(ace_arr[27]),si10.append(ace_arr[28])
            si11.append(ace_arr[29]),si12.append(ace_arr[30]),fe6.append(ace_arr[31]),fe7.append(ace_arr[32]),fe8.append(ace_arr[33])
            fe9.append(ace_arr[34]),fe10.append(ace_arr[35]),fe11.append(ace_arr[36]),fe12.append(ace_arr[37]),fe13.append(ace_arr[38])
            fe14.append(ace_arr[39]),fe15.append(ace_arr[40]),fe16.append(ace_arr[41]),fe17.append(ace_arr[42])
            fe18.append(ace_arr[43]),fe19.append(ace_arr[44]),fe20.append(ace_arr[45])
                                
            #just create placeholders for new data lists:
            n2o.append(-9999.)
            s2o.append(-9999.)
            vc5.append(-9999.)
            vfe10.append(-9999.)
            vmg10.append(-9999.)
            vn5.append(-9999.)
            vne8.append(-9999.)
            vo6.append(-9999.)
            vs8.append(-9999.)
            vsi8.append(-9999.)
            vthc5.append(-9999.)
            vthfe10.append(-9999.)
            vthmg10.append(-9999.)
            vthn5.append(-9999.)
            vthne8.append(-9999.)
            vtho6.append(-9999.)
            vths8.append(-9999.)
            vthsi8.append(-9999.)
            
            index += 1   
        
    dnum = np.array(dnum) 
    asdnum = np.around(dnum,5)
    esdnum = np.floor(dnum) #rounding out to the dnum's 5th decimal place allows for accurate
    n2o = np.array(n2o)     #lists to arrays so things can be done.
    s2o = np.array(s2o)
    vc5 = np.array(vc5)
    vfe10 = np.array(vfe10)
    vmg10 = np.array(vmg10)
    vn5 = np.array(vn5)
    vne8 = np.array(vne8)
    vo6 = np.array(vo6)
    vs8 = np.array(vs8)
    vsi8 = np.array(vsi8)
    vthc5 = np.array(vthc5)
    vthfe10 = np.array(vthfe10)
    vthmg10 = np.array(vthmg10)
    vthn5 = np.array(vthn5)
    vthne8 = np.array(vthne8)
    vtho6 = np.array(vtho6)
    vths8 = np.array(vths8)
    vthsi8 = np.array(vthsi8)
    
    for i in range(1,5):
        year = 2000 + i
        ns2hr = idl2python('/home/andy/Desktop/new_SWICS_data_IDL_save_files/Genesis_N_S_O_ratio'+str(year)+'.save')
        nwvthrm = idl2python('/home/andy/Desktop/new_SWICS_data_IDL_save_files/Genesis_V_Vthermal_'+str(year)+'.save')
        
        #create the dnum values correspondent to the new data:
        
        ns2hrdnum = np.around(unknown2dnum(year,ns2hr.doy_genesis),5)
        nwvthrmdnum = np.round(unknown2dnum(year,nwvthrm.doy_genesis),5)
        dnumind1 = np.where([w == ns2hrdnum for w in asdnum])
        dnumind2 = np.where([w == nwvthrmdnum for w in asdnum])
        
        #I used several For ... zip() statements because there is a limit to how many elements can be zip()'d but this runs
        #sufficiently fast.
        
        if (len(dnumind1[0]) == len(ns2hrdnum)) & (len(dnumind2[0]) == len(nwvthrmdnum)): 
            for no,so,dnm in zip(ns2hr.n_o_ratio,ns2hr.s_o_ratio,dnumind1[0]):
            
                n2o[dnm] = no
                s2o[dnm] = so
                
            for vc,vfe,vmg,vn,dnm in zip(nwvthrm.v_c5,nwvthrm.v_fe10,nwvthrm.v_mg10,nwvthrm.v_n5,dnumind2[0]):
                
                vc5[dnm] = vc
                vfe10[dnm] = vfe
                vmg10[dnm] = vmg
                vn5[dnm] = vn
                
            for vne,vo,vs,vsi,dnm in zip(nwvthrm.v_ne8,nwvthrm.v_o6,nwvthrm.v_s8,nwvthrm.v_si8,dnumind2[0]):
                
                vne8[dnm] = vne
                vo6[dnm] = vo
                vs8[dnm] = vs
                vsi8[dnm] = vsi
                
            for c,fe,mg,n,dnm in zip(nwvthrm.vth_c5,nwvthrm.vth_fe10,nwvthrm.vth_mg10,nwvthrm.vth_n5,dnumind2[0]):
                
                vthc5[dnm] = c
                vthfe10[dnm] = fe
                vthmg10[dnm] = mg
                vthn5[dnm] = n
                
            for ne,o,s,si,dnm in zip(nwvthrm.vth_ne8,nwvthrm.vth_o6,nwvthrm.vth_s8,nwvthrm.vth_si8,dnumind2[0]):
                
                vthne8[dnm] = ne
                vtho6[dnm] = o
                vths8[dnm] = s
                vthsi8[dnm] = si
            
        else:   #handle for times when new data dnum's do not match old:
            
            for num in range(1,len(ns2hrdnum)):
                
                old_dnum1 = np.floor(ns2hrdnum[num-1])
                new_dnum1 = np.floor(ns2hrdnum[num])
                old_dnum2 = np.floor(nwvthrmdnum[num-1])
                new_dnum2 = np.floor(nwvthrmdnum[num])
    
                stoo = ns2hr.s_o_ratio[np.where((ns2hrdnum >= old_dnum1) & 
                                              (ns2hrdnum < new_dnum1))]
                ntoo = ns2hr.n_o_ratio[np.where((ns2hrdnum >= old_dnum1) & 
                                              (ns2hrdnum < new_dnum1))]
                #Velocities:
                    
                vcfive = nwvthrm.v_c5[np.where((nwvthrmdnum >= old_dnum2) & 
                                              (nwvthrmdnum < new_dnum2))]
                vfeten = nwvthrm.v_fe10[np.where((nwvthrmdnum >= old_dnum2) & 
                                              (nwvthrmdnum < new_dnum2))]
                vmgten = nwvthrm.v_mg10[np.where((nwvthrmdnum >= old_dnum2) & 
                                              (nwvthrmdnum < new_dnum2))]
                vnfive = nwvthrm.v_n5[np.where((nwvthrmdnum >= old_dnum2) & 
                                              (nwvthrmdnum < new_dnum2))]
                vneeight= nwvthrm.v_ne8[np.where((nwvthrmdnum >= old_dnum2) & 
                                              (nwvthrmdnum < new_dnum2))]
                vosix = nwvthrm.v_o6[np.where((nwvthrmdnum >= old_dnum2) & 
                                              (nwvthrmdnum < new_dnum2))]
                vseight = nwvthrm.v_s8[np.where((nwvthrmdnum >= old_dnum2) & 
                                              (nwvthrmdnum < new_dnum2))]
                vsieight = nwvthrm.v_si8[np.where((nwvthrmdnum >= old_dnum2) & 
                                              (nwvthrmdnum < new_dnum2))]
                #Thermal Velocities:
                    
                vthc = nwvthrm.vth_c5[np.where((nwvthrmdnum >= old_dnum2) & 
                                              (nwvthrmdnum < new_dnum2))]
                vthfe = nwvthrm.vth_fe10[np.where((nwvthrmdnum >= old_dnum2) & 
                                              (nwvthrmdnum < new_dnum2))]
                vthmg = nwvthrm.vth_mg10[np.where((nwvthrmdnum >= old_dnum2) & 
                                              (nwvthrmdnum < new_dnum2))]
                vthn = nwvthrm.v_c5[np.where((nwvthrmdnum >= old_dnum2) & 
                                              (nwvthrmdnum < new_dnum2))]
                vthne = nwvthrm.v_c5[np.where((nwvthrmdnum >= old_dnum2) & 
                                              (nwvthrmdnum < new_dnum2))]
                vtho = nwvthrm.v_c5[np.where((nwvthrmdnum >= old_dnum2) & 
                                              (nwvthrmdnum < new_dnum2))]
                vths = nwvthrm.v_c5[np.where((nwvthrmdnum >= old_dnum2) & 
                                              (nwvthrmdnum < new_dnum2))]
                vthsi = nwvthrm.v_c5[np.where((nwvthrmdnum >= old_dnum2) & 
                                              (nwvthrmdnum < new_dnum2))]
    
                dnumind1 = np.where(esdnum == old_dnum1)
                dnumind2 = np.where(esdnum == old_dnum2)
                
                
                if ((len(ntoo) > 0) & (len(stoo) > 0)):
                    for vc,vfe,vmg,vn,dnm in zip(vcfive,vfeten,vmgten,vnfive,dnumind2[0]):
                        
                        vc5[dnm] = vc
                        vfe10[dnm] = vfe
                        vmg10[dnm] = vmg
                        vn5[dnm] = vn
                        
                    for vne,vo,vs,vsi,dnm in zip(vneeight,vosix,vseight,vsieight,dnumind2[0]):
                        
                        vne8[dnm] = vne
                        vo6[dnm] = vo
                        vs8[dnm] = vs
                        vsi8[dnm] = vsi
                        
                    for no,so,dnm in zip(ntoo,stoo,dnumind1[0]):
                        
                        n2o[dnm] = no
                        s2o[dnm] = so
                    
                    for c,fe,mg,n,dnm in zip(vthc,vthfe,vthmg,vthn,dnumind2[0]):
                        
                        vthc5[dnm] = c
                        vthfe10[dnm] = fe
                        vthmg10[dnm] = mg
                        vthn5[dnm] = n
                        
                    for ne,o,s,si,dnm in zip(vthne,vtho,vths,vthsi,dnumind2[0]):
                        
                        vthne8[dnm] = ne
                        vtho6[dnm] = o
                        vths8[dnm] = s
                        vthsi8[dnm] = si
    
    aswics = np.recarray((len(yist),), dtype =  [('dnum','d'),('year','d'),('doy','d'),('he2o','d'),('c2o','d'),('n2o','d'),('ne2o','d'),('mg2o','d'),('si2o','d'),
    ('s2o','d'),('fe2o','d'),('c56','d'),('o76','d'),('avq_c','d'),('avq_o','d'),('avq_fe','d'),('nhe','d'),
    ('vhe','d'),('vc5','d'),('vo6','d'),('vfe10','d'),('c4','d'),('c5','d'),('c6','d'),('o5','d'),('o6','d'),('o7','d'),
    ('o8','d'),('ne8','d'),('ne9','d'),('mg6','d'),('mg7','d'),('mg8','d'),('mg9','d'),('mg10','d'),('mg11','d'),
    ('mg12','d'),('si6','d'),('si7','d'),('si8','d'),('si9','d'),('si10','d'),('si11','d'),('si12','d'),('fe6','d'),
    ('fe7','d'),('fe8','d'),('fe9','d'),('fe10','d'),('fe11','d'),('fe12','d'),('fe13','d'),('fe14','d'),('fe15','d'),
    ('fe16','d'),('fe17','d'),('fe18','d'),('fe19','d'),('fe20','d'),('vthhe','d'),('vthc5','d'),('vtho6','d'),
    ('vthfe10','d'),('swtype','d'),('vthn5','d'),('vthne8','d'),('vthmg10','d'),('vthsi8','d'),('vths8','d'),('vmg10','d'),('vn5','d'),
    ('vne8','d'),('vs8','d'),('vsi8','d')])
    
    x = 0
    while x < len(yist):
        aswics[x]['dnum']=dnum[x]; aswics[x]['year']=yist[x]   #this syntax allows for some compact code.
        aswics[x]['doy']=doy[x]; aswics[x]['he2o']=he2o[x]
        aswics[x]['c2o']=c2o[x]; aswics[x]['n2o']=n2o[x]
        aswics[x]['ne2o']=ne2o[x]; aswics[x]['mg2o']=mg2o[x]
        aswics[x]['si2o']=si2o[x]; aswics[x]['s2o']=s2o[x]
        aswics[x]['fe2o']=fe2o[x]; aswics[x]['c56']=c56[x]
        aswics[x]['o76']=o76[x]; aswics[x]['avq_c']=avq_c[x]
        aswics[x]['avq_o']=avq_o[x]; aswics[x]['avq_fe']=avq_fe[x]
        aswics[x]['nhe']=nhe[x]; aswics[x]['vhe']=vhe[x]
        aswics[x]['vc5']=vc5[x]; aswics[x]['vo6']=vo6[x]
        aswics[x]['vfe10']=vfe10[x]; aswics[x]['c4']=c4[x]
        aswics[x]['c5']=c5[x]; aswics[x]['c6']=c6[x]
        aswics[x]['o5']=o5[x]; aswics[x]['o6']=o6[x]
        aswics[x]['o7']=o7[x]; aswics[x]['o8']=o8[x]
        aswics[x]['ne8']=ne8[x]; aswics[x]['ne9']=ne9[x]
        aswics[x]['mg6']=mg6[x]; aswics[x]['mg7']=mg7[x]
        aswics[x]['mg8']=mg8[x]; aswics[x]['mg9']=mg9[x]
        aswics[x]['mg10']=mg10[x]; aswics[x]['mg11']=mg11[x]
        aswics[x]['mg12']=mg12[x]; aswics[x]['si6']=si6[x]
        aswics[x]['si7']=si7[x]; aswics[x]['si8']=si8[x]
        aswics[x]['si9']=si9[x]; aswics[x]['si10']=si10[x]
        aswics[x]['si11']=si11[x]; aswics[x]['si12']=si12[x]
        aswics[x]['fe6']=fe6[x]; aswics[x]['fe7']=fe7[x]
        aswics[x]['fe8']=fe8[x]; aswics[x]['fe9']=fe9[x]
        aswics[x]['fe10']=fe10[x]; aswics[x]['fe11']=fe11[x]
        aswics[x]['fe12']=fe12[x]; aswics[x]['fe13']=fe13[x]
        aswics[x]['fe14']=fe14[x]; aswics[x]['fe15']=fe15[x]
        aswics[x]['fe16']=fe16[x]; aswics[x]['fe17']=fe17[x]
        aswics[x]['fe18']=fe18[x]; aswics[x]['fe19']=fe19[x]
        aswics[x]['fe20']=fe20[x]; aswics[x]['vthhe']=vthhe[x]
        aswics[x]['vthc5']=vthc5[x]; aswics[x]['vtho6']=vtho6[x]
        aswics[x]['vthfe10']=vthfe10[x]; aswics[x]['swtype']=swtype[x]  
        aswics[x]['vthn5'] = vthn5[x]; aswics[x]['vthne8'] = vthne8[x]
        aswics.vthmg10[x] = vthmg10[x]; aswics.vthsi8[x] = vthsi8[x]
        aswics.vths8[x] = vths8[x]; aswics.vmg10[x] = vmg10[x]
        aswics.vn5[x] = vn5[x]; aswics.vne8[x] = vne8[x]
        aswics.vs8[x] = vs8[x]; aswics.vsi8[x] = vsi8[x]
        
        x += 1

    dnum = []
    he2p = []
    p_den = []
    p_tem = []
    p_spd = []
    arrlen = 0 
    iy = range(1,5)
    
    for i in iy:  #iterate through files by year
        
        year = 2000 + i
        
        file_wind = open(pathwind + filename_wind + str(i) + '.txt')
        file_swep = open(pathswep + filename_swep + str(i) + '.txt')
        line_wind = file_wind.readlines()
        line_swep = file_swep.readline()
        while line_swep:
            line_swep += file_swep.readline()
            if 'BEGIN DATA' in line_swep:
                break
        line_swep = file_swep.readlines()
        swep_len = len(line_swep)
        file_swep.close()
    
        index = 0
        
        while index != swep_len:
            

            swep_arr = np.array(line_swep[index].split())
            
            dnum.append(unknown2dnum(year,swep_arr[6])); p_den.append(swep_arr[8]); p_tem.append(swep_arr[9])
            p_spd.append(swep_arr[11]); he2p.append(swep_arr[10])
            
            index += 1
            arrlen += 1
    print arrlen
    sweparr = np.recarray((arrlen),dtype = [('dnum','d'), ('he42p','d'),('prot_den','d'),('prot_temp','d'),('prot_spd','d')])
    
    x = 0
    while x < arrlen:
        sweparr.dnum[x] = dnum[x]
        sweparr.he42p[x] = he2p[x]
        sweparr.prot_den[x] = p_den[x]
        sweparr.prot_temp[x] = p_tem[x]
        sweparr.prot_spd[x] = p_spd[x]
        x += 1
    np.save(path + 'swepam_sav',sweparr)
    np.save(path + 'aswics_sav',aswics)
    
    print "It has been done..."
    return sweparr
    
    
  
    
