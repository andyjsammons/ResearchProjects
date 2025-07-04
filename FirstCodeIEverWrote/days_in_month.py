

def days_in_month(m,y):
    from new_thng.py import leapyear
    import numpy as np
    from matplotlib.cbook import flatten
    '''
    PURPOSE: Return an unsigned integer number of days in the month and year.
    
    INPUT: 'm' -An optional int value representing the month of year. If not
                provided, the current month and year are used.
           'y' -An optional int value representing the year. If not provided, 
                current year is used.
    **Compatible with multi-dimensional lists and arrays**
                
    '''
    if np.ndim(m,y) >= 1:
        m = list(flatten(m))
        ndays = []
        for i in y:
            if leapyear(i) == True:
                dim = (31,29,31,30,31,30,31,31,30,31,30,31)
                mi = m - 1
                ndays.append(dim[mi])
            else:
                dim = (31,28,31,30,31,30,31,31,30,31,30,31)
                mi = m - 1
                ndays.append(dim[mi])
    if np.ndim(m,y) == 0:
        if leapyear(y) == True:
            dim = (31,29,31,30,31,30,31,31,30,31,30,31)
        else:
            dim = (31,28,31,30,31,30,31,31,30,31,30,31)
        mi = m - 1
        ndays = dim[mi]

        
    return ndays
    