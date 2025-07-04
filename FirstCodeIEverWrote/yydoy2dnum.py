''' yydoy2dnum '''

def yydoy2dnum(yy,doy,dnum):
    ''' Return the Day number since January 1, 2000'''
    import numpy as np
    try:
        ss = np.ndim(yy)
        if ss == 0:
            doycopy = float(doy)
            float(yy)
            if (yy % 4) == 0:
                doycopy = doycopy - 1.0
        else:
            doycopy = []
            for d in doy:
                doycopy.append(float(d))
            leap = []
            for n in yy:
                if n % 4 == 0:
                    leap.append(float(n))
                    doycopy[leap] = doycopy[leap] - 1.0
        dnum = np.floor((int(yy) - 2000)*365.25) + doycopy
        return dnum
    except ValueError:
        print "Sorry, invalid input."
        
                
                