def ymd2doy(yy,mm,dd):
    '''
    PURPOSE: Given a year/month/day, return the day of the year.
    
    ARGUMENTS: 'yy' - four-digit year
               'mm' - month (1-12)
               'dd' - day of month (1-31)
               
    EXAMPLE: >>> print ymd2doy(1998, 2, 1)
             32
             '''
    import days_in_month
    doy = dd
    m = 1
    while (m < mm):
        doy = doy + days_in_month(m,yy)
        m += 1
    return doy