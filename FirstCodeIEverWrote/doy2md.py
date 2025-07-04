def doy2md(year,doy):
    '''NAME: doy2md
       **Converted from Ed Santiago's IDL version for python compatibility** 
       PURPOSE:
           Converts a day of year to month, day   
       INPUT:
           'year' - four-digit year
           'doy'  - day of year (1-365, or 1-366)
       OUPUT:
           'month' - month of year (1-12)
           'day'   - day of year (see doy)
       SIDE EFFECTS:
           - Mild confusion
           - Night sweats
           - Strange dreams
           - loss of appetite
       Example: >>> doy2md(year, doy)
                04, 09 '''
    try: 
        
        if year < 100:
            print 'Use a four-digit year.'
        if doy < 1 or int(doy) > 366:
            print "Enter 'day of year' inbetween or equal to 1 and 366."
        monthdays = [31,28,31,30,31,30,31,31,30,31,30,31]
        isleap = year % 4 == 0 and year % 100 != 0 or year % 400 == 0
        if isleap == True:
            monthdays[1] += 1
        day = doy
        month = 0
        while int(day) > monthdays[month]:
            day -= monthdays[month]
            month += 1
        month += 1
        return month, day
    except TypeError:
        print 'Usage: doy2md(year,doy)'


