def leapyear(y):
    '''
    Return 'True' or 'False' for status of given year as leap.
    
    INPUT: 'y' -Year to be tested, Should be full year (e.g.:1999).
    
    **Supports both multidimensional lists and arrays, but returns a 1D list**
    '''
    import numpy as np
    from matplotlib.cbook import flatten
    if np.ndim(y) >= 1:
        y = list(flatten(y))
        leap = []
        for i in y:
            if i % 4 == 0 and i % 100 != 0 or i % 400 == 0:
                i = True
                leap.append(i)
            else:
                i = False
                leap.append(i)
    if isinstance(y, list) == True:
        y = np.array(y)
    if np.ndim(y) == 0:
        leap = None 
        if y % 4 == 0 and y % 100 != 0 or y % 400 == 0:
            leap = True
        else:
            leap = False       
    return leap


